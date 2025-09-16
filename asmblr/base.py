
from abc import ABC, abstractmethod
from collections import defaultdict
import torch as th
import numpy as np
import sympy as sp
import copy
import uuid
import json
import base64
import gzip
from io import BytesIO
from PIL import Image
from typing import Optional, Any, Dict, Union, Tuple
from .settings import Settings


def copy_value(value: Any):
    if isinstance(value, th.Tensor):
        return value.clone().detach()
    elif isinstance(value, np.ndarray):
        return np.copy(value)
    elif isinstance(value, (sp.Symbol, sp.Function)):
        return value
    else:
        return copy.deepcopy(value)


def process_value_for_serialization(value: Any) -> Dict[str, Any]:
    """
    Process a value for JSON serialization.
    
    Returns a dictionary with 'type' and 'data' keys indicating how to reconstruct the value.
    """
    if value is None:
        return {"type": "none", "data": None}
    
    elif isinstance(value, bool):
        return {"type": "bool", "data": value}
    
    elif isinstance(value, str):
        return {"type": "string", "data": value}
    
    elif isinstance(value, (int, float)):
        # Convert single numbers to tuples as requested
        return {"type": "tuple", "data": (value,)}
    
    elif isinstance(value, (tuple, list)):
        # Keep tuples as tuples, convert lists to tuples
        return {"type": "tuple", "data": tuple(value)}
    
    elif isinstance(value, th.Tensor):
        # Compress torch tensor with gzip
        tensor_bytes = value.cpu().numpy().tobytes()
        compressed = gzip.compress(tensor_bytes)
        encoded = base64.b64encode(compressed).decode('utf-8')
        
        return {
            "type": "torch_tensor",
            "data": encoded,
            "shape": list(value.shape),
            "dtype": str(value.dtype),
            "device": str(value.device)
        }
    
    elif isinstance(value, np.ndarray):
        # Compress numpy array with gzip
        array_bytes = value.tobytes()
        compressed = gzip.compress(array_bytes)
        encoded = base64.b64encode(compressed).decode('utf-8')
        
        return {
            "type": "numpy_array", 
            "data": encoded,
            "shape": list(value.shape),
            "dtype": str(value.dtype)
        }
    
    else:
        # Fallback for other types - try to convert to string
        return {"type": "other", "data": str(value)}


def unprocess_value_from_serialization(processed_data: Dict[str, Any]) -> Any:
    """
    Reconstruct a value from its processed serialization format.
    """
    value_type = processed_data["type"]
    data = processed_data["data"]
    
    if value_type == "none":
        return None
    
    elif value_type == "bool":
        return data
    
    elif value_type == "string":
        return data
    
    elif value_type == "tuple":
        return tuple(data)
    
    elif value_type == "torch_tensor":
        # Decompress torch tensor
        compressed = base64.b64decode(data.encode('utf-8'))
        tensor_bytes = gzip.decompress(compressed)
        
        # Reconstruct tensor
        shape = processed_data["shape"]
        dtype_str = processed_data["dtype"]
        
        # Map string dtype back to torch dtype
        dtype_map = {
            "torch.float32": th.float32,
            "torch.float64": th.float64,
            "torch.int32": th.int32,
            "torch.int64": th.int64,
            "torch.bool": th.bool,
        }
        dtype = dtype_map.get(dtype_str, th.float32)
        
        # Map torch dtype to numpy dtype
        numpy_dtype_map = {
            th.float32: np.float32,
            th.float64: np.float64,
            th.int32: np.int32,
            th.int64: np.int64,
            th.bool: np.bool_,
        }
        numpy_dtype = numpy_dtype_map.get(dtype, np.float32)
        
        # Create numpy array first, then convert to torch
        np_array = np.frombuffer(tensor_bytes, dtype=numpy_dtype).reshape(shape)
        tensor = th.from_numpy(np_array)
        
        return tensor
    
    elif value_type == "numpy_array":
        # Decompress numpy array
        compressed = base64.b64decode(data.encode('utf-8'))
        array_bytes = gzip.decompress(compressed)
        
        # Reconstruct array
        shape = processed_data["shape"]
        dtype_str = processed_data["dtype"]
        
        # Create numpy array
        array = np.frombuffer(array_bytes, dtype=dtype_str).reshape(shape)
        return array
    
    elif value_type == "other":
        # Try to evaluate as Python literal, fallback to string
        try:
            import ast
            return ast.literal_eval(data)
        except:
            return data
    
    else:
        raise ValueError(f"Unknown serialization type: {value_type}")
    


class BaseNode(ABC):
    """Base class for all DAG nodes in ASMBLR."""
    
    def __init__(self, **kwargs):
        """Initialize a BaseNode with proper two-phase initialization."""
        # Core attributes
        self.unique_id = str(uuid.uuid4())
        self.inputs = {}
        self.outputs = {}
        self.clean = True
        self.do_copy = Settings.copy_mode
        
        # Type hints (optional, not enforced)
        self.arg_types = getattr(self, 'arg_types', {})
        
        # Initialize sockets through template method pattern
        try:
            self.input_sockets = self._create_input_sockets()
            self.output_sockets = self._create_output_sockets()
        except Exception as e:
            raise ValueError(f"Failed to initialize sockets: {str(e)}")
        
        # Apply any provided socket values
        self._apply_socket_values(kwargs)


    @abstractmethod
    def _create_input_sockets(self) -> Dict[str, 'InputSocket']:
        """Create and return input sockets for this node type."""
        pass
    
    @abstractmethod 
    def _create_output_sockets(self) -> Dict[str, 'OutputSocket']:
        """Create and return output sockets for this node type."""
        pass

    @abstractmethod
    def inner_eval(self, sketcher=None, **kwargs):
        """Node-specific evaluation logic."""
        pass
    
    def _apply_socket_values(self, values: Dict[str, Any]) -> None:
        """Apply provided values to input sockets."""
        for name, value in values.items():
            if name in self.input_sockets:
                try:
                    self.input_sockets[name].set_value(value)
                except Exception as e:
                    raise ValueError(f"Failed to set value for socket '{name}': {str(e)}")

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__

    def resolve_inputs(self, sketcher=None, **kwargs):
        """Fetch inputs from connected sockets or use default values."""
        for name, socket in self.input_sockets.items():
            if socket.connections:
                # Use connected values (evaluate connected nodes)
                value = socket.resolve(sketcher, **kwargs)
                if value is not None:
                    self.inputs[name] = value
            elif socket.value is not None:
                # Use direct socket value (set via set_value)
                self.inputs[name] = socket.value
            # If neither connections nor direct value, leave unset (None)

    def evaluate(self, sketcher=None, **kwargs):
        """Evaluate this node, returning cached results if available."""
        self.clean = False
        if self.outputs:
            return self.outputs  # Return cached output if available
        
        self.resolve_inputs(sketcher, **kwargs)  # Get data from input connections
        self.inner_eval(sketcher, **kwargs)  # Run node-specific evaluation logic
        return self.outputs
    
    def register_input(self, name, value, copy=None):
        """Register an input value for this node."""
        try:
            do_copy = False
            if copy is None:
                if hasattr(self, 'copy_data') and self.copy_data:
                    do_copy = True
            else:
                do_copy = copy

            if do_copy:
                self.inputs[name] = copy_value(value)
            else:
                self.inputs[name] = value
        except Exception as e:
            raise ValueError(f"Failed to register input '{name}': {str(e)}")

    def register_output(self, name, value):
        """Register an output value for this node."""
        try:
            self.outputs[name] = value
        except Exception as e:
            raise ValueError(f"Failed to register output '{name}': {str(e)}")
    
    def socket_request_count(self, socket_name):
        """Get the number of connections for an output socket."""
        try:
            return len(self.output_sockets[socket_name].connections)
        except KeyError:
            raise KeyError(f"Output socket '{socket_name}' does not exist")
    
    def clean_outputs(self):
        self.outputs = defaultdict()
    
    def clean_inputs(self):
        self.inputs = defaultdict()
    
    def clean_graph(self):
        if not self.clean:
            self.clean_outputs()
            self.clean_inputs()
            for _, socket in self.input_sockets.items():
                for conn in socket.connections:
                    conn.input_node.clean_graph()
            self.clean = True
    
    def deduplicate_nodes(self, graph_data):
        
        node_map = {}
        for node in graph_data["nodes"]:
            node_id = node["id"]
            if node_id not in node_map:
                node_map[node_id] = node
            else:
                pass
        graph_data["nodes"] = list(node_map.values())
        return graph_data  

    def to_dict(self, device="cpu"):
        """Serialize the node and its connections to a JSON-compatible format."""
        graph_data = {
            "nodes": [],
            "connections": []
        }

        def serialize_node(node, graph_data, node_map):
            node_data = {
                "id": node.unique_id,
                "name": node.__class__.__name__,
            }
            data = {}
            for key, socket in node.input_sockets.items():
                if socket.value is not None:
                    socket_value = socket.value
                    # Move torch tensors to specified device before processing
                    if isinstance(socket_value, th.Tensor):
                        socket_value = socket_value.cpu() if device == "cpu" else socket_value
                    
                    # Process the value for JSON serialization
                    data[key] = process_value_for_serialization(socket_value)
                    
            node_data["data"] = data
            graph_data["nodes"].append(node_data)
            node_map[node.unique_id] = node

            # Serialize connections (unchanged - already simple)
            for output_name, output_socket in node.output_sockets.items():
                for conn in output_socket.connections:
                    connection_data = {
                        "source": node.unique_id,
                        "sourceOutput": output_name,
                        "target": conn.output_node.unique_id,
                        "targetInput": conn.input_socket
                    }
                    graph_data["connections"].append(connection_data)

        def traverse_graph(node, visited, graph_data, node_map):
            if node.unique_id in visited:
                return
            visited.add(node.unique_id)
            serialize_node(node, graph_data, node_map)
            for socket in node.input_sockets.values():
                if socket.connections:
                    for conn in socket.connections:
                        if conn.input_node:
                            traverse_graph(conn.input_node, visited, graph_data, node_map)

        visited_nodes = set()
        node_map = {}
        traverse_graph(self, visited_nodes, graph_data, node_map)
        graph_data = self.deduplicate_nodes(graph_data)
        return graph_data

    def make_json_compatible(self, graph_data):
        """Convert data to JSON-compatible types."""
        node_data = graph_data['nodes']
        compatible_data = []
        for node in node_data:
            compatible_node = {}
            for key, socket_value in node['data'].items():
                if isinstance(socket_value, th.Tensor):
                    socket_value = socket_value.cpu()
                    if len(socket_value.shape) == 0:
                        processed = float(socket_value.item())
                        key_name = key
                    elif len(socket_value.shape) == 1:
                        new_val = socket_value.cpu().numpy().tolist()
                        processed = tuple([float(x) for x in new_val])
                        key_name = key
                    elif len(socket_value.shape) == 3:
                        # TODO: Improve handling of Image and other Tensors
                        img = socket_value.cpu().numpy()#.dtype(np.float64)
                        pil_img = Image.fromarray((img * 255).astype(np.uint8))
                        # Temp
                        buff = BytesIO()
                        pil_img.save(buff, format="PNG")
                        new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
                        processed = f"data:image/png;base64,{new_image_string}"
                        key_name = f"{key}_IMG"
                    else:
                        print(socket_value.shape)
                        raise NotImplementedError("Not implemented yet.")
                else:
                    print(socket_value.shape)
                    raise NotImplementedError("Not implemented yet.")
                socket_value = processed
                key = key_name
                compatible_node[key] = socket_value
            compatible_data.append(compatible_node)
        graph_data['nodes'] = compatible_data
        return graph_data

    def to_json(self, wrapper_name=None, device="cpu"):
        """Serialize the graph to JSON format."""
        graph_data = self.to_dict(device=device)
        graph_data = self.make_json_compatible(graph_data)
        if wrapper_name:
            graph_data = {wrapper_name: graph_data}
        return json.dumps(graph_data, cls=CustomJSONEncoder)
    

    @classmethod
    def from_dict(cls, graph_data: Dict[str, Any]):
        """Reconstruct the graph from JSON data."""

        # A map from unique ID to the node instance
        node_map = {}
        from .simple_registry import NODE_REGISTRY
        # Step 1: Recreate nodes
        for node_data in graph_data["nodes"]:
            node_class = NODE_REGISTRY.get(node_data["name"], None)
            if node_class is None:
                raise ValueError(f"Node class {node_data['name']} not found in NODE_REGISTRY")
            
            node = node_class()
            node.unique_id = node_data["id"]  # Assign the stored unique ID

            # Restore input-socket values using the new unprocessing function
            for param_name, processed_value in node_data["data"].items():
                try:
                    # Unprocess the serialized value
                    actual_value = unprocess_value_from_serialization(processed_value)
                    node.input_sockets[param_name].set_value(actual_value)
                except Exception as e:
                    print(f"Warning: Failed to restore parameter {param_name} for node {node_data['name']}: {e}")
                    # Try fallback for backward compatibility
                    if isinstance(processed_value, list):
                        node.input_sockets[param_name].set_value(tuple(processed_value))
                    else:
                        node.input_sockets[param_name].set_value(processed_value)
            
            node_map[node.unique_id] = node  # Store in the node map

        # Step 2: Recreate connections
        for connection_data in graph_data["connections"]:
            try:
                from_node = node_map[connection_data["source"]]
                to_node = node_map[connection_data["target"]]
                Connection(
                    input_node=from_node,
                    output_socket=connection_data["sourceOutput"],
                    output_node=to_node,
                    input_socket=connection_data["targetInput"]
                )
            except Exception as e:
                print(f"Error in connection: {from_node} -> {to_node}")
        parent_nodes = []
        for node in node_map.values():
            count = 0
            for socket in node.output_sockets.keys():
                count += node.socket_request_count(socket)
            if count == 0:
                parent_nodes.append(node)
        if len(parent_nodes) == 1:
            return parent_nodes[0]
        else:
            # Return the root node (the first node created)
            return parent_nodes

    @classmethod
    def from_json(cls, graph_data: Dict[str, Any]):
        """Reconstruct the graph from JSON data."""
        return cls.from_dict(graph_data)
    

    def inspect_graph(self, visited=None, indent=0):
        """Recursively inspect the graph starting from this node and print details."""
        if visited is None:
            visited = set()

        # If this node has already been visited, avoid printing it again (to avoid infinite loops)
        if self.unique_id in visited:
            return
        visited.add(self.unique_id)

        # Print the current node's UUID
        print(f"{'  ' * indent}Node: {self.unique_id} ({self.__class__.__name__})")

        # Print details for each input socket
        for socket_name, socket in self.input_sockets.items():
            if socket.connections:  # If there's a connection, print the connected node's UUID
                for conn in socket.connections:
                    print(f"{'  ' * (indent + 1)}Input [{socket_name}] connected to Node {conn.input_node.unique_id}")
                    # Recursively inspect the connected node
                    conn.input_node.inspect_graph(visited, indent + 2)
            elif socket.value is not None:  # If there's a direct value, print the value
                print(f"{'  ' * (indent + 1)}Input [{socket_name}] has value: {socket.value}")
            else:
                print(f"{'  ' * (indent + 1)}Input [{socket_name}] is unconnected")

        
class Connection:
    """Represents a connection between two nodes through their sockets."""
    
    def __init__(self, input_node: BaseNode, output_socket: str,
                 output_node: BaseNode, input_socket: str):
        self.input_node = input_node
        self.output_socket = output_socket
        self.output_node = output_node
        self.input_socket = input_socket

        # Validate connection
        self._validate_connection()
        
        # Register this connection in the nodes' sockets
        try:
            self.input_node.output_sockets[output_socket].connect(self)
            self.output_node.input_sockets[input_socket].connect(self)
        except KeyError as e:
            raise KeyError(f"Socket not found during connection: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to establish connection: {str(e)}")
    
    def _validate_connection(self):
        """Validate that this connection is valid."""
        if self.output_socket not in self.input_node.output_sockets:
            raise ValueError(f"Output socket '{self.output_socket}' does not exist on input node")
        
        if self.input_socket not in self.output_node.input_sockets:
            raise ValueError(f"Input socket '{self.input_socket}' does not exist on output node")

    def get_output(self, sketcher=None, **kwargs):
        # Resolve the output of the input node and return the value
        self.input_node.evaluate(sketcher, **kwargs)
        return self.input_node.outputs.get(self.output_socket, None)


    def delete(self):
        """Disconnect and clean up."""
        self.input_node.output_sockets[self.output_socket].connections.remove(self)
        self.output_node.input_sockets[self.input_socket].connections.remove(self)

    @property
    def name(self):
        name = f"{self.input_node.__repr__()}:{self.output_socket} -> {self.output_node.__repr__()}:{self.input_socket}"
        return name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (float, int, str)):
            return obj
        if isinstance(obj, sp.Float):
            return float(obj)  # Convert sympy Float to Python float
        elif isinstance(obj, sp.Integer):
            return int(obj)  # Convert sympy Float to Python float
        elif isinstance(obj, sp.Symbol):
            return str(obj.name)
        elif isinstance(obj, sp.Tuple):
            return tuple([self.default(item) for item in obj])
        elif isinstance(obj, tuple):
            return tuple([self.default(item) for item in obj])
        # Add more custom conversions if needed
        elif isinstance(obj, th.Tensor):
            # Depends on the form.
            raise NotImplementedError("Should not encounter this.")
        else:
            # Need to figure these out.
            raise NotImplementedError(f"{type(obj)} needs to be resolved.")
        return super().default(obj)
    

class InputSocket:
    def __init__(self, name, value: Any =None, parent: Optional[BaseNode]=None):
        self.name = name
        self.connections = []  # Holds the connection if one exists
        self.value = value       # Holds a direct value if no connection
        self.parent = parent

    def connect(self, connection):
        self.connections.append(connection)
        self.value = None  # Clear any direct value when connected

    def set_value(self, value):
        self.value = value
        self.connections = []  # Clear connection when directly set

    def resolve(self, sketcher=None, **kwargs):
        # Resolve by returning the connected node's output or direct value
        if self.connections:
            outputs = [conn.get_output(sketcher, **kwargs) for conn in self.connections]
            if len(outputs) == 1:
                return outputs[0]
            else:
                return tuple(outputs)
        return self.value

class OutputSocket:
    def __init__(self, name: str, parent: Optional[BaseNode] = None):
        self.name = name
        self.connections = []  # Multiple connections can feed from one output
        self.parent = parent

    def connect(self, connection):
        self.connections.append(connection)

    def get_output(self):
        # For now, return output from the first connection
        if self.connections:
            return self.connections[0].output_node.outputs[self.name]
        return None

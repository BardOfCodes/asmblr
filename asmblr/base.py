
from abc import ABC, abstractmethod
from collections import defaultdict
import torch as th
import numpy as np
import sympy as sp
import copy
import uuid
import json
from typing import Optional, Any, Dict, Union, Tuple
from .settings import Settings
from .serialize import make_json_compatible, deduplicate_nodes, process_value_for_serialization, unprocess_value_from_serialization


def copy_value(value: Any):
    if isinstance(value, th.Tensor):
        return value.clone().detach()
    elif isinstance(value, np.ndarray):
        return np.copy(value)
    elif isinstance(value, (sp.Symbol, sp.Function)):
        return value
    else:
        return copy.deepcopy(value)



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
    

    def to_dict(self, device="cpu"):
        """Serialize the node and its connections to a JSON-compatible format."""
        graph_data = {
            "nodes": [],
            "connections": []
        }
        visited_nodes = set()
        node_map = {}
        traverse_graph(self, visited_nodes, graph_data, node_map, device)
        graph_data = deduplicate_nodes(graph_data)
        return graph_data

    def to_json(self, wrapper_name=None, device="cpu"):
        """Serialize the graph to JSON format."""
        graph_data = self.to_dict(device=device)
        graph_data = make_json_compatible(graph_data)
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


def serialize_node(node, graph_data, node_map, device):
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


def traverse_graph(node, visited, graph_data, node_map, device):
    if node.unique_id in visited:
        return
    visited.add(node.unique_id)
    serialize_node(node, graph_data, node_map, device)
    for socket in node.input_sockets.values():
        if socket.connections:
            for conn in socket.connections:
                if conn.input_node:
                    traverse_graph(conn.input_node, visited, graph_data, node_map, device)

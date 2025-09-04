
from abc import ABC, abstractmethod
from collections import defaultdict
import torch as th
import numpy as np
import sympy as sp
import copy
import uuid
import json
import base64
from io import BytesIO
from PIL import Image
from typing import Optional, Any, Dict
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
    


class BaseNode(ABC):
    input_sockets: dict
    output_sockets: dict
    clean: bool
    unique_id: str
    inputs: dict
    outputs: dict
    do_copy: bool
    copy_data: bool

    def __new__(cls, *args, **kwargs):
        # Create the node instance
        instance = super(BaseNode, cls).__new__(cls)
        
        # Perform setup that doesn't rely on arguments
        instance.inputs = defaultdict()
        instance.outputs = defaultdict()
        instance.input_sockets = {}  # Store socket objects
        instance.output_sockets = {}
        instance.clean = True
        instance.unique_id = str(uuid.uuid4())
        
        # Call setup_sockets in __new__, moving socket initialization here
        instance.setup_base()
        instance.setup_sockets()

        return instance

    @abstractmethod
    def __init__(self, *args, **kwargs):
        # Init should be relaxed; handle instance-specific configuration only
        self.do_copy = Settings.copy_mode


    @abstractmethod
    def setup_sockets(self):
        """Define input and output sockets in each subclass."""
        pass

    @abstractmethod
    def setup_base(self):
        """Define required variables for the sockets in each subclass."""
        pass

    @abstractmethod
    def inner_eval(self, copy=False, *args, **kwargs):
        # Just do what is required.
        pass

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__

    def resolve_inputs(self, *args, **kwargs):
        """Fetch inputs from connected sockets."""
        for name, socket in self.input_sockets.items():
            value = socket.resolve(*args, **kwargs)
            do_copy = self.do_copy
            if value is not None:
                self.inputs[name] = value

    def evaluate(self, *args, **kwargs):
        self.clean = False
        if self.outputs:
            return self.outputs  # If already computed, return cached output
        else:
            self.resolve_inputs(*args, **kwargs)  # Get data from input connections
            self.inner_eval(*args, **kwargs)  # Run the node-specific evaluation logic
            return self.outputs
    
    def register_input(self, name, value, copy=None):
        do_copy = False
        if copy is None:
            if self.copy_data:
                do_copy = True
        else:
            do_copy = copy

        if do_copy:
            self.inputs[name] = copy_value(value)
        else:
            self.inputs[name] = value

    def register_output(self, name, value):
        self.outputs[name] = value
    
    def socket_request_count(self, socket_name):
        return len(self.output_sockets[socket_name].connections)
    
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
        """Serialize the node and its connections to a Python-loadable format."""
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
                    # Only move torch tensors to cpu
                    if isinstance(socket_value, th.Tensor):
                        socket_value = socket_value.cpu() if device == "cpu" else socket_value
                    data[key] = socket_value
            node_data["data"] = data
            graph_data["nodes"].append(node_data)
            node_map[node.unique_id] = node

            # Serialize connections
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
        import asmblr.symbolic as asms
        # Step 1: Recreate nodes
        for node_data in graph_data["nodes"]:
            node_class = getattr(asms, node_data["name"])  # Get the class from the module
            # node = node_class.__new__(node_class)  # Use __new__ to create the node
            node = node_class()
            node.unique_id = node_data["id"]  # Assign the stored unique ID

            # Restore input-socket default values (params)
            collected_param = {}
            for param_name, param_value in node_data["data"].items():
                ## Custom conversion from sequence 0, 1, 2
                if "_IMG" in param_name:
                    # TODO: Improve handling of Image and other Tensors
                    img_data = param_value.split(",")[1]
                    img = Image.open(BytesIO(base64.b64decode(img_data)))
                    img = np.array(img)
                    img = th.tensor(img, dtype=th.float32) / 255.0
                    node.input_sockets[param_name[:-4]].set_value(img)
                elif isinstance(param_value, list):
                    param_value = tuple(param_value)
                    node.input_sockets[param_name].set_value(param_value)
                else:
                    node.input_sockets[param_name].set_value(param_value)
            for key, value in collected_param.items():
                node.input_sockets[key].set_value(tuple(value))
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
    def __init__(self, input_node: BaseNode, output_socket: str,
                 output_node: BaseNode, input_socket: str):
        self.input_node = input_node
        self.output_socket = output_socket
        self.output_node = output_node
        self.input_socket = input_socket

        # Register this connection in the nodes' sockets
        self.input_node.output_sockets[output_socket].connect(self)
        self.output_node.input_sockets[input_socket].connect(self)

    def get_output(self, sketcher_2d):
        # Resolve the output of the input node and return the value
        self.input_node.evaluate(sketcher_2d)
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

    def resolve(self, sketcher_2d):
        # Resolve by returning the connected node's output or direct value
        if self.connections:
            outputs = [conn.get_output(sketcher_2d) for conn in self.connections]
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

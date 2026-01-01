import torch as th
from PIL import Image
from io import BytesIO
import numpy as np
import base64

import gzip
from typing import Any, Dict

def make_json_compatible(graph_data):
    """Convert data to JSON-compatible types.
    
    Args:
        graph_data: Dictionary with 'nodes' key containing node data.
        
    Returns:
        Modified graph_data with JSON-compatible values.
    """
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
                    # Handle image tensors (H, W, C)
                    img = socket_value.cpu().numpy()
                    pil_img = Image.fromarray((img * 255).astype(np.uint8))
                    buff = BytesIO()
                    pil_img.save(buff, format="PNG")
                    new_image_string = base64.b64encode(buff.getvalue()).decode("utf-8")
                    processed = f"data:image/png;base64,{new_image_string}"
                    key_name = f"{key}_IMG"
                else:
                    raise NotImplementedError(
                        f"Tensor with shape {socket_value.shape} not supported. "
                        f"Supported shapes: scalar (0D), vector (1D), image (3D)."
                    )
            else:
                raise NotImplementedError(
                    f"Value type {type(socket_value).__name__} not supported in make_json_compatible. "
                    f"Use process_value_for_serialization for general serialization."
                )
            socket_value = processed
            key = key_name
            compatible_node[key] = socket_value
        compatible_data.append(compatible_node)
    graph_data['nodes'] = compatible_data
    return graph_data


def deduplicate_nodes(graph_data):
    
    node_map = {}
    for node in graph_data["nodes"]:
        node_id = node["id"]
        if node_id not in node_map:
            node_map[node_id] = node
        else:
            pass
    graph_data["nodes"] = list(node_map.values())
    return graph_data  
    
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
        except (ValueError, SyntaxError):
            return data
    
    else:
        raise ValueError(f"Unknown serialization type: {value_type}")
    
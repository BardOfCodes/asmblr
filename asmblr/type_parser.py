"""
Type hint parsing utilities for ASMBLR nodes.
"""

import re
from typing import Dict, List, Optional, Union


def parse_batch_size_to_type(batch_spec: str) -> str:
    """
    Convert GeoLIPI batch specification to ASMBLR type hint.
    
    Args:
        batch_spec: String like "[batch, 3]", "[batch, 1]", "[batch, num_points, 3]"
        
    Returns:
        Type hint string: "vec3", "float", "vec3", etc.
    """
    # Remove brackets and split
    spec = batch_spec.strip("[]").split(",")
    
    # Look at the last dimension (the actual data dimension)
    if len(spec) >= 2:
        last_dim = spec[-1].strip()
        
        # Handle numeric dimensions
        if last_dim.isdigit():
            dim = int(last_dim)
            if dim == 1:
                return "float"
            elif dim == 2:
                return "vec2"
            elif dim == 3:
                return "vec3"
            elif dim == 4:
                return "vec4"
            else:
                return f"vec{dim}"  # For higher dimensions
        
        # Handle named dimensions
        elif last_dim in ["num_points"]:
            # This is typically a coordinate array, check previous dimension
            if len(spec) >= 3:
                coord_dim = spec[-2].strip()
                if coord_dim.isdigit():
                    dim = int(coord_dim)
                    if dim == 2:
                        return "vec2"
                    elif dim == 3:
                        return "vec3"
                    elif dim == 4:
                        return "vec4"
            return "vec3"  # Default for coordinate arrays
    
    # Default fallback
    return "float"


def parse_geolipi_docstring(docstring: str) -> Dict[str, str]:
    """
    Parse GeoLIPI function docstring to extract parameter types.
    
    Args:
        docstring: Function docstring containing Parameters section
        
    Returns:
        Dictionary mapping parameter names to type hints
    """
    if not docstring:
        return {}
    
    # Find the Parameters section
    lines = docstring.strip().split('\n')
    param_section = False
    param_types = {}
    
    for line in lines:
        line = line.strip()
        
        # Start of parameters section
        if line.startswith("Parameters:"):
            param_section = True
            continue
        
        # End of parameters section (next section starts)
        if param_section and line.endswith(":") and not line.startswith(" "):
            break
        
        # Parse parameter line
        if param_section and line and ":" in line:
            # Look for pattern: "param_name: description, shape [batch, N]"
            # or "param_name (type): description, shape [batch, N]"
            
            # Extract parameter name and description
            param_part = line.split(":")[0].strip()
            desc_part = line.split(":", 1)[1].strip()
            
            # Remove type annotations in parentheses
            param_name = re.sub(r'\s*\([^)]*\)', '', param_part).strip()
            
            # Look for shape specification in the description
            shape_match = re.search(r'shape\s+\[([^\]]+)\]', desc_part)
            if shape_match:
                batch_spec = f"[{shape_match.group(1)}]"
                param_types[param_name] = parse_batch_size_to_type(batch_spec)
            else:
                # Default type if no shape specified
                param_types[param_name] = "float"
    
    return param_types


def validate_type_hint(type_hint: str) -> bool:
    """
    Validate that a type hint is one of the supported types.
    
    Args:
        type_hint: Type hint string to validate
        
    Returns:
        True if valid, False otherwise
    """
    valid_types = {
        "String", "bool", "int", "float", 
        "vec2", "vec3", "vec4",
        "List[String]", "List[bool]", "List[int]", "List[float]",
        "List[vec2]", "List[vec3]", "List[vec4]"
    }
    
    return type_hint in valid_types


def format_arg_types(arg_keys: List[str], type_hints: Dict[str, str]) -> Dict[str, str]:
    """
    Format type hints to match arg_keys, filling in defaults where needed.
    
    Args:
        arg_keys: List of argument names
        type_hints: Dictionary of type hints (may be incomplete)
        
    Returns:
        Complete dictionary with type hints for all arg_keys
    """
    formatted = {}
    
    for key in arg_keys:
        if key in type_hints and validate_type_hint(type_hints[key]):
            formatted[key] = type_hints[key]
        else:
            # Default to float for unknown types
            formatted[key] = "float"
    
    return formatted

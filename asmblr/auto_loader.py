"""
Automatic node loader for ASMBLR.
This module can generate static Python files containing all GeoLIPI nodes.
"""

from typing import List, Callable, Type, Dict, Optional
import inspect
import os
from pathlib import Path
from .simple_registry import register_node, NODE_REGISTRY
from .type_parser import parse_geolipi_docstring, format_arg_types


def generate_geolipi_nodes_file(output_dir: Optional[str] = None) -> str:
    """
    Generate a static Python file containing all GeoLIPI nodes.
    
    Args:
        output_dir: Directory to save the generated file. Defaults to auto_nodes/
        
    Returns:
        Path to the generated file
    """
    from geolipi.torch_compute.maps import PRIMITIVE_MAP, COMBINATOR_MAP, MODIFIER_MAP, COLOR_FUNCTIONS
    
    if output_dir is None:
        # Default to auto_nodes directory relative to this file
        current_dir = Path(__file__).parent
        output_dir = current_dir / "auto_nodes"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "geolipi_nodes.py"
    
    # Filter out custom nodes that need special handling
    def exclude_custom_nodes(cls):
        custom_node_names = {
            'PolyLine2D', 'EvaluateLayoutNode',  # MXG and splitweave custom nodes
            'VarSplitter'  # Custom geolipi nodes (SplitVec2D, SplitVec3D, SplitVec4D use this)
        }
        return cls.__name__ not in custom_node_names
    
    # Collect all node information
    all_node_info = []
    
    # Process primitives (geometric shapes) - ignore 'points' parameter
    all_node_info.extend(_collect_node_info(
        PRIMITIVE_MAP, "primitives", class_filter=exclude_custom_nodes, ignore_arg_inds=[0]
    ))
    
    # Process combinators (Union, Difference, etc.) - use all parameters
    all_node_info.extend(_collect_node_info(
        COMBINATOR_MAP, "combinators", ignore_arg_inds=[]
    ))
    
    # Process modifiers/transforms (Translate, Scale, etc.) - use all parameters
    all_node_info.extend(_collect_node_info(
        MODIFIER_MAP, "modifiers", ignore_arg_inds=[]
    ))
    
    # Process color functions - use all parameters
    all_node_info.extend(_collect_node_info(
        COLOR_FUNCTIONS, "color_functions", ignore_arg_inds=[]
    ))
    
    # Generate the Python file content
    file_content = _generate_file_content(all_node_info)
    
    # Write the file
    with open(output_file, 'w') as f:
        f.write(file_content)
    
    # Also create __init__.py to make it a proper Python package
    init_file = output_dir / "__init__.py"
    with open(init_file, 'w') as f:
        f.write('"""Auto-generated GeoLIPI nodes for ASMBLR."""\n\nfrom .geolipi_nodes import *\n')
    
    print(f"Generated {len(all_node_info)} GeoLIPI nodes in: {output_file}")
    return str(output_file)


def load_all_geolipi_nodes() -> List[str]:
    """
    Load all nodes from geolipi maps automatically.
    
    This function first tries to import from auto_nodes/. If that fails,
    it generates the auto_nodes file and then imports from it.
    """
    try:
        # Try to import from pre-generated auto_nodes
        from .auto_nodes.geolipi_nodes import register_all_nodes
        registered_names = register_all_nodes()
        return registered_names
    except ImportError:
        # Auto_nodes doesn't exist, generate it
        print("Auto-generated nodes not found. Generating geolipi_nodes.py...")
        generate_geolipi_nodes_file()
        
        # Now import and use the generated file
        from .auto_nodes.geolipi_nodes import register_all_nodes
        registered_names = register_all_nodes()
        return registered_names


def _collect_node_info(
    primitive_map: Dict[Type, Callable],
    category: str,
    class_filter: Optional[Callable[[Type], bool]] = None,
    ignore_arg_inds: List[int] = [0]
) -> List[Dict]:
    """Collect node information from a mapping for code generation."""
    node_info_list = []
    
    for expr_class, execution_function in primitive_map.items():
        if class_filter and not class_filter(expr_class):
            continue
        
        # Inspect the execution function to get parameter names
        sig = inspect.signature(execution_function)
        all_params = list(sig.parameters.items())
        
        # Remove parameters at specified indices
        filtered_params = [
            (param_name, param) for i, (param_name, param) in enumerate(all_params)
            if i not in ignore_arg_inds
        ]
        
        # Handle variadic functions (*args) - these should accept multiple inputs
        has_varargs = any(param.kind == inspect.Parameter.VAR_POSITIONAL for _, param in filtered_params)
        
        if has_varargs:
            # For variadic functions like Union(*args), create a special multi-input socket
            arg_keys = ['inputs']  # Single socket that accepts multiple connections
            default_values = {}
            is_variadic = True
            arg_types = {'inputs': 'List[float]'}  # Default for variadic
        else:
            arg_keys = [param_name for param_name, param in filtered_params]
            default_values = {
                param_name: param.default 
                for param_name, param in filtered_params
                if param.default != inspect.Parameter.empty
            }
            is_variadic = False
            
            # Extract type hints from execution function docstring
            docstring_types = {}
            if hasattr(execution_function, '__doc__') and execution_function.__doc__:
                docstring_types = parse_geolipi_docstring(execution_function.__doc__)
            
            # Format type hints to match arg_keys (excluding 'points' parameter)
            arg_types = format_arg_types(arg_keys, docstring_types)
        
        node_info = {
            'name': expr_class.__name__,
            'expr_class_name': expr_class.__name__,
            'expr_class_module': expr_class.__module__,
            'arg_keys': arg_keys,
            'default_values': default_values,
            'is_variadic': is_variadic,
            'category': category,
            'arg_types': arg_types
        }
        
        node_info_list.append(node_info)
    
    return node_info_list


def _generate_file_content(all_node_info: List[Dict]) -> str:
    """Generate the Python file content for all nodes."""
    
    # File header
    content = '''"""
Auto-generated GeoLIPI nodes for ASMBLR.

This file is automatically generated by asmblr.auto_loader.generate_geolipi_nodes_file().
Do not edit this file manually - regenerate it instead.
"""

from typing import List
from ..expr_node import GLNode
from ..base import InputSocket
from ..simple_registry import register_node


'''
    
    # Generate node classes
    for node_info in all_node_info:
        content += _generate_node_class(node_info)
        content += "\n\n"
    
    # Generate decorator and registration tracking
    content += "# Auto-registration decorator with tracking\n"
    content += "_registered_nodes = []\n\n"
    content += "def auto_register(cls):\n"
    content += '    """Decorator to automatically register a node class and track it."""\n'
    content += "    register_node(cls)\n"
    content += "    _registered_nodes.append(cls.__name__)\n"
    content += "    return cls\n\n\n"
    
    # Apply decorator to all classes
    content += "# Apply auto-registration decorator to all classes\n"
    for node_info in all_node_info:
        node_name = node_info['name']
        content += f"{node_name} = auto_register({node_name})\n"
    
    content += "\n\n"
    
    # Generate dynamic registration function
    content += "def register_all_nodes() -> List[str]:\n"
    content += '    """Return list of all auto-registered GeoLIPI nodes."""\n'
    content += "    # All nodes are already registered via the auto_register decorator\n"
    content += "    # Return the dynamically tracked list\n"
    content += "    return _registered_nodes.copy()\n"
    
    return content


def _generate_node_class(node_info: Dict) -> str:
    """Generate a single node class definition."""
    name = node_info['name']
    expr_class_name = node_info['expr_class_name']
    expr_class_module = node_info['expr_class_module']
    arg_keys = node_info['arg_keys']
    default_values = node_info['default_values']
    is_variadic = node_info['is_variadic']
    arg_types = node_info.get('arg_types', {})
    
    # Import statement for the expression class
    import_line = f"# {expr_class_module}.{expr_class_name}"
    
    class_def = f'''class {name}(GLNode):
    """{import_line}"""
    
    def __init__(self, *args, **kwargs):
        # Import the expression class dynamically to avoid circular imports
        import {expr_class_module}
        self.expr_class = {expr_class_module}.{expr_class_name}
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for {name}."""
        self.arg_keys = {repr(arg_keys)}
        self.default_values = {repr(default_values)}
        self.is_variadic = {is_variadic}
        self.arg_types = {repr(arg_types)}
        return {{key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}}'''
    
    return class_def


def get_auto_load_summary() -> dict:
    """
    Get summary of auto-loaded nodes.
    
    Returns:
        Dictionary with node counts by category
    """
    all_nodes = list(NODE_REGISTRY.keys())
    
    summary = {
        "total": len(all_nodes),
        "3d_primitives": len([n for n in all_nodes if n.endswith('3D')]),
        "2d_primitives": len([n for n in all_nodes if n.endswith('2D')]),
        "operations": len([n for n in all_nodes if not n.endswith(('2D', '3D'))]),
    }
    
    return summary



# Auto-load nodes when module is imported
import os
if os.environ.get('ASMBLR_DISABLE_AUTO_LOAD') != '1':
    _loaded_nodes = load_all_geolipi_nodes()
    _summary = get_auto_load_summary()
    print(f"Auto-registered {_summary['total']} nodes "
          f"({_summary['3d_primitives'] + _summary['2d_primitives']} primitives, "
          f"{_summary['operations']} operations)")

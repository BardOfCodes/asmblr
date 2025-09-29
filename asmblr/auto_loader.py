"""
Automatic node loader for ASMBLR.
This module can generate static Python files containing all symbolic nodes from GeoLIPI and SySL libraries.
Nodes are organized by their source files and use the respective registry systems.
"""

from typing import List, Callable, Type, Dict, Optional
import inspect
import os
from pathlib import Path
from .simple_registry import register_node, NODE_REGISTRY

# Symbols we exclude from auto-generation; implemented manually elsewhere
EXCLUDE_SYMBOLS = {
    'PolyLine2D', 'EvaluateLayoutNode', 'VarSplitter',
}


def generate_geolipi_nodes_file(output_dir: Optional[str] = None) -> str:
    """
    Generate a static Python file containing all GeoLIPI nodes.
    
    Args:
        output_dir: Directory to save the generated file. Defaults to auto_nodes/
        
    Returns:
        Path to the generated file
    """
    if output_dir is None:
        current_dir = Path(__file__).parent
        output_dir = os.path.join(current_dir, "auto_nodes")
    output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    output_file = os.path.join(output_dir, "geolipi_nodes.py")
    
    # Collect geolipi node information
    geolipi_node_info = _collect_geolipi_nodes()
    
    # Generate the Python file content
    file_content = _generate_file_content(geolipi_node_info, "GeoLIPI")
    
    # Write the file
    with open(output_file, 'w') as f:
        f.write(file_content)
    
    print(f"Generated {len(geolipi_node_info)} GeoLIPI nodes in: {output_file}")
    return str(output_file)


def generate_sysl_nodes_file(output_dir: Optional[str] = None) -> str:
    """
    Generate a static Python file containing all SySL nodes.
    
    Args:
        output_dir: Directory to save the generated file. Defaults to auto_nodes/
        
    Returns:
        Path to the generated file
    """
    if output_dir is None:
        current_dir = Path(__file__).parent
        output_dir = os.path.join(current_dir, "auto_nodes")
    output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    output_file = os.path.join(output_dir, "sysl_nodes.py")
    
    # Collect sysl node information
    sysl_node_info = _collect_sysl_nodes()
    
    # Generate the Python file content
    file_content = _generate_file_content(sysl_node_info, "SySL")
    
    # Write the file
    with open(output_file, 'w') as f:
        f.write(file_content)
    
    print(f"Generated {len(sysl_node_info)} SySL nodes in: {output_file}")
    return str(output_file)


def generate_all_nodes_files(output_dir: Optional[str] = None) -> List[str]:
    """
    Generate both GeoLIPI and SySL node files.
    
    Args:
        output_dir: Directory to save the generated files. Defaults to auto_nodes/
        
    Returns:
        List of paths to the generated files
    """
    if output_dir is None:
        current_dir = Path(__file__).parent
        output_dir = os.path.join(current_dir, "auto_nodes")
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    # Generate both files
    geolipi_file = generate_geolipi_nodes_file(output_dir)
    sysl_file = generate_sysl_nodes_file(output_dir)
    
    # Create __init__.py to import from both files
    init_file = os.path.join(output_dir, "__init__.py")
    with open(init_file, 'w') as f:
        f.write('"""Auto-generated nodes for ASMBLR."""\n\n')
        f.write('from .geolipi_nodes import *\n')
        f.write('from .sysl_nodes import *\n')
    
    return [geolipi_file, sysl_file]


# Backward compatibility
def generate_symbolic_nodes_file(output_dir: Optional[str] = None) -> str:
    """Backward compatibility wrapper for generate_all_nodes_files."""
    files = generate_all_nodes_files(output_dir)
    return files[0]  # Return first file path for compatibility


def load_all_symbolic_nodes() -> List[str]:
    """
    Load all nodes from both geolipi and sysl libraries.
    """
    # Get registered nodes from both libraries
    geolipi_nodes = load_all_geolipi_nodes()
    sysl_nodes = load_all_sysl_nodes()
    
    return geolipi_nodes + sysl_nodes


def load_all_geolipi_nodes() -> List[str]:
    """
    Load all nodes from geolipi symbolic library automatically.
    
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
        print("Auto-generated geolipi nodes not found. Generating geolipi_nodes.py...")
        generate_geolipi_nodes_file()
        
        # Now import and use the generated file
        from .auto_nodes.geolipi_nodes import register_all_nodes
        registered_names = register_all_nodes()
        return registered_names


def load_all_sysl_nodes() -> List[str]:
    """
    Load all nodes from sysl symbolic library automatically.
    
    This function first tries to import from auto_nodes/. If that fails,
    it generates the auto_nodes file and then imports from it.
    """
    try:
        # Try to import from pre-generated auto_nodes
        from .auto_nodes.sysl_nodes import register_all_nodes
        registered_names = register_all_nodes()
        return registered_names
    except ImportError:
        # Auto_nodes doesn't exist, generate it
        print("Auto-generated sysl nodes not found. Generating sysl_nodes.py...")
        generate_sysl_nodes_file()
        
        # Now import and use the generated file
        from .auto_nodes.sysl_nodes import register_all_nodes
        registered_names = register_all_nodes()
        return registered_names

def _collect_geolipi_nodes() -> List[Dict]:
    """Collect nodes from geolipi registry, organized by source files."""
    import sys
    from pathlib import Path
    
    # Add the project paths to sys.path if not already there
    project_root = Path(__file__).parent.parent.parent  # Go up to mpspy root
    geolipi_path = os.path.join(project_root, "geolipi")
    
    if str(geolipi_path) not in sys.path:
        sys.path.insert(0, str(geolipi_path))
    
    try:
        # Import all geolipi.symbolic modules to trigger symbol registration
        import geolipi.symbolic.primitives_2d
        import geolipi.symbolic.primitives_3d
        import geolipi.symbolic.primitives_higher
        import geolipi.symbolic.transforms_2d
        import geolipi.symbolic.transforms_3d
        import geolipi.symbolic.combinators
        import geolipi.symbolic.color
        import geolipi.symbolic.variables
        import geolipi.symbolic.reference
        
        from geolipi.symbolic.base import GLFunction
        from geolipi.symbolic.registry import SYMBOL_REGISTRY
    except Exception as e:
        print(f"Warning: Could not import geolipi: {e}")
        return []
    
    node_info_list: List[Dict] = []
    
    # Process all registered symbols from geolipi
    for class_name, cls in SYMBOL_REGISTRY.items():
        if not issubclass(cls, GLFunction):
            continue
        if class_name in EXCLUDE_SYMBOLS:
            continue
            
        # Get the source module to determine category
        module_path = getattr(cls, "__module__", "")
        
        # Only process geolipi modules
        if not module_path.startswith("geolipi.symbolic"):
            continue
            
        category = _get_category_from_module(module_path)
        
        # Skip if no category could be determined
        if not category:
            continue
            
        # Try to get default_spec
        try:
            spec = cls.default_spec()
            if not isinstance(spec, dict):
                continue
        except Exception:
            continue

        arg_keys = list(spec.keys())
        arg_types = {k: (v.get("type", "") if isinstance(v, dict) else "") for k, v in spec.items()}
        is_variadic = any(isinstance(v, dict) and (v.get("varadic", False) or v.get("variadic", False)) for v in spec.values())
        
        # Extract default values from spec
        default_values = {}
        for k, v in spec.items():
            if isinstance(v, dict) and "default" in v:
                default_values[k] = v["default"]

        node_info = {
            'name': class_name,
            'expr_class_name': class_name,
            'expr_class_module': module_path,
            'arg_keys': arg_keys,
            'default_values': default_values,
            'is_variadic': is_variadic,
            'category': category,
            'arg_types': arg_types
        }
        node_info_list.append(node_info)
    
    return node_info_list


def _collect_sysl_nodes() -> List[Dict]:
    """Collect nodes from sysl registry, organized by source files."""
    try:
        # Import all sysl.symbolic modules to trigger symbol registration
        import sysl.symbolic.base
        import sysl.symbolic.materials
        import sysl.symbolic.mat_solid_combinators

        from geolipi.symbolic.base import GLFunction
        from geolipi.symbolic.registry import SYMBOL_REGISTRY
    except Exception as e:
        print(f"Warning: Could not import sysl: {e}")
        import traceback
        traceback.print_exc()
        return []
    
    node_info_list: List[Dict] = []
    
    # Process all registered symbols from sysl
    for class_name, cls in SYMBOL_REGISTRY.items():
        if not issubclass(cls, GLFunction):
            continue
        if class_name in EXCLUDE_SYMBOLS:
            continue
            
        # Get the source module to determine category
        module_path = getattr(cls, "__module__", "")
        
        # Only process sysl modules
        if not module_path.startswith("sysl.symbolic"):
            continue
            
        category = _get_category_from_module(module_path)
        
        # Skip if no category could be determined
        if not category:
            continue
            
        # Try to get default_spec
        try:
            spec = cls.default_spec()
            if not isinstance(spec, dict):
                continue
        except Exception:
            continue

        arg_keys = list(spec.keys())
        arg_types = {k: (v.get("type", "") if isinstance(v, dict) else "") for k, v in spec.items()}
        is_variadic = any(isinstance(v, dict) and (v.get("varadic", False) or v.get("variadic", False)) for v in spec.values())
        
        # Extract default values from spec
        default_values = {}
        for k, v in spec.items():
            if isinstance(v, dict) and "default" in v:
                default_values[k] = v["default"]

        node_info = {
            'name': class_name,
            'expr_class_name': class_name,
            'expr_class_module': module_path,
            'arg_keys': arg_keys,
            'default_values': default_values,
            'is_variadic': is_variadic,
            'category': category,
            'arg_types': arg_types
        }
        node_info_list.append(node_info)
    
    return node_info_list


def _get_category_from_module(module_path: str) -> str:
    """Determine category based on the module path."""
    if not module_path:
        raise ValueError("Module path is empty")
    
    mode = module_path.split(".")[-1]
    return mode


def _generate_file_content(all_node_info: List[Dict], library_name: str) -> str:
    """Generate the Python file content for all nodes."""
    
    # File header
    content = f'''"""
Auto-generated {library_name} nodes for ASMBLR.

This file is automatically generated by asmblr.auto_loader.
Do not edit this file manually - regenerate it instead.
"""

from typing import List
from ..expr_node import GLNode
from ..base import InputSocket
from ..simple_registry import register_node_decorator


'''
    
    # Generate node classes
    for node_info in all_node_info:
        content += _generate_node_class(node_info)
        content += "\n\n"
    
    # Generate registration function
    content += "def register_all_nodes() -> List[str]:\n"
    content += f'    """Return list of all auto-registered {library_name} nodes."""\n'
    content += "    # All nodes are registered via the @register_node_decorator\n"
    content += "    return [\n"
    for node_info in all_node_info:
        node_name = node_info['name']
        content += f'        "{node_name}",\n'
    content += "    ]\n"
    
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
    category = node_info.get('category', 'unknown')
    
    # Import statement for the expression class
    import_line = f"# {expr_class_module}.{expr_class_name}"
    
    class_def = f'''@register_node_decorator
class {name}(GLNode):
    """{import_line}"""
    # Associate the expression class at class level for external tools
    import {expr_class_module} as _expr_mod
    expr_class = _expr_mod.{expr_class_name}
    
    # Embed category metadata in the class
    node_category = "{category}"
    
    def __init__(self, *args, **kwargs):
        # Keep super init simple; expr_class is already bound at class-level
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


# Auto-load nodes when module is imported
import os
if os.environ.get('ASMBLR_DISABLE_AUTO_LOAD') != '1':
    _loaded_nodes = load_all_symbolic_nodes()
    print(f"Auto-registered {len(_loaded_nodes)} nodes")

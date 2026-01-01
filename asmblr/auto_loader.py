"""
Automatic node loader for ASMBLR.
This module can generate static Python files containing all symbolic nodes from GeoLIPI, SySL, 
and optionally Migumi libraries. Nodes are organized by their source files and use the 
respective registry systems.

Required dependencies: geolipi, sysl
Optional dependencies: migumi
"""

from typing import List, Callable, Type, Dict, Optional
import inspect
import logging
import os
from pathlib import Path

_logger = logging.getLogger(__name__)

# Required imports - geolipi and sysl
import geolipi.symbolic as gls
import geolipi.symbolic.primitives_2d as gls_prim2d
import geolipi.symbolic.primitives_3d as gls_prim3d
import geolipi.symbolic.primitives_higher as gls_prim_higher
import geolipi.symbolic.transforms_2d as gls_t2d
import geolipi.symbolic.transforms_3d as gls_t3d
import geolipi.symbolic.combinators as gls_comb
import geolipi.symbolic.color as gls_color
import geolipi.symbolic.variables as gls_vars

import sysl.symbolic.base as sysl_base
import sysl.symbolic.materials as sysl_materials
import sysl.symbolic.mat_solid_combinators as sysl_mat_solid_combinators

from geolipi.symbolic.registry import SYMBOL_REGISTRY

from .simple_registry import register_node, NODE_REGISTRY


# Track available optional libraries
def _check_migumi_available() -> bool:
    """Check if migumi library is available."""
    try:
        import migumi
        return True
    except ImportError:
        return False


MIGUMI_AVAILABLE = _check_migumi_available()

# Symbols we exclude from auto-generation; implemented manually elsewhere
EXCLUDE_SYMBOLS = {
    'VarSplitter',
    'EvaluateLayoutNode', 
    "PolyArc2D", 
    "RegisterGeometry",
    "RegisterState",
}


def get_classes_in_module(module):
    return {
        name: cls
        for name, cls in inspect.getmembers(module, inspect.isclass)
        if cls.__module__ == module.__name__
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
    geolipi_module_dict = {}
    modules_to_collect = [gls_prim2d, gls_prim3d, gls_prim_higher, gls_t2d, gls_t3d, gls_comb, gls_color, gls_vars]
    for module in modules_to_collect:
        class_dict = get_classes_in_module(module)
        valid_subset = {name: cls for name, cls in class_dict.items() if name in SYMBOL_REGISTRY}
        geolipi_module_dict.update(valid_subset)
    geolipi_node_info = _collect_module_nodes(geolipi_module_dict)
    
    # Generate the Python file content
    file_content = _generate_file_content(geolipi_node_info, "GeoLIPI")
    
    # Write the file
    with open(output_file, 'w') as f:
        f.write(file_content)
    
    _logger.info(f"Generated {len(geolipi_node_info)} GeoLIPI nodes in: {output_file}")
    
    return str(output_file)


def generate_all_nodes_files(output_dir: Optional[str] = None) -> Dict[str, Optional[str]]:
    """
    Generate static Python files for all available symbolic libraries.
    
    This function generates node files for:
        - geolipi (required)
        - sysl (required)
        - migumi (optional, if available)
    
    Args:
        output_dir: Directory to save the generated files. Defaults to auto_nodes/
        
    Returns:
        Dictionary mapping library name to the generated file path (or None if skipped).
    """
    results = {}
    
    # Required: GeoLIPI
    results['geolipi'] = generate_geolipi_nodes_file(output_dir)
    
    # Required: SySL
    results['sysl'] = generate_sysl_nodes_file(output_dir)
    
    # Optional: Migumi
    if MIGUMI_AVAILABLE:
        results['migumi'] = generate_migumi_nodes_file(output_dir)
    else:
        results['migumi'] = None
        _logger.info("Migumi is not available, skipping migumi nodes generation.")
    
    return results


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
    sysl_module_dict = {}
    modules_to_collect = [sysl_base, sysl_materials, sysl_mat_solid_combinators]
    for module in modules_to_collect:
        class_dict = get_classes_in_module(module)
        valid_subset = {name: cls for name, cls in class_dict.items() if name in SYMBOL_REGISTRY}
        sysl_module_dict.update(valid_subset)
    sysl_node_info = _collect_module_nodes(sysl_module_dict)
    
    # Generate the Python file content
    file_content = _generate_file_content(sysl_node_info, "SySL")
    
    # Write the file
    with open(output_file, 'w') as f:
        f.write(file_content)
    
    _logger.info(f"Generated {len(sysl_node_info)} SySL nodes in: {output_file}")
    return str(output_file)

def generate_migumi_nodes_file(output_dir: Optional[str] = None) -> Optional[str]:
    """
    Generate a static Python file containing all Migumi nodes.
    
    Returns:
        Path to the generated file, or None if migumi is not available.
    """
    if not MIGUMI_AVAILABLE:
        _logger.info("Migumi is not available, skipping migumi nodes generation.")
        return None
    
    # Import migumi modules only when needed
    import migumi.symbolic.base as migumi_base
    import migumi.symbolic.base_old as migumi_base_old
    
    if output_dir is None:
        current_dir = Path(__file__).parent
        output_dir = os.path.join(current_dir, "auto_nodes")
    output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)
    output_file = os.path.join(output_dir, "migumi_nodes.py")

    # Collect migumi node information
    migumi_module_dict = {}
    modules_to_collect = [migumi_base_old]
    for module in modules_to_collect:
        class_dict = get_classes_in_module(module)
        valid_subset = {name: cls for name, cls in class_dict.items() if name in SYMBOL_REGISTRY}
        migumi_module_dict.update(valid_subset)

    migumi_node_info = _collect_module_nodes(migumi_module_dict)

    # Generate the Python file content
    file_content = _generate_file_content(migumi_node_info, "Migumi")
    
    # Write the file
    with open(output_file, 'w') as f:
        f.write(file_content)
    
    _logger.info(f"Generated {len(migumi_node_info)} Migumi nodes in: {output_file}")
    return str(output_file)



def load_all_symbolic_nodes() -> List[str]:
    """
    Load all nodes from available symbolic libraries.
    
    Required libraries (always loaded):
        - geolipi
        - sysl
    
    Optional libraries (loaded if available):
        - migumi
    
    Returns:
        List of all registered node names.
    """
    all_nodes = []
    
    # Required: GeoLIPI nodes
    geolipi_nodes = load_all_geolipi_nodes()
    all_nodes.extend(geolipi_nodes)
    
    # Required: SySL nodes
    sysl_nodes = load_all_sysl_nodes()
    all_nodes.extend(sysl_nodes)
    
    # Optional: Migumi nodes (only if available)
    if MIGUMI_AVAILABLE:
        migumi_nodes = load_all_migumi_nodes()
        all_nodes.extend(migumi_nodes)
    
    # Future optional libraries:
    # if SPLITWEAVE_AVAILABLE:
    #     splitweave_nodes = load_all_splitweave_nodes()
    #     all_nodes.extend(splitweave_nodes)
    # if SUPERFIT_AVAILABLE:
    #     superfit_nodes = load_all_superfit_nodes()
    #     all_nodes.extend(superfit_nodes)
    # if PARSEL_AVAILABLE:
    #     parsel_nodes = load_all_parsel_nodes()
    #     all_nodes.extend(parsel_nodes)
    
    return all_nodes


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
        _logger.info("Auto-generated geolipi nodes not found. Generating geolipi_nodes.py...")
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
        _logger.info("Auto-generated sysl nodes not found. Generating sysl_nodes.py...")
        generate_sysl_nodes_file()
        
        # Now import and use the generated file
        from .auto_nodes.sysl_nodes import register_all_nodes
        registered_names = register_all_nodes()
        return registered_names

def load_all_migumi_nodes() -> List[str]:
    """
    Load all nodes from migumi symbolic library automatically.
    
    This function first tries to import from auto_nodes/. If that fails,
    it generates the auto_nodes file and then imports from it.
    
    Returns:
        List of registered node names, or empty list if migumi is not available.
    """
    if not MIGUMI_AVAILABLE:
        return []
    
    try:
        # Try to import from pre-generated auto_nodes
        from .auto_nodes.migumi_nodes import register_all_nodes
        registered_names = register_all_nodes()
        return registered_names
    except ImportError:
        # Auto_nodes doesn't exist, generate it
        _logger.info("Auto-generated migumi nodes not found. Generating migumi_nodes.py...")
        result = generate_migumi_nodes_file()
        if result is None:
            return []
        
        # Now import and use the generated file
        from .auto_nodes.migumi_nodes import register_all_nodes
        registered_names = register_all_nodes()
        return registered_names

def _collect_module_nodes(module_dict) -> List[Dict]:
    """Collect nodes from geolipi registry, organized by source files."""
    import sys
    from pathlib import Path
    
    # Add the project paths to sys.path if not already there
    project_root = Path(__file__).parent.parent.parent  # Go up to mpspy root
    geolipi_path = os.path.join(project_root, "geolipi")
    
    if str(geolipi_path) not in sys.path:
        sys.path.insert(0, str(geolipi_path))
    
    
    node_info_list: List[Dict] = []
    

    # Process all registered symbols from geolipi
    for class_name, cls in module_dict.items():
        if class_name in EXCLUDE_SYMBOLS:
            continue
            
        # Get the source module to determine category
        module_path = getattr(cls, "__module__", "")
        

        if hasattr(cls, "symbol_category"):
            category = cls.symbol_category
        else:
            category = _get_category_from_module(module_path)
        
        if not hasattr(cls, "default_spec"):
            continue
        try:
            spec = cls.default_spec()
            if not isinstance(spec, dict):
                continue
        except Exception:
            continue

        if not isinstance(spec, dict):
            _logger.warning(f"default spec for {class_name}: {spec}")
            raise ValueError(f"Default spec for {class_name} is not a dictionary")

        arg_keys = list(spec.keys())
        arg_types = {k: (v.get("type", "") if isinstance(v, dict) else "") for k, v in spec.items()}
        is_variadic = any(isinstance(v, dict) and (v.get("variadic", False) or v.get("variadic", False)) for v in spec.values())
        
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
if os.environ.get('ASMBLR_DISABLE_AUTO_LOAD') != '1':
    _loaded_nodes = load_all_symbolic_nodes()
    _logger.debug(f"Auto-registered {len(_loaded_nodes)} nodes")

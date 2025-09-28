"""
Generate a frontend-friendly nodes.json from asmblr nodes.

Rules:
- Uses class-level expr_class and its default_specs()/default_spec() to discover inputs.
- Expression-typed inputs (Expr[...]) become socket-only inputs.
- Non-expression params become inputs with sockets AND linked controls.
- No min/max are emitted. Defaults are retained. Step is handled in frontend theme.

Usage:
  python asmblr/scripts/asmblr_frontend_json.py --out asmblr/nodes.json
"""

import argparse
import json
import os
from typing import Any, Dict, List

from asmblr.auto_loader import load_all_geolipi_nodes, load_all_sysl_nodes  # noqa: F401 (ensures registry is populated)
from asmblr.simple_registry import NODE_REGISTRY

# Ensure both geolipi and sysl nodes are loaded
load_all_geolipi_nodes()
load_all_sysl_nodes()


# Type mapping constants
SOCKET_TYPE_MAP = {
    # Vector types
    'vector[2]': 'VectorSocket',
    'vector[3]': 'VectorSocket', 
    'vector[4]': 'VectorSocket',
    'vec2': 'VectorSocket',
    'vec3': 'VectorSocket',
    'vec4': 'VectorSocket',
    # Matrix types
    'matrix[': 'VectorSocket',  # prefix match
    # Tensor types
    'tensor[': 'VectorSocket',  # prefix match
    # Numeric types
    'float': 'FloatSocket',
    'int': 'FloatSocket',
    'number': 'FloatSocket',
    # Boolean types
    'bool': 'BoolSocket',
    'boolean': 'BoolSocket',
    # String types
    'str': 'StringSocket',
    'string': 'StringSocket',
}

CONTROL_TYPE_MAP = {
    # Vector types
    'vector[2]': 'vector2',
    'vector[3]': 'vector3',
    'vector[4]': 'vector4',
    'vector[': 'vector3',  # default for other vector types
    # Numeric types
    'float': 'float',
    'int': 'float',
    'number': 'float',
    # Boolean types
    'bool': 'checkbox',
    'boolean': 'checkbox',
    # String types
    'str': 'string',
    'string': 'string',
}

# Expression type prefixes
EXPR_TYPE_PREFIXES = ('expr', 'expr[')

# Default socket and control types
DEFAULT_SOCKET_TYPE = 'ExprSocket'
DEFAULT_CONTROL_TYPE = 'string'


def _get_spec(expr_class) -> Dict[str, Any]:
    # Prefer default_specs (plural) if available; else default_spec
    spec = None
    if hasattr(expr_class, 'default_specs') and callable(expr_class.default_specs):
        try:
            spec = expr_class.default_specs()
        except Exception:
            spec = None
    if spec is None and hasattr(expr_class, 'default_spec') and callable(expr_class.default_spec):
        try:
            spec = expr_class.default_spec()
        except Exception:
            spec = None
    if not isinstance(spec, dict):
        return {}
    return spec


def _is_expr_type(type_str: str) -> bool:
    """Check if a type string represents an expression type."""
    normalized_type = (type_str or '').lower()
    return normalized_type.startswith(EXPR_TYPE_PREFIXES)


def _socket_type_for(type_str: str) -> str:
    """Get the socket type for a given type string."""
    normalized_type = (type_str or '').lower()
    
    # Check exact matches first
    if normalized_type in SOCKET_TYPE_MAP:
        return SOCKET_TYPE_MAP[normalized_type]
    
    # Check prefix matches for complex types
    for type_key, socket_type in SOCKET_TYPE_MAP.items():
        if type_key.endswith('[') and normalized_type.startswith(type_key):
            return socket_type
    
    return DEFAULT_SOCKET_TYPE


def _control_type_for(type_str: str) -> str:
    """Get the control type for a given type string."""
    normalized_type = (type_str or '').lower()
    
    # Check exact matches first
    if normalized_type in CONTROL_TYPE_MAP:
        return CONTROL_TYPE_MAP[normalized_type]
    
    # Check prefix matches for complex types (like vector[N])
    for type_key, control_type in CONTROL_TYPE_MAP.items():
        if type_key.endswith('[') and normalized_type.startswith(type_key):
            return control_type
    
    return DEFAULT_CONTROL_TYPE


def _get_category_from_module_path(module_path: str) -> str:
    """Determine category based on the module path."""
    if not module_path:
        return "unknown"
    
    # GeoLIPI categories
    if "geolipi.symbolic" in module_path:
        if "primitives_2d" in module_path:
            return "primitives_2d"
        elif "primitives_3d" in module_path:
            return "primitives_3d"
        elif "primitives_higher" in module_path:
            return "primitives_higher"
        elif "transforms_2d" in module_path:
            return "transforms_2d"
        elif "transforms_3d" in module_path:
            return "transforms_3d"
        elif "combinators" in module_path:
            return "combinators"
        elif "color" in module_path:
            return "color"
        elif "variables" in module_path:
            return "variables"
        elif "reference" in module_path:
            return "reference"
        else:
            return "geolipi_other"
    
    # SySL categories
    elif "sysl.symbolic" in module_path:
        if "base" in module_path:
            return "sysl_base"
        elif "materials" in module_path:
            return "sysl_materials"
        elif "mat_solid_combinators" in module_path:
            return "sysl_combinators"
        else:
            return "sysl_other"
    
    return "auto"


def build_nodes_payload() -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []

    for node_name, node_cls in NODE_REGISTRY.items():
        expr_class = getattr(node_cls, 'expr_class', None)
        spec = _get_spec(expr_class) if expr_class is not None else {}

        # Fallback: try instance-level expr_class if class-level missing
        if (not spec) and (expr_class is None):
            try:
                inst = node_cls()
                expr_class = getattr(inst, 'expr_class', None)
                spec = _get_spec(expr_class) if expr_class is not None else {}
            except Exception:
                spec = {}

        inputs: List[Dict[str, Any]] = []
        controls: List[Dict[str, Any]] = []

        for key, entry in spec.items():
            entry = entry if isinstance(entry, dict) else {}
            type_str = entry.get('type', '')
            default_val = entry.get('default', None)
            variadic = bool(entry.get('variadic') or entry.get('varadic') or False)

            if _is_expr_type(type_str):
                inputs.append({
                    'key': key,
                    'label': key.replace('_', ' ').title(),
                    'socketType': 'ExprSocket',
                    'required': True,
                    'variadic': variadic
                })
            else:
                socket_type = _socket_type_for(type_str)
                inputs.append({
                    'key': key,
                    'label': key.replace('_', ' ').title(),
                    'socketType': socket_type,
                    'required': False,
                    'variadic': variadic
                })
                controls.append({
                    'key': key,
                    'type': _control_type_for(type_str),
                    'label': key.replace('_', ' ').title(),
                    'linkedToInput': key,
                    'hasSocket': True,
                    'socketType': socket_type,
                    'config': {
                        'defaultValue': default_val
                    },
                    'showLabel': True
                })

        # Get category from node class metadata (embedded during auto-generation)
        category = getattr(node_cls, 'node_category', 'auto')
        module_path = getattr(expr_class, "__module__", "") if expr_class else ""
        
        node_payload = {
            'type': node_name,
            'label': node_name,
            'category': category,
            'description': f'Auto-generated from {module_path}.' if expr_class else 'Auto-generated',
            'inputs': inputs,
            'outputs': [
                { 'key': 'expr', 'label': 'expr', 'socketType': 'ExprSocket' }
            ],
            'controls': controls,
        }
        nodes.append(node_payload)

    return { 'nodes': nodes }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, default=os.path.join('asmblr', 'nodes.json'))
    args = parser.parse_args()

    payload = build_nodes_payload()
    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote nodes JSON: {out_path} ({len(payload.get('nodes', []))} nodes)")


if __name__ == '__main__':
    main()



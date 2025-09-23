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

from asmblr.auto_loader import load_all_geolipi_nodes  # noqa: F401 (ensures registry is populated)
from asmblr.simple_registry import NODE_REGISTRY


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
    ts = (type_str or '').lower()
    return ts.startswith('expr') or ts.startswith('expr[')


def _socket_type_for(type_str: str) -> str:
    t = (type_str or '').lower()
    if t.startswith('vector[') or t in ('vec2', 'vec3', 'vec4'):
        return 'VectorSocket'
    if t.startswith('matrix['):
        return 'VectorSocket'
    if t.startswith('tensor['):
        return 'VectorSocket'
    if t in ('float', 'int', 'number'):
        return 'FloatSocket'
    if t in ('bool', 'boolean'):
        return 'BoolSocket'
    if t in ('str', 'string'):
        return 'StringSocket'
    return 'ExprSocket'


def _control_type_for(type_str: str) -> str:
    t = (type_str or '').lower()
    if t.startswith('vector['):
        if '[2]' in t:
            return 'vector2'
        if '[3]' in t:
            return 'vector3'
        if '[4]' in t:
            return 'vector4'
        return 'vector3'
    if t in ('float', 'int', 'number'):
        return 'float'
    if t in ('bool', 'boolean'):
        return 'checkbox'
    if t in ('str', 'string'):
        return 'string'
    return 'string'


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

        node_payload = {
            'type': node_name,
            'label': node_name,
            'category': 'auto',
            'description': f'Auto-generated from {getattr(expr_class, "__module__", "")}.' if expr_class else 'Auto-generated',
            'inputs': inputs,
            'outputs': [
                { 'key': 'expr', 'label': 'Expression', 'socketType': 'ExprSocket' }
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



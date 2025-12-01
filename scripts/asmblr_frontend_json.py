"""
Generate a frontend-friendly nodes.json from asmblr nodes.

Rules:
- Uses class-level expr_class and its default_specs()/default_spec() to discover inputs.
- Expression-typed inputs (Expr[...]) become socket-only inputs.
- Non-expression params become inputs with sockets AND linked controls.
- No min/max are emitted. Defaults are retained. Step is handled in frontend theme.

Usage:
  python asmblr/scripts/asmblr_frontend_json.py --out nodes.json
"""

import argparse
import json
import os
from typing import Any, Dict, List

from asmblr.auto_loader import load_all_geolipi_nodes, load_all_sysl_nodes  # noqa: F401 (ensures registry is populated)
from asmblr.simple_registry import NODE_REGISTRY


# Type mapping constants - simplified approach
# All sockets are expressions, controls use raw type strings
EXCLUDE_SYMBOLS = {
    'JoinUnion', 'EncodedRGBGrid3D', 'RGBGrid3D', "SDFGrid3D",
    "TileUV2D", "SinRepeatX2D", "SinRepeatY2D",
    "SinAlongAxisY2D", "SinDiagonal2D", "SinDiagonalFlip2D",
    "SinRadial2D", "SquiggleX2D", "SquiggleY2D",
    "SquiggleDiagonal2D", "SquiggleDiagonalFlip2D",
    "SquiggleRadial2D", "SquiggleDistortion2D",
    "EncodedLowPrecisionSDFGrid3D", "EncodedSDFGrid3D", "LowPrecisionSDFGrid3D"
}
# Expression type prefixes
EXPR_TYPE_PREFIXES = ('expr', 'expr[')


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





def build_nodes_payload() -> Dict[str, Any]:
    nodes: List[Dict[str, Any]] = []

    for node_name, node_cls in NODE_REGISTRY.items():
        if node_name in EXCLUDE_SYMBOLS:
            continue
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
            variadic = bool(entry.get('variadic') or entry.get('variadic') or False)
            if _is_expr_type(type_str):
                inputs.append({
                    'key': key,
                    'label': key.replace('_', ' ').title(),
                    'required': True,
                    'variadic': variadic
                })
            else:
                inputs.append({
                    'key': key,
                    'label': key.replace('_', ' ').title(),
                    'required': False,
                    'variadic': variadic
                })
                controls.append({
                    'key': key,
                    'type': type_str,
                    'label': key.replace('_', ' ').title(),
                    'linkedToInput': key,
                    'hasSocket': True,
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
                { 'key': 'expr', 'label': 'expr' }
            ],
            'controls': controls,
        }
        nodes.append(node_payload)

    return { 'nodes': nodes }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, default='./nodes.json')
    args = parser.parse_args()

    payload = build_nodes_payload()
    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote nodes JSON: {out_path} ({len(payload.get('nodes', []))} nodes)")


if __name__ == '__main__':
    main()



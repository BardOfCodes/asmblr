"""
Node access module for ASMBLR.
Provides direct access to all registered nodes as anode.NodeName.

Usage:
    import asmblr.nodes as anode
    sphere = anode.Sphere3D(radius=1.0)
    union = anode.Union(sphere, box)
"""

from .simple_registry import NODE_REGISTRY


def __getattr__(name):
    """
    Get a node class by name when accessed as anode.NodeName.
    This uses Python 3.7+ module-level __getattr__ for clean dynamic access.
    """
    if name in NODE_REGISTRY:
        return NODE_REGISTRY[name]
    raise AttributeError(f"Node '{name}' not found. Available nodes: {list(NODE_REGISTRY.keys())}")


def __dir__():
    """Support for tab completion and dir(anode)."""
    return list(NODE_REGISTRY.keys())


def list_nodes():
    """List all available nodes."""
    return list(NODE_REGISTRY.keys())


def search_nodes(pattern: str):
    """Search for nodes matching a pattern."""
    import re
    regex = re.compile(pattern, re.IGNORECASE)
    return [name for name in NODE_REGISTRY.keys() if regex.search(name)]

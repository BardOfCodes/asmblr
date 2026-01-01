"""
Node access module for ASMBLR.
Provides direct access to all registered nodes as anode.NodeName.

Usage:
    import asmblr.nodes as anode
    sphere = anode.Sphere3D(radius=1.0)
    union = anode.Union(sphere, box)
    
For node discovery functions, use the main asmblr module:
    import asmblr
    asmblr.list_nodes()
    asmblr.search_nodes("sphere")
"""

from .simple_registry import NODE_REGISTRY


def __getattr__(name):
    """
    Get a node class by name when accessed as anode.NodeName.
    This uses Python 3.7+ module-level __getattr__ for clean dynamic access.
    """
    if name in NODE_REGISTRY:
        return NODE_REGISTRY[name]
    raise AttributeError(f"Node '{name}' not found. Use asmblr.list_nodes() to see available nodes.")


def __dir__():
    """Support for tab completion and dir(anode)."""
    return list(NODE_REGISTRY.keys())

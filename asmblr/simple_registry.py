"""
Simple node registry system for ASMBLR - following the geolipi pattern.
Just a dictionary mapping node names to node classes.
"""

import inspect
from typing import Dict, Type, Callable, List, Any, Optional

# Global registry - simple dictionary like geolipi
NODE_REGISTRY: Dict[str, Type] = {}

def register_node(node_class: Type) -> Type:
    """Register a node class in the global registry."""
    NODE_REGISTRY[node_class.__name__] = node_class
    return node_class

def register_node_decorator(node_class: Type) -> Type:
    """Decorator to register a node class in the global registry."""
    return register_node(node_class)
"""
Simple node inspection utilities for ASMBLR.
"""

from typing import List, Union, Type
from .simple_registry import NODE_REGISTRY


def inspect_node(node_or_class: Union[Type, object]) -> None:
    """Print basic information about a node class or instance."""
    # Handle both class and instance
    if isinstance(node_or_class, type):
        node_class = node_or_class
        try:
            node_instance = node_class()
        except Exception as e:
            print(f"{node_class.__name__}: Error creating instance - {e}")
            return
    else:
        node_instance = node_or_class
        node_class = node_instance.__class__
    
    print(f"{node_class.__name__}")
    
    # Show input sockets with type hints
    if hasattr(node_instance, 'input_sockets') and node_instance.input_sockets:
        inputs = list(node_instance.input_sockets.keys())
        if hasattr(node_instance, 'arg_types') and node_instance.arg_types:
            input_info = []
            for inp in inputs:
                type_hint = node_instance.arg_types.get(inp, 'float')
                input_info.append(f"{inp}:{type_hint}")
            print(f"  Inputs: [{', '.join(input_info)}]")
        else:
            print(f"  Inputs: {inputs}")
    else:
        print("  Inputs: []")
    
    # Show output sockets  
    if hasattr(node_instance, 'output_sockets') and node_instance.output_sockets:
        outputs = list(node_instance.output_sockets.keys())
        print(f"  Outputs: {outputs}")
    else:
        print("  Outputs: ['expr']")  # Default for most nodes
    
    # Show expression class if available
    if hasattr(node_instance, 'expr_class') and node_instance.expr_class:
        print(f"  Expression: {node_instance.expr_class.__name__}")


def list_nodes() -> List[str]:
    """Get list of all registered node names."""
    return sorted(NODE_REGISTRY.keys())


def search_nodes(pattern: str) -> List[str]:
    """Search for nodes matching a pattern (case-insensitive)."""
    import re
    regex = re.compile(pattern, re.IGNORECASE)
    return sorted([name for name in NODE_REGISTRY.keys() if regex.search(name)])




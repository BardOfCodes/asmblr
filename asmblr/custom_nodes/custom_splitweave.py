"""
Custom SplitWeave nodes that require special behavior and cannot be auto-generated.

SplitWeave is an optional library for advanced geometry operations.
Add custom SplitWeave nodes here if the library becomes available and
nodes require special handling.

Example:
    @register_node_decorator
    class MySplitWeaveNode(GLNode):
        node_category = 'splitweave'
        
        def _create_input_sockets(self):
            ...
        
        def _create_output_sockets(self):
            ...
        
        def inner_eval(self, sketcher=None, **kwargs):
            ...
"""

from ..expr_node import GLNode
from ..base import InputSocket, OutputSocket
from ..simple_registry import register_node_decorator

# Add custom SplitWeave nodes below as needed

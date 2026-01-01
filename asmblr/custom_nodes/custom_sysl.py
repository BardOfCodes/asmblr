"""
Custom SySL nodes that require special behavior and cannot be auto-generated.

SySL (Symbolic Shading Language) nodes are auto-generated in auto_nodes/sysl_nodes.py.
Add custom SySL nodes here only if they require:
- Multiple output sockets
- Special evaluation logic
- Custom input handling

Example:
    @register_node_decorator
    class MySySLNode(GLNode):
        node_category = 'materials'
        
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

# Add custom SySL nodes below as needed



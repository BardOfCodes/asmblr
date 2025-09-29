
import torch as th
import sympy as sp
from typing import Any, Dict
import geolipi.symbolic as gls
from .base import BaseNode, Connection, InputSocket, OutputSocket

VALID_INPUT_TYPES = (str, tuple, sp.Tuple, sp.Symbol, th.Tensor, gls.GLExpr, gls.GLFunction)

class GLNode(BaseNode):
    """Base class for nodes that wrap geometric/symbolic expressions."""
    
    def __init__(self, *args, **kwargs):
        """Initialize GLNode with expression class and arguments."""
        # Extract GLNode-specific parameters, but preserve existing attributes
        if 'expr_class' in kwargs:
            self.expr_class = kwargs.pop('expr_class')
        elif not hasattr(self, 'expr_class'):
            self.expr_class = None
        
        # Set up argument configuration, preserve existing if set
        if not hasattr(self, 'arg_keys'):
            self.arg_keys = []
        if not hasattr(self, 'default_values'):
            self.default_values = {}
        
        # Call parent constructor with remaining kwargs
        super().__init__(**kwargs)
        
        # Handle positional and keyword arguments for connections
        self._handle_node_arguments(args, kwargs)
    
    def _create_input_sockets(self) -> Dict[str, InputSocket]:
        """Create input sockets based on arg_keys."""
        return {
            key: InputSocket(key, self.default_values.get(key, None)) 
            for key in self.arg_keys
        }
    
    def _create_output_sockets(self) -> Dict[str, OutputSocket]:
        """Create output sockets - GLNode typically has one 'expr' output."""
        return {"expr": OutputSocket("expr", parent=self)}
    
    def _handle_node_arguments(self, args, kwargs):
        """Handle positional and keyword arguments for node connections."""
        # Handle positional arguments
        if hasattr(self, 'is_variadic') and self.is_variadic and len(args) > 0:
            # For variadic nodes, connect all args to the single input socket
            variadic_socket = self.arg_keys[0] if self.arg_keys else 'inputs'
            for arg in args:
                self._connect_or_set_input(variadic_socket, arg)
        else:
            # For non-variadic nodes, map args to sockets by index
            for ind, arg in enumerate(args):
                if ind >= len(self.arg_keys):
                    break  # Skip if we don't have enough sockets
                    
                input_socket_name = self.arg_keys[ind]
                self._connect_or_set_input(input_socket_name, arg)
        
        # Handle keyword arguments
        for key, value in kwargs.items():
            if key in self.input_sockets:
                self._connect_or_set_input(key, value)
    
    def _connect_or_set_input(self, socket_name: str, value):
        """Connect or set input based on value type."""
        if isinstance(value, BaseNode):
            # Connect node's expr output to this socket
            Connection(
                input_node=value, 
                output_socket="expr", 
                output_node=self, 
                input_socket=socket_name
            )
        elif isinstance(value, OutputSocket):
            # Connect specific output socket to this input
            Connection(
                input_node=value.parent, 
                output_socket=value.name, 
                output_node=self, 
                input_socket=socket_name
            )
        else:
            # Set direct value (float, tuple, bool, etc.)
            self.input_sockets[socket_name].set_value(value)
    
    def _get_input_socket_for_index(self, index: int) -> str:
        """Get the input socket name for a given positional argument index."""
        if index < len(self.arg_keys):
            return self.arg_keys[index]
        elif self.arg_keys:
            return self.arg_keys[-1]  # Default to last socket for overflow
        else:
            return "args"  # Fallback

    def inner_eval(self, sketcher=None, **kwargs):
        """Evaluate the GLNode by creating the expression."""
        # Gather arguments from inputs (these should now be evaluated expressions, not nodes)
        arguments = []
        for key in self.arg_keys:
            arg = self.inputs.get(key, None)
            if arg is None:
                break
            # For variadic nodes, don't wrap single expressions in tuples
            if hasattr(self, 'is_variadic') and self.is_variadic:
                for true_arg in arg:
                    if not isinstance(true_arg, VALID_INPUT_TYPES):
                        true_arg = (true_arg,)
                    arguments.append(true_arg)
            else:
                if not isinstance(arg, VALID_INPUT_TYPES):
                    arg = (arg,)
                arguments.append(arg)
        
        # Create the expression
        expr = self.expr_class(*arguments)
        self.register_output("expr", expr)


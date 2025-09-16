"""
Custom geolipi nodes that require special behavior and cannot be auto-generated.
"""

from ..expr_node import GLNode
from ..base import InputSocket, OutputSocket
from ..simple_registry import register_node
import sympy as sp
import torch as th
import geolipi.symbolic as gls


# Registration decorator
def auto_register(cls):
    """Decorator to automatically register a node class."""
    register_node(cls)
    return cls


@auto_register
class SplitVec2D(GLNode):
    """Split a 2D vector into its components - requires multiple outputs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.VarSplitter
    
    def _create_input_sockets(self):
        """Create input sockets for SplitVec2D."""
        self.arg_keys = ['expr']
        self.default_values = {}
        self.arg_types = {'expr': 'vec2'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}

    def _create_output_sockets(self):
        """Create output sockets for SplitVec2D - multiple outputs."""
        self.output_keys = ["value_1", "value_2"]
        return {key: OutputSocket(key, parent=self) for key in self.output_keys}

    def inner_eval(self, sketcher=None, **kwargs):
        """Custom evaluation for vector splitting."""
        arguments = [self.inputs.get(key, None) for key in self.arg_keys]
        
        # Process arguments
        marked_ind = len(arguments)
        for ind, arg in enumerate(arguments):
            if not isinstance(arg, (tuple, sp.Symbol, th.Tensor, gls.GLExpr, gls.GLFunction)):
                arguments[ind] = (arg,)
            if arg is None:
                marked_ind = ind
                break
        arguments = arguments[:marked_ind]
        
        # Create output for each component
        for ind, key in enumerate(self.output_keys):
            cur_expr = self.expr_class(*arguments, ind)
            self.register_output(key, cur_expr)


@auto_register
class SplitVec3D(SplitVec2D):
    """Split a 3D vector into its components - requires multiple outputs."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.VarSplitter
    
    def _create_input_sockets(self):
        """Create input sockets for SplitVec3D."""
        self.arg_keys = ['expr']
        self.default_values = {}
        self.arg_types = {'expr': 'vec3'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def _create_output_sockets(self):
        """Create output sockets for SplitVec3D - three outputs."""
        self.output_keys = ["value_1", "value_2", "value_3"]
        return {key: OutputSocket(key, parent=self) for key in self.output_keys}


@auto_register
class SplitVec4D(SplitVec2D):
    """Split a 4D vector into its components - requires multiple outputs."""
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.VarSplitter
    
    def _create_input_sockets(self):
        """Create input sockets for SplitVec4D."""
        self.arg_keys = ['expr']
        self.default_values = {}
        self.arg_types = {'expr': 'vec4'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def _create_output_sockets(self):
        """Create output sockets for SplitVec4D - four outputs."""
        self.output_keys = ["value_1", "value_2", "value_3", "value_4"]
        return {key: OutputSocket(key, parent=self) for key in self.output_keys}

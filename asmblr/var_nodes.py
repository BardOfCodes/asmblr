
from .expr_node import GLNode
from .base import InputSocket, OutputSocket
import sympy as sp
import torch as th
import geolipi.symbolic as gls

class UniformFloat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.expr_class = gls.UniformFloat
    
    def setup_base(self):
        self.arg_keys = ['min', 'value', 'max', 'name']
        self.default_values = {}

class UniformVec2(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.UniformVec2
    
    def setup_base(self):
        self.arg_keys = ['min', 'value', 'max', 'name']
        self.default_values = {}

class UniformVec3(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.UniformVec3
    
    def setup_base(self):
        self.arg_keys = ['min', 'value', 'max', 'name']
        self.default_values = {}

class UniformVec4(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.UniformVec4
    
    def setup_base(self):
        self.arg_keys = ['min', 'value', 'max', 'name']
        self.default_values = {}

class Float(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Float
    
    def setup_base(self):
        self.arg_keys = ['value']
        self.default_values = {}

class Vec2(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Vec2
    
    def setup_base(self):
        self.arg_keys = ['value_1', 'value_2']
        self.default_values = {}

class Vec3(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Vec3
    
    def setup_base(self):
        self.arg_keys = ['value_1', 'value_2', 'value_3']
        self.default_values = {}

class Vec4(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Vec4
    
    def setup_base(self):
        self.arg_keys = ['value_1', 'value_2', 'value_3', 'value_4']
        self.default_values = {}

class UnaryOperator(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.UnaryOperator
    
    def setup_base(self):
        self.arg_keys = ['expr', 'operator']
        self.default_values = {}

        
class BinaryOperator(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.BinaryOperator
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2', 'operator']
        self.default_values = {}

class VectorOperator(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.VectorOperator
    
    def setup_base(self):
        self.arg_keys = ['expr', 'operator']
        self.default_values = {}


class SplitVec2D(GLNode):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.VarSplitter
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.output_keys = ["value_1", "value_2"]
        self.default_values = {}

    def setup_sockets(self):
        self.input_sockets = {key: InputSocket(key, self.default_values.get(key, None)) for key in self.arg_keys}
        self.output_sockets = {key: OutputSocket(key, parent=self) for key in self.output_keys}

    def inner_eval(self, sketcher, copy=False):
        arguments = [self.inputs.get(key, None) for key in self.arg_keys]
        # IDEA - If anything is none - dont pass anything beyond it.
        marked_ind = len(arguments)
        for ind, arg in enumerate(arguments):
            if not isinstance(arg, (tuple, sp.Symbol, th.Tensor, gls.GLExpr, gls.GLFunction)):
                arguments[ind] = (arg,)
            if arg is None:
                marked_ind = ind
                break
        arguments = arguments[:marked_ind]
        for ind, key in enumerate(self.output_keys):
            cur_expr = self.expr_class(*arguments, ind)
            self.register_output(key, cur_expr)


class SplitVec3D(SplitVec2D):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.VarSplitter
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.output_keys = ["value_1", "value_2", "value_3"]
        self.default_values = {}
        
class SplitVec4D(SplitVec2D):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.VarSplitter
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.output_keys = ["value_1", "value_2", "value_3", "value_4"]
        self.default_values = {}

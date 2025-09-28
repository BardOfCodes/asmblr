
from ..expr_node import GLNode
from ..simple_registry import register_node_decorator
import geolipi.symbolic as gls
import sympy as sp
import torch as th


# polyline
@register_node_decorator
class PolyLine2D(GLNode):
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.PolyLine2D
    
    def setup_base(self):
        self.arg_keys = ['points']
        self.default_values = {}

    def inner_eval(self, sketcher=None, **kwargs):
        arguments = [self.inputs.get(key, None) for key in self.arg_keys]
        # IDEA - If anything is none - dont pass anything beyond it.
        if isinstance(arguments[0], (tuple, sp.Tuple)):
            # convert to list
            arguments = [tuple([tuple(x) for x in arguments[0]])]
        marked_ind = len(arguments)
        for ind, arg in enumerate(arguments):
            if not isinstance(arg, (tuple, str, sp.Symbol, th.Tensor, gls.GLExpr, gls.GLFunction)):
                arguments[ind] = (arg,)
            if arg is None:
                marked_ind = ind
                break
        arguments = arguments[:marked_ind]
        expr = self.expr_class(*arguments)
        self.register_output("expr", expr)


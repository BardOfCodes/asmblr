
from ..expr_node import GLNode
from ..simple_registry import register_node_decorator
import geolipi.symbolic as gls
import sympy as sp
import torch as th
from ..base import InputSocket, OutputSocket
from typing import Dict

# I think it should be the Symbols in MXG -> SOLID. 
# Extrusion. 
# polyline
@register_node_decorator
class PolyArc2D(GLNode):
    node_category = 'primitives_2d'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.PolyArc2D


    def _create_input_sockets(self):
        """Create input sockets for BoundedSolid."""
        self.default_values = {}
        self.arg_keys = ['points']
        self.arg_types = {'points': 'List[Vector[3]]'}
        self.is_variadic = False
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}


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

@register_node_decorator
class PolyLine2D(PolyArc2D):
    node_category = 'primitives_2d'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.PolyArc2D
        


@register_node_decorator
class RegisterGeometry(GLNode):
    """# migumi.symbolic.base.RegisterGeometry"""
    # Associate the expression class at class level for external tools
    import migumi.symbolic.base as _expr_mod
    expr_class = _expr_mod.RegisterGeometry
    
    # Embed category metadata in the class
    node_category = "mxg"
    
    def __init__(self, *args, **kwargs):
        # Keep super init simple; expr_class is already bound at class-level
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for RegisterGeometry."""
        self.arg_keys = ['expr', 'name', 'bbox']
        self.default_values = {}
        self.is_variadic = False
        self.arg_types = {'expr': 'Expr', 'name': 'str', 'bbox': 'Vector[3]'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}

    def _create_output_sockets(self) -> Dict[str, OutputSocket]:
        """Create output sockets - GLNode typically has one 'expr' output."""

        self.output_sockets = {
            "expr": OutputSocket("expr", parent=self),
            "name": OutputSocket("name", parent=self),
            "bbox": OutputSocket("bbox", parent=self),
        }
        return self.output_sockets

    def inner_eval(self, sketcher_2d=None, copy=False):
        expr = self.inputs.get('expr', None)
        name = self.inputs.get('name', None)
        bbox = self.inputs.get('bbox', None)

        self.register_output("expr", expr)
        self.register_output("name", name)
        self.register_output("bbox", bbox)

@register_node_decorator
class RegisterState(GLNode):
    """# migumi.symbolic.base.RegisterState"""
    # Associate the expression class at class level for external tools
    import migumi.symbolic.base as _expr_mod
    expr_class = _expr_mod.RegisterState
    
    # Embed category metadata in the class
    node_category = "mxg"
    
    def __init__(self, *args, **kwargs):
        # Keep super init simple; expr_class is already bound at class-level
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for RegisterState."""
        self.arg_keys = ['expr', 'state']
        self.default_values = {}
        self.is_variadic = False
        self.arg_types = {'expr': 'Expr', 'state': 'float'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}

    def _create_output_sockets(self) -> Dict[str, OutputSocket]:
        """Create output sockets - GLNode typically has one 'expr' output."""

        self.output_sockets = {
            "expr": OutputSocket("expr", parent=self),
            "state": OutputSocket("state", parent=self),
        }
        return self.output_sockets
    
    def inner_eval(self, sketcher_2d=None, copy=False):
        expr = self.inputs.get('expr', None)
        state = self.inputs.get('state', None)

        self.register_output("expr", expr)
        self.register_output("state", state)

@register_node_decorator
class PlaneV23D(GLNode):

    # Embed category metadata in the class
    node_category = "primitives_3d"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Plane3D

    def _create_input_sockets(self):
        """Create input sockets for BoundedSolid."""
        self.default_values = {}
        self.arg_keys = ['origin', 'normal']
        self.arg_types = {'origin': 'Vector[3]', 'normal': 'Vector[3]'}
        self.is_variadic = False
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}

    def setup_base(self):
        self.default_values = {}

@register_node_decorator
class DifferenceV2(GLNode):

    # Embed category metadata in the class
    node_category = "combinators"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Difference
    def _create_input_sockets(self):
        self.arg_keys = ['expr1', 'expr2']
        self.arg_types = {'expr1': 'Expr', 'expr2': 'Expr'}
        self.default_values = {}
        self.is_variadic = False
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
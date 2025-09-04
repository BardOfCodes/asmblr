
import torch as th
import sympy as sp
import geolipi.symbolic as gls
from typing import Any
from .base import BaseNode, Connection, InputSocket, OutputSocket

class GLNode(BaseNode):
    expr_class: Any
    def __init__(self, *args, **kwargs):
        # __init__ is now relaxed, just handling instance-specific setup
        super().__init__(*args, **kwargs)

    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}
        
    def setup_sockets(self):
        self.input_sockets = {key: InputSocket(key, self.default_values.get(key, None)) for key in self.arg_keys}
        self.output_sockets = {"expr": OutputSocket("expr", parent=self),}

    # This will just give the expression.
    def __new__(cls, *args, **kwargs):
        # Create the node instance using the default constructor
        instance = super(GLNode, cls).__new__(cls)

        # After setting up sockets in BaseNode, now handle connections
        for ind, arg in enumerate(args):
            if isinstance(arg, GLNode):
                current_keys = list(instance.input_sockets.keys())
                if ind < len(current_keys):
                    input_socket_name = list(instance.input_sockets.keys())[ind]
                else:
                    input_socket_name = current_keys[-1]
                Connection(input_node=arg, output_socket="expr", input_socket=input_socket_name, output_node=instance)
            elif isinstance(arg, (int, float, tuple, sp.Symbol, sp.Tuple, th.Tensor)):
                input_socket_name = list(instance.input_sockets.keys())[ind]
                instance.input_sockets[input_socket_name].set_value(arg)
            elif isinstance(arg, str):
                instance.input_sockets[input_socket_name].set_value(arg)
            else:
                print("type", type(arg))
                raise ValueError("What to do here?")
        # Handle keyword arguments (for params like width, height)
        for key, value in kwargs.items():
            if isinstance(value, BaseNode) and not isinstance(value, GLNode):
                raise ValueError("What to do here?")
            elif isinstance(value, OutputSocket):
                node = value.parent
                if node is None:
                    raise ValueError("OutputSocket's parent is None, cannot create Connection.")
                Connection(input_node=node, output_socket=value.name, output_node=instance, input_socket=key)
            else:
                instance.input_sockets[key].set_value(value)
                instance.default_values[key] = value
        

        return instance
    
    def inner_eval(self, sketcher, copy=False):
        arguments = [self.inputs.get(key, None) for key in self.arg_keys]
        # IDEA - If anything is none - dont pass anything beyond it.
        marked_ind = len(arguments)
        for ind, arg in enumerate(arguments):
            if not isinstance(arg, (tuple, str, sp.Tuple, sp.Symbol, th.Tensor, gls.GLExpr, gls.GLFunction)):
                arguments[ind] = (arg,)
            if arg is None:
                marked_ind = ind
                break
        arguments = arguments[:marked_ind]
        expr = self.expr_class(*arguments)
        self.register_output("expr", expr)


# MAP an expression in GEOLIPI to the corresponding one in SplitWeaver
# MAP an expresssion in layout to the corresponding one in SplitWeaver
import torch as th
from typing import Any
import sympy as sp
import base64
import geolipi.symbolic as gls
from geolipi.torch_compute.sympy_to_torch import SYMPY_TO_TEXT
from .base import BaseNode
from .simple_registry import NODE_REGISTRY

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def convert_to_asmblr(expr: Any):
    if isinstance(expr, (int, float, tuple, th.Tensor, sp.Float, sp.Integer, sp.Tuple)):
        return expr
    elif (not isinstance(expr, gls.GLFunction)) and isinstance(expr, gls.GLExpr):
        # A Custom Node. 
        # For now a BinaryGLExpr
        left = convert_to_asmblr(expr.args[0])
        right = convert_to_asmblr(expr.args[1])
        op = SYMPY_TO_TEXT[expr.func]
        import asmblr.nodes as anode
        binary_gl_expr = anode.BinaryOperator(left=left.output_sockets['expr'], 
                                      right=right.output_sockets['expr'], 
                                      op=op)
        return binary_gl_expr
    else:
        # Get the corresponding node class
        corresponding_class = NODE_REGISTRY.get(expr.__class__.__name__, None)
        if corresponding_class is None:
            raise ValueError(f"Node class {expr.__class__.__name__} not found in NODE_REGISTRY")
        
        # Convert arguments to appropriate values/nodes
        converted_args = []
        for arg in expr.args:
            if isinstance(arg, (sp.Symbol, sp.Float, sp.Integer, int, float, bool, str, tuple, sp.Tuple)):
                # Primitive value - convert to Python types
                if isinstance(arg, sp.Symbol):
                    if hasattr(expr, 'lookup_table') and arg in expr.lookup_table:
                        converted_args.append(expr.lookup_table[arg])
                    else:
                        converted_args.append(arg.name)
                elif isinstance(arg, (sp.Float, sp.Integer)):
                    converted_args.append(float(arg) if isinstance(arg, sp.Float) else int(arg))
                elif isinstance(arg, (sp.Tuple, tuple)):
                    # Convert sympy Tuple to Python tuple, handling nested values
                    if isinstance(arg, sp.Tuple):
                        converted_args.append(tuple(float(x) if isinstance(x, sp.Float) else 
                                                  int(x) if isinstance(x, sp.Integer) else x 
                                                  for x in arg))
                    else:
                        converted_args.append(arg)
                else:
                    converted_args.append(arg)
            else:
                # Sub-expression - recursively convert to node
                converted_args.append(convert_to_asmblr(arg))
        
        # Create node with converted arguments (using the new initialization pattern)
        return corresponding_class(*converted_args)
# MAP an expression in GEOLIPI to the corresponding one in SplitWeaver
# MAP an expresssion in layout to the corresponding one in SplitWeaver
import torch as th
from typing import Any
import sympy as sp
import base64
import geolipi.symbolic as gls
from .var_nodes import BinaryOperator
from .base import BaseNode
import asmblr.dag as asmdag
op_to_str = {
    sp.Add: "ADD",
    sp.Mul: "MUL",
    sp.Pow: "POW",
    sp.sin: "SIN",
    sp.cos: "COS",
    sp.tan: "TAN",
    sp.asin: "ASIN",
    sp.acos: "ACOS",
    sp.atan: "ATAN",
    sp.atan2: "ATAN2",
    sp.log: "LOG",
    sp.exp: "EXP",
    sp.Abs: "ABS",
    sp.Min: "MIN",
    sp.Max: "MAX",
    sp.floor: "FLOOR",
    sp.ceiling: "CEIL",
    sp.frac: "FRAC",
    sp.sign: "SIGN",
    sp.Mod: "MOD",
    # sp.step: "STEP",
    # sp.round: "ROUND",
    # sp.Normalize: "NORMALIZE",
    # sp.Norm: "NORM",
}

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
        op = op_to_str[expr.func]

        binary_gl_expr = BinaryOperator(left=left.output_sockets['expr'], 
                                      right=right.output_sockets['expr'], 
                                      op=op)
        return binary_gl_expr
    else:
        args_list = []
        for arg in expr.args:
            if isinstance(arg, sp.Symbol):
                if arg in expr.lookup_table:
                    arg = expr.lookup_table[arg]
                else:
                    arg = arg.name
            else:
                arg = convert_to_asmblr(arg)
            args_list.append(arg)
        
        corresponding_class = getattr(asmdag, expr.__class__.__name__)
        return corresponding_class(*args_list)
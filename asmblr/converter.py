# MAP an expression in GEOLIPI to the corresponding one in SplitWeaver
# MAP an expresssion in layout to the corresponding one in SplitWeaver
import torch as th
from typing import Any
import sympy as sp
import base64
import geolipi.symbolic as gls
from .base import BaseNode
from .simple_registry import NODE_REGISTRY
op_to_str = {
    # Basic arithmetic operations
    sp.Add: "add",
    sp.Mul: "mul", 
    sp.Pow: "pow",
    # Note: sub, div, neg are handled by analyzing Add/Mul args, not separate classes
    sp.sqrt: "sqrt",
    # Trigonometric functions
    sp.sin: "sin", 
    sp.cos: "cos",
    sp.tan: "tan",
    sp.asin: "asin",
    sp.acos: "acos",
    sp.atan: "atan",
    sp.atan2: "atan2",
    # Exponential and logarithmic
    sp.log: "log",
    sp.exp: "exp",
    # Comparison and utility functions
    sp.Abs: "abs",
    sp.Min: "min",
    sp.Max: "max",
    sp.floor: "floor",
    sp.ceiling: "ceil",
    sp.frac: "frac",
    sp.sign: "sign",
    sp.Mod: "mod",
    # Additional functions to match param_evaluate.py
    # Note: These may need custom SymPy implementations or special handling
    # "step": "step",      # No direct SymPy equivalent
    # "round": "round",    # sp.round exists but may need special handling
    # "normalize": "normalize",  # No direct SymPy equivalent  
    # "norm": "norm",      # No direct SymPy equivalent
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
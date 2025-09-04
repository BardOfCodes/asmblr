
from geolipi.torch_compute.evaluate_expression import recursive_evaluate
import geolipi.symbolic as gls
from geolipi.torch_compute.utils import COLOR_MAP, COMBINATOR_MAP, PRIMITIVE_MAP, NORMAL_MAP, MODIFIER_MAP, INVERTED_MAP, COLOR_FUNCTIONS
import patternator.executors.symbols as gs
from patternator.executors.evaluator import sym_to_fn_mapper
import os
import types
import string
import inspect
import sympy as sp

import splitweaver.symbolic as sws

from geolipi.symbolic.types import (
    MACRO_TYPE,
    MOD_TYPE,
    TRANSLATE_TYPE,
    SCALE_TYPE,
    PRIM_TYPE,
    TRANSSYM_TYPE,
    COMBINATOR_TYPE,
    TRANSFORM_TYPE,
    POSITIONALMOD_TYPE,
    SDFMOD_TYPE,
    HIGERPRIM_TYPE,
    COLOR_MOD,
    APPLY_COLOR_TYPE,
    SVG_COMBINATORS,
)
# First lets do geolipi Nodes
IGNORE_NODES = [gls.TileUV2D]

GEOLIPI_REMOVE_KEYS = ["points", "matrix", "args", "kwargs", "sdf_a", "sdf_b",
               "source", "destination", "color_canvas"]

class_template = string.Template("""
class $class_name($base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = $other_library.$class_name
    
    def setup_base(self):
        self.arg_keys = $arg_keys
        self.default_values = $default_values
""")
LAYOUT_REMOVE_KEYS = ['grid', "args", "kwargs", "resolution"]


def write_node_classes_to_file(converted_classes, filename, mode):
    with open(filename, 'w') as f:
        # Write the header with imports
        f.write("# Auto-generated Node Classes\n")
        f.write("from .base import BaseNode, InputSocket, OutputSocket\n")  # Adjust as needed
        if mode == "geolipi":
            f.write("from .geolipi_base import GLNode\n")  # Adjust as needed
            f.write("import geolipi.symbolic as gls\n\n")
        else:
            f.write("from .layout_base import LayoutNode\n")  # Adjust as needed
            f.write("import patternator.executors.symbols as gs\n\n")
        
        # Write each class definition
        for cur_cls in converted_classes:
            class_def = generate_class_code(cur_cls, mode)
            f.write(class_def)
            f.write("\n")
    

def convert_nodes(node_to_fn_map, mode):
    if mode == "geolipi":
        all_classes = gls.__dict__
    else:
        all_classes = gs.__dict__
    all_classes = [value for key, value in all_classes.items() if isinstance(value, type) and issubclass(value, gls.GLFunction)]
    all_classes = [cur_cls for cur_cls in all_classes if cur_cls not in IGNORE_NODES]
    
    converted_classes = []
    for cur_cls in all_classes:
        if cur_cls not in node_to_fn_map:
            continue
        node_fn = node_to_fn_map[cur_cls]
        glnode_version = get_swnode_version(cur_cls, node_fn, mode)
        converted_classes.append(glnode_version)
    
    return converted_classes

def get_geolip_type_args(cur_cls):
    return_list = []
    if issubclass(cur_cls, MACRO_TYPE):
        return_list.append('expr')
    elif issubclass(cur_cls, MOD_TYPE):
        return_list.append('expr')
    elif issubclass(cur_cls, PRIM_TYPE):
        pass
    elif issubclass(cur_cls, COMBINATOR_TYPE):
        if issubclass(cur_cls, (gls.Dilate2D, gls.Erode2D, gls.Dilate3D, gls.Erode3D, gls.Complement)):
            return_list.append('expr')
        else:
            return_list.append('expr1')
            return_list.append('expr2')
    elif issubclass(cur_cls, SVG_COMBINATORS):
        return_list.append('expr1')
        return_list.append('expr2')
    elif issubclass(cur_cls, APPLY_COLOR_TYPE):
        return_list.append('expr')
    elif issubclass(cur_cls, COLOR_MOD):
        return_list.append('expr')
    return return_list

def get_layout_type_args(cur_cls):
    return_list = []
    if issubclass(cur_cls, gs.InstantiateGrid):
        pass
    elif issubclass(cur_cls, gs.ConvertGrid):
        return_list.append('expr')
    elif issubclass(cur_cls, gs.PartitionGrid):
        return_list.append('expr')
    elif issubclass(cur_cls, gs.TransformGrid):
        return_list.append('expr')
    elif issubclass(cur_cls, gs.SignalTransformGrid):
        return_list.append('expr')
    elif issubclass(cur_cls, gs.Scalar2D):
        pass
    elif issubclass(cur_cls, gls.GLExpr):
        raise ValueError("This should not be here")
    elif issubclass(cur_cls, (sp.core.operations.AssocOp, sp.core.power.Pow)):
        raise ValueError("This should not be here")
    elif issubclass(cur_cls, gs.Param):
        return_list.append('expr')
    elif issubclass(cur_cls, sp.core.numbers.IntegerConstant):
        raise ValueError("This should not be here")
    elif issubclass(cur_cls, gs.GridBundle):
        raise ValueError("This should not be here")
    elif issubclass(cur_cls, sp.Symbol):
        raise ValueError("This should not be here")
    return return_list

def get_swnode_version(cur_cls, node_fn, mode="geolipi"):

    if mode == "geolipi":
        removekey_list = GEOLIPI_REMOVE_KEYS
        type_func = get_geolip_type_args
        base_class = sws.GLNode
    elif mode == "layout":
        removekey_list = LAYOUT_REMOVE_KEYS
        type_func = get_layout_type_args
        base_class = sws.LayoutNode
    sig = inspect.signature(node_fn)
    params = sig.parameters

    arg_keys = list(params.keys())
    for key in removekey_list:
        if key in arg_keys:
            arg_keys.remove(key)

    default_values = {
        name: param.default for name, param in params.items()
        if param.default is not inspect.Parameter.empty
    }
    # Type based additional parameters:
    type_args = type_func(cur_cls)
    arg_keys = type_args + arg_keys
    
    def __init__(self, *args, **kwargs):
        self.expr_class = cur_cls
        self.arg_keys = arg_keys
        self.default_values = default_values
        super(self.__class__, self).__init__(*args, **kwargs)

    node_class = types.new_class(
        cur_cls.__name__,
        (base_class,),
        exec_body = lambda ns: ns.update({
            "__init__": __init__,
            "expr_class": cur_cls,
            "arg_keys": arg_keys,
            "default_values": default_values
        })
    )
    return node_class




def generate_class_code(cls, mode="geolipi"):
    """Generate the source code for a dynamically created class."""
    class_name = cls.__name__
    arg_keys = str(cls.arg_keys)
    default_values = str(cls.default_values)
    if mode == "geolipi":
        base_class = "GLNode"
        other_library = "gls"
    else:
        base_class = "LayoutNode"
        other_library = "gs"
    class_code = class_template.substitute(class_name=class_name, arg_keys=arg_keys, default_values=default_values,
                                           base_class=base_class, other_library=other_library)
    return class_code


if __name__ == "__main__":
    node_to_fn_map = {}
    node_to_fn_map.update(COMBINATOR_MAP)
    node_to_fn_map.update(PRIMITIVE_MAP)
    node_to_fn_map.update(NORMAL_MAP)
    node_to_fn_map.update(MODIFIER_MAP)
    node_to_fn_map.update(INVERTED_MAP)
    node_to_fn_map.update(COLOR_MAP)
    node_to_fn_map.update(COLOR_FUNCTIONS)
    mode = "geolipi"
    converted_classes = convert_nodes(node_to_fn_map, mode)


    cur_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(cur_dir, "../splitweaver/symbolic/auto_geolipi_nodes.py")
    print("Writing to", filename)
    write_node_classes_to_file(converted_classes, filename, mode)

    # Now for layout nodes
    node_to_fn_map = {}
    node_to_fn_map.update(sym_to_fn_mapper)
    mode = "layout"
    converted_classes = convert_nodes(node_to_fn_map, mode)

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(cur_dir, "../splitweaver/symbolic/auto_layout_nodes.py")
    print("Writing to", filename)
    write_node_classes_to_file(converted_classes, filename, mode)
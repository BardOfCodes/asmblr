""" Geometry Naming and Referencing System """
""" PolyCurve Extrusions """
""" State system """
from ..expr_node import GLNode
# import mxg.symbolic as mxg

class NamedGeometry(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = mxg.NamedGeometry
    
    def setup_base(self):
        self.arg_keys = ['name']
        self.default_values = {}
    


class LinkedHeightField3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = mxg.LinkedHeightField3D
    
    def setup_base(self):
        self.arg_keys = ['plane', 'apply_height']
        self.default_values = {}

class BBoxedLinkedHeightField3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = mxg.BBoxedLinkedHeightField3D
    
    def setup_base(self):
        self.arg_keys = ['plane', 'apply_height', 'bbox_scale', 'bbox_origin']
        self.default_values = {}


class ApplyHeight(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = mxg.ApplyHeight
    
    def setup_base(self):
        self.arg_keys = ['expr', 'height']
        self.default_values = {}
        
        
class MarkerNode(GLNode):
    "Only a Marker Node"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.default_values = {}

    def inner_eval(self, sketcher, copy=False):
        expr = self.inputs.get('expr', None)
        
        self.register_output("expr", expr)
        
class SetMaterial(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = mxg.SetMaterial
    
    def setup_base(self):
        self.arg_keys = ['expr', 'material',]
        self.default_values = {}


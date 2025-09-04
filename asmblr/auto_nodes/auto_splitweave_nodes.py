# Auto-generated Node Classes
from ..base import BaseNode, InputSocket, OutputSocket
from ..expr_node import GLNode
# import splitweaver.symbolic as sws


class CartesianGrid(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.CartesianGrid
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class PolarGrid(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.PolarGrid
    
    def setup_base(self):
        self.arg_keys = ['radial_unit', 'angular_unit']
        self.default_values = {'radial_unit': 1, 'angular_unit': 1}


class CartToPolar(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.CartToPolar
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'angular_unit']
        self.default_values = {'radial_unit': 1, 'angular_unit': 1}


class PolarToCart(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.PolarToCart
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.default_values = {}


class RectRepeat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RectRepeat
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width', 'height']
        self.default_values = {}


class RectRepeatInner(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RectRepeatInner
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width', 'height', 'max_size']
        self.default_values = {}


class RectRepeatFitting(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RectRepeatFitting
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width', 'height']
        self.default_values = {}


class RectRepeatShiftedX(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RectRepeatShiftedX
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width', 'height', 'shift']
        self.default_values = {'shift': None}


class RectRepeatShiftedY(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RectRepeatShiftedY
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width', 'height', 'shift']
        self.default_values = {'shift': None}


class TriangularRepeat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.TriangularRepeat
    
    def setup_base(self):
        self.arg_keys = ['expr', 'incircle_radius', 'center']
        self.default_values = {'center': True}


class DiamondRepeat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.DiamondRepeat
    
    def setup_base(self):
        self.arg_keys = ['expr', 'side_length', 'resize_dif']
        self.default_values = {'resize_dif': True}


class HexRepeat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.HexRepeat
    
    def setup_base(self):
        self.arg_keys = ['expr', 'hex_size']
        self.default_values = {}


class HexRepeatX(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.HexRepeatX
    
    def setup_base(self):
        self.arg_keys = ['expr', 'hex_size']
        self.default_values = {}


class HexRepeatY(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.HexRepeatY
    
    def setup_base(self):
        self.arg_keys = ['expr', 'hex_size']
        self.default_values = {}


class RectRepeatEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RectRepeatEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width', 'height']
        self.default_values = {}


class RectRepeatShiftedXEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RectRepeatShiftedXEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width', 'height', 'shift']
        self.default_values = {'shift': None}


class RectRepeatShiftedYEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RectRepeatShiftedYEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width', 'height', 'shift']
        self.default_values = {'shift': None}


class DiamondRepeatEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.DiamondRepeatEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'side_length']
        self.default_values = {}


class TriangularRepeatEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.TriangularRepeatEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'incircle_radius']
        self.default_values = {}


class HexRepeatEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.HexRepeatEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'hex_size']
        self.default_values = {}


class HexRepeatXEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.HexRepeatXEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'hex_size']
        self.default_values = {}


class HexRepeatYEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.HexRepeatYEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'hex_size']
        self.default_values = {}


class AxialRepeatX(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.AxialRepeatX
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width']
        self.default_values = {}


class AxialRepeatY(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.AxialRepeatY
    
    def setup_base(self):
        self.arg_keys = ['expr', 'width']
        self.default_values = {}


class RadialRepeatAngular(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatAngular
    
    def setup_base(self):
        self.arg_keys = ['expr', 'angular_unit']
        self.default_values = {}


class RadialRepeatInitRadial(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatInitRadial
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'angular_unit', 'init_gap']
        self.default_values = {}


class RadialRepeatCentered(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatCentered
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'angular_unit']
        self.default_values = {}


class RadialRepeatFixedArc(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatFixedArc
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'arc_length', 'init_gap']
        self.default_values = {}


class RadialRepeatBricked(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatBricked
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'angular_unit', 'init_gap']
        self.default_values = {}


class RadialRepeatFixedArcBricked(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatFixedArcBricked
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'arc_length', 'init_gap']
        self.default_values = {}


class RadialRepeatEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'angular_unit', 'init_gap']
        self.default_values = {}


class RadialRepeatFixedArcEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatFixedArcEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'arc_length', 'init_gap']
        self.default_values = {}


class RadialRepeatBrickedEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatBrickedEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'angular_unit', 'init_gap']
        self.default_values = {}


class RadialRepeatFixedArcBrickedEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RadialRepeatFixedArcBrickedEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'arc_length', 'init_gap']
        self.default_values = {}


class PolarRepeatEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.PolarRepeatEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'radial_unit', 'angular_unit', 'init_gap']
        self.default_values = {}


class AngularRepeat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.AngularRepeat
    
    def setup_base(self):
        self.arg_keys = ['expr', 'angular_unit']
        self.default_values = {}


class VoronoiRepeat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.VoronoiRepeat
    
    def setup_base(self):
        self.arg_keys = ['expr', 'x_size', 'y_size', 'noise_rate', 'precomputed_centroids']
        self.default_values = {'noise_rate': 0.5, 'precomputed_centroids': None}


class VoronoiRepeatRadialDeformed(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.VoronoiRepeatRadialDeformed
    
    def setup_base(self):
        self.arg_keys = ['expr', 'x_size', 'y_size', 'noise_rate', 'precomputed_centroids']
        self.default_values = {'noise_rate': 0.5, 'precomputed_centroids': None}


class VoronoiRepeatEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.VoronoiRepeatEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'x_size', 'y_size', 'noise_rate', 'precomputed_centroids']
        self.default_values = {'noise_rate': 0.5, 'precomputed_centroids': None}


class IrregularRectRepeat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.IrregularRectRepeat
    
    def setup_base(self):
        self.arg_keys = ['expr', 'simple_grid', 'box_height', 'box_width', 'noise_rate', 'precomputed_n_vals']
        self.default_values = {'noise_rate': 0.5, 'precomputed_n_vals': None}


class IrregularRectRepeatEdge(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.IrregularRectRepeatEdge
    
    def setup_base(self):
        self.arg_keys = ['expr', 'simple_grid', 'box_height', 'box_width', 'noise_rate', 'precomputed_n_vals']
        self.default_values = {'noise_rate': 0.5, 'precomputed_n_vals': None}


class DelaunayRepeat(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.DelaunayRepeat
    
    def setup_base(self):
        self.arg_keys = ['expr', 'n_centroids_x', 'n_centroids_y', 'noise_rate', 'precomputed_centroids']
        self.default_values = {'noise_rate': 0.5, 'precomputed_centroids': None}


class CartTranslate(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.CartTranslate
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class CartScale(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.CartScale
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class CartRotate(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.CartRotate
    
    def setup_base(self):
        self.arg_keys = ['expr', 'theta']
        self.default_values = {}


class CartAffine(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.CartAffine
    
    def setup_base(self):
        self.arg_keys = ['expr', 'transform']
        self.default_values = {}


class PolarRotate(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.PolarRotate
    
    def setup_base(self):
        self.arg_keys = ['expr', 'theta']
        self.default_values = {}


class PolarScale(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.PolarScale
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class PolarTranslate(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.PolarTranslate
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class TranslateWtSignal(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.TranslateWtSignal
    
    def setup_base(self):
        self.arg_keys = ['expr', 'signal', 'apply_exp', 'invert', 'scaling_sigma']
        self.default_values = {'apply_exp': False, 'invert': False, 'scaling_sigma': 1}


class RotateWtSignal(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.RotateWtSignal
    
    def setup_base(self):
        self.arg_keys = ['expr', 'signal', 'apply_exp', 'invert', 'scaling_sigma']
        self.default_values = {'apply_exp': False, 'invert': False, 'scaling_sigma': 1}


class ScaleWtSignal(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.ScaleWtSignal
    
    def setup_base(self):
        self.arg_keys = ['expr', 'signal', 'apply_exp', 'invert', 'scaling_sigma']
        self.default_values = {'apply_exp': False, 'invert': False, 'scaling_sigma': 1}


class TranslateXWtSignal(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.TranslateXWtSignal
    
    def setup_base(self):
        self.arg_keys = ['expr', 'signal', 'apply_exp', 'invert', 'scaling_sigma']
        self.default_values = {'apply_exp': False, 'invert': False, 'scaling_sigma': 1}


class TranslateYWtSignal(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.TranslateYWtSignal
    
    def setup_base(self):
        self.arg_keys = ['expr', 'signal', 'apply_exp', 'invert', 'scaling_sigma']
        self.default_values = {'apply_exp': True, 'invert': False, 'scaling_sigma': 1}


class ScaleXWtSignal(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.ScaleXWtSignal
    
    def setup_base(self):
        self.arg_keys = ['expr', 'signal', 'apply_exp', 'invert', 'scaling_sigma']
        self.default_values = {'apply_exp': False, 'invert': False, 'scaling_sigma': 1}


class ScaleYWtSignal(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.ScaleYWtSignal
    
    def setup_base(self):
        self.arg_keys = ['expr', 'signal', 'apply_exp', 'invert', 'scaling_sigma']
        self.default_values = {'apply_exp': False, 'invert': False, 'scaling_sigma': 1}


class ValueNoise(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.ValueNoise
    
    def setup_base(self):
        self.arg_keys = ['noise_res']
        self.default_values = {}


class PerlinNoise(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.PerlinNoise
    
    def setup_base(self):
        self.arg_keys = ['noise_res']
        self.default_values = {}


class Param(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = sws.Param
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.default_values = {}


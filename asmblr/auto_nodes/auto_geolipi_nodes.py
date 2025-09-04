# Auto-generated Node Classes
from .base import BaseNode, InputSocket, OutputSocket
from .expr_node import GLNode
import geolipi.symbolic as gls
import sympy as sp
import torch as th

class Sphere3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Sphere3D
    
    def setup_base(self):
        self.arg_keys = ['radius']
        self.default_values = {}


class Box3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Box3D
    
    def setup_base(self):
        self.arg_keys = ['size']
        self.default_values = {}


class Cuboid3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Cuboid3D
    
    def setup_base(self):
        self.arg_keys = ['size']
        self.default_values = {}


class RoundedBox3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RoundedBox3D
    
    def setup_base(self):
        self.arg_keys = ['size', 'radius']
        self.default_values = {}


class BoxFrame3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.BoxFrame3D
    
    def setup_base(self):
        self.arg_keys = ['b', 'e']
        self.default_values = {}


class Torus3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Torus3D
    
    def setup_base(self):
        self.arg_keys = ['t']
        self.default_values = {}


class CappedTorus3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.CappedTorus3D
    
    def setup_base(self):
        self.arg_keys = ['angle', 'ra', 'rb']
        self.default_values = {}


class Link3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Link3D
    
    def setup_base(self):
        self.arg_keys = ['le', 'r1', 'r2']
        self.default_values = {}


class InfiniteCylinder3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.InfiniteCylinder3D
    
    def setup_base(self):
        self.arg_keys = ['c']
        self.default_values = {}


class Cone3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Cone3D
    
    def setup_base(self):
        self.arg_keys = ['angle', 'h']
        self.default_values = {}


class InexactCone3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.InexactCone3D
    
    def setup_base(self):
        self.arg_keys = ['angle', 'h']
        self.default_values = {}


class InfiniteCone3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.InfiniteCone3D
    
    def setup_base(self):
        self.arg_keys = ['angle']
        self.default_values = {}


class Plane3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Plane3D
    
    def setup_base(self):
        self.arg_keys = ['origin', 'normal']
        self.default_values = {}


class HexPrism3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.HexPrism3D
    
    def setup_base(self):
        self.arg_keys = ['h']
        self.default_values = {}


class TriPrism3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.TriPrism3D
    
    def setup_base(self):
        self.arg_keys = ['h']
        self.default_values = {}


class Capsule3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Capsule3D
    
    def setup_base(self):
        self.arg_keys = ['a', 'b', 'r']
        self.default_values = {}


class VerticalCapsule3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.VerticalCapsule3D
    
    def setup_base(self):
        self.arg_keys = ['h', 'r']
        self.default_values = {}


class CappedCylinder3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.CappedCylinder3D
    
    def setup_base(self):
        self.arg_keys = ['h', 'r']
        self.default_values = {}


class Cylinder3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Cylinder3D
    
    def setup_base(self):
        self.arg_keys = ['h', 'r']
        self.default_values = {}


class ArbitraryCappedCylinder3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ArbitraryCappedCylinder3D
    
    def setup_base(self):
        self.arg_keys = ['a', 'b', 'r']
        self.default_values = {}


class RoundedCylinder3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RoundedCylinder3D
    
    def setup_base(self):
        self.arg_keys = ['ra', 'rb', 'h']
        self.default_values = {}


class CappedCone3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.CappedCone3D
    
    def setup_base(self):
        self.arg_keys = ['r1', 'r2', 'h']
        self.default_values = {}


class ArbitraryCappedCone(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ArbitraryCappedCone
    
    def setup_base(self):
        self.arg_keys = ['a', 'b', 'ra', 'rb']
        self.default_values = {}


class SolidAngle3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SolidAngle3D
    
    def setup_base(self):
        self.arg_keys = ['angle', 'ra']
        self.default_values = {}


class CutSphere3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.CutSphere3D
    
    def setup_base(self):
        self.arg_keys = ['r', 'h']
        self.default_values = {}


class CutHollowSphere(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.CutHollowSphere
    
    def setup_base(self):
        self.arg_keys = ['r', 'h', 't']
        self.default_values = {}


class DeathStar3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.DeathStar3D
    
    def setup_base(self):
        self.arg_keys = ['ra', 'rb', 'd']
        self.default_values = {}


class RoundCone3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RoundCone3D
    
    def setup_base(self):
        self.arg_keys = ['r1', 'r2', 'h']
        self.default_values = {}


class ArbitraryRoundCone3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ArbitraryRoundCone3D
    
    def setup_base(self):
        self.arg_keys = ['a', 'b', 'r1', 'r2']
        self.default_values = {}


class InexactEllipsoid3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.InexactEllipsoid3D
    
    def setup_base(self):
        self.arg_keys = ['r']
        self.default_values = {}


class RevolvedVesica3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RevolvedVesica3D
    
    def setup_base(self):
        self.arg_keys = ['a', 'b', 'w']
        self.default_values = {}


class Rhombus3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Rhombus3D
    
    def setup_base(self):
        self.arg_keys = ['la', 'lb', 'h', 'ra']
        self.default_values = {}


class Octahedron3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Octahedron3D
    
    def setup_base(self):
        self.arg_keys = ['s']
        self.default_values = {}


class InexactOctahedron3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.InexactOctahedron3D
    
    def setup_base(self):
        self.arg_keys = ['s']
        self.default_values = {}


class Pyramid3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Pyramid3D
    
    def setup_base(self):
        self.arg_keys = ['h']
        self.default_values = {}


class Triangle3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Triangle3D
    
    def setup_base(self):
        self.arg_keys = ['a', 'b', 'c']
        self.default_values = {}


class Quadrilateral3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Quadrilateral3D
    
    def setup_base(self):
        self.arg_keys = ['a', 'b', 'c', 'd']
        self.default_values = {}


class NoParamCuboid3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.NoParamCuboid3D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class NoParamSphere3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.NoParamSphere3D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class NoParamCylinder3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.NoParamCylinder3D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class InexactSuperQuadrics3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.InexactSuperQuadrics3D
    
    def setup_base(self):
        self.arg_keys = ['skew_vec', 'epsilon_1', 'epsilon_2']
        self.default_values = {}


class InexactAnisotropicGaussian3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.InexactAnisotropicGaussian3D
    
    def setup_base(self):
        self.arg_keys = ['center', 'axial_radii', 'scale_constant']
        self.default_values = {}


class NullExpression3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.NullExpression3D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class Circle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Circle2D
    
    def setup_base(self):
        self.arg_keys = ['radius']
        self.default_values = {}


class RoundedBox2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RoundedBox2D
    
    def setup_base(self):
        self.arg_keys = ['bounds', 'radius']
        self.default_values = {}


class Box2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Box2D
    
    def setup_base(self):
        self.arg_keys = ['size']
        self.default_values = {}


class Rectangle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Rectangle2D
    
    def setup_base(self):
        self.arg_keys = ['size']
        self.default_values = {}


class OrientedBox2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.OrientedBox2D
    
    def setup_base(self):
        self.arg_keys = ['start_point', 'end_point', 'thickness']
        self.default_values = {}


class Rhombus2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Rhombus2D
    
    def setup_base(self):
        self.arg_keys = ['size']
        self.default_values = {}


class Trapezoid2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Trapezoid2D
    
    def setup_base(self):
        self.arg_keys = ['r1', 'r2', 'height']
        self.default_values = {}


class Parallelogram2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Parallelogram2D
    
    def setup_base(self):
        self.arg_keys = ['width', 'height', 'skew']
        self.default_values = {}


class EquilateralTriangle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.EquilateralTriangle2D
    
    def setup_base(self):
        self.arg_keys = ['side_length']
        self.default_values = {}


class IsoscelesTriangle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.IsoscelesTriangle2D
    
    def setup_base(self):
        self.arg_keys = ['wi_hi']
        self.default_values = {}


class Triangle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Triangle2D
    
    def setup_base(self):
        self.arg_keys = ['p0', 'p1', 'p2']
        self.default_values = {}


class UnevenCapsule2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.UnevenCapsule2D
    
    def setup_base(self):
        self.arg_keys = ['r1', 'r2', 'h']
        self.default_values = {}


class RegularPentagon2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RegularPentagon2D
    
    def setup_base(self):
        self.arg_keys = ['r']
        self.default_values = {}


class RegularHexagon2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RegularHexagon2D
    
    def setup_base(self):
        self.arg_keys = ['r']
        self.default_values = {}


class RegularOctagon2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RegularOctagon2D
    
    def setup_base(self):
        self.arg_keys = ['r']
        self.default_values = {}


class Hexagram2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Hexagram2D
    
    def setup_base(self):
        self.arg_keys = ['r']
        self.default_values = {}


class Star2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Star2D
    
    def setup_base(self):
        self.arg_keys = ['r', 'rf']
        self.default_values = {}


class RegularStar2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RegularStar2D
    
    def setup_base(self):
        self.arg_keys = ['r', 'n', 'm']
        self.default_values = {}


class Pie2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Pie2D
    
    def setup_base(self):
        self.arg_keys = ['c', 'r']
        self.default_values = {}


class CutDisk2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.CutDisk2D
    
    def setup_base(self):
        self.arg_keys = ['r', 'h']
        self.default_values = {}


class Arc2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Arc2D
    
    def setup_base(self):
        self.arg_keys = ['angle', 'ra', 'rb']
        self.default_values = {}


class HorseShoe2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.HorseShoe2D
    
    def setup_base(self):
        self.arg_keys = ['angle', 'r', 'w']
        self.default_values = {}


class Vesica2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Vesica2D
    
    def setup_base(self):
        self.arg_keys = ['r', 'd']
        self.default_values = {}


class OrientedVesica2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.OrientedVesica2D
    
    def setup_base(self):
        self.arg_keys = ['a', 'b', 'w']
        self.default_values = {}


class Moon2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Moon2D
    
    def setup_base(self):
        self.arg_keys = ['d', 'ra', 'rb']
        self.default_values = {}


class RoundedCross2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RoundedCross2D
    
    def setup_base(self):
        self.arg_keys = ['h']
        self.default_values = {}


class Egg2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Egg2D
    
    def setup_base(self):
        self.arg_keys = ['ra', 'rb']
        self.default_values = {}


class Heart2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Heart2D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class Cross2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Cross2D
    
    def setup_base(self):
        self.arg_keys = ['b', 'r']
        self.default_values = {}


class RoundedX2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RoundedX2D
    
    def setup_base(self):
        self.arg_keys = ['w', 'r']
        self.default_values = {}


class Polygon2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Polygon2D
    
    def setup_base(self):
        self.arg_keys = ['verts']
        self.default_values = {}


class Ellipse2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Ellipse2D
    
    def setup_base(self):
        self.arg_keys = ['ab']
        self.default_values = {}


class Parabola2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Parabola2D
    
    def setup_base(self):
        self.arg_keys = ['k']
        self.default_values = {}


class ParabolaSegment2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ParabolaSegment2D
    
    def setup_base(self):
        self.arg_keys = ['wi', 'he']
        self.default_values = {}


class BlobbyCross2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.BlobbyCross2D
    
    def setup_base(self):
        self.arg_keys = ['he']
        self.default_values = {}


class Tunnel2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Tunnel2D
    
    def setup_base(self):
        self.arg_keys = ['wh']
        self.default_values = {}


class Stairs2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Stairs2D
    
    def setup_base(self):
        self.arg_keys = ['wh', 'n']
        self.default_values = {}


class QuadraticCircle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.QuadraticCircle2D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class CoolS2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.CoolS2D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class CircleWave2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.CircleWave2D
    
    def setup_base(self):
        self.arg_keys = ['tb', 'ra']
        self.default_values = {}


class Hyperbola2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Hyperbola2D
    
    def setup_base(self):
        self.arg_keys = ['k', 'he']
        self.default_values = {}


class QuadraticBezierCurve2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.QuadraticBezierCurve2D
    
    def setup_base(self):
        self.arg_keys = ['A', 'B', 'C']
        self.default_values = {}


class Segment2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Segment2D
    
    def setup_base(self):
        self.arg_keys = ['start_point', 'end_point']
        self.default_values = {}


class NoParamRectangle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.NoParamRectangle2D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class NoParamCircle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.NoParamCircle2D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class NoParamTriangle2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.NoParamTriangle2D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class NullExpression2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.NullExpression2D
    
    def setup_base(self):
        self.arg_keys = []
        self.default_values = {}


class SinRepeatX2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SinRepeatX2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift']
        self.default_values = {}


class SinRepeatY2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SinRepeatY2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift']
        self.default_values = {}


class SinAlongAxisY2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SinAlongAxisY2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift', 'scale']
        self.default_values = {}


class SinDiagonal2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SinDiagonal2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift']
        self.default_values = {}


class SinDiagonalFlip2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SinDiagonalFlip2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift']
        self.default_values = {}


class SinRadial2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SinRadial2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift']
        self.default_values = {}


class SquiggleX2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SquiggleX2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift', 'shift_amount', 'freq_2', 'phase_shift_2']
        self.default_values = {}


class SquiggleY2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SquiggleY2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift', 'shift_amount', 'freq_2', 'phase_shift_2']
        self.default_values = {}


class SquiggleDiagonal2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SquiggleDiagonal2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift', 'shift_amount', 'freq_2', 'phase_shift_2']
        self.default_values = {}


class SquiggleDiagonalFlip2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SquiggleDiagonalFlip2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift', 'shift_amount', 'freq_2', 'phase_shift_2']
        self.default_values = {}


class SquiggleRadial2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SquiggleRadial2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift', 'shift_amount', 'freq_2', 'phase_shift_2']
        self.default_values = {}


class SquiggleDistortion2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SquiggleDistortion2D
    
    def setup_base(self):
        self.arg_keys = ['freq', 'phase_shift', 'shift_amount', 'freq_2', 'phase_shift_2']
        self.default_values = {}


class InstantiatedPrim2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.InstantiatedPrim2D
    
    def setup_base(self):
        self.arg_keys = ['instance', 'height', 'width', 'mode']
        self.default_values = {'height': None, 'width': None, 'mode': 'bicubic'}


class Union(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Union
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.default_values = {}

    def inner_eval(self, sketcher, copy=False):
        arguments = [self.inputs.get(key, None) for key in self.arg_keys][0]
        if isinstance(arguments, (list, tuple)):
            # IDEA - If anything is none - dont pass anything beyond it.
            ## TODO -> if not list input.
            marked_ind = len(arguments)
            for ind, arg in enumerate(arguments):
                if not isinstance(arg, (tuple, sp.Symbol, th.Tensor, gls.GLExpr, gls.GLFunction)):
                    arguments[ind] = (arg,)
                if arg is None:
                    marked_ind = ind
                    break
            arguments = arguments[:marked_ind]
            expr = self.expr_class(*arguments)
            self.register_output("expr", expr)
        else:
            super().inner_eval(sketcher, copy=copy)


class JoinUnion(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.JoinUnion
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.default_values = {}


class Intersection(Union):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Intersection
    
    def setup_base(self):
        self.arg_keys = ['expr']
        self.default_values = {}


class Complement(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Complement
    
    def setup_base(self):
        self.arg_keys = ['expr',]
        self.default_values = {}


class Difference(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Difference
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class SwitchedDifference(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SwitchedDifference
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class SmoothUnion(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SmoothUnion
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2', 'k']
        self.default_values = {}


class SmoothIntersection(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SmoothIntersection
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2', 'k']
        self.default_values = {}


class SmoothDifference(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SmoothDifference
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2', 'k']
        self.default_values = {}


class Translate2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Translate2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class EulerRotate2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.EulerRotate2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class Scale2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Scale2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class Shear2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Shear2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class Affine2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Affine2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'params']
        self.default_values = {}


class Distort2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Distort2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'positions', 'k']
        self.default_values = {}


class ReflectCoords2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ReflectCoords2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class Dilate2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Dilate2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'k']
        self.default_values = {}


class Erode2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Erode2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'k']
        self.default_values = {}


class Onion2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Onion2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'k']
        self.default_values = {}


class Translate3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Translate3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class EulerRotate3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.EulerRotate3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class Scale3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Scale3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class Shear3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Shear3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class Distort3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Distort3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'positions', 'k']
        self.default_values = {}


class Twist3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Twist3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'positions', 'k']
        self.default_values = {}


class Bend3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Bend3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'positions', 'k']
        self.default_values = {}


class ReflectCoords3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ReflectCoords3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'param']
        self.default_values = {}


class Dilate3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Dilate3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'k']
        self.default_values = {}


class Erode3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Erode3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'k']
        self.default_values = {}


class Onion3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Onion3D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'k']
        self.default_values = {}


class Revolution3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.Revolution3D
    
    def setup_base(self):
        self.arg_keys = ['o']
        self.default_values = {}


class SimpleExtrusion3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SimpleExtrusion3D
    
    def setup_base(self):
        self.arg_keys = ['h']
        self.default_values = {}


class LinearExtrude3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.LinearExtrude3D
    
    def setup_base(self):
        self.arg_keys = ['start_point', 'end_point', 'theta', 'line_plane_normal']
        self.default_values = {'line_plane_normal': None}


class QuadraticBezierExtrude3D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.QuadraticBezierExtrude3D
    
    def setup_base(self):
        self.arg_keys = ['start_point', 'control_point', 'end_point', 'theta', 'plane_normal']
        self.default_values = {'plane_normal': None}


class LinearCurve1D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.LinearCurve1D
    
    def setup_base(self):
        self.arg_keys = ['point1', 'point2']
        self.default_values = {}


class QuadraticCurve1D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.QuadraticCurve1D
    
    def setup_base(self):
        self.arg_keys = ['param_a', 'param_b', 'param_c']
        self.default_values = {}


class DestinationIn(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.DestinationIn
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class DestinationOut(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.DestinationOut
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class DestinationOver(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.DestinationOver
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class DestinationAtop(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.DestinationAtop
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class SourceIn(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SourceIn
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class SourceOut(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SourceOut
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class SourceOver(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SourceOver
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class SourceAtop(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SourceAtop
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class SVGXOR(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SVGXOR
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class ApplyColor2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ApplyColor2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'occupancy', 'color']
        self.default_values = {}


class ModifyOpacity2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ModifyOpacity2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'opacity']
        self.default_values = {}


class ModifyColor2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ModifyColor2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'new_color']
        self.default_values = {}


class ModifyColorTritone2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.ModifyColorTritone2D
    
    def setup_base(self):
        self.arg_keys = ['expr', 'mid_color', 'black', 'white', 'mid_point']
        self.default_values = {'black': None, 'white': None, 'mid_point': 0.5}


class SourceOverSequence(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.SourceOverSequence
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class AlphaMask2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.AlphaMask2D
    
    def setup_base(self):
        self.arg_keys = ['expr1', 'expr2']
        self.default_values = {}


class AlphaToSDF2D(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.AlphaToSDF2D
    
    def setup_base(self):
        self.arg_keys = ['dx', 'canvas_shape']
        self.default_values = {'canvas_shape': None}


class RGB2HSL(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RGB2HSL
    
    def setup_base(self):
        self.arg_keys = ['rgb']
        self.default_values = {}


class RGB2HSV(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.RGB2HSV
    
    def setup_base(self):
        self.arg_keys = ['rgb']
        self.default_values = {}


class HSV2RGB(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.HSV2RGB
    
    def setup_base(self):
        self.arg_keys = ['hsv']
        self.default_values = {}


class HSL2RGB(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.HSL2RGB
    
    def setup_base(self):
        self.arg_keys = ['hsl']
        self.default_values = {}


class HueShift(GLNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expr_class = gls.HueShift
    
    def setup_base(self):
        self.arg_keys = ['hsl', 'delta']
        self.default_values = {}


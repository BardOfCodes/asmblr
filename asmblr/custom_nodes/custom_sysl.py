"""
Custom SySL nodes for ASMBLR.

These nodes have special behavior that cannot be auto-generated from shader modules.
"""

import geolipi.symbolic as gls
import sysl.symbolic as sls
from ..expr_node import GLNode
from ..base import InputSocket
from ..simple_registry import register_node


# Registration decorator
def auto_register(cls):
    """Decorator to automatically register a node class."""
    register_node(cls)
    return cls


@auto_register
class GeomOnlySmoothUnion(GLNode):
    """
    Custom SySL node that behaves like gls.SmoothUnion but for geometry-only operations.
    
    This node inherits from gls.SmoothUnion but is used specifically in SySL contexts
    where we want smooth union operations on geometry without material considerations.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to gls.SmoothUnion since GeomOnlySmoothUnion inherits from it
        self.expr_class = gls.SmoothUnion
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for GeomOnlySmoothUnion."""
        self.arg_keys = ['expr_1', 'expr_2', 'smoothing']
        self.default_values = {}
        self.arg_types = {'expr_1': 'float', 'expr_2': 'float', 'smoothing': 'float'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """
        Evaluate the GeomOnlySmoothUnion node.
        
        This behaves exactly like gls.SmoothUnion but is semantically distinct
        for SySL material/geometry separation.
        """
        # Resolve inputs
        expr_1 = self.input_sockets['expr_1'].resolve(sketcher)
        expr_2 = self.input_sockets['expr_2'].resolve(sketcher)
        smoothing = self.input_sockets['smoothing'].resolve(sketcher)
        
        # Create the smooth union expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(expr_1, expr_2, smoothing)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


@auto_register
class MatSolidV1(GLNode):
    """
    SySL MatSolidV1 node: vec2 MatSolidV1(float sdf, float mat)
    
    Combines an SDF (signed distance field) with a material ID to create a material solid.
    Returns a vec2 where x=sdf, y=material.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.MatSolidV1
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for MatSolidV1."""
        self.arg_keys = ['sdf', 'mat']  # float sdf, float mat
        self.default_values = {}
        self.arg_types = {'sdf': 'float', 'mat': 'float'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the MatSolidV1 node."""
        # Resolve inputs
        sdf = self.input_sockets['sdf'].resolve(sketcher)
        mat = self.input_sockets['mat'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(sdf, mat)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


@auto_register
class MatSolidV2(GLNode):
    """
    SySL MatSolidV2 node: vec4 MatSolidV2(float sdf, vec3 mat)
    
    Combines an SDF with a 3-component material (RGB or other properties).
    Returns a vec4 where x=sdf, yzw=material components.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.MatSolidV2
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for MatSolidV2."""
        self.arg_keys = ['sdf', 'mat']  # float sdf, vec3 mat
        self.default_values = {}
        self.arg_types = {'sdf': 'float', 'mat': 'vec3'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the MatSolidV2 node."""
        # Resolve inputs
        sdf = self.input_sockets['sdf'].resolve(sketcher)
        mat = self.input_sockets['mat'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(sdf, mat)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


@auto_register
class MatSolidV3(GLNode):
    """
    SySL MatSolidV3 node: vec2 MatSolidV3(float sdf, float mat)
    
    Similar to MatSolidV1 but potentially with different material handling semantics.
    Returns a vec2 where x=sdf, y=material.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.MatSolidV3
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for MatSolidV3."""
        self.arg_keys = ['sdf', 'mat']  # float sdf, float mat
        self.default_values = {}
        self.arg_types = {'sdf': 'float', 'mat': 'float'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the MatSolidV3 node."""
        # Resolve inputs
        sdf = self.input_sockets['sdf'].resolve(sketcher)
        mat = self.input_sockets['mat'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(sdf, mat)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


# Material Nodes from materials.py

@auto_register
class SMPLMaterial(GLNode):
    """
    SySL SMPLMaterial node: Single value input material.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.SMPLMaterial
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for SMPLMaterial."""
        self.arg_keys = ['value']  # Single value input
        self.default_values = {}
        self.arg_types = {'value': 'float'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the SMPLMaterial node."""
        # Resolve inputs
        value = self.input_sockets['value'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(value)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


@auto_register
class RGBMaterial(GLNode):
    """
    SySL RGBMaterial node: Color input material.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.RGBMaterial
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for RGBMaterial."""
        self.arg_keys = ['color']  # Color input
        self.default_values = {}
        self.arg_types = {'color': 'vec3'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the RGBMaterial node."""
        # Resolve inputs
        color = self.input_sockets['color'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(color)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


@auto_register
class MaterialV3(GLNode):
    """
    SySL MaterialV3 node: Full PBR material with albedo, emission, metallic, roughness, clearcoat.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.MaterialV3
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for MaterialV3."""
        self.arg_keys = ['albedo', 'emission', 'metallic', 'roughness', 'clearcoat']
        self.default_values = {}
        self.arg_types = {'albedo': 'vec3', 'emission': 'vec3', 'metallic': 'float', 'roughness': 'float', 'clearcoat': 'float'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the MaterialV3 node."""
        # Resolve inputs
        albedo = self.input_sockets['albedo'].resolve(sketcher)
        emission = self.input_sockets['emission'].resolve(sketcher)
        metallic = self.input_sockets['metallic'].resolve(sketcher)
        roughness = self.input_sockets['roughness'].resolve(sketcher)
        clearcoat = self.input_sockets['clearcoat'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(albedo, emission, metallic, roughness, clearcoat)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


@auto_register
class NonEmissiveMaterialV3(GLNode):
    """
    SySL NonEmissiveMaterialV3 node: PBR material without emission (albedo, metallic, roughness, clearcoat).
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.NonEmissiveMaterialV3
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for NonEmissiveMaterialV3."""
        self.arg_keys = ['albedo', 'metallic', 'roughness', 'clearcoat']  # No emission
        self.default_values = {}
        self.arg_types = {'albedo': 'vec3', 'metallic': 'float', 'roughness': 'float', 'clearcoat': 'float'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the NonEmissiveMaterialV3 node."""
        # Resolve inputs
        albedo = self.input_sockets['albedo'].resolve(sketcher)
        metallic = self.input_sockets['metallic'].resolve(sketcher)
        roughness = self.input_sockets['roughness'].resolve(sketcher)
        clearcoat = self.input_sockets['clearcoat'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(albedo, metallic, roughness, clearcoat)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


@auto_register
class MatReference(GLNode):
    """
    SySL MatReference node: Material reference by name.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.MatReference
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for MatReference."""
        self.arg_keys = ['name']  # Just material name
        self.default_values = {}
        self.arg_types = {'name': 'String'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the MatReference node."""
        # Resolve inputs
        name = self.input_sockets['name'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(name)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")


@auto_register
class RegisterMaterial(GLNode):
    """
    SySL RegisterMaterial node: Register a material with name and full PBR properties.
    """
    
    def __init__(self, *args, **kwargs):
        # Set the expression class to the SySL symbolic class
        self.expr_class = sls.RegisterMaterial
        
        super().__init__(*args, **kwargs)
    
    def _create_input_sockets(self):
        """Create input sockets for RegisterMaterial."""
        self.arg_keys = ['name', 'albedo', 'emission', 'metallic', 'roughness', 'clearcoat']
        self.default_values = {}
        self.arg_types = {'name': 'String', 'albedo': 'vec3', 'emission': 'vec3', 'metallic': 'float', 'roughness': 'float', 'clearcoat': 'float'}
        return {key: InputSocket(key, parent=self, value=self.default_values.get(key, None)) 
                for key in self.arg_keys}
    
    def inner_eval(self, sketcher=None):
        """Evaluate the RegisterMaterial node."""
        # Resolve inputs
        name = self.input_sockets['name'].resolve(sketcher)
        albedo = self.input_sockets['albedo'].resolve(sketcher)
        emission = self.input_sockets['emission'].resolve(sketcher)
        metallic = self.input_sockets['metallic'].resolve(sketcher)
        roughness = self.input_sockets['roughness'].resolve(sketcher)
        clearcoat = self.input_sockets['clearcoat'].resolve(sketcher)
        
        # Create the SySL expression
        if self.expr_class and hasattr(self.expr_class, '__call__'):
            return self.expr_class(name, albedo, emission, metallic, roughness, clearcoat)
        else:
            raise NotImplementedError(f"Cannot evaluate {self.__class__.__name__}: expr_class not properly set")

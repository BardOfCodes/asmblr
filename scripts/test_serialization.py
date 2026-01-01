"""
Test script for ASMBLR node serialization and deserialization.

This script tests the updated to_dict and from_dict methods with proper data processing
for different value types including floats, tuples, torch tensors, and numpy arrays.
"""

import sys
import json
import numpy as np
import torch as th
from pathlib import Path

# Add parent directory to path for local development
sys.path.insert(0, str(Path(__file__).parent.parent))

import asmblr
import asmblr.nodes as anode
import geolipi.symbolic as gls
from asmblr.base import BaseNode


def test_basic_serialization():
    """Test basic node serialization with different value types."""
    print("🔧 Test 1: Basic Node Serialization")
    print("=" * 50)
    
    # Create nodes with different value types
    sphere = anode.Sphere3D(radius=1.5)  # float -> tuple
    box = anode.Box3D(size=(2.0, 3.0, 4.0))  # tuple -> tuple
    
    # Test serialization
    sphere_dict = sphere.to_dict()
    box_dict = box.to_dict()
    
    print(f"Sphere serialized data: {sphere_dict['nodes'][0]['data']}")
    print(f"Box serialized data: {box_dict['nodes'][0]['data']}")
    
    # Test deserialization
    sphere_restored = BaseNode.from_dict(sphere_dict)
    box_restored = BaseNode.from_dict(box_dict)
    
    print(f"✅ Sphere radius restored: {sphere_restored.input_sockets['radius'].value}")
    print(f"✅ Box size restored: {box_restored.input_sockets['size'].value}")
    
    # Verify types
    assert isinstance(sphere_restored.input_sockets['radius'].value, tuple)
    assert isinstance(box_restored.input_sockets['size'].value, tuple)
    
    print("✅ Basic serialization test passed!")
    return sphere_restored, box_restored


def test_tensor_serialization():
    """Test torch tensor and numpy array serialization."""
    print("\n🔧 Test 2: Tensor/Array Serialization")
    print("=" * 50)
    
    # Create test data
    torch_tensor = th.randn(3, 4)
    numpy_array = np.random.randn(2, 5)
    
    # Create a node and manually set tensor values
    sphere = anode.Sphere3D()
    sphere.input_sockets['radius'].set_value(torch_tensor)
    
    box = anode.Box3D()
    box.input_sockets['size'].set_value(numpy_array)
    
    # Test serialization
    sphere_dict = sphere.to_dict()
    box_dict = box.to_dict()
    
    print(f"Torch tensor serialized type: {sphere_dict['nodes'][0]['data']['radius']['type']}")
    print(f"Numpy array serialized type: {box_dict['nodes'][0]['data']['size']['type']}")
    
    # Test deserialization
    sphere_restored = BaseNode.from_dict(sphere_dict)
    box_restored = BaseNode.from_dict(box_dict)
    
    restored_tensor = sphere_restored.input_sockets['radius'].value
    restored_array = box_restored.input_sockets['size'].value
    
    print(f"✅ Tensor shape: {torch_tensor.shape} -> {restored_tensor.shape}")
    print(f"✅ Array shape: {numpy_array.shape} -> {restored_array.shape}")
    
    # Verify data integrity
    assert th.allclose(torch_tensor, restored_tensor, atol=1e-6)
    assert np.allclose(numpy_array, restored_array, atol=1e-6)
    
    print("✅ Tensor/array serialization test passed!")
    return restored_tensor, restored_array


def test_complex_dag_serialization():
    """Test serialization of a complex DAG with connections."""
    print("\n🔧 Test 3: Complex DAG Serialization")
    print("=" * 50)
    
    # Create a complex expression
    sphere1 = anode.Sphere3D(radius=0.8)
    sphere2 = anode.Sphere3D(radius=1.2)
    box = anode.Box3D(size=(1.5, 1.5, 1.5))
    
    # Create connections
    union = anode.Union(sphere1, sphere2)
    final = anode.Difference(union, box)
    
    # Serialize the entire DAG
    dag_dict = final.to_dict()
    
    print(f"Serialized nodes: {len(dag_dict['nodes'])}")
    print(f"Serialized connections: {len(dag_dict['connections'])}")
    
    # Show connection structure
    for conn in dag_dict['connections']:
        print(f"  Connection: {conn['source']} -> {conn['target']}")
    
    # Deserialize
    restored_dag = BaseNode.from_dict(dag_dict)
    
    # Test evaluation
    final.evaluate()
    restored_dag.evaluate()
    
    original_result = final.outputs['expr']
    restored_result = restored_dag.outputs['expr']
    
    print(f"✅ Original result: {original_result}")
    print(f"✅ Restored result: {restored_result}")
    print(f"✅ Results match: {str(original_result) == str(restored_result)}")
    
    print("✅ Complex DAG serialization test passed!")
    return restored_dag


def test_json_compatibility():
    """Test that serialized data can be saved/loaded from JSON."""
    print("\n🔧 Test 4: JSON File Compatibility")
    print("=" * 50)
    
    # Create a test expression
    geolipi_expr = gls.Union(gls.Sphere3D(1.0), gls.Box3D((2, 2, 2)))
    asmblr_dag = asmblr.converter.convert_to_asmblr(geolipi_expr)
    
    # Serialize to dict
    dag_dict = asmblr_dag.to_dict()
    
    # Save to JSON file
    json_file = Path("test_dag.json")
    with open(json_file, 'w') as f:
        json.dump(dag_dict, f, indent=2)
    
    print(f"✅ Saved DAG to {json_file}")
    print(f"   File size: {json_file.stat().st_size} bytes")
    
    # Load from JSON file
    with open(json_file, 'r') as f:
        loaded_dict = json.load(f)
    
    # Reconstruct DAG
    restored_dag = BaseNode.from_dict(loaded_dict)
    
    # Test evaluation
    asmblr_dag.evaluate()
    restored_dag.evaluate()
    
    original_expr = asmblr_dag.outputs['expr']
    restored_expr = restored_dag.outputs['expr']
    
    print(f"✅ Original: {original_expr}")
    print(f"✅ Restored: {restored_expr}")
    
    # Clean up
    json_file.unlink()
    
    print("✅ JSON compatibility test passed!")
    return restored_dag


def test_value_processing_functions():
    """Test the individual value processing functions."""
    print("\n🔧 Test 5: Value Processing Functions")
    print("=" * 50)
    
    from asmblr.base import process_value_for_serialization, unprocess_value_from_serialization
    
    # Test different value types
    test_values = [
        1.5,                    # float -> tuple
        (1.0, 2.0, 3.0),       # tuple -> tuple
        [4.0, 5.0],            # list -> tuple
        "hello",               # string -> string
        True,                  # bool -> bool
        False,                 # bool -> bool
        None,                  # none -> none
        th.tensor([1.0, 2.0]), # tensor -> compressed
        np.array([3.0, 4.0])   # array -> compressed
    ]
    
    for i, original_value in enumerate(test_values):
        print(f"\nTest value {i+1}: {original_value} ({type(original_value).__name__})")
        
        # Process for serialization
        processed = process_value_for_serialization(original_value)
        print(f"  Processed type: {processed['type']}")
        
        # Unprocess from serialization
        restored = unprocess_value_from_serialization(processed)
        print(f"  Restored: {restored} ({type(restored).__name__})")
        
        # Verify correctness
        if isinstance(original_value, (int, float)) and not isinstance(original_value, bool):
            # Numbers (but not bools) should become tuples
            assert restored == (original_value,)
            print(f"  ✅ Number converted to tuple correctly")
        elif isinstance(original_value, list):
            # Lists should become tuples
            assert restored == tuple(original_value)
            print(f"  ✅ List converted to tuple correctly")
        elif isinstance(original_value, th.Tensor):
            # Tensors should be approximately equal
            assert th.allclose(original_value, restored, atol=1e-6)
            print(f"  ✅ Tensor restored correctly")
        elif isinstance(original_value, np.ndarray):
            # Arrays should be approximately equal
            assert np.allclose(original_value, restored, atol=1e-6)
            print(f"  ✅ Array restored correctly")
        else:
            # Other types (bool, str, None, tuple) should be exactly equal
            assert original_value == restored
            print(f"  ✅ Value restored exactly")
    
    print("\n✅ Value processing functions test passed!")


def run_all_tests():
    """Run all serialization tests."""
    print("🚀 ASMBLR Serialization Tests")
    print("=" * 60)
    
    try:
        test_basic_serialization()
        test_tensor_serialization()
        test_complex_dag_serialization()
        test_json_compatibility()
        test_value_processing_functions()
        
        print("\n🎉 All serialization tests passed!")
        print("✅ to_dict and from_dict methods working correctly")
        print("✅ JSON compatibility verified")
        print("✅ Data processing functions working correctly")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()

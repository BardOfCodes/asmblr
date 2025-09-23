"""
ASMBLR Examples: GeoLIPI Expression to Node DAG Conversion

This file demonstrates how to:
1. Create ASMBLR nodes directly
2. Convert GeoLIPI expressions to ASMBLR DAGs
3. Evaluate DAGs to recover expressions
4. Inspect nodes and their properties
"""

import asmblr.nodes as anode
import asmblr
import geolipi.symbolic as gls


def example_1_direct_instantiation():
    """Example 1: Direct node instantiation with type hints."""
    print("🔧 Example 1: Direct Node Instantiation")
    print("=" * 50)
    
    # Create nodes directly
    sphere = anode.Sphere3D(radius=1.5)
    box = anode.Box3D(size=(2, 2, 2))
    union = anode.Union(sphere, box)  # Multi-input variadic node
    
    # Inspect the nodes
    print("\n📋 Node Inspection:")
    asmblr.inspect_node(sphere)
    print()
    asmblr.inspect_node(box) 
    print()
    asmblr.inspect_node(union)
    
    # Evaluate to get the expression
    union.evaluate()
    result_expr = union.outputs['expr']
    print(f"\n✅ Result expression: {result_expr}")
    print(f"   Type: {type(result_expr)}")
    
    return union


def example_2_geolipi_conversion():
    """Example 2: Convert GeoLIPI expression to ASMBLR DAG."""
    print("\n🔄 Example 2: GeoLIPI to ASMBLR Conversion")
    print("=" * 50)
    
    # Create a GeoLIPI expression
    geolipi_expr = gls.Union(gls.Sphere3D(1.0), gls.Box3D((1, 1, 1)))
    print(f"Original GeoLIPI: {geolipi_expr}")
    
    # Convert to ASMBLR DAG
    asmblr_dag = asmblr.converter.convert_to_asmblr(geolipi_expr)
    print(f"ASMBLR DAG type: {type(asmblr_dag)}")
    
    # Evaluate the DAG
    asmblr_dag.evaluate()
    recovered_expr = asmblr_dag.outputs['expr']
    
    print(f"✅ Recovered expression: {recovered_expr}")
    print(f"   Original == Recovered: {str(geolipi_expr) == str(recovered_expr)}")
    
    return asmblr_dag


def example_3_complex_expression():
    """Example 3: Complex expression with multiple operations."""
    print("\n🏗️ Example 3: Complex Multi-Operation Expression")
    print("=" * 50)
    
    # Create a complex GeoLIPI expression
    sphere1 = gls.Sphere3D(0.8)
    sphere2 = gls.Sphere3D(0.6)
    box = gls.Box3D((0.5, 0.5, 0.5))
    
    # Translate and combine
    translated_sphere = gls.Translate3D(sphere2, (1.0, 0.0, 0.0))
    union_spheres = gls.Union(sphere1, translated_sphere)
    final_expr = gls.Difference(union_spheres, box)
    
    print(f"Complex GeoLIPI: {final_expr}")
    
    # Convert and evaluate
    asmblr_dag = asmblr.converter.convert_to_asmblr(final_expr)
    asmblr_dag.evaluate()
    recovered = asmblr_dag.outputs['expr']
    
    print(f"✅ Recovered: {recovered}")
    
    # Inspect the root node
    print(f"\n📋 Root Node Inspection:")
    asmblr.inspect_node(asmblr_dag)
    
    return asmblr_dag


def example_4_material_nodes():
    """Example 4: SySL material nodes with type hints."""
    print("\n🎨 Example 4: SySL Material Nodes")
    print("=" * 50)
    
    # Create material nodes (inspect only, don't evaluate due to SySL complexity)
    material = anode.MaterialV3(
        albedo=(0.8, 0.2, 0.1),      # vec3
        emission=(0.0, 0.0, 0.0),    # vec3  
        metallic=0.0,                # float
        roughness=0.5,               # float
        clearcoat=0.0                # float
    )
    
    # Create simpler material nodes
    simple_material = anode.SMPLMaterial(value=0.5)
    rgb_material = anode.RGBMaterial(color=(1.0, 0.0, 0.0))
    
    print("📋 Full PBR Material:")
    asmblr.inspect_node(material)
    print("\n📋 Simple Material:")
    asmblr.inspect_node(simple_material)
    print("\n📋 RGB Material:")
    asmblr.inspect_node(rgb_material)
    
    # Show material solid node structure
    mat_solid = anode.MatSolidV1()  # Don't connect inputs for inspection
    print("\n📋 Material Solid V1 Node:")
    asmblr.inspect_node(mat_solid)
    
    print("\n✅ Material nodes demonstrate rich type system:")
    print("   - String types for names")
    print("   - vec3 types for colors/vectors") 
    print("   - float types for scalar values")
    
    return material


def example_5_vector_splitting():
    """Example 5: Vector splitting with multiple outputs."""
    print("\n✂️ Example 5: Vector Splitting")
    print("=" * 50)
    
    # Create vector splitters
    vec3_splitter = anode.SplitVec3D(expr=(1.0, 2.0, 3.0))
    vec4_splitter = anode.SplitVec4D(expr=(1.0, 2.0, 3.0, 4.0))
    
    print("📋 Vec3 Splitter:")
    asmblr.inspect_node(vec3_splitter)
    print("\n📋 Vec4 Splitter:")
    asmblr.inspect_node(vec4_splitter)
    
    # Evaluate to get individual components
    vec3_splitter.evaluate()
    print(f"\n✅ Vec3 components:")
    for key in vec3_splitter.output_sockets.keys():
        print(f"   {key}: {vec3_splitter.outputs.get(key, 'None')}")
    
    vec4_splitter.evaluate()
    print(f"\n✅ Vec4 components:")
    for key in vec4_splitter.output_sockets.keys():
        print(f"   {key}: {vec4_splitter.outputs.get(key, 'None')}")
    
    return vec3_splitter, vec4_splitter


def example_6_node_search_and_discovery():
    """Example 6: Node discovery and search capabilities."""
    print("\n🔍 Example 6: Node Discovery")
    print("=" * 50)
    
    # Search for specific node types
    sphere_nodes = asmblr.search_nodes("sphere")
    print(f"Sphere nodes: {sphere_nodes}")
    
    material_nodes = asmblr.search_nodes("material")
    print(f"Material nodes: {material_nodes}")
    
    # Get all available nodes
    all_nodes = asmblr.list_nodes()
    print(f"\nTotal available nodes: {len(all_nodes)}")
    print(f"First 10 nodes: {all_nodes[:10]}")
    
    # Inspect a few different types
    print(f"\n📋 Sample Node Types:")
    sample_types = ['Translate3D', 'SmoothUnion', 'RoundedBox2D']
    for node_name in sample_types:
        if hasattr(anode, node_name):
            print(f"\n{node_name}:")
            asmblr.inspect_node(getattr(anode, node_name))


def example_7_variadic_union():
    """Example 7: Variadic Union node with multiple inputs."""
    print("\n🔗 Example 7: Variadic Union (Multiple Inputs)")
    print("=" * 50)
    
    # Create multiple primitives
    sphere1 = anode.Sphere3D(radius=0.8)
    sphere2 = anode.Sphere3D(radius=0.6)
    box = anode.Box3D(size=(0.5, 0.5, 0.5))
    
    # Create union with 3 inputs (variadic)
    union = anode.Union(sphere1, sphere2, box)
    
    print("📋 Variadic Union Node:")
    asmblr.inspect_node(union)
    
    # Evaluate
    union.evaluate()
    result = union.outputs['expr']
    print(f"\n✅ Union result: {result}")
    
    return union


def run_all_examples():
    """Run all examples in sequence."""
    print("🚀 ASMBLR Examples - Complete Demonstration")
    print("=" * 60)
    
    # Run all examples
    examples = [
        example_1_direct_instantiation,
        example_2_geolipi_conversion,
        example_3_complex_expression,
        example_4_material_nodes,
        example_5_vector_splitting,
        example_6_node_search_and_discovery,
        example_7_variadic_union
    ]
    
    results = []
    for example_func in examples:
        try:
            result = example_func()
            results.append(result)
            print("\n" + "─" * 60)
        except Exception as e:
            print(f"❌ Error in {example_func.__name__}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🎉 Completed {len(examples)} examples!")
    return results


if __name__ == "__main__":
    run_all_examples()

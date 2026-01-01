# ASMBLR

DAG-based Representation for Symbolic Geometry (GeoLIPI, SySL, Migumi, and others).

ASMBLR provides a node-based programming interface for symbolic expressions. It allows you to build, manipulate, and evaluate directed acyclic graphs (DAGs) that represent geometric and material expressions.

**[Quick Start](#quick-start)** | **[Generating Node Files](#generating-node-files)** | **[API Reference](#api-reference)**

## Features

- **Node-based DAG construction** - Build complex expressions by connecting nodes
- **Auto-generated nodes** - Automatically generates node wrappers for GeoLIPI, SySL, and Migumi symbols
- **Bidirectional conversion** - Convert between GeoLIPI expressions and ASMBLR DAGs
- **Serialization** - Save/load DAGs to/from JSON format
- **Frontend export** - Generate `nodes.json` for visual node editors

## Installation

### From source

```bash
cd asmblr
pip install -e .
```

### Dependencies

Required:
- `geolipi` - Symbolic geometry library
- `sysl` - Symbolic shading language

Optional:
- `migumi` - Extended geometry primitives (nodes generated only if available)

## Quick Start

### 1. Direct Node Instantiation

```python
import asmblr.nodes as anode
import asmblr

# Create nodes directly
sphere = anode.Sphere3D(radius=1.5)
box = anode.Box3D(size=(2, 2, 2))
union = anode.Union(sphere, box)

# Evaluate to get the expression
union.evaluate()
result_expr = union.outputs['expr']
print(result_expr)  # Union(Sphere3D(1.5), Box3D((2, 2, 2)))
```

### 2. Convert GeoLIPI Expressions to ASMBLR DAGs

```python
import asmblr
import geolipi.symbolic as gls

# Create a GeoLIPI expression
geolipi_expr = gls.Union(gls.Sphere3D(1.0), gls.Box3D((1, 1, 1)))

# Convert to ASMBLR DAG
asmblr_dag = asmblr.converter.convert_to_asmblr(geolipi_expr)

# Evaluate the DAG to recover the expression
asmblr_dag.evaluate()
recovered_expr = asmblr_dag.outputs['expr']
```

### 3. Building Complex DAGs with Connections

```python
import asmblr.nodes as anode

# Create primitives
sphere1 = anode.Sphere3D(radius=0.8)
sphere2 = anode.Sphere3D(radius=0.6)
box = anode.Box3D(size=(0.5, 0.5, 0.5))

# Build the DAG
translated = anode.Translate3D(sphere2, translation=(1.0, 0.0, 0.0))
union = anode.Union(sphere1, translated)
final = anode.Difference(union, box)

# Evaluate
final.evaluate()
print(final.outputs['expr'])
```

### 4. Serialization

```python
import json
from asmblr.base import BaseNode

# Serialize to dictionary
dag_dict = final.to_dict()

# Save to JSON file
with open("my_dag.json", "w") as f:
    json.dump(dag_dict, f, indent=2)

# Load from JSON file
with open("my_dag.json", "r") as f:
    loaded_dict = json.load(f)

# Reconstruct the DAG
restored_dag = BaseNode.from_dict(loaded_dict)
```

## Node Discovery

```python
import asmblr

# List all available nodes
all_nodes = asmblr.list_nodes()
print(f"Total nodes: {len(all_nodes)}")

# Search for specific nodes
sphere_nodes = asmblr.search_nodes("sphere")
material_nodes = asmblr.search_nodes("material")

# Inspect a node's inputs and outputs
asmblr.inspect_node(anode.Sphere3D)
# Output:
# Sphere3D
#   Inputs: [radius:float]
#   Outputs: ['expr']
#   Expression: Sphere3D
```

## Generating Node Files

ASMBLR can auto-generate Python node files from symbolic libraries. Use this whenever the underlying libraries get updated to generate nodes corresponding to updated symbols.

```bash
# Generate all node files (GeoLIPI, SySL, Migumi if available)
python generate_nodes.py

# Force regenerate (overwrite existing)
python generate_nodes.py --force

# Generate specific libraries only
python generate_nodes.py --geolipi
python generate_nodes.py --sysl
python generate_nodes.py --migumi
```

Generated files are saved to `asmblr/auto_nodes/`.

## Frontend JSON Export

Generate a `nodes.json` file for visual node editors:

```bash
python scripts/asmblr_frontend_json.py --out nodes.json
```

This creates a JSON file with node definitions including:
- Input/output socket definitions
- Control configurations (for non-expression parameters)
- Category metadata

## Project Structure

```
asmblr/
├── asmblr/
│   ├── __init__.py          # Main exports
│   ├── base.py              # BaseNode, Connection, Socket classes
│   ├── expr_node.py         # GLNode base for expression nodes
│   ├── nodes.py             # Dynamic node access (anode.NodeName)
│   ├── converter.py         # GeoLIPI ↔ ASMBLR conversion
│   ├── serialize.py         # Serialization utilities
│   ├── simple_registry.py   # Node registry
│   ├── auto_loader.py       # Auto-generation of node files
│   ├── auto_nodes/          # Auto-generated node classes
│   │   ├── geolipi_nodes.py
│   │   ├── sysl_nodes.py
│   │   └── migumi_nodes.py
│   └── custom_nodes/        # Manually defined custom nodes
│       ├── custom_geolipi.py
│       └── custom_mxg.py
├── scripts/
│   ├── asmblr_frontend_json.py  # Frontend JSON generator
│   ├── examples.py              # Usage examples
│   └── test_serialization.py    # Serialization tests
├── generate_nodes.py        # Node generation CLI
└── README.md
```

## Environment Variables

- `ASMBLR_DISABLE_AUTO_LOAD=1` - Disable automatic node loading on import

## API Reference

### Core Classes

- **`BaseNode`** - Abstract base class for all DAG nodes
- **`GLNode`** - Base class for expression-wrapping nodes  
- **`Connection`** - Represents a connection between node sockets
- **`InputSocket`** / **`OutputSocket`** - Node socket classes

### Key Functions

- **`asmblr.list_nodes()`** - List all registered node names
- **`asmblr.search_nodes(pattern)`** - Search nodes by regex pattern
- **`asmblr.inspect_node(node)`** - Print node information
- **`asmblr.converter.convert_to_asmblr(expr)`** - Convert GeoLIPI expression to DAG

### Node Registry

```python
from asmblr import NODE_REGISTRY

# Access registered nodes
node_class = NODE_REGISTRY['Sphere3D']

# Register custom nodes
from asmblr import register_node

@register_node
class MyCustomNode(GLNode):
    ...
```

## License

Research code - see repository license.

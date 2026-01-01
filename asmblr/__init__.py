# Asmblr - DAG-based Symbolic Expression Library

# Core components
from .base import BaseNode, Connection, InputSocket, OutputSocket
from .expr_node import GLNode

# Simple registry system (like geolipi)
from .simple_registry import (
    NODE_REGISTRY, register_node
)

# Settings
from .settings import Settings, update_settings

# Auto-loader (imports and registers nodes automatically)
from .auto_loader import load_all_geolipi_nodes, load_all_sysl_nodes, load_all_symbolic_nodes

# Node inspection utilities
from .inspect_nodes import inspect_node, list_nodes, search_nodes

# Converter utilities
from . import converter

# Custom nodes (manual registration)
from .custom_nodes.custom_mxg import PolyLine2D, PolyArc2D
from .custom_nodes.custom_geolipi import SplitVec2D, SplitVec3D, SplitVec4D

# Custom nodes are auto-registered via decorators when imported


__version__ = "0.2.0"
__all__ = [
    # Core
    "BaseNode", "GLNode", "Connection", "InputSocket", "OutputSocket",
    # Simple Registry
    "NODE_REGISTRY", "register_node",
    # Auto-loader
    "load_all_geolipi_nodes", "load_all_sysl_nodes", "load_all_symbolic_nodes",
    # Node inspection
    "inspect_node", "list_nodes", "search_nodes",
    # Converter
    "converter",
    # Custom nodes
    "PolyLine2D", "PolyArc2D", "SplitVec2D", "SplitVec3D", "SplitVec4D",
    # Settings
    "Settings", "update_settings",
]

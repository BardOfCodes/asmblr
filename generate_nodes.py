#!/usr/bin/env python3
"""
Generate static GeoLIPI nodes file for ASMBLR.

This script generates a static Python file containing all GeoLIPI nodes,
which improves import performance and makes the codebase more transparent.

Usage:
    python generate_nodes.py

The generated file will be saved to asmblr/auto_nodes/geolipi_nodes.py
"""

import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """Generate the GeoLIPI nodes file."""
    try:
        from asmblr.auto_loader import generate_geolipi_nodes_file
        
        print("🔧 Generating GeoLIPI nodes file...")
        output_file = generate_geolipi_nodes_file()
        
        print(f"✅ Successfully generated: {output_file}")
        print("\n📋 Next steps:")
        print("  1. The generated file contains all GeoLIPI nodes as static Python classes")
        print("  2. ASMBLR will now load faster on subsequent imports")
        print("  3. You can inspect the generated nodes in asmblr/auto_nodes/geolipi_nodes.py")
        print("\n💡 To regenerate (e.g., after GeoLIPI updates), run this script again.")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Make sure you have GeoLIPI installed and accessible:")
        print("   pip install geolipi")
        print("   # or ensure GeoLIPI is in your PYTHONPATH")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()


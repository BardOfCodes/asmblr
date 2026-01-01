#!/usr/bin/env python3
"""
Generate static node files for ASMBLR.

This script generates static Python files containing all symbolic nodes from
available libraries (GeoLIPI, SySL, and optionally Migumi).

Required libraries:
    - geolipi
    - sysl

Optional libraries:
    - migumi (generated only if available)

Usage:
    python generate_nodes.py              # Generate missing node files
    python generate_nodes.py --force      # Force regenerate all files
    python generate_nodes.py --geolipi    # Generate only GeoLIPI nodes
    python generate_nodes.py --sysl       # Generate only SySL nodes
    python generate_nodes.py --migumi     # Generate only Migumi nodes (if available)

The generated files will be saved to asmblr/auto_nodes/
"""

import sys
import argparse
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Path to auto_nodes directory
AUTO_NODES_DIR = current_dir / "asmblr" / "auto_nodes"


def file_exists(name: str) -> bool:
    """Check if a node file already exists."""
    return (AUTO_NODES_DIR / f"{name}_nodes.py").exists()


def main():
    """Generate the node files for all available libraries."""
    parser = argparse.ArgumentParser(
        description="Generate static node files for ASMBLR"
    )
    parser.add_argument(
        "--geolipi", action="store_true", 
        help="Generate only GeoLIPI nodes"
    )
    parser.add_argument(
        "--sysl", action="store_true", 
        help="Generate only SySL nodes"
    )
    parser.add_argument(
        "--migumi", action="store_true", 
        help="Generate only Migumi nodes (if available)"
    )
    parser.add_argument(
        "-f", "--force", action="store_true",
        help="Force regeneration even if files already exist"
    )
    args = parser.parse_args()
    
    # If no specific library is selected, generate all
    generate_all = not (args.geolipi or args.sysl or args.migumi)
    force = args.force
    
    try:
        from asmblr.auto_loader import (
            generate_geolipi_nodes_file,
            generate_sysl_nodes_file,
            generate_migumi_nodes_file,
            MIGUMI_AVAILABLE,
        )
        
        results = {}
        skipped = {}
        
        if force:
            print("🔄 Force mode: existing files will be overwritten\n")
        
        # Determine which libraries to generate
        libraries_to_generate = []
        if generate_all:
            libraries_to_generate = ['geolipi', 'sysl']
            if MIGUMI_AVAILABLE:
                libraries_to_generate.append('migumi')
        else:
            if args.geolipi:
                libraries_to_generate.append('geolipi')
            if args.sysl:
                libraries_to_generate.append('sysl')
            if args.migumi:
                libraries_to_generate.append('migumi')
        
        print("🔧 Generating node files...")
        
        # Generate GeoLIPI
        if 'geolipi' in libraries_to_generate:
            if force or not file_exists('geolipi'):
                results['geolipi'] = generate_geolipi_nodes_file()
            else:
                skipped['geolipi'] = str(AUTO_NODES_DIR / "geolipi_nodes.py")
        
        # Generate SySL
        if 'sysl' in libraries_to_generate:
            if force or not file_exists('sysl'):
                results['sysl'] = generate_sysl_nodes_file()
            else:
                skipped['sysl'] = str(AUTO_NODES_DIR / "sysl_nodes.py")
        
        # Generate Migumi (if available)
        if 'migumi' in libraries_to_generate:
            if not MIGUMI_AVAILABLE:
                print("⚠️  Migumi is not available, skipping...")
                results['migumi'] = None
            elif force or not file_exists('migumi'):
                results['migumi'] = generate_migumi_nodes_file()
            else:
                skipped['migumi'] = str(AUTO_NODES_DIR / "migumi_nodes.py")
        
        # Print summary
        print("\n" + "=" * 50)
        print("📋 Generation Summary:")
        print("=" * 50)
        
        for library, output_file in results.items():
            if output_file:
                print(f"  ✅ {library}: {output_file}")
            else:
                print(f"  ⏭️  {library}: skipped (not available)")
        
        for library, output_file in skipped.items():
            print(f"  📁 {library}: already exists ({output_file})")
        
        if skipped:
            print("\n💡 Use --force to regenerate existing files")
        
        print("\n📝 Next steps:")
        print("  1. The generated files contain all symbolic nodes as static Python classes")
        print("  2. ASMBLR will now load faster on subsequent imports")
        print("  3. You can inspect the generated nodes in asmblr/auto_nodes/")
        print("\n🔄 To regenerate (e.g., after library updates), run: python generate_nodes.py --force")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n💡 Make sure you have the required libraries installed:")
        print("   pip install geolipi sysl")
        print("   # Optionally: pip install migumi")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

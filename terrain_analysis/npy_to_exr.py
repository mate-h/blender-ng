#!/usr/bin/env python3
"""
Convert BeamNG terrain .npy files to EXR textures for Blender

This script takes the .npy output from ter_parser.py and converts them
to EXR format that can be directly loaded as image textures in Blender.
"""

import numpy as np
import OpenEXR
import Imath
import json
from pathlib import Path
import argparse

def numpy_to_exr_heightmap(heightmap_array, output_path):
    """Convert heightmap numpy array to EXR displacement texture"""
    
    print("🏔️  Converting heightmap to EXR...")
    print(f"   Input shape: {heightmap_array.shape}")
    print(f"   Value range: {heightmap_array.min()} - {heightmap_array.max()}")
    
    heightmap_normalized = heightmap_array.astype(np.float32) / 65535.0
    
    height, width = heightmap_normalized.shape
    
    # Create RGBA channels (R=G=B=height, A=1)
    r_channel = heightmap_normalized.flatten()
    g_channel = heightmap_normalized.flatten() 
    b_channel = heightmap_normalized.flatten()
    a_channel = np.ones(height * width, dtype=np.float32)
    
    # Convert to bytes for OpenEXR
    r_bytes = r_channel.astype(np.float32).tobytes()
    g_bytes = g_channel.astype(np.float32).tobytes()
    b_bytes = b_channel.astype(np.float32).tobytes()
    a_bytes = a_channel.astype(np.float32).tobytes()
    
    # Create EXR header
    header = OpenEXR.Header(width, height)
    header['channels'] = {
        'R': Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT)),
        'G': Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT)),
        'B': Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT)),
        'A': Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT))
    }
    
    # Write EXR file
    exr_file = OpenEXR.OutputFile(str(output_path), header)
    exr_file.writePixels({
        'R': r_bytes,
        'G': g_bytes, 
        'B': b_bytes,
        'A': a_bytes
    })
    exr_file.close()
    
    print(f"✅ Heightmap EXR saved: {output_path}")
    print(f"   Size: {width}x{height}")
    print(f"   Value range: {heightmap_normalized.min():.1f} - {heightmap_normalized.max():.1f}")

def numpy_to_exr_layermap(layermap_array, materials_list, output_path):
    """Convert layermap numpy array to EXR material texture"""
    
    print("🎨 Converting layermap to EXR...")
    print(f"   Input shape: {layermap_array.shape}")
    print(f"   Value range: {layermap_array.min()} - {layermap_array.max()}")
    print(f"   Unique materials: {len(np.unique(layermap_array))}")
    
    # Keep raw material ID values without normalization
    layermap_normalized = layermap_array.astype(np.float32)
    if layermap_array.max() == 0:
        print("⚠️  WARNING: Layermap is all zeros")
    
    height, width = layermap_normalized.shape
    
    # For material data, we can use different strategies:
    # Option 1: R=material_id, G=B=0, A=1 (material index in red channel)
    # Option 2: R=G=B=material_id, A=1 (grayscale representation)
    # We'll use Option 2 for better visibility
    
    r_channel = layermap_normalized.flatten()
    g_channel = layermap_normalized.flatten()
    b_channel = layermap_normalized.flatten()
    a_channel = np.ones(height * width, dtype=np.float32)
    
    # Convert to bytes for OpenEXR
    r_bytes = r_channel.astype(np.float32).tobytes()
    g_bytes = g_channel.astype(np.float32).tobytes()
    b_bytes = b_channel.astype(np.float32).tobytes()
    a_bytes = a_channel.astype(np.float32).tobytes()
    
    # Create EXR header
    header = OpenEXR.Header(width, height)
    header['channels'] = {
        'R': Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT)),
        'G': Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT)),
        'B': Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT)),
        'A': Imath.Channel(Imath.PixelType(Imath.PixelType.FLOAT))
    }
    
    # Write EXR file
    exr_file = OpenEXR.OutputFile(str(output_path), header)
    exr_file.writePixels({
        'R': r_bytes,
        'G': g_bytes,
        'B': b_bytes,
        'A': a_bytes
    })
    exr_file.close()
    
    print(f"✅ Layermap EXR saved: {output_path}")
    print(f"   Size: {width}x{height}")
    
    # Print material mapping
    unique_values = np.unique(layermap_array)
    print("   Material mapping:")
    for i, mat_id in enumerate(unique_values):  # Show first 10
        if mat_id < len(materials_list):
            material_name = materials_list[mat_id]
            print(f"     ID {mat_id} → {material_name}")

def convert_npy_to_exr(input_dir="blender_export", output_dir="exr_textures"):
    """Convert all .npy files to EXR textures"""
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory
    output_path.mkdir(exist_ok=True)
    
    print("🔄 Converting BeamNG terrain data to EXR textures...")
    print(f"📁 Input: {input_path}")
    print(f"📁 Output: {output_path}")
    
    # Load metadata
    metadata_file = input_path / "terrain_metadata.json"
    if not metadata_file.exists():
        print(f"❌ Metadata file not found: {metadata_file}")
        return
    
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    materials = metadata['materials']['list']
    terrain_info = metadata['terrain_info']
    
    print(f"🏞️  Terrain: {Path(terrain_info['source_file']).name}")
    print(f"📊 Dimensions: {terrain_info['dimensions']}")
    print(f"🎭 Materials: {len(materials)}")
    
    # Convert heightmap
    heightmap_file = input_path / "heightmap.npy"
    if heightmap_file.exists():
        heightmap = np.load(heightmap_file)
        heightmap_exr = output_path / "BeamNG_Terrain_Displacement.exr"
        numpy_to_exr_heightmap(heightmap, heightmap_exr)
    else:
        print(f"⚠️  Heightmap file not found: {heightmap_file}")
    
    # Convert layermap
    layermap_file = input_path / "layermap.npy"
    if layermap_file.exists():
        layermap = np.load(layermap_file)
        layermap_exr = output_path / "BeamNG_Terrain_Layermap.exr"
        numpy_to_exr_layermap(layermap, materials, layermap_exr)
    else:
        print(f"⚠️  Layermap file not found: {layermap_file}")
    
    # Copy metadata to output directory
    output_metadata = output_path / "terrain_info.json"
    with open(output_metadata, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n✅ Conversion complete!")
    print(f"📁 EXR textures ready for Blender in: {output_path}")
    print("📋 Files created:")
    for exr_file in output_path.glob("*.exr"):
        print(f"   • {exr_file.name}")

def main():
    parser = argparse.ArgumentParser(description="Convert BeamNG terrain .npy files to EXR textures")
    parser.add_argument("--input", "-i", default="blender_export", 
                       help="Input directory containing .npy files (default: blender_export)")
    parser.add_argument("--output", "-o", default="exr_textures",
                       help="Output directory for EXR files (default: exr_textures)")
    
    args = parser.parse_args()
    
    try:
        convert_npy_to_exr(args.input, args.output)
    except ImportError as e:
        if "OpenEXR" in str(e):
            print("❌ OpenEXR library not found!")
            print("💡 Install with: pip install OpenEXR")
            print("   On macOS: brew install openexr && pip install OpenEXR")
        else:
            print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 
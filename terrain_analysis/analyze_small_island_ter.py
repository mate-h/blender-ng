#!/usr/bin/env python3
"""
Analyze the working small_island.ter file to understand proper BeamNG terrain structure
"""

import struct
import numpy as np
from pathlib import Path
import json

def analyze_ter_file(ter_path, json_path=None):
    """Analyze BeamNG .ter file structure"""
    print(f"🔍 Analyzing BeamNG terrain file: {ter_path}")
    
    if not Path(ter_path).exists():
        print(f"❌ File not found: {ter_path}")
        return
    
    file_size = Path(ter_path).stat().st_size
    print(f"📊 File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
    
    with open(ter_path, 'rb') as f:
        # Read header
        version = struct.unpack('B', f.read(1))[0]
        size = struct.unpack('<I', f.read(4))[0]
        
        print(f"📋 Header:")
        print(f"   Version: {version}")
        print(f"   Size: {size}x{size}")
        print(f"   Expected heightmap size: {size*size*2:,} bytes")
        print(f"   Expected layermap size: {size*size:,} bytes")
        
        # Read heightmap
        heightmap_bytes = size * size * 2
        heightmap_data = f.read(heightmap_bytes)
        heights = struct.unpack(f'<{len(heightmap_data)//2}H', heightmap_data)
        heightmap = np.array(heights, dtype=np.uint16).reshape((size, size))
        
        print(f"🏔️  Heightmap analysis:")
        print(f"   Shape: {heightmap.shape}")
        print(f"   Range: {heightmap.min()} - {heightmap.max()}")
        print(f"   Unique values: {len(np.unique(heightmap))}")
        
        # Read layermap
        layermap_bytes = size * size
        layermap_data = f.read(layermap_bytes)
        layermap = np.array(struct.unpack(f'{layermap_bytes}B', layermap_data), dtype=np.uint8).reshape((size, size))
        
        print(f"🎨 Layermap analysis:")
        print(f"   Shape: {layermap.shape}")
        print(f"   Range: {layermap.min()} - {layermap.max()}")
        print(f"   Unique values: {len(np.unique(layermap))}")
        print(f"   Unique material IDs: {sorted(np.unique(layermap))}")
        
        # Check for holes (255 values)
        holes = np.sum(layermap == 255)
        if holes > 0:
            print(f"   🕳️  Holes detected: {holes} pixels ({holes/layermap.size*100:.2f}%)")
        
        # Try to read layer texture map
        current_pos = f.tell()
        remaining_bytes = file_size - current_pos
        print(f"📍 Current position: {current_pos:,} bytes")
        print(f"📏 Remaining bytes: {remaining_bytes:,} bytes")
        
        if remaining_bytes >= size * size:
            print(f"🛰️  Reading layer texture map...")
            layer_texture_data = f.read(size * size)
            layer_texture = np.array(struct.unpack(f'{size*size}B', layer_texture_data), dtype=np.uint8).reshape((size, size))
            
            print(f"   Shape: {layer_texture.shape}")
            print(f"   Range: {layer_texture.min()} - {layer_texture.max()}")
            print(f"   Unique values: {len(np.unique(layer_texture))}")
            print(f"   Mean value: {layer_texture.mean():.2f}")
            print(f"   Std deviation: {layer_texture.std():.2f}")
            
            # Check if layer texture looks like material IDs or actual texture data
            unique_vals = np.unique(layer_texture)
            if len(unique_vals) <= 20:
                print(f"   ⚠️  Few unique values - might be material IDs: {sorted(unique_vals)}")
            else:
                print(f"   ✅ Many unique values - looks like texture data")
            
            current_pos = f.tell()
            remaining_bytes = file_size - current_pos
        
        # Read any additional coverage maps
        coverage_maps = []
        map_index = 0
        while remaining_bytes >= size * size and map_index < 4:
            print(f"📊 Reading coverage map {map_index + 1}...")
            coverage_data = f.read(size * size)
            coverage_map = np.array(struct.unpack(f'{size*size}B', coverage_data), dtype=np.uint8).reshape((size, size))
            
            print(f"   Shape: {coverage_map.shape}")
            print(f"   Range: {coverage_map.min()} - {coverage_map.max()}")
            print(f"   Unique values: {len(np.unique(coverage_map))}")
            print(f"   Non-zero pixels: {np.sum(coverage_map > 0)} ({np.sum(coverage_map > 0)/coverage_map.size*100:.2f}%)")
            
            coverage_maps.append(coverage_map)
            current_pos = f.tell()
            remaining_bytes = file_size - current_pos
            map_index += 1
        
        # Read material information
        if remaining_bytes >= 4:
            print(f"📝 Reading materials...")
            material_count = struct.unpack('<I', f.read(4))[0]
            print(f"   Material count: {material_count}")
            
            materials = []
            for i in range(material_count):
                if f.tell() < file_size:
                    name_length = struct.unpack('B', f.read(1))[0]
                    if f.tell() + name_length <= file_size:
                        material_name = f.read(name_length).decode('ascii')
                        materials.append(material_name)
                        print(f"   Material {i}: '{material_name}' ({name_length} chars)")
            
            print(f"📋 Total materials found: {len(materials)}")
        
        final_pos = f.tell()
        print(f"📍 Final position: {final_pos:,} bytes")
        print(f"📏 Bytes remaining: {file_size - final_pos}")
    
    # Load JSON config if available
    if json_path and Path(json_path).exists():
        print(f"\n📄 JSON Config analysis:")
        with open(json_path, 'r') as f:
            config = json.load(f)
        
        print(f"   Materials in JSON: {len(config.get('materials', []))}")
        print(f"   Materials: {config.get('materials', [])}")
        print(f"   Size: {config.get('size', 'unknown')}")
        print(f"   Version: {config.get('version', 'unknown')}")

if __name__ == "__main__":
    print("="*60)
    print("WORKING TERRAIN ANALYSIS")
    print("="*60)
    # Analyze the working small_island terrain
    ter_path = "/Volumes/Goodboy/github/blend-ng/terrain_analysis/small_island/small_island.ter"
    json_path = "/Volumes/Goodboy/github/blend-ng/terrain_analysis/small_island/small_island.terrain.json"
    
    analyze_ter_file(ter_path, json_path)
    
    print("\n" + "="*60)
    print("OUR GENERATED TERRAIN ANALYSIS")
    print("="*60)
    # Analyze our generated terrain
    our_ter_path = "/Volumes/Goodboy/github/blend-ng/terrain_analysis/beamng_export/final_asphalt_terrain.ter"
    our_json_path = "/Volumes/Goodboy/github/blend-ng/terrain_analysis/beamng_export/final_asphalt_terrain.terrain.json"
    
    analyze_ter_file(our_ter_path, our_json_path)

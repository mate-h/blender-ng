#!/usr/bin/env python3
"""
Binary .ter File Comparison Tool

Compare the binary structure of original and exported .ter files
to identify differences that might cause game crashes.
"""

import struct
import os
from pathlib import Path

def analyze_ter_file(file_path: str, max_bytes: int = 1024):
    """Analyze the binary structure of a .ter file"""
    
    print(f"\n📁 Analyzing: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None
    
    file_size = os.path.getsize(file_path)
    print(f"📊 File size: {file_size:,} bytes")
    
    with open(file_path, 'rb') as f:
        # Read header (5 bytes)
        version = struct.unpack('B', f.read(1))[0]
        size = struct.unpack('<I', f.read(4))[0]
        
        print(f"🔢 Header:")
        print(f"   Version: {version}")
        print(f"   Size: {size}")
        print(f"   Expected heightmap bytes: {size * size * 2:,}")
        print(f"   Expected layermap bytes: {size * size:,}")
        print(f"   Expected minimum file size: {5 + (size * size * 2) + (size * size):,}")
        
        # Calculate data positions
        heightmap_start = 5
        heightmap_bytes = size * size * 2
        layermap_start = heightmap_start + heightmap_bytes
        layermap_bytes = size * size
        
        print(f"📍 Data layout:")
        print(f"   Header: 0x000 - 0x004 (5 bytes)")
        print(f"   Heightmap: 0x{heightmap_start:03x} - 0x{layermap_start-1:x} ({heightmap_bytes:,} bytes)")
        print(f"   Layermap: 0x{layermap_start:x} - 0x{layermap_start + layermap_bytes - 1:x} ({layermap_bytes:,} bytes)")
        
        # Check if file has expected data
        remaining_after_layermap = file_size - (layermap_start + layermap_bytes)
        print(f"   Remaining after layermap: {remaining_after_layermap:,} bytes")
        
        # Sample some heightmap data
        f.seek(heightmap_start)
        sample_heights = []
        for i in range(min(10, heightmap_bytes // 2)):
            height_bytes = f.read(2)
            if len(height_bytes) == 2:
                height = struct.unpack('<H', height_bytes)[0]
                sample_heights.append(height)
        
        print(f"🏔️  Sample heights (first 10): {sample_heights}")
        
        # Sample some layermap data
        if layermap_start < file_size:
            f.seek(layermap_start)
            sample_materials = []
            for i in range(min(20, layermap_bytes)):
                mat_byte = f.read(1)
                if len(mat_byte) == 1:
                    mat_id = struct.unpack('B', mat_byte)[0]
                    sample_materials.append(mat_id)
            
            print(f"🎨 Sample materials (first 20): {sample_materials}")
            
            # Check for holes (255 values)
            f.seek(layermap_start)
            layermap_data = f.read(min(layermap_bytes, file_size - layermap_start))
            hole_count = layermap_data.count(255)
            print(f"🕳️  Holes detected: {hole_count} pixels")
        
        # Look for additional data after layermap
        if remaining_after_layermap > 0:
            print(f"📦 Additional data found ({remaining_after_layermap} bytes):")
            f.seek(layermap_start + layermap_bytes)
            
            # Try to parse as coverage maps (4 maps expected)
            coverage_maps_size = size * size * 4  # 4 coverage maps
            if remaining_after_layermap >= coverage_maps_size:
                print(f"   Possible coverage maps: {coverage_maps_size:,} bytes")
                remaining_after_coverage = remaining_after_layermap - coverage_maps_size
                print(f"   Remaining after coverage maps: {remaining_after_coverage} bytes")
                
                # Check for material count and names
                if remaining_after_coverage >= 4:
                    f.seek(layermap_start + layermap_bytes + coverage_maps_size)
                    material_count_bytes = f.read(4)
                    if len(material_count_bytes) == 4:
                        material_count = struct.unpack('<I', material_count_bytes)[0]
                        print(f"   Material count: {material_count}")
                        
                        # Try to read material names
                        materials_read = []
                        for i in range(min(material_count, 20)):  # Max 20 to avoid infinite loop
                            name_len_byte = f.read(1)
                            if len(name_len_byte) == 1:
                                name_len = struct.unpack('B', name_len_byte)[0]
                                if name_len > 0 and name_len < 100:  # Reasonable name length
                                    name_bytes = f.read(name_len)
                                    if len(name_bytes) == name_len:
                                        try:
                                            name = name_bytes.decode('ascii').rstrip('\x00')
                                            materials_read.append(name)
                                        except:
                                            break
                                else:
                                    break
                            else:
                                break
                        
                        if materials_read:
                            print(f"   Materials found: {materials_read}")
    
    return {
        'file_size': file_size,
        'version': version,
        'size': size,
        'heightmap_bytes': heightmap_bytes,
        'layermap_bytes': layermap_bytes,
        'remaining_bytes': remaining_after_layermap
    }

def hex_dump(file_path: str, start: int = 0, length: int = 256):
    """Create a hex dump of file contents"""
    print(f"\n🔍 Hex dump of {file_path} (offset {start}, {length} bytes):")
    
    with open(file_path, 'rb') as f:
        f.seek(start)
        data = f.read(length)
        
        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            hex_str = ' '.join(f'{b:02x}' for b in chunk)
            ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
            print(f"{start + i:08x}: {hex_str:<48} |{ascii_str}|")

def main():
    """Main comparison function"""
    
    original_path = "small_island/small_island.ter"
    exported_path = "beamng_export/exported_terrain.ter"
    
    print("🔍 BeamNG .ter File Binary Comparison")
    print("=" * 50)
    
    # Analyze both files
    original_info = analyze_ter_file(original_path)
    exported_info = analyze_ter_file(exported_path)
    
    if original_info and exported_info:
        print(f"\n📊 Comparison Summary:")
        print(f"   File sizes: {original_info['file_size']:,} vs {exported_info['file_size']:,}")
        print(f"   Versions: {original_info['version']} vs {exported_info['version']}")
        print(f"   Sizes: {original_info['size']} vs {exported_info['size']}")
        print(f"   Remaining bytes: {original_info['remaining_bytes']:,} vs {exported_info['remaining_bytes']:,}")
        
        # Check for critical differences
        if original_info['remaining_bytes'] > 0 and exported_info['remaining_bytes'] == 0:
            print(f"\n⚠️  CRITICAL: Original has {original_info['remaining_bytes']:,} additional bytes, exported has none!")
            print("   This likely includes coverage maps and material names that BeamNG requires.")
    
    # Show hex dumps of the beginning of both files
    if os.path.exists(original_path):
        hex_dump(original_path, 0, 64)
    
    if os.path.exists(exported_path):
        hex_dump(exported_path, 0, 64)

if __name__ == "__main__":
    main()
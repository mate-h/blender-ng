#!/usr/bin/env python3
"""
BeamNG .ter Terrain Parser - Fixed Version

Data starts at offset 5 (after header). All data uses little-endian encoding.
"""

import struct
import json
import numpy as np
from pathlib import Path
from typing import Dict, Optional

class BeamNGTerrainParser:
    def __init__(self, ter_file: str, json_file: str):
        self.ter_file = Path(ter_file)
        self.json_file = Path(json_file)
        
        # Load JSON configuration
        with open(self.json_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract parameters
        self.version = self.config['version']
        self.size = self.config['size']
        self.heightmap_size = self.config['heightMapSize']
        self.heightmap_item_size = self.config['heightMapItemSize']
        self.layermap_size = self.config['layerMapSize']
        self.layermap_item_size = self.config['layerMapItemSize']
        self.materials = self.config['materials']
        
        print("🏞️  BeamNG Terrain Parser")
        print(f"📁 Terrain: {self.ter_file.name}")
        print(f"📊 Dimensions: {self.size}x{self.size}")
        print(f"🎭 Materials: {len(self.materials)}")
        print("✅ Using offset 5 (after header), all data: little-endian")
    
    def parse_terrain(self) -> Dict:
        """Parse the terrain file using CORRECTED offset and encoding"""
        
        with open(self.ter_file, 'rb') as f:
            # Read header (little-endian)
            version = struct.unpack('B', f.read(1))[0]
            size = struct.unpack('<I', f.read(4))[0]
            
            # Verify header
            if version != self.version or size != self.size:
                raise ValueError(f"Header mismatch: got version={version}, size={size}")
            
            # FIXED: Data starts at offset 5 (immediately after header)
            data_start = 5
            print(f"📍 Using CORRECTED data offset: {data_start} (0x{data_start:x})")
            
            # Read heightmap with LITTLE-ENDIAN encoding
            f.seek(data_start)
            heightmap_bytes = self.heightmap_size * self.heightmap_item_size
            heightmap_data = f.read(heightmap_bytes)
            
            if len(heightmap_data) != heightmap_bytes:
                print(f"⚠️  Warning: Expected {heightmap_bytes} bytes, got {len(heightmap_data)}")
            
            # Parse as 16-bit LITTLE-ENDIAN (CORRECTED)
            num_heights = len(heightmap_data) // 2
            heights = struct.unpack(f'<{num_heights}H', heightmap_data)  # <H = little-endian
            
            # Reshape to 2D
            heightmap = np.array(heights, dtype=np.uint16).reshape((self.size, self.size))
            
            # Calculate layer map position
            layermap_start = data_start + heightmap_bytes
            layermap = None
            
            try:
                f.seek(layermap_start)
                
                # Calculate how much layermap data is actually available
                remaining_file_bytes = len(f.read())  # Read to end to get remaining size
                f.seek(layermap_start)  # Seek back
                
                expected_layermap_bytes = self.layermap_size * self.layermap_item_size
                available_layermap_bytes = min(expected_layermap_bytes, remaining_file_bytes)
                
                print("📊 Layermap info:")
                print(f"   Expected: {expected_layermap_bytes:,} bytes")
                print(f"   Available: {available_layermap_bytes:,} bytes")
                
                if available_layermap_bytes > 0:
                    layermap_data = f.read(available_layermap_bytes)
                    layers = struct.unpack(f'{len(layermap_data)}B', layermap_data)
                    
                    # Calculate how many complete rows we have
                    pixels_available = len(layers)
                    complete_rows = pixels_available // self.size
                    remaining_pixels = pixels_available % self.size
                    
                    print(f"   Pixels available: {pixels_available:,}")
                    print(f"   Complete rows: {complete_rows}")
                    print(f"   Remaining pixels: {remaining_pixels}")
                    
                    if complete_rows > 0:
                        # Create layermap with available data, pad with zeros if needed
                        if pixels_available == self.layermap_size:
                            # Perfect match
                            layermap = np.array(layers, dtype=np.uint8).reshape((self.size, self.size))
                            print(f"✅ Complete layer map loaded: {layermap.shape}")
                        else:
                            # Partial data - pad with zeros or truncate
                            if pixels_available < self.layermap_size:
                                # Pad with zeros
                                padded_layers = list(layers) + [0] * (self.layermap_size - pixels_available)
                                layermap = np.array(padded_layers, dtype=np.uint8).reshape((self.size, self.size))
                                print(f"⚠️  Partial layer map loaded and padded: {layermap.shape}")
                            else:
                                # Truncate to expected size
                                truncated_layers = layers[:self.layermap_size]
                                layermap = np.array(truncated_layers, dtype=np.uint8).reshape((self.size, self.size))
                                print(f"⚠️  Layer map loaded and truncated: {layermap.shape}")
                    else:
                        print("❌ Not enough data for even one complete row")
                        layermap = None
                else:
                    print("❌ No layermap data available")
                    layermap = None
                    
            except Exception as e:
                print(f"❌ Could not read layer map: {e}")
                layermap = None
            
            return {
                'header': {
                    'version': version,
                    'size': size,
                    'data_start': data_start,
                    'encoding': 'all_little_endian'  # CORRECTED encoding description
                },
                'heightmap': heightmap,
                'layermap': layermap,
                'materials': self.materials,
                'config': self.config
            }
    
    def get_terrain_stats(self, heightmap: np.ndarray) -> Dict:
        """Calculate terrain statistics"""
        return {
            'shape': heightmap.shape,
            'min_height': int(np.min(heightmap)),
            'max_height': int(np.max(heightmap)),
            'mean_height': float(np.mean(heightmap)),
            'std_height': float(np.std(heightmap)),
            'median_height': float(np.median(heightmap)),
            'unique_values': len(np.unique(heightmap)),
            'zero_count': int(np.sum(heightmap == 0)),
            'zero_percentage': float(np.sum(heightmap == 0) / heightmap.size * 100)
        }
    
    def analyze_materials(self, layermap: Optional[np.ndarray]) -> Dict:
        """Analyze material usage"""
        if layermap is None:
            return {'error': 'No layer map available'}
        
        unique_materials, counts = np.unique(layermap, return_counts=True)
        
        material_usage = {}
        for mat_id, count in zip(unique_materials, counts):
            if mat_id < len(self.materials):
                material_name = self.materials[mat_id]
                percentage = count / layermap.size * 100
                material_usage[material_name] = {
                    'id': int(mat_id),
                    'count': int(count),
                    'percentage': float(percentage)
                }
        
        return {
            'total_materials_used': len(unique_materials),
            'usage': material_usage
        }
    
    def export_for_blender(self, output_dir: str = "blender_export") -> Dict:
        """Export terrain data in format suitable for Blender import"""
        
        # Parse terrain
        terrain_data = self.parse_terrain()
        heightmap = terrain_data['heightmap']
        layermap = terrain_data['layermap']
        
        # Calculate statistics
        stats = self.get_terrain_stats(heightmap)
        material_analysis = self.analyze_materials(layermap)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save heightmap as float32 for Blender (better precision)
        heightmap_normalized = heightmap.astype(np.float32)
        np.save(output_path / "heightmap.npy", heightmap_normalized)
        
        # Save layer map if available
        if layermap is not None:
            np.save(output_path / "layermap.npy", layermap)
        
        # Create Blender import metadata
        blender_metadata = {
            'terrain_info': {
                'source_file': str(self.ter_file),
                'dimensions': [self.size, self.size],
                'heightmap_file': 'heightmap.npy',
                'layermap_file': 'layermap.npy' if layermap is not None else None,
            },
            'heightmap_stats': stats,
            'materials': {
                'list': self.materials,
                'analysis': material_analysis
            },
            'format_info': {
                'version': terrain_data['header']['version'],
                'data_start_offset': terrain_data['header']['data_start'],
                'encoding': terrain_data['header']['encoding'],
                'original_config': self.config
            }
        }
        
        # Save metadata as JSON
        with open(output_path / "terrain_metadata.json", 'w') as f:
            json.dump(blender_metadata, f, indent=2)
        
        print(f"✅ Exported corrected terrain data to: {output_path}")
        print(f"📊 Heightmap: {heightmap.shape} values")
        print(f"🎭 Materials: {len(self.materials)} defined")
        
        return blender_metadata

def main():
    """Test the FIXED parser with correct offset and endianness"""
    default_path = "/Volumes/Goodboy/crossover/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/levels/small_island"
    
    ter_file = f"{default_path}/small_island.ter"
    json_file = f"{default_path}/small_island.terrain.json"
    
    # Create parser
    parser = BeamNGTerrainParser(ter_file, json_file)
    
    # Parse and export
    parser.export_for_blender()
    
    # Print verification
    terrain_data = parser.parse_terrain()
    heightmap = terrain_data['heightmap']
    stats = parser.get_terrain_stats(heightmap)
    
    print("\n🎉 TERRAIN STATS (Offset 5, Little-Endian):")
    print(f"   Shape: {stats['shape']}")
    print(f"   Height range: {stats['min_height']} - {stats['max_height']}")
    print(f"   Mean height: {stats['mean_height']:.1f}")
    print(f"   Unique values: {stats['unique_values']:,}")
    print(f"   Water area: {stats['zero_percentage']:.1f}%")

if __name__ == "__main__":
    main() 
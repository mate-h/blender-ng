#!/usr/bin/env python3
"""
EXR to BeamNG .ter Export Script

This script converts Blender EXR displacement and layermap textures back to BeamNG .ter format.
Reverses the import process from import_level.py to allow terrain modifications in Blender
to be exported back to BeamNG.

Usage:
    python exr_to_ter.py
    
Input:
    - exr_textures/BeamNG_Terrain_Displacement.exr (heightmap data)
    - exr_textures/BeamNG_Terrain_Layermap.exr (material IDs)
    - exr_textures/terrain_info.json (metadata)
    
Output:
    - exported_terrain.ter (BeamNG terrain file)
    - exported_terrain.terrain.json (BeamNG terrain config)
"""

import struct
import json
import numpy as np
from pathlib import Path
import OpenEXR
import Imath
import array
import shutil

class EXRToTerExporter:
    """Export Blender EXR textures to BeamNG .ter format"""
    
    def __init__(self, exr_dir: str = "exr_textures"):
        self.exr_dir = Path(exr_dir)
        self.displacement_path = self.exr_dir / "BeamNG_Terrain_Displacement.exr"
        self.layermap_path = self.exr_dir / "BeamNG_Terrain_Layermap.exr"
        self.info_path = self.exr_dir / "terrain_info.json"
        
        # Load terrain info
        self.load_terrain_info()
        
        print("🏞️  BeamNG EXR to .ter Exporter")
        print(f"📁 EXR Directory: {self.exr_dir}")
        print(f"📊 Terrain Size: {self.size}x{self.size}")
        print(f"🎭 Materials: {len(self.materials)}")
        print(f"🔢 Version: {self.version}")
    
    def load_terrain_info(self):
        """Load terrain information from JSON file"""
        try:
            with open(self.info_path, 'r') as f:
                info = json.load(f)
            
            # Extract format info
            format_info = info['format_info']
            original_config = format_info['original_config']
            
            self.version = original_config['version']
            self.size = original_config['size']
            self.materials = original_config['materials']
            self.heightmap_item_size = original_config['heightMapItemSize']
            self.layermap_item_size = original_config['layerMapItemSize']
            
            print(f"✅ Loaded terrain info: {self.size}x{self.size}, {len(self.materials)} materials")
            
        except Exception as e:
            print(f"❌ Error loading terrain info: {e}")
            # Use fallback values
            self.version = 9
            self.size = 1024
            self.materials = ["Grass", "dirt_grass", "BeachSand", "dirt_rocky_large", "dirt_loose", "dirt_dusty", "groundmodel_asphalt1", "Concrete", "Grass2", "Mud", "Rock"]
            self.heightmap_item_size = 2
            self.layermap_item_size = 1
            print("⚠️  Using fallback terrain parameters")
    
    def read_exr_displacement(self):
        """Read heightmap data from EXR displacement texture"""
        print(f"📖 Reading displacement EXR: {self.displacement_path}")
        
        if not self.displacement_path.exists():
            raise FileNotFoundError(f"Displacement EXR not found: {self.displacement_path}")
        
        # Open EXR file
        exr_file = OpenEXR.InputFile(str(self.displacement_path))
        
        # Get header info
        header = exr_file.header()
        dw = header['dataWindow']
        width = dw.max.x - dw.min.x + 1
        height = dw.max.y - dw.min.y + 1
        
        print(f"   EXR dimensions: {width}x{height}")
        
        # Read red channel (contains height data)
        FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
        red_str = exr_file.channel('R', FLOAT)
        red = array.array('f', red_str)
        
        # Convert to numpy array and reshape
        heightmap_normalized = np.array(red, dtype=np.float32).reshape((height, width))
        
        # Convert back from normalized 0-1 range to 16-bit values (reverse of import process)
        # In import_level.py: heightmap_normalized = heightmap.astype(np.float32) / 65535.0
        heightmap = (heightmap_normalized * 65535.0).astype(np.uint16)
        
        print(f"   Height range: {heightmap.min()} - {heightmap.max()}")
        print(f"   Shape: {heightmap.shape}")
        
        exr_file.close()
        return heightmap
    
    def read_exr_layermap(self):
        """Read layermap data from EXR layermap texture"""
        print(f"📖 Reading layermap EXR: {self.layermap_path}")
        
        if not self.layermap_path.exists():
            print("⚠️  Layermap EXR not found, creating empty layermap")
            return np.zeros((self.size, self.size), dtype=np.uint8)
        
        # Open EXR file
        exr_file = OpenEXR.InputFile(str(self.layermap_path))
        
        # Get header info
        header = exr_file.header()
        dw = header['dataWindow']
        width = dw.max.x - dw.min.x + 1
        height = dw.max.y - dw.min.y + 1
        
        print(f"   EXR dimensions: {width}x{height}")
        
        # Read red channel (contains material ID data)
        FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
        red_str = exr_file.channel('R', FLOAT)
        red = array.array('f', red_str)
        
        # Convert to numpy array and reshape
        layermap_float = np.array(red, dtype=np.float32).reshape((height, width))
        
        # Convert back to 8-bit material IDs (layermap was stored as raw values in import)
        layermap = np.round(layermap_float).astype(np.uint8)
        
        # Validate material IDs
        unique_ids = np.unique(layermap)
        print(f"   Material IDs found: {unique_ids}")
        print(f"   Max material ID: {layermap.max()}")
        
        # Check for holes (ID 255)
        hole_count = np.sum(layermap == 255)
        if hole_count > 0:
            print(f"   Holes detected: {hole_count} pixels ({hole_count/layermap.size*100:.1f}%)")
        
        exr_file.close()
        return layermap
    
    def write_ter_file(self, heightmap: np.ndarray, layermap: np.ndarray, output_path: str):
        """Write .ter file in BeamNG format"""
        print(f"💾 Writing .ter file: {output_path}")
        
        with open(output_path, 'wb') as f:
            # Write header (5 bytes total)
            # Version (1 byte)
            f.write(struct.pack('B', self.version))
            
            # Size (4 bytes, little-endian)
            f.write(struct.pack('<I', self.size))
            
            print(f"   Header: version={self.version}, size={self.size}")
            
            # Write heightmap data (little-endian 16-bit values)
            print(f"   Writing heightmap: {heightmap.shape} -> {heightmap.size * 2} bytes")
            
            # Flatten and pack as little-endian 16-bit unsigned integers
            heightmap_flat = heightmap.flatten()
            heightmap_bytes = struct.pack(f'<{len(heightmap_flat)}H', *heightmap_flat)
            f.write(heightmap_bytes)
            
            # Write layermap data (8-bit values)
            print(f"   Writing layermap: {layermap.shape} -> {layermap.size} bytes")
            
            # Flatten and pack as 8-bit unsigned integers
            layermap_flat = layermap.flatten()
            layermap_bytes = struct.pack(f'{len(layermap_flat)}B', *layermap_flat)
            f.write(layermap_bytes)
            
            # Write material information (CRITICAL for BeamNG)
            print(f"   Writing material data: {len(self.materials)} materials")
            
            # Write material count (4 bytes, little-endian)
            f.write(struct.pack('<I', len(self.materials)))
            
            # Write material names as length-prefixed strings (no null terminators)
            for material in self.materials:
                # Write length byte followed by material name
                material_bytes = material.encode('ascii')
                f.write(struct.pack('B', len(material_bytes)))
                f.write(material_bytes)
                print(f"     • {material} ({len(material_bytes)} bytes)")
            
            print(f"✅ Wrote .ter file: {Path(output_path).name}")
            print(f"   Total size: {f.tell()} bytes")
    
    def write_terrain_json(self, output_path: str):
        """Write .terrain.json configuration file"""
        print(f"💾 Writing terrain config: {output_path}")
        
        config = {
            "binaryFormat": "version(char), size(unsigned int), heightMap(heightMapSize * heightMapItemSize), layerMap(layerMapSize * layerMapItemSize), layerTextureMap(layerMapSize * layerMapItemSize), materialNames",
            "datafile": f"/{Path(output_path).stem}.ter",
            "heightMapItemSize": self.heightmap_item_size,
            "heightMapSize": self.size * self.size,
            "layerMapItemSize": self.layermap_item_size,
            "layerMapSize": self.size * self.size,
            "materials": self.materials,
            "size": self.size,
            "version": self.version
        }
        
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Wrote terrain config: {Path(output_path).name}")
    
    def export_terrain(self, output_name: str = "exported_terrain"):
        """Export complete terrain from EXR files to .ter format"""
        try:
            print("🚀 Starting terrain export...")
            
            # Read EXR textures
            heightmap = self.read_exr_displacement()
            layermap = self.read_exr_layermap()
            
            # Validate dimensions match
            if heightmap.shape != (self.size, self.size):
                print(f"⚠️  Heightmap size mismatch: {heightmap.shape} vs expected {self.size}x{self.size}")
                # Resize if needed
                if heightmap.shape[0] != self.size or heightmap.shape[1] != self.size:
                    print("🔧 Resizing heightmap to match expected dimensions...")
                    from scipy import ndimage
                    heightmap = ndimage.zoom(heightmap, (self.size/heightmap.shape[0], self.size/heightmap.shape[1]), order=1)
                    heightmap = heightmap.astype(np.uint16)
            
            if layermap.shape != (self.size, self.size):
                print(f"⚠️  Layermap size mismatch: {layermap.shape} vs expected {self.size}x{self.size}")
                # Resize if needed
                if layermap.shape[0] != self.size or layermap.shape[1] != self.size:
                    print("🔧 Resizing layermap to match expected dimensions...")
                    from scipy import ndimage
                    layermap = ndimage.zoom(layermap, (self.size/layermap.shape[0], self.size/layermap.shape[1]), order=0)
                    layermap = layermap.astype(np.uint8)

            # create or delete beamng_export directory
            if Path("beamng_export").exists():
                shutil.rmtree("beamng_export")
            Path("beamng_export").mkdir(parents=True, exist_ok=True)
            
            # Write output files
            ter_path = Path("beamng_export") / f"{output_name}.ter"
            json_path = Path("beamng_export") / f"{output_name}.terrain.json"
            
            self.write_ter_file(heightmap, layermap, ter_path)
            self.write_terrain_json(json_path)
            
            # Print export summary
            print("\n📊 Export Summary:")
            print(f"   Terrain size: {self.size}x{self.size}")
            print(f"   Height range: {heightmap.min()} - {heightmap.max()}")
            print(f"   Materials: {len(self.materials)}")
            print(f"   Unique material IDs: {len(np.unique(layermap))}")
            print(f"   Output files:")
            print(f"     • {ter_path}")
            print(f"     • {json_path}")
            
            return ter_path, json_path
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            raise

def main():
    """Main export function"""
    try:
        # Create exporter
        exporter = EXRToTerExporter()
        
        # Export terrain
        ter_file, json_file = exporter.export_terrain("exported_terrain")
        
        print(f"\n🎉 Export completed successfully!")
        print(f"📁 Files created:")
        print(f"   • {ter_file}")
        print(f"   • {json_file}")
        print(f"\n💡 Next steps:")
        print(f"   1. Copy {ter_file} to your BeamNG level directory")
        print(f"   2. Copy {json_file} to your BeamNG level directory")
        print(f"   3. Test in BeamNG.drive")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
#!/usr/bin/env python3
"""
Process final.exr (10km x 10km terrain) to BeamNG .ter format
Handles blue channel height data from Blender position bake with asphalt-only material.
"""

import struct
import json
import numpy as np
from pathlib import Path
import OpenEXR
import Imath
import array
import shutil
from PIL import Image
from scipy import ndimage

class FinalEXRToTerExporter:
    """Export center-cropped terrain from final.exr to BeamNG .ter format"""
    
    def __init__(self, exr_path: str, satellite_path: str, target_size: int = 8192, max_terrain_height: float = 1000.0):
        self.exr_path = Path(exr_path)
        self.satellite_path = Path(satellite_path)
        self.target_size = target_size  # Cropped resolution: 1 meter per pixel
        self.max_terrain_height = max_terrain_height  # Max height in meters for BeamNG
        self.real_world_size = target_size  # Real world size in meters (1:1 scale)
        
        # Terrain configuration for 8.192km x 8.192km with satellite texture
        self.version = 9
        self.materials = ["Asphalt"]  # Only asphalt material
        self.heightmap_item_size = 2
        self.layermap_item_size = 1
        
        print("🏁 Final.exr to BeamNG .ter Exporter (CENTER CROP + SATELLITE)")
        print(f"📁 Terrain: {self.exr_path}")
        print(f"🛰️  Satellite: {self.satellite_path}")
        print(f"📊 Crop to: {self.target_size}x{self.target_size} (center crop from 10000x10000)")
        print(f"🌍 Real size: {self.real_world_size/1000:.3f}km x {self.real_world_size/1000:.3f}km")
        print(f"🏔️  Max height: {self.max_terrain_height}m")
        print(f"🛣️  Material: {self.materials[0]} only")
    
    def read_and_process_height_data(self):
        """Read height data from blue channel and process for BeamNG"""
        print(f"📖 Reading height data from: {self.exr_path}")
        
        if not self.exr_path.exists():
            raise FileNotFoundError(f"EXR file not found: {self.exr_path}")
        
        # Open EXR file
        exr_file = OpenEXR.InputFile(str(self.exr_path))
        
        # Get header info
        header = exr_file.header()
        dw = header['dataWindow']
        width = dw.max.x - dw.min.x + 1
        height = dw.max.y - dw.min.y + 1
        
        print(f"   Source dimensions: {width}x{height}")
        
        # Read blue channel (height data from Blender position bake)
        FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
        blue_str = exr_file.channel('B', FLOAT)
        blue_data = array.array('f', blue_str)
        
        # Convert to numpy array
        height_data = np.array(blue_data, dtype=np.float32).reshape((height, width))
        
        print(f"   Original height range: {height_data.min():.3f} - {height_data.max():.3f}m")
        
        # Handle zero/negative values (likely background/sky pixels)
        # Replace with minimum valid height
        valid_mask = height_data > 0
        if np.any(valid_mask):
            min_valid_height = np.min(height_data[valid_mask])
            height_data[~valid_mask] = min_valid_height
            print(f"   Replaced {np.sum(~valid_mask)} zero/negative values with {min_valid_height:.3f}m")
        
        # Normalize height data to terrain-appropriate range
        original_min = height_data.min()
        original_max = height_data.max()
        original_range = original_max - original_min
        
        print(f"   Normalizing from range {original_range:.3f}m to {self.max_terrain_height}m")
        
        # Normalize to 0-1 range, then scale to target height
        height_normalized = (height_data - original_min) / original_range
        height_scaled = height_normalized * self.max_terrain_height
        
        print(f"   Normalized height range: {height_scaled.min():.3f} - {height_scaled.max():.3f}m")
        
        # Center crop from 10000x10000 to target size (no scaling)
        if height_scaled.shape == (10000, 10000):
            if self.target_size == 10000:
                print(f"   ✅ No cropping needed: preserving full {height_scaled.shape} resolution")
            else:
                # Calculate center crop coordinates
                source_size = height_scaled.shape[0]  # Should be 10000
                crop_offset = (source_size - self.target_size) // 2
                crop_end = crop_offset + self.target_size
                
                print(f"   ✂️  Center cropping from {height_scaled.shape} to {self.target_size}x{self.target_size}")
                print(f"   Crop region: [{crop_offset}:{crop_end}, {crop_offset}:{crop_end}]")
                
                # Perform center crop (no scaling)
                height_scaled = height_scaled[crop_offset:crop_end, crop_offset:crop_end]
                
                print(f"   ✅ Cropped to: {height_scaled.shape}")
        else:
            print(f"   ⚠️  Unexpected source dimensions: {height_scaled.shape}, expected (10000, 10000)")
            raise ValueError(f"Source must be 10000x10000, got {height_scaled.shape}")
        
        # Convert to 16-bit format for .ter file (0-65535 range)
        heightmap = (height_scaled / self.max_terrain_height * 65535.0).astype(np.uint16)
        
        # Flip Y axis for BeamNG coordinate system
        heightmap = np.flipud(heightmap)
        
        print(f"   Final heightmap: {heightmap.shape}, range {heightmap.min()} - {heightmap.max()}")
        print(f"   ↕️  Y-axis flipped for BeamNG coordinate system")
        
        exr_file.close()
        
        return heightmap, {
            'original_min': float(original_min),
            'original_max': float(original_max),
            'original_range': float(original_range),
            'scaled_min': float(height_scaled.min()),
            'scaled_max': float(height_scaled.max()),
            'terrain_scale': self.max_terrain_height
        }
    
    def create_asphalt_layermap(self):
        """Create layermap with only asphalt material (ID 0)"""
        print(f"🛣️  Creating asphalt-only layermap: {self.target_size}x{self.target_size}")
        
        # All pixels get material ID 0 (first and only material: asphalt)
        layermap = np.zeros((self.target_size, self.target_size), dtype=np.uint8)
        
        # Flip Y axis to match heightmap coordinate system
        layermap = np.flipud(layermap)
        
        print(f"   Layermap: {layermap.shape}, all pixels = material ID 0 (asphalt)")
        print(f"   ↕️  Y-axis flipped to match heightmap")
        
        return layermap
    
    def process_satellite_texture(self):
        """Process satellite imagery for layer texture map"""
        print(f"🛰️  Processing satellite imagery: {self.satellite_path}")
        
        if not self.satellite_path.exists():
            raise FileNotFoundError(f"Satellite image not found: {self.satellite_path}")
        
        # Load satellite image
        satellite_img = Image.open(self.satellite_path)
        print(f"   Source dimensions: {satellite_img.size[0]}x{satellite_img.size[1]}")
        
        # Convert to RGB if needed
        if satellite_img.mode != 'RGB':
            satellite_img = satellite_img.convert('RGB')
            print(f"   Converted to RGB mode")
        
        # Resize from 10240x10240 to exactly 10000x10000
        if satellite_img.size != (10000, 10000):
            print(f"   Resizing from {satellite_img.size} to 10000x10000")
            satellite_img = satellite_img.resize((10000, 10000), Image.LANCZOS)
        
        # Convert to numpy array
        satellite_array = np.array(satellite_img)
        print(f"   Satellite array shape: {satellite_array.shape}")
        
        # Center crop from 10000x10000 to target size (same as heightmap)
        if self.target_size == 10000:
            print(f"   ✅ No cropping needed: preserving full resolution")
            cropped_satellite = satellite_array
        else:
            # Calculate center crop coordinates (same logic as heightmap)
            source_size = satellite_array.shape[0]  # Should be 10000
            crop_offset = (source_size - self.target_size) // 2
            crop_end = crop_offset + self.target_size
            
            print(f"   ✂️  Center cropping from {satellite_array.shape[:2]} to {self.target_size}x{self.target_size}")
            print(f"   Crop region: [{crop_offset}:{crop_end}, {crop_offset}:{crop_end}]")
            
            # Perform center crop
            cropped_satellite = satellite_array[crop_offset:crop_end, crop_offset:crop_end]
            print(f"   ✅ Cropped to: {cropped_satellite.shape}")
        
        # Flip Y axis to match heightmap coordinate system
        cropped_satellite = np.flipud(cropped_satellite)
        
        # Convert RGB to grayscale for layer texture map (BeamNG expects single channel)
        # Use luminance formula: 0.299*R + 0.587*G + 0.114*B
        if len(cropped_satellite.shape) == 3:
            layer_texture = np.dot(cropped_satellite, [0.299, 0.587, 0.114]).astype(np.uint8)
            print(f"   Converted RGB to grayscale using luminance formula")
        else:
            layer_texture = cropped_satellite.astype(np.uint8)
        
        print(f"   Final layer texture: {layer_texture.shape}, range {layer_texture.min()} - {layer_texture.max()}")
        print(f"   ↕️  Y-axis flipped to match heightmap")
        
        return layer_texture
    
    def write_ter_file(self, heightmap: np.ndarray, layermap: np.ndarray, output_path: str):
        """Write .ter file in BeamNG format (WITHOUT layer texture map to avoid material limit)"""
        print(f"💾 Writing .ter file: {output_path}")
        
        with open(output_path, 'wb') as f:
            # Write header (5 bytes total)
            f.write(struct.pack('B', self.version))  # Version (1 byte)
            f.write(struct.pack('<I', self.target_size))  # Size (4 bytes, little-endian)
            
            print(f"   Header: version={self.version}, size={self.target_size}")
            
            # Write heightmap data (little-endian 16-bit values)
            print(f"   Writing heightmap: {heightmap.shape} -> {heightmap.size * 2} bytes")
            heightmap_flat = heightmap.flatten()
            heightmap_bytes = struct.pack(f'<{len(heightmap_flat)}H', *heightmap_flat)
            f.write(heightmap_bytes)
            
            # Write layermap data (8-bit values)
            print(f"   Writing layermap: {layermap.shape} -> {layermap.size} bytes")
            layermap_flat = layermap.flatten()
            layermap_bytes = struct.pack(f'{len(layermap_flat)}B', *layermap_flat)
            f.write(layermap_bytes)
            
            # SKIP layer texture map to avoid BeamNG material limit issues
            print(f"   ⚠️  Skipping layer texture map to avoid material limit (254 max)")
            
            # Write material information
            print(f"   Writing material data: {len(self.materials)} materials")
            f.write(struct.pack('<I', len(self.materials)))  # Material count
            
            # Write material names
            for material in self.materials:
                material_bytes = material.encode('ascii')
                f.write(struct.pack('B', len(material_bytes)))
                f.write(material_bytes)
                print(f"     • {material} ({len(material_bytes)} bytes)")
            
            print(f"✅ Wrote .ter file: {Path(output_path).name}")
            print(f"   Total size: {f.tell()} bytes")
    
    def write_terrain_json(self, output_path: str, height_stats: dict):
        """Write .terrain.json configuration file"""
        print(f"💾 Writing terrain config: {output_path}")
        
        config = {
            "binaryFormat": "version(char), size(unsigned int), heightMap(heightMapSize * heightMapItemSize), layerMap(layerMapSize * layerMapItemSize), layerTextureMap(layerMapSize * layerMapItemSize), materialNames",
            "datafile": f"/{Path(output_path).stem}.ter",
            "heightMapItemSize": self.heightmap_item_size,
            "heightMapSize": self.target_size * self.target_size,
            "layerMapItemSize": self.layermap_item_size,
            "layerMapSize": self.target_size * self.target_size,
            "materials": self.materials,
            "size": self.target_size,
            "version": self.version,
        }
        
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Wrote terrain config: {Path(output_path).name}")
    
    def export_terrain(self, output_name: str = "final_terrain"):
        """Export complete terrain from final.exr to .ter format"""
        try:
            print("🚀 Starting terrain export from final.exr...")
            
            # Process height data
            heightmap, height_stats = self.read_and_process_height_data()
            
            # Create asphalt-only layermap
            layermap = self.create_asphalt_layermap()
            
            # Skip satellite texture processing to avoid material limit
            print("⚠️  Skipping satellite texture processing to avoid BeamNG 254 material limit")
            
            # Create or clean output directory
            output_dir = Path("beamng_export")
            if output_dir.exists():
                shutil.rmtree(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Write output files
            ter_path = output_dir / f"{output_name}.ter"
            json_path = output_dir / f"{output_name}.terrain.json"
            
            self.write_ter_file(heightmap, layermap, ter_path)
            self.write_terrain_json(json_path, height_stats)
            
            # Print export summary
            print("\n📊 Export Summary:")
            print(f"   Source: 10km x 10km terrain ({self.exr_path.name})")
            print(f"   Output: {self.target_size}x{self.target_size} BeamNG terrain (CENTER CROPPED)")
            print(f"   Real size: {self.real_world_size/1000:.3f}km x {self.real_world_size/1000:.3f}km")
            print(f"   Pixel size: 1.0m per pixel (no scaling)")
            print(f"   Height range: {height_stats['scaled_min']:.1f}m - {height_stats['scaled_max']:.1f}m")
            print(f"   Material: {self.materials[0]} only")
            print(f"   Estimated file size: ~{(self.target_size*self.target_size*3)/1024/1024:.0f}MB (no satellite texture)")
            print(f"   Files created:")
            print(f"     • {ter_path}")
            print(f"     • {json_path}")
            
            return ter_path, json_path, height_stats
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            raise

def main():
    """Main export function"""
    try:
        # Set up paths and parameters
        exr_path = "/Volumes/Goodboy/github/blend-ng/terrain_analysis/exr_textures/final.exr"
        satellite_path = "/Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_49.3375_-123.2065_1ppm_9.765625km.jpg"
        target_size = 8192  # Center crop: 1 meter per pixel
        max_height = 500.0  # Reasonable max height for racing terrain (meters)
        
        print(f"🎯 Processing terrain for BeamNG (CENTER CROP)")
        print(f"   Source: 10000x10000 pixels (10km x 10km)")
        print(f"   Target: {target_size}x{target_size} pixels ({target_size/1000:.3f}km x {target_size/1000:.3f}km)")
        print(f"   Resolution: 1.0m per pixel (no scaling)")
        print(f"   Max height: {max_height}m")
        
        # Create exporter
        exporter = FinalEXRToTerExporter(exr_path, satellite_path, target_size, max_height)
        
        # Export terrain
        ter_file, json_file, stats = exporter.export_terrain("final_asphalt_terrain")
        
        print(f"\n🎉 Export completed successfully!")
        print(f"📁 Files created:")
        print(f"   • {ter_file}")
        print(f"   • {json_file}")
        print(f"\n💡 Next steps:")
        print(f"   1. Copy files to your BeamNG level directory")
        print(f"   2. Update level config to reference the new terrain")
        print(f"   3. Test in BeamNG.drive")
        print(f"\n📏 Terrain specs:")
        print(f"   • {target_size/1000:.3f}km x {target_size/1000:.3f}km real-world size")
        print(f"   • {target_size}x{target_size} resolution (CENTER CROPPED)")
        print(f"   • 1.0m per pixel detail (no scaling)")
        print(f"   • Asphalt surface throughout")
        print(f"   • File size: ~{(target_size*target_size*3)/1024/1024:.0f}MB (no satellite texture)")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
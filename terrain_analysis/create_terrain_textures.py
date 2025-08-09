#!/usr/bin/env python3
"""
Create BeamNG terrain textures from satellite imagery
Generates PBR texture maps for use with BeamNG terrain materials
"""

import numpy as np
from PIL import Image
from pathlib import Path
import shutil

class TerrainTextureGenerator:
    """Generate BeamNG terrain textures from satellite imagery"""
    
    def __init__(self, satellite_path: str, output_dir: str, target_size: int = 8192):
        self.satellite_path = Path(satellite_path)
        self.output_dir = Path(output_dir)
        self.target_size = target_size  # Final texture resolution (1m per pixel)
        
        print("🎨 BeamNG Terrain Texture Generator (1m per pixel)")
        print(f"📁 Satellite: {self.satellite_path}")
        print(f"📂 Output: {self.output_dir}")
        print(f"🖼️  Final texture: {self.target_size}x{self.target_size} (1m per pixel)")
    
    def process_satellite_image(self):
        """Process satellite image with same pipeline as terrain"""
        print(f"🛰️  Processing satellite imagery...")
        
        if not self.satellite_path.exists():
            raise FileNotFoundError(f"Satellite image not found: {self.satellite_path}")
        
        # Load satellite image
        satellite_img = Image.open(self.satellite_path)
        print(f"   Source dimensions: {satellite_img.size[0]}x{satellite_img.size[1]}")
        
        # Convert to RGB if needed
        if satellite_img.mode != 'RGB':
            satellite_img = satellite_img.convert('RGB')
            print(f"   Converted to RGB mode")
        
        # Resize from 10240x10240 to exactly 10000x10000 (same as terrain processing)
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
        print(f"   ↕️  Y-axis flipped to match terrain")
        
        return cropped_satellite
    
    def create_base_texture(self, satellite_data: np.ndarray):
        """Create base texture (albedo/diffuse) from satellite data at 1m per pixel"""
        print(f"🎨 Creating base texture (albedo) at 1m per pixel resolution...")
        
        # Keep full resolution - no downsampling
        satellite_img = Image.fromarray(satellite_data)
        print(f"   Maintaining full resolution: {satellite_img.size} (1m per pixel)")
        
        # Enhance contrast and saturation for better terrain appearance
        from PIL import ImageEnhance
        
        # Slightly increase contrast
        enhancer = ImageEnhance.Contrast(satellite_img)
        satellite_img = enhancer.enhance(1.1)
        
        # Slightly increase saturation
        enhancer = ImageEnhance.Color(satellite_img)
        satellite_img = enhancer.enhance(1.15)
        
        print(f"   Enhanced contrast and saturation for terrain use")
        print(f"   Final base texture: {satellite_img.size} (1m per pixel)")
        
        return satellite_img
    
    def save_textures(self, base_texture: Image.Image):
        """Save texture files to output directory"""
        print(f"💾 Saving texture files...")
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save base texture (albedo/diffuse)
        base_path = self.output_dir / "t_terrain_base_b.png"
        base_texture.save(base_path, "PNG", optimize=True)
        
        print(f"   ✅ Base texture: {base_path}")
        print(f"      Size: {base_texture.size}")
        print(f"      File size: {base_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        return [base_path]
    
    def generate_textures(self):
        """Generate all terrain textures"""
        try:
            print("🚀 Starting texture generation...")
            
            # Process satellite imagery
            satellite_data = self.process_satellite_image()
            
            # Create base texture
            base_texture = self.create_base_texture(satellite_data)
            
            # Save textures
            texture_files = self.save_textures(base_texture)
            
            # Print summary
            print("\n📊 Texture Generation Summary:")
            print(f"   Source: {self.satellite_path.name}")
            print(f"   Terrain coverage: {self.target_size/1000:.3f}km x {self.target_size/1000:.3f}km")
            print(f"   Texture resolution: {self.target_size}x{self.target_size}")
            print(f"   Pixel density: 1.0m per texture pixel (FULL RESOLUTION)")
            print(f"   Files created:")
            for tex_file in texture_files:
                print(f"     • {tex_file.name}")
            
            return texture_files
            
        except Exception as e:
            print(f"❌ Texture generation failed: {e}")
            raise

def main():
    """Main texture generation function"""
    try:
        # Set up paths and parameters
        satellite_path = "/Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_49.3375_-123.2065_1ppm_9.765625km.jpg"
        output_dir = "/Volumes/Goodboy/github/blend-ng/terrain_analysis/beamng_export"
        target_size = 8192  # Final texture resolution (1m per pixel)
        
        print(f"🎯 Creating BeamNG terrain textures (1m per pixel)")
        print(f"   Processing: 10240x10240 → 10000x10000 → 8192x8192")
        print(f"   Final texture: {target_size}x{target_size} pixels ({target_size/1000:.3f}km)")
        print(f"   Resolution: 1.0m per texture pixel (FULL RESOLUTION)")
        
        # Create texture generator
        generator = TerrainTextureGenerator(satellite_path, output_dir, target_size)
        
        # Generate textures
        texture_files = generator.generate_textures()
        
        print(f"\n🎉 Texture generation completed successfully!")
        print(f"📁 Output directory: {output_dir}")
        print(f"💡 Next steps:")
        print(f"   1. Use textures with BeamNG terrain material")
        print(f"   2. Create material definition (.json)")
        print(f"   3. Test in BeamNG.drive")
        
    except Exception as e:
        print(f"❌ Texture generation failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

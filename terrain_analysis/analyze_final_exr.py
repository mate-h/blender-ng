#!/usr/bin/env python3
"""
Analyze final.exr height data from blue channel
"""

import numpy as np
import OpenEXR
import Imath
import array
from pathlib import Path

def analyze_height_data(exr_path: str):
    """Analyze height data from blue channel of EXR file"""
    print(f"📊 Analyzing height data from: {exr_path}")
    
    # Open EXR file
    exr_file = OpenEXR.InputFile(exr_path)
    
    # Get header info
    header = exr_file.header()
    dw = header['dataWindow']
    width = dw.max.x - dw.min.x + 1
    height = dw.max.y - dw.min.y + 1
    
    print(f"   Dimensions: {width}x{height}")
    
    # Read blue channel (contains height data from Blender position bake)
    FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
    blue_str = exr_file.channel('B', FLOAT)
    blue_data = array.array('f', blue_str)
    
    # Convert to numpy array
    height_data = np.array(blue_data, dtype=np.float32).reshape((height, width))
    
    # Calculate statistics
    min_height = float(np.min(height_data))
    max_height = float(np.max(height_data))
    mean_height = float(np.mean(height_data))
    std_height = float(np.std(height_data))
    median_height = float(np.median(height_data))
    
    print(f"   Height statistics:")
    print(f"     Min: {min_height:.3f} meters")
    print(f"     Max: {max_height:.3f} meters")
    print(f"     Mean: {mean_height:.3f} meters")
    print(f"     Std: {std_height:.3f} meters")
    print(f"     Median: {median_height:.3f} meters")
    print(f"     Range: {max_height - min_height:.3f} meters")
    
    # Check for zero/negative values
    zero_count = np.sum(height_data <= 0)
    zero_percentage = (zero_count / height_data.size) * 100
    print(f"     Zero/negative values: {zero_count} ({zero_percentage:.2f}%)")
    
    exr_file.close()
    
    return {
        'dimensions': [width, height],
        'min_height': min_height,
        'max_height': max_height,
        'mean_height': mean_height,
        'std_height': std_height,
        'median_height': median_height,
        'range': max_height - min_height,
        'zero_count': zero_count,
        'zero_percentage': zero_percentage,
        'height_data': height_data
    }

if __name__ == "__main__":
    # Analyze the final.exr file
    exr_path = "/Volumes/Goodboy/github/blend-ng/terrain_analysis/exr_textures/final.exr"
    stats = analyze_height_data(exr_path)
    
    print(f"\n🎯 Summary for 10km x 10km terrain:")
    print(f"   Pixel resolution: {stats['dimensions'][0]}x{stats['dimensions'][1]}")
    print(f"   Pixel size: {10000/stats['dimensions'][0]:.3f}m per pixel")
    print(f"   Height range: {stats['min_height']:.3f}m to {stats['max_height']:.3f}m")
    print(f"   Total elevation: {stats['range']:.3f}m")
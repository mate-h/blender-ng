#!/usr/bin/env python3
"""
Visualize Final Corrected Terrain

Test the final corrected parser and create a visualization to verify
the terrain is properly loaded without wrapping artifacts.
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from terrain_analysis.ter_parser import BeamNGTerrainParser

def visualize_corrected_terrain():
    """Visualize the final corrected terrain data"""
    
    default_path = "/Volumes/Goodboy/crossover/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/levels/small_island"
    ter_file = f"{default_path}/small_island.ter"
    json_file = f"{default_path}/small_island.terrain.json"
    
    # Create parser
    parser = BeamNGTerrainParser(ter_file, json_file)
    
    # Parse terrain
    terrain_data = parser.parse_terrain()
    heightmap = terrain_data['heightmap']
    
    print(f"Terrain data loaded successfully!")
    print(f"   Shape: {heightmap.shape}")
    print(f"   Min/Max heights: {heightmap.min()} / {heightmap.max()}")
    print(f"   Mean height: {heightmap.mean():.1f}")
    print(f"   Unique values: {len(np.unique(heightmap)):,}")
    
    # Create comprehensive visualization
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('BeamNG Small Island - CORRECTED (No Wrapping!)', fontsize=16, color='green', weight='bold')
    
    # 1. Full heightmap
    im1 = axes[0,0].imshow(heightmap, cmap='terrain', aspect='equal', origin='lower')
    axes[0,0].set_title('Corrected Heightmap\n(Offset 2048, Big-Endian)')
    axes[0,0].set_xlabel('X (East)')
    axes[0,0].set_ylabel('Y (North)')
    plt.colorbar(im1, ax=axes[0,0], label='Height Value')
    
    # 2. Height histogram
    axes[0,1].hist(heightmap.flatten(), bins=100, alpha=0.7, color='green', edgecolor='black')
    axes[0,1].set_title('Height Distribution')
    axes[0,1].set_xlabel('Height Value')
    axes[0,1].set_ylabel('Frequency')
    axes[0,1].grid(True, alpha=0.3)
    
    # Add statistics
    mean_h = heightmap.mean()
    std_h = heightmap.std()
    axes[0,1].axvline(mean_h, color='red', linestyle='--', label=f'Mean: {mean_h:.0f}')
    axes[0,1].axvline(mean_h + std_h, color='orange', linestyle='--', label=f'+1σ: {mean_h + std_h:.0f}')
    axes[0,1].axvline(mean_h - std_h, color='orange', linestyle='--', label=f'-1σ: {mean_h - std_h:.0f}')
    axes[0,1].legend()
    
    # 3. Edge analysis (to verify no wrapping)
    axes[1,0].plot(heightmap[:, 0], label='Left edge', alpha=0.7)
    axes[1,0].plot(heightmap[:, -1], label='Right edge', alpha=0.7)
    axes[1,0].plot(heightmap[0, :], label='Bottom edge', alpha=0.7)
    axes[1,0].plot(heightmap[-1, :], label='Top edge', alpha=0.7)
    axes[1,0].set_title('Edge Analysis\n(Should show smooth coastlines)')
    axes[1,0].set_xlabel('Position along edge')
    axes[1,0].set_ylabel('Height')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # 4. Gradient magnitude (terrain steepness)
    grad_y, grad_x = np.gradient(heightmap.astype(np.float32))
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    
    im4 = axes[1,1].imshow(gradient_magnitude, cmap='hot', aspect='equal', origin='lower')
    axes[1,1].set_title('Terrain Steepness\n(Gradient Magnitude)')
    axes[1,1].set_xlabel('X (East)')
    axes[1,1].set_ylabel('Y (North)')
    plt.colorbar(im4, ax=axes[1,1], label='Gradient Magnitude')
    
    plt.tight_layout()
    
    # Save visualization
    output_file = "final_corrected_terrain.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"📊 Visualization saved to: {output_file}")
    
    plt.show()
    
    # Analyze edge continuity to verify no wrapping
    left_edge = heightmap[:, 0]
    right_edge = heightmap[:, -1]
    top_edge = heightmap[0, :]
    bottom_edge = heightmap[-1, :]
    
    lr_diff = np.mean(np.abs(left_edge - right_edge))
    tb_diff = np.mean(np.abs(top_edge - bottom_edge))
    
    print(f"\n🔍 Edge Continuity Analysis:")
    print(f"   Left-Right edge difference: {lr_diff:.1f}")
    print(f"   Top-Bottom edge difference: {tb_diff:.1f}")
    
    if lr_diff < 5000 and tb_diff < 5000:
        print(f"✅ EXCELLENT: Low edge differences indicate proper terrain continuity!")
    elif lr_diff < 15000 and tb_diff < 15000:
        print(f"✅ GOOD: Moderate edge differences, much better than before!")
    else:
        print(f"⚠️  CAUTION: Still some edge discontinuities")
    
    # Check for realistic terrain features
    water_threshold = np.percentile(heightmap, 10)
    land_areas = heightmap > water_threshold
    water_areas = heightmap <= water_threshold
    
    print(f"\n🌊 Terrain Features:")
    print(f"   Water threshold: {water_threshold:.0f}")
    print(f"   Land area: {np.sum(land_areas)/heightmap.size*100:.1f}%")
    print(f"   Water/low areas: {np.sum(water_areas)/heightmap.size*100:.1f}%")
    print(f"   Highest point: {heightmap.max()}")
    print(f"   Elevation range: {heightmap.max() - heightmap.min()}")

if __name__ == "__main__":
    visualize_corrected_terrain() 
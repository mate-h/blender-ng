#!/usr/bin/env python3
"""
Visualize Final Corrected Terrain

Test the final corrected parser and create a visualization to verify
the terrain is properly loaded without wrapping artifacts.
"""

import numpy as np
import matplotlib.pyplot as plt
from ter_parser import BeamNGTerrainParser

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
    layermap = terrain_data['layermap']
    materials = terrain_data['materials']
    
    print("Terrain data loaded successfully!")
    print(f"   Shape: {heightmap.shape}")
    print(f"   Min/Max heights: {heightmap.min()} / {heightmap.max()}")
    print(f"   Mean height: {heightmap.mean():.1f}")
    print(f"   Unique values: {len(np.unique(heightmap)):,}")
    
    # Create simplified visualization with 3 key plots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('BeamNG Small Island', fontsize=16, color='gray', weight='bold')
    
    # 1. Heightmap
    im1 = axes[0].imshow(heightmap, cmap='terrain', aspect='equal', origin='lower')
    axes[0].set_title('Heightmap', fontsize=12, weight='bold')
    axes[0].set_xlabel('X (East)')
    axes[0].set_ylabel('Y (North)')
    plt.colorbar(im1, ax=axes[0], label='Height Value')
    
    # 2. Materials/Layermap visualization
    if layermap is not None:
        # Create a custom colormap for materials
        import matplotlib.colors as mcolors
        n_materials = len(materials)
        colors = plt.cm.Set3(np.linspace(0, 1, n_materials))
        material_cmap = mcolors.ListedColormap(colors)
        
        im2 = axes[1].imshow(layermap, cmap=material_cmap, aspect='equal', origin='lower', vmin=0, vmax=n_materials-1)
        axes[1].set_title('Material Layers', fontsize=12, weight='bold')
        axes[1].set_xlabel('X (East)')
        axes[1].set_ylabel('Y (North)')
        
        # Create custom colorbar with material names
        cbar2 = plt.colorbar(im2, ax=axes[1], label='Material ID')
        if len(materials) <= 11:  # Only show labels if reasonable number
            cbar2.set_ticks(range(len(materials)))
            cbar2.set_ticklabels([f"{i}: {mat[:8]}" for i, mat in enumerate(materials)])
        
        # Show material statistics
        unique_mats, counts = np.unique(layermap, return_counts=True)
        print("\n🎨 Material Distribution:")
        for mat_id, count in zip(unique_mats, counts):
            if mat_id < len(materials):
                percentage = count / layermap.size * 100
                print(f"   {materials[mat_id]}: {percentage:.1f}%")
    else:
        axes[1].text(0.5, 0.5, 'No Layermap\nData Available', 
                      transform=axes[1].transAxes, ha='center', va='center',
                      fontsize=14, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        axes[1].set_title('Material Distribution\n(Not Available)', fontsize=12)
    
    # 3. Terrain steepness
    grad_y, grad_x = np.gradient(heightmap.astype(np.float32))
    gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    
    # Use a more dramatic colormap and scale
    im3 = axes[2].imshow(gradient_magnitude, cmap='plasma', aspect='equal', origin='lower')
    axes[2].set_title('Terrain Steepness', fontsize=12, weight='bold')
    axes[2].set_xlabel('X (East)')
    axes[2].set_ylabel('Y (North)')
    plt.colorbar(im3, ax=axes[2], label='Gradient')
    
    # Add dramatic color scaling
    gradient_99th = np.percentile(gradient_magnitude, 99)
    im3.set_clim(0, gradient_99th)  # Clip to 99th percentile for more dramatic contrast
    
    plt.tight_layout()

    # Save visualization
    output_file = "terrain_visualization.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"📊 Visualization saved to: {output_file}")
    
    plt.show()
    
    # Check for realistic terrain features
    water_threshold = np.percentile(heightmap, 10)
    land_areas = heightmap > water_threshold
    water_areas = heightmap <= water_threshold
    
    print("\n🌊 Terrain Features:")
    print(f"   Water threshold: {water_threshold:.0f}")
    print(f"   Land area: {np.sum(land_areas)/heightmap.size*100:.1f}%")
    print(f"   Water/low areas: {np.sum(water_areas)/heightmap.size*100:.1f}%")
    print(f"   Highest point: {heightmap.max()}")
    print(f"   Elevation range: {heightmap.max() - heightmap.min()}")

if __name__ == "__main__":
    visualize_corrected_terrain() 
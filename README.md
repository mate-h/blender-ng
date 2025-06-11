# BeamNG.drive Blender Importer/Exporter

A comprehensive Blender addon for importing and exporting BeamNG.drive level data, featuring **16-bit EXR displacement terrain import** for high-quality, non-destructive terrain workflows.

## 🌟 Features

### ✅ **Current (Phase 2)**
- **🏞️ EXR Terrain Import** - Import BeamNG `.ter` terrain files as 16-bit EXR displacement textures
- **⚡ Real-time Preview** - Live viewport displacement preview with subdivision surfaces  
- **🎛️ Configurable Parameters** - Adjustable terrain scale, displacement strength, and subdivision levels
- **🔧 Non-destructive Workflow** - Displacement-based approach preserves original heightmap data
- **📁 Level Detection** - Automatic BeamNG level directory validation
- **🎨 Material System** - Automated terrain material setup with proper displacement nodes

### 🔄 **Coming Soon**
- **Static Objects Import** - Prefab objects and meshes from `.prefab` files
- **Texture Pipeline** - DDS texture conversion and material assignment
- **Export Functionality** - Export Blender scenes back to BeamNG format
- **Advanced Materials** - Multi-layer terrain textures and blending

## 📦 Installation

### Automatic Install (Recommended)
```bash
# Clone repository
git clone https://github.com/yourusername/beamng-blender-addon.git
cd beamng-blender-addon

# Run installation script
chmod +x quick_install.sh
./quick_install.sh
```

### Manual Install
1. Download or clone this repository
2. Copy `beamng_blender_addon/` to your Blender addons directory:
   - **macOS**: `~/Library/Application Support/Blender/4.x/scripts/addons/`
   - **Windows**: `%APPDATA%/Blender Foundation/Blender/4.x/scripts/addons/`
   - **Linux**: `~/.config/blender/4.x/scripts/addons/`
3. Open Blender > Edit > Preferences > Add-ons
4. Search for "BeamNG" and enable the addon

## 🚀 Usage

### EXR Terrain Import Workflow

1. **Open Import Dialog**
   - Go to `File > Import > BeamNG Level`
   - Navigate to your BeamNG level directory (contains `.ter` and `.terrain.json`)

2. **Configure Terrain Settings** (in BeamNG panel)
   - **Terrain Scale**: Overall size multiplier (default: 1.0)
   - **Displacement Strength**: Height variation intensity (try 50-200 for realistic results)
   - **Subdivision Levels**: Detail level (6+ recommended, 8+ for high detail)

3. **Import Terrain**
   - Enable "Import Terrain" option
   - Click "Import BeamNG Level"

4. **Optimize Viewport** (for performance)
   - Switch to "Material Preview" or "Rendered" viewport shading
   - Lower subdivision levels for initial testing

### Expected Results
- Creates `BeamNG_Terrain` object with subdivision surface modifier
- Generates `BeamNG_Terrain_Displacement.exr` texture (16-bit precision)
- Applies green terrain material with displacement nodes
- Real-time viewport preview of terrain displacement

## 📋 Requirements

- **Blender 4.0+** (tested with 4.3)
- **Python 3.9+** with NumPy
- **BeamNG.drive** (for test data)

## 🗂️ Supported File Formats

### ✅ Currently Supported
- **`.ter`** - Binary terrain heightmaps (with corrected parser)
- **`.terrain.json`** - Terrain configuration metadata
- **Level Detection** - `info.json`, `mainLevel.lua`

### 🔄 Planned Support
- **`.prefab`** - TorqueScript object definitions
- **`.dds`** - DirectDraw Surface textures
- **`.json`** - Various configuration files
- **`.dae`** - Collada mesh files

## 🏗️ Technical Details

### EXR Displacement Pipeline
1. **Parse `.ter` files** using corrected binary format (offset 2048, big-endian)
2. **Normalize heightmap** to 0-1 range for displacement
3. **Create 16-bit EXR texture** with RGBA channels (R=G=B=height, A=1)
4. **Generate base plane** with subdivision surface modifier
5. **Apply displacement material** with image texture and displacement nodes

### Performance Considerations
- **Subdivision Level 6**: ~4K triangles (good for preview)
- **Subdivision Level 8**: ~65K triangles (high detail, may be slow)
- **Subdivision Level 10**: ~1M triangles (production quality, GPU required)

## 🧪 Testing with BeamNG Levels

### Test Data Locations
```bash
# Default BeamNG installation (Steam)
Windows: "Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/levels/"
macOS: "/Volumes/Goodboy/crossover/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/levels/"

# Example levels to test:
- small_island      # 1024x1024 island terrain
- gridmap_v2        # Flat grid for testing
- automation        # Complex multi-biome terrain
```

### Test Workflow
1. Navigate to a level directory (e.g., `small_island/`)
2. Ensure both `.ter` and `.terrain.json` files exist
3. Import with displacement settings:
   - Scale: 1.0
   - Displacement: 100-200
   - Subdivision: 6-7
4. Verify terrain appears with proper island shape and elevation

## 📈 Development Status

**Completed Tasks (12/67)**:
- ✅ **Phase 1**: Foundation & addon structure
- ✅ **Phase 2**: Terrain parsing & EXR displacement
- 🔄 **Phase 3**: Static objects import (next)

See [BeamNG_Blender_Task_Breakdown.md](BeamNG_Blender_Task_Breakdown.md) for detailed progress.

## 🐛 Known Issues

- High subdivision levels may cause viewport lag
- Displacement strength requires manual adjustment per terrain
- Layer map texture blending not yet implemented
- Some terrain edge artifacts in complex landscapes

## 🔧 Development & Debugging

### Hot-Reload Addon During Development

When developing or debugging the addon, you can hot-reload it without restarting Blender:

1. **Open Blender's Scripting Workspace**
2. **Paste this code snippet** into the text editor:

```python
def reload_addon(module_name='beamng_blender_addon'):
    import sys
    modules_to_remove = [name for name in sys.modules.keys() if name.startswith(module_name)]
    for module_name in modules_to_remove:
        del sys.modules[module_name]
    
    # Now disable and re-enable
    import addon_utils
    addon_utils.disable(module_name)
    addon_utils.enable(module_name)
    
reload_addon()
```

3. **Run the script** - This will completely reload the addon with your latest changes
4. **Alternative**: You can also run this one-liner in the Python console:
   ```python
   exec("import sys; [sys.modules.pop(k) for k in [k for k in sys.modules.keys() if k.startswith('beamng_blender_addon')]]; import addon_utils; addon_utils.disable('beamng_blender_addon'); addon_utils.enable('beamng_blender_addon')")
   ```

This method cleans the Python module cache and forces a complete reload, which is more reliable than the standard disable/enable approach for complex multi-module addons.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under Unlicense - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- BeamNG GmbH for the amazing BeamNG.drive simulation
- Blender Foundation for the powerful 3D creation suite
- Community contributors and testers

---

For issues or questions, please open a GitHub issue. 
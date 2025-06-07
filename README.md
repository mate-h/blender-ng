# BeamNG.drive Level Importer/Exporter for Blender

A comprehensive Blender addon for importing and exporting BeamNG.drive level data, enabling level designers to work with BeamNG content in Blender's familiar environment.

## 🚀 Current Status: Phase 1 Complete

**Version**: 0.1.0 (Alpha)  
**Phase**: Foundation & Research Complete  
**Next**: Terrain Import (Phase 2)

### ✅ What's Working Now:
- ✅ Basic addon structure and registration
- ✅ Import/Export operators with file browser integration
- ✅ UI panels in 3D Viewport
- ✅ Menu integration (File > Import/Export)
- ✅ Development workflow and installation scripts
- ✅ BeamNG level detection and validation

### 🔄 What's Coming Next:
- 🔧 Terrain data parsing (.ter files)
- 🔧 Heightmap to mesh conversion
- 🔧 DDS texture conversion pipeline
- 🔧 Basic terrain materials

## 📦 Installation

### For Users (Simple Installation)

1. **Download the addon package:**
   ```bash
   git clone https://github.com/your-repo/beamng-blender-addon.git
   cd beamng-blender-addon
   python install_addon.py --package
   ```

2. **Install in Blender:**
   - Open Blender
   - Go to `Edit > Preferences > Add-ons`
   - Click `Install...` and select the generated `.zip` file
   - Search for "BeamNG" and enable the addon

### For Developers (Development Installation)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/beamng-blender-addon.git
   cd beamng-blender-addon
   ```

2. **Install for development (creates symlink for live editing):**
   ```bash
   python install_addon.py --dev
   ```

3. **Manual installation (if auto-detection fails):**
   ```bash
   # Find your Blender addon directory and specify it
   python install_addon.py --dev --target "/path/to/blender/addons/"
   ```

### Installation Options

| Command | Description |
|---------|-------------|
| `python install_addon.py` | Standard installation (copies files) |
| `python install_addon.py --dev` | Development installation (symlink for live editing) |
| `python install_addon.py --package` | Package addon as .zip for distribution |
| `python install_addon.py --target <path>` | Specify custom Blender addon directory |

## 🎯 Usage

### Accessing the Addon

1. **In the 3D Viewport:** Press `N` to open the sidebar, look for the "BeamNG" tab
2. **In the File Menu:** `File > Import > BeamNG Level` or `File > Export > BeamNG Level`

### Import BeamNG Levels

1. Click "Import Level" in the BeamNG panel or use `File > Import > BeamNG Level`
2. Navigate to a BeamNG level directory (e.g., `/BeamNG.drive/content/levels/levels/small_island/`)
3. Select any file in the level directory (the addon will detect the level automatically)
4. Configure import options:
   - ☑️ Import Terrain
   - ☑️ Import Objects  
   - ☑️ Import Materials
   - ☐ Import Lighting
5. Click "Import BeamNG Level"

### Export Blender Scenes

1. Create your level in Blender
2. Click "Export Level" in the BeamNG panel or use `File > Export > BeamNG Level`
3. Choose output directory and level name
4. Configure export options:
   - ☑️ Export Terrain
   - ☑️ Export Objects
   - ☑️ Export Materials
   - ☑️ Export Config
5. Click "Export BeamNG Level"

## 🗂️ Supported File Formats

### Import (Planned):
- ✅ **Level Detection**: `info.json`, `mainLevel.lua`, `*.ter`
- 🔧 **Terrain**: `.ter` (binary terrain data), `.terrain.json`
- 🔧 **Objects**: `.prefab` (TorqueScript format)
- 🔧 **Meshes**: `.dae` (Collada)
- 🔧 **Textures**: `.dds`, `.png`, `.jpg`
- 🔧 **Configuration**: Various `.json` files

### Export (Planned):
- 🔧 **Terrain**: `.ter` files
- 🔧 **Objects**: `.prefab` files  
- 🔧 **Configuration**: `info.json`, level structure
- 🔧 **Assets**: Mesh and texture references

## 🏗️ Project Structure

```
beamng_blender_addon/
├── __init__.py              # Main addon file with bl_info
├── operators/               # Import/Export operators
│   ├── __init__.py
│   ├── import_level.py      # Level import functionality
│   └── export_level.py      # Level export functionality
├── ui/                      # User interface panels
│   ├── __init__.py
│   └── main_panel.py        # Main UI panel
├── utils/                   # Utilities and helpers
│   ├── __init__.py
│   └── properties.py        # Addon properties
├── parsers/                 # File format parsers (future)
├── exporters/               # File format exporters (future)
└── README.md
```

## 🔧 Development

### Prerequisites

- Blender 3.0 or higher
- Python 3.9+ (included with Blender)
- BeamNG.drive (for testing exported levels)

### Development Workflow

1. **Install for development:**
   ```bash
   python install_addon.py --dev
   ```

2. **Make changes to the code**

3. **Reload addon in Blender:**
   - Disable the addon in Preferences
   - Re-enable the addon
   - Or restart Blender for major changes

### Development Tools

- **Install Script**: `install_addon.py` - Automated installation and packaging
- **Task Tracking**: See `BeamNG_Blender_Task_Breakdown.md` for detailed task list
- **Project Plan**: See `BeamNG_Blender_Importer_Plan.md` for overall project plan

### Contributing

This project follows the task breakdown in `BeamNG_Blender_Task_Breakdown.md`. Current focus areas:

1. **Phase 2: Terrain Import** (Weeks 3-4)
   - `.ter` file parsing
   - Heightmap to mesh conversion
   - DDS texture conversion

2. **Phase 3: Static Objects** (Weeks 5-6)
   - Prefab file parsing
   - Collada mesh import
   - Scene hierarchy

## 📋 Roadmap

| Phase | Timeline | Status | Description |
|-------|----------|--------|-------------|
| **Phase 1** | Weeks 1-2 | ✅ **Complete** | Foundation & Research |
| **Phase 2** | Weeks 3-4 | 🔄 **Next** | Terrain Import |
| **Phase 3** | Weeks 5-6 | ⏳ Planned | Static Objects Import |
| **Phase 4** | Weeks 7-8 | ⏳ Planned | Materials and Textures |
| **Phase 5** | Weeks 9-10 | ⏳ Planned | Level Metadata & Config |
| **Phase 6** | Weeks 11-13 | ⏳ Planned | Export Functionality |
| **Phase 7** | Weeks 14-15 | ⏳ Planned | UI & Polish |
| **Phase 8** | Weeks 16-17 | ⏳ Planned | Testing & Optimization |

## 🐛 Known Issues

- Import/Export functions are currently placeholders (Phase 1 complete)
- Terrain parsing not yet implemented (Phase 2)
- Material conversion requires `oiiotool` dependency (Phase 4)

## 📚 Documentation

- **[Project Plan](BeamNG_Blender_Importer_Plan.md)** - Comprehensive development plan
- **[Task Breakdown](BeamNG_Blender_Task_Breakdown.md)** - Detailed task list with progress tracking
- **[BeamNG Documentation](https://documentation.beamng.com/)** - Official BeamNG modding docs

## 🤝 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Development**: Check the task breakdown for current priorities
- **Testing**: Test with BeamNG levels located at: `/BeamNG.drive/content/levels/levels/`

## 📄 License

[Specify your license here]

---

**Note**: This addon is in active development. Features marked with 🔧 are planned but not yet implemented. See the task breakdown for detailed progress tracking. 
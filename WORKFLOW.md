# BeamNG ↔ Blender Complete Workflow

## 🚀 Quick Reference Guide

This document provides a condensed reference for the complete BeamNG terrain workflow.

## 📥 Import Process

### 1. Launch Import
```
File → Import → BeamNG Level (.ter, .prefab)
```

### 2. Select Level Directory
- Navigate to BeamNG level folder (contains `.ter` and `.terrain.json`)
- Examples: `small_island/`, `gridmap_v2/`, `automation/`

### 3. Import Options
- ✅ **Import Terrain** (heightmap + materials)
- ✅ **Import Objects** (prefab objects)  
- ✅ **Import Materials** (terrain materials)
- ✅ **Import DecalRoads** (road networks)

## 🎯 What Gets Imported

| Asset | Blender Object | Description |
|-------|---------------|-------------|
| Terrain heightmap | `BeamNG_Terrain` | Geometry nodes object with subdivision |
| Height data | `BeamNG_Terrain_Displacement.exr` | 16-bit displacement texture |
| Material map | `BeamNG_Terrain_Layermap.exr` | 8-bit material assignment texture |
| Roads | `DecalRoad_*` curves | Curve objects with materials + geometry nodes |
| Coordinate fix | Automatic Y-flip | BeamNG bottom-left → Blender top-left |

## 🎨 Editing in Blender

### Texture Painting Workflow
1. **Switch to Shading workspace**
2. **Select `BeamNG_Terrain` object**
3. **Open Shader Editor**
4. **Select displacement texture node**
5. **Switch to Texture Paint workspace**
6. **Paint directly on EXR texture**

### Alternative Editing Methods
- **Sculpting**: Use sculpt tools on subdivided mesh
- **Modifiers**: Add noise, displacement, other modifiers
- **Material Painting**: Edit layermap to change terrain materials
- **Geometry Nodes**: Modify terrain node group

### Real-time Preview
- Changes update automatically in viewport
- Use **Material Preview** or **Rendered** viewport shading
- All edits preserve 16-bit precision

## 📤 Export Process

### 1. Launch Export
```
File → Export → BeamNG Level
```

### 2. Export Options
- ✅ **Export Terrain** (generates `.ter` + `.terrain.json`)
- ✅ **Export Objects** (prefab objects - placeholder)
- ✅ **Export Materials** (material definitions)
- ✅ **Export Config** (level configuration files)
- **Level Name**: Set custom name

### 3. Output Files
```
your_level/
├── your_level.ter           # Binary terrain data
├── your_level.terrain.json  # Terrain configuration  
├── info.json               # Level metadata
└── art/                    # Asset directories
    ├── shapes/
    ├── terrains/
    └── skies/
```

## 🎮 Testing in BeamNG

### 1. Install Level
```bash
# Copy exported folder to BeamNG mods directory:
BeamNG.drive/mods/unpacked/levels/[your_level_name]/
```

### 2. Launch & Test
1. Start BeamNG.drive
2. Go to **Levels** menu
3. Select your custom level
4. Verify terrain matches Blender edits

## 🔄 Coordinate System

| System | Origin | Y-Axis Direction | Array Index [0][0] |
|--------|--------|------------------|-------------------|
| **BeamNG** | Bottom-left | South → North | Bottom-left corner |
| **Blender** | Top-left | Top → Bottom | Top-left corner |
| **Solution** | Y-flip on import | No export flip needed | Automatic correction |

## ⚡ Key Benefits

- **Non-destructive**: 16-bit EXR preserves all data
- **Coordinate consistent**: Automatic system conversion
- **Real-time preview**: Live feedback during editing
- **Complete pipeline**: Import → Edit → Export → Test
- **No quality loss**: Perfect round-trip workflow

## 🚨 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| No terrain object found | Check for `BeamNG_Terrain` in scene |
| Export fails | Ensure displacement texture exists |
| Terrain appears flat | Verify texture has height variations |
| Flipped in BeamNG | Should not occur - report as bug |
| Export dialog missing | Reload addon, check console |

## 📁 Recommended Test Levels

- **`small_island`** - 1024×1024 varied terrain (best for testing)
- **`gridmap_v2`** - Flat grid (coordinate system testing)
- **`automation`** - Complex multi-biome terrain
- **`hirochi_raceway`** - Road-heavy (DecalRoad testing)

---

For detailed information, see the main [README.md](README.md) file.
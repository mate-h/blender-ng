# BeamNG .ter Terrain Format Documentation

## Overview

This document describes the binary format structure for BeamNG.drive `.ter` terrain files, based on reverse engineering analysis and community research from the BeamNG forums.

**Key Sources:**
- [BeamNG Forum Discussion](https://www.beamng.com/threads/edit-theterrain-ter-files-programatically.85819/)
- [BeamNG Level Template Creator](https://github.com/Grille/BeamNG_LevelTemplateCreator/blob/main/Grille.BeamNG.Lib/IO/Binary/TerrainV9Serializer.cs)
- Community reverse engineering efforts

## File Format Specification

### Header Structure

The `.ter` file begins with a 5-byte header:

| Offset | Size | Type | Description |
|--------|------|------|-------------|
| 0x00   | 1    | char | Format version number (typically 9) |
| 0x01   | 4    | uint32 (little-endian) | Terrain dimensions (size × size) |

### Data Layout

**CORRECTED**: Data starts immediately after the header at offset 0x05 (not 0x100):

```
Offset 0x000: [Header - 5 bytes]
Offset 0x005: [Heightmap Data - size×size×2 bytes]
Offset 0x005+heightmap: [Layer Map Data - size×size×1 byte]
Offset varies: [Layer Texture Map - size×size×1 byte]
Offset varies: [Additional Coverage Maps - 4×(size×size×1 byte)]
Offset varies: [Material Count - 4 bytes (int32)]
Offset varies: [Material Names - variable length strings]
```

## Data Sections

### 1. Heightmap Data

- **Offset**: Immediately after header (0x05)
- **Size**: size × size × 2 bytes (e.g., 1024×1024×2 = 2,097,152 bytes)
- **Format**: 16-bit unsigned integers, **little-endian**
- **Purpose**: Stores elevation data for terrain mesh generation
- **Range**: 0x0000 (lowest) to 0xFFFF (highest)

**Height Value Interpretation**:
- `0x0000` = Lowest terrain point
- `0xFFFF` = Highest terrain point  
- Height scaling is applied in the game engine based on terrain settings

### 2. Layer Map Data (Material Assignment)

- **Offset**: After heightmap data
- **Size**: size × size × 1 byte
- **Format**: 8-bit unsigned integers
- **Purpose**: Maps each terrain pixel to a material ID

**Special Values**:
- `0x00` = First material in materials list
- `0x01` = Second material in materials list
- `...`
- **`0xFF` (255) = HOLE in terrain** 🔥

### 3. Layer Texture Map

- **Offset**: After layer map
- **Size**: size × size × 1 byte
- **Format**: 8-bit unsigned integers
- **Purpose**: Texture blending weights or secondary material information

### 4. Additional Coverage Maps

According to reverse engineering, there are **4 additional coverage maps** after the layer texture map:

- **Count**: 4 separate maps
- **Size**: size × size × 1 byte each
- **Purpose**: Unknown, possibly related to:
  - Vegetation coverage
  - Detail object placement (flowers, rocks, etc.)
  - Ambient occlusion or lighting data
  - Terrain detail masks

### 5. Material Count and Names

- **Material Count**: 4 bytes (int32, little-endian)
- **Material Names**: Variable-length strings with length prefixes
  - Each string is prefixed by its length (1 byte)
  - Strings are null-terminated ASCII
  - Example: `[0x05]"Grass"[0x00][0x04]"Rock"[0x00]`

## Terrain Holes Detection

**Critical Finding**: Terrain holes are created by setting the layer map value to `0xFF` (255).

```python
def detect_holes(layermap):
    """Detect holes in BeamNG terrain"""
    hole_mask = layermap == 255
    hole_positions = np.where(hole_mask)
    return hole_mask, hole_positions
```

## Configuration File (.terrain.json)

The JSON file provides metadata and format description:

```json
{
  "binaryFormat": "version(char), size(unsigned int), heightMap(heightMapSize * heightMapItemSize), layerMap(layerMapSize * layerMapItemSize), layerTextureMap(layerMapSize * layerMapItemSize), materialNames",
  "datafile": "/levels/small_island/small_island.ter",
  "heightMapItemSize": 2,
  "heightMapSize": 1048576,
  "layerMapItemSize": 1,
  "layerMapSize": 1048576,
  "materials": ["Grass", "dirt_grass", "BeachSand", "rock_desert"],
  "size": 1024,
  "version": 9
}
```

## Key Corrections from Original Analysis

### ❌ Previous Incorrect Information:
- Data starts at offset 0x100 (256 bytes)
- 251 bytes of padding after header
- Big-endian encoding for heightmap
- No information about terrain holes

### ✅ Corrected Information:
- Data starts at offset 0x05 (immediately after header)
- No padding between header and data
- Little-endian encoding for all data
- Layer map value 0xFF (255) creates terrain holes
- Additional coverage maps present

## Implementation Notes

### Reading Terrain Data

```python
def read_beamng_terrain(ter_file, json_config):
    with open(ter_file, 'rb') as f:
        # Read header
        version = struct.unpack('B', f.read(1))[0]
        size = struct.unpack('<I', f.read(4))[0]  # Little-endian
        
        # Read heightmap (little-endian)
        heightmap_bytes = size * size * 2
        heightmap_data = f.read(heightmap_bytes)
        heights = struct.unpack(f'<{len(heightmap_data)//2}H', heightmap_data)
        heightmap = np.array(heights).reshape((size, size))
        
        # Read layer map
        layermap_data = f.read(size * size)
        layermap = np.array(struct.unpack(f'{size*size}B', layermap_data)).reshape((size, size))
        
        # Detect holes
        holes = layermap == 255
        
        return heightmap, layermap, holes
```

### Hole Processing for Blender

```python
def process_terrain_holes(heightmap, layermap):
    """Process terrain holes for Blender mesh generation"""
    hole_mask = layermap == 255
    
    # Option 1: Set hole areas to minimum height
    processed_heightmap = heightmap.copy()
    processed_heightmap[hole_mask] = 0
    
    # Option 2: Create separate hole geometry
    hole_positions = np.where(hole_mask)
    
    return processed_heightmap, hole_positions
```

## File Format Summary

Based on community reverse engineering:

1. **Header**: Version (1 byte) + Size (4 bytes, little-endian)
2. **Heightmap**: 16-bit little-endian height values
3. **Layer Map**: 8-bit material IDs (255 = hole)
4. **Layer Texture Map**: 8-bit texture blending data
5. **Coverage Maps**: 4× additional coverage data layers
6. **Materials**: Count + length-prefixed strings

## References

- [BeamNG Forum: Edit theTerrain.ter files programatically?](https://www.beamng.com/threads/edit-theterrain-ter-files-programatically.85819/)
- [BeamNG Level Template Creator Repository](https://github.com/Grille/BeamNG_LevelTemplateCreator/)
- Community contributions from emlodnaor, unyxium, and others

## Version History

- **v1.0**: Initial analysis with incorrect offset assumptions
- **v2.0**: Corrected format based on community research
  - Fixed data offset: 0x100 → 0x05
  - Fixed endianness: big → little
  - Added hole detection: layer map value 255
  - Added coverage maps documentation 
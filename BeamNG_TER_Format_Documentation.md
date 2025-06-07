# BeamNG .ter Terrain Format Documentation

## Overview

This document describes the binary format structure for BeamNG.drive `.ter` terrain files, based on reverse engineering analysis of the `small_island.ter` file.

## File Format Specification

### Header Structure

The `.ter` file begins with a 5-byte header:

| Offset | Size | Type | Description |
|--------|------|------|-------------|
| 0x00   | 1    | char | Format version number |
| 0x01   | 4    | uint32 (little-endian) | Terrain dimensions (size × size) |

### Data Layout

After the header, there's padding until offset 0x100 (256 bytes), where the actual terrain data begins:

```
Offset 0x000: [Header - 5 bytes]
Offset 0x005: [Padding - 251 bytes of zeros]
Offset 0x100: [Heightmap Data - 2,097,152 bytes]
Offset 0x200100: [Layer Map Data - ~1,048,441 bytes*]
Offset 0x300000+: [Texture Map Data - variable*]
Offset EOF: [Material Names - null-terminated strings*]
```

**Note**: The layer map and texture map sections appear to be shorter than expected based on the JSON specification, suggesting the format may vary or contain additional compression/optimization.

## Data Sections

### 1. Heightmap Data

- **Size**: 2,097,152 bytes (1024 × 1024 × 2 bytes)
- **Format**: 16-bit unsigned integers, little-endian
- **Purpose**: Stores elevation data for terrain mesh generation

**Analyzed Values for small_island.ter**:
- Height range: 0 - 65,531 (16-bit range)
- Mean height: 33,064.62
- Standard deviation: 18,882.54
- Unique height values: 52,919 out of 1,048,576 possible

**Coordinate System**:
- Array index `[y][x]` where `y` is row (north-south) and `x` is column (east-west)
- Height values likely represent elevation in BeamNG units (meters)

### 2. Layer Map Data

- **Expected Size**: 1,048,576 bytes (1024 × 1024 × 1 byte)
- **Actual Size**: ~1,048,441 bytes (135 bytes short)
- **Format**: 8-bit unsigned integers
- **Purpose**: Maps each terrain pixel to a material ID from the materials list

### 3. Texture Map Data

- **Expected Size**: 1,048,576 bytes (1024 × 1024 × 1 byte)  
- **Actual Size**: 0 bytes (not present in small_island.ter)
- **Format**: 8-bit unsigned integers
- **Purpose**: Texture blending weights or additional material information

### 4. Material Names

- **Format**: Null-terminated ASCII strings
- **Location**: End of file
- **Status**: Not present in small_island.ter (uses JSON material list instead)

## Configuration File (.terrain.json)

Each `.ter` file has an accompanying `.terrain.json` file that provides metadata:

```json
{
  "binaryFormat": "version(char), size(unsigned int), heightMap(...), layerMap(...), layerTextureMap(...), materialNames",
  "datafile": "/levels/small_island/small_island.ter",
  "heightMapItemSize": 2,
  "heightMapSize": 1048576,
  "layerMapItemSize": 1,
  "layerMapSize": 1048576,
  "materials": ["Grass", "dirt_grass", "BeachSand", ...],
  "size": 1024,
  "version": 9
}
```

## Coordinate System and Scaling

- **Grid Size**: 1024 × 1024 heightmap points
- **World Coordinates**: Each heightmap point represents a specific world coordinate
- **Height Scaling**: 16-bit values likely map to world elevation units
- **Material Resolution**: Same resolution as heightmap (1:1 mapping)

## Implementation Notes for Blender Import

### Heightmap to Mesh Conversion

1. **Read heightmap data** as 1024×1024 array of 16-bit values
2. **Create mesh vertices** at regular intervals based on world scale
3. **Set Z-coordinates** from heightmap values (may need scaling factor)
4. **Generate faces** using standard grid tessellation

### Material Assignment

1. **Read layer map** to get material ID per vertex/face
2. **Map material IDs** to material names from JSON config
3. **Create Blender materials** for each unique material
4. **Assign face materials** based on layer map data

### Terrain Scaling

The relationship between heightmap values and world coordinates needs to be determined:
- Test with known BeamNG level dimensions
- Compare with other level files for scaling patterns
- Check for scale factors in other BeamNG configuration files

## File Format Variations

Based on analysis, the actual `.ter` format may vary from the JSON specification:

1. **Padding**: 251 bytes of padding between header and data
2. **Shortened sections**: Layer map shorter than expected
3. **Missing sections**: Texture map and material names not present
4. **Alternative storage**: Materials defined in JSON instead of binary

## Next Steps for Implementation

1. **Create Python parser** based on this specification
2. **Test with multiple terrain files** to validate format consistency  
3. **Implement Blender mesh generation** from heightmap data
4. **Add material system** using layer map and JSON configuration
5. **Handle file format variations** and error cases

## Analysis Tools

The analysis was performed using:
- `ter_format_analyzer.py`: Python script for binary analysis
- `hexdump`: For examining raw binary structure
- `numpy`: For statistical analysis of heightmap data

## File Size Analysis

**small_island.ter breakdown**:
- Total file size: 3,145,849 bytes
- Header: 5 bytes
- Padding: 251 bytes  
- Heightmap: 2,097,152 bytes (exact)
- Layer map: ~1,048,441 bytes (135 bytes short)
- Texture map: 0 bytes (missing)
- Material names: 0 bytes (in JSON instead)

This suggests the format may be optimized or compressed in ways not described by the JSON specification string. 
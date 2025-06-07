# BeamNG.drive Level Data Importer/Exporter for Blender - Development Plan

## Project Overview

This project aims to create a comprehensive Blender plugin that can import and export BeamNG.drive level data, enabling level designers to work with BeamNG content in Blender's familiar environment.

## Analysis of BeamNG Level Structure

Based on exploration of the `small_island` test level, BeamNG levels contain:

### File Types Identified:
- **Terrain Files**: `.ter` (binary terrain data), `.terrain.json` (terrain configuration)
- **Texture Files**: `.dds` (DirectDraw Surface), `.png` (standard images)
- **Prefab Files**: `.prefab` (scene objects and configurations)
- **JSON Files**: Various `.json` files for metadata, decals, forest brushes
- **Lua Scripts**: `.lua` for level logic and behavior
- **Preview Images**: `.jpg` and `.png` for level previews and minimaps

### Directory Structure:

Test data location:
```
/Volumes/Goodboy/crossover/Steam/drive_c/Program Files (x86)/Steam/steamapps/common/BeamNG.drive/content/levels/levels/small_island
```

```
levels/small_island/
├── art/
│   ├── cubemaps/      # Environmental lighting
│   ├── decals/        # Road markings, textures
│   ├── forest/        # Vegetation assets
│   ├── lights/        # Lighting objects
│   ├── prefabs/       # Reusable scene objects
│   ├── road/          # Road meshes and materials
│   ├── shapes/        # 3D models (.dae files)
│   ├── skies/         # Skybox textures
│   ├── terrains/      # Terrain textures and materials
│   └── water/         # Water materials and effects
├── forest/            # Forest/vegetation placement data
├── main/              # Main level data
├── quickrace/         # Race-specific configurations
├── *.prefab           # Scene object definitions
├── *.json             # Various configuration files
├── *.lua              # Level scripts
└── *.ter              # Binary terrain data
```

## Development Plan - Phase Breakdown

### Phase 1: Foundation & Research (Weeks 1-2)
**Goal**: Establish project structure and understand file formats

#### Tasks:
1. **Set up Blender addon structure**
   - Create proper `__init__.py` with addon metadata
   - Set up UI panels and operators
   - Implement basic menu integration

2. **Research and document file formats**
   - Reverse engineer `.ter` terrain format
   - Understand `.prefab` structure (TorqueScript-based)
   - Document `.dds` texture handling requirements
   - Analyze JSON schema for various configuration files

3. **Set up development environment**
   - Create test data directory structure
   - Set up version control
   - Create utilities for file format conversion

#### Deliverables:
- Working Blender addon skeleton
- Documentation of key file formats
- Basic project structure

### Phase 2: Terrain Import (Weeks 3-4)
**Goal**: Import BeamNG terrain data into Blender

#### Tasks:
1. **Terrain Data Parser**
   - Create `.ter` file reader
   - Parse terrain heightmaps and dimensions
   - Handle terrain texture blending information

2. **Terrain Mesh Generation**
   - Generate Blender mesh from heightmap data
   - Apply proper scaling and positioning
   - Create terrain material nodes

3. **Terrain Texture Handling**
   - Implement `.dds` to Blender texture conversion using `oiiotool`
   - Set up material nodes for terrain textures
   - Handle texture blending and layering

#### Tools Required:
- `oiiotool` for DDS conversion
- Python struct module for binary data parsing
- Blender Python API for mesh creation

#### Deliverables:
- Terrain importer that creates Blender terrain mesh
- Texture conversion pipeline
- Basic terrain materials

### Phase 3: Static Objects Import (Weeks 5-6)
**Goal**: Import prefab objects and static meshes

#### Tasks:
1. **Prefab Parser**
   - Parse TorqueScript `.prefab` files
   - Extract object positions, rotations, scales
   - Identify mesh references and materials

2. **Mesh Import**
   - Import `.dae` (Collada) files referenced in prefabs
   - Handle mesh positioning and transformation
   - Apply materials and textures

3. **Scene Hierarchy**
   - Create proper Blender object hierarchy
   - Group objects by prefab or type
   - Maintain BeamNG naming conventions

#### Deliverables:
- Prefab parser and object importer
- Mesh import pipeline
- Hierarchical scene organization

### Phase 4: Materials and Textures (Weeks 7-8)
**Goal**: Comprehensive material and texture support

#### Tasks:
1. **Material System**
   - Create BeamNG-compatible material nodes
   - Handle diffuse, normal, specular maps
   - Implement material property mapping

2. **Texture Pipeline Enhancement**
   - Batch texture conversion from DDS
   - Automatic texture path resolution
   - Texture compression and optimization

3. **Skybox Import**
   - Import skybox textures from `/art/skies/`
   - Create Blender world shader nodes
   - Handle HDR and cubemap textures

#### Deliverables:
- Complete material import system
- Automated texture processing
- Skybox support

### Phase 5: Level Metadata and Configuration (Weeks 9-10)
**Goal**: Handle level configuration and metadata

#### Tasks:
1. **Level Info Import**
   - Parse `info.json` for level metadata
   - Import spawn points and their configurations
   - Handle level preview images

2. **Decals and Forest Data**
   - Import decal placement from `.decals.json`
   - Process forest brush data from `.forestbrushes.json`
   - Create Blender representation of vegetation

3. **Lighting and Environment**
   - Import light objects from prefabs
   - Set up environment lighting
   - Handle time-of-day configurations

#### Deliverables:
- Level metadata integration
- Decal and vegetation import
- Environmental lighting setup

### Phase 6: Export Functionality (Weeks 11-13)
**Goal**: Export Blender scenes back to BeamNG format

#### Tasks:
1. **Terrain Export**
   - Convert Blender terrain mesh to `.ter` format
   - Generate heightmaps from mesh data
   - Export terrain texture assignments

2. **Prefab Export**
   - Generate `.prefab` files from Blender objects
   - Maintain object hierarchy and properties
   - Export mesh references and materials

3. **Configuration Export**
   - Generate `info.json` from level metadata
   - Export modified textures and materials
   - Update file references and paths

#### Deliverables:
- Bidirectional import/export workflow
- Level package creation
- Configuration file generation

### Phase 7: User Interface and Polish (Weeks 14-15)
**Goal**: Create intuitive user interface and polish features

#### Tasks:
1. **UI Enhancement**
   - Create comprehensive import/export dialogs
   - Add progress indicators and logging
   - Implement batch processing options

2. **Validation and Error Handling**
   - Validate file formats and data integrity
   - Provide meaningful error messages
   - Handle edge cases and corrupted data

3. **Documentation and Examples**
   - Create user manual and tutorials
   - Provide example workflows
   - Document API for extensibility

#### Deliverables:
- Polished user interface
- Comprehensive error handling
- Complete documentation

### Phase 8: Testing and Optimization (Weeks 16-17)
**Goal**: Thorough testing and performance optimization

#### Tasks:
1. **Comprehensive Testing**
   - Test with multiple BeamNG levels
   - Validate import/export accuracy
   - Performance benchmarking

2. **Optimization**
   - Optimize mesh processing algorithms
   - Improve texture conversion speed
   - Memory usage optimization

3. **Integration Testing**
   - Test exported levels in BeamNG
   - Validate game compatibility
   - Fix any conversion issues

#### Deliverables:
- Tested and optimized plugin
- Performance benchmarks
- Compatibility validation

## Technical Requirements

### Dependencies:
- **Python Libraries**:
  - `struct` - Binary data parsing
  - `json` - JSON file handling
  - `xml.etree.ElementTree` - XML parsing for DAE files
  - `PIL/Pillow` - Image processing
  - `numpy` - Numerical operations

- **External Tools**:
  - `oiiotool` - DDS texture conversion
  - `blender` - Blender Python API

### Development Tools:
- **IDE**: VS Code with Python and Blender extensions
- **Version Control**: Git
- **Testing**: Blender's testing framework
- **Documentation**: Markdown and Sphinx

## File Format Priorities

### High Priority (Essential):
1. `.ter` - Terrain data (binary format)
2. `.prefab` - Scene objects (TorqueScript)
3. `.dds` - Texture files
4. `.json` - Configuration files
5. `.dae` - 3D meshes (Collada)

### Medium Priority (Important):
1. `.lua` - Level scripts
2. `.png/.jpg` - Standard images
3. Forest and decal data files

### Low Priority (Nice to have):
1. Audio files
2. Physics data
3. Advanced lighting configurations

## Success Metrics

1. **Functionality**: Successfully import and export a complete BeamNG level
2. **Accuracy**: Exported levels run correctly in BeamNG
3. **Performance**: Handle large levels within reasonable time limits
4. **Usability**: Intuitive interface for level designers
5. **Compatibility**: Support for multiple BeamNG level formats

## Risk Assessment

### High Risk:
- **File Format Complexity**: BeamNG formats may be more complex than initially assessed
- **Binary Data Parsing**: `.ter` format may require reverse engineering

### Medium Risk:
- **Performance**: Large levels may cause memory/performance issues
- **Compatibility**: BeamNG version compatibility across different game versions

### Low Risk:
- **UI Development**: Blender UI system is well-documented
- **Texture Conversion**: `oiiotool` is proven for DDS handling

## Conclusion

This plan provides a structured approach to developing a comprehensive BeamNG.drive level importer/exporter for Blender. The phased approach allows for iterative development and testing, ensuring each component works correctly before building upon it.

The project will significantly enhance the level design workflow for BeamNG.drive by leveraging Blender's powerful modeling and editing capabilities while maintaining compatibility with the game's native formats. 
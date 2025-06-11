# BeamNG.drive Blender Importer - Updated Task Breakdown

## Project Status Overview
- **Total Tasks**: 89
- **Completed**: 12 
- **In Progress**: 1
- **Not Started**: 76

## Recent Achievements ✅
- **Terrain Import**: Successfully implemented complete terrain import with EXR displacement
- **Layermap Support**: Fixed layermap texture creation with proper material ID preservation
- **Height Scale Discovery**: Found terrain `heightScale` parameter in terrain preset files
- **Package Structure Analysis**: Identified zip-based level distribution system

## New Priority: Complete Level Package Import 🔴

BeamNG levels are distributed as zip files containing:
- Terrain data (`.ter` + `.terrain.json`)
- Art assets (`/art/` directory with textures, models, materials)
- Prefab objects (`.prefab` files)
- Configuration files (`info.json`, various `.json` configs)
- Lua scripts (`mainLevel.lua`)
- Preview images and minimaps

## Legend
- 🔴 **High Priority** - Critical path items
- 🟡 **Medium Priority** - Important but not blocking
- 🟢 **Low Priority** - Nice to have features
- ⏳ **Not Started**
- 🔄 **In Progress**  
- ✅ **Completed**
- 🚫 **Blocked**

---

## Phase 0: Enhanced Package Import System (NEW - Weeks 1-3)

### 0.1 Zip Package Handler 🔴
- [ ] **Task 0.1.1**: Implement zip file browser and extraction ⏳
  - **Effort**: 2 days
  - **Dependencies**: None
  - **Deliverable**: File browser that can select and extract BeamNG level zips
  - **Details**: Handle `/content/levels/*.zip` files, extract to temp directory

- [ ] **Task 0.1.2**: Parse level package structure validation ⏳
  - **Effort**: 1 day
  - **Dependencies**: Task 0.1.1
  - **Deliverable**: Package validation system
  - **Details**: Verify required files exist (info.json, .ter, .terrain.json)

- [ ] **Task 0.1.3**: Implement temp directory management ⏳
  - **Effort**: 1 day
  - **Dependencies**: Task 0.1.1
  - **Deliverable**: Safe temp file handling with cleanup
  - **Details**: Extract zips to temp dirs, clean up on completion/error

### 0.2 Level Metadata Parser 🔴
- [ ] **Task 0.2.1**: Parse info.json for level metadata ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 0.1.2
  - **Deliverable**: Level info parser with spawn points, size, etc.
  - **Details**: Extract title, description, spawn points, size, country, biome

- [ ] **Task 0.2.2**: Parse terrain preset for height scale ⏳
  - **Effort**: 1 day
  - **Dependencies**: Task 0.2.1
  - **Deliverable**: Automatic height scale detection
  - **Details**: Read `*terrainPreset.json` files for `heightScale` parameter

- [ ] **Task 0.2.3**: Extract and organize asset references ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 0.2.1
  - **Deliverable**: Asset dependency map
  - **Details**: Map all texture/model/prefab references for import prioritization

### 0.3 Enhanced Terrain Import 🔴
- [x] **Task 0.3.1**: Integrate automatic height scale detection ✅
  - **Effort**: 0.5 days
  - **Dependencies**: Task 0.2.2, Completed terrain import
  - **Deliverable**: Terrain import with correct height scaling
  - **Details**: Use heightScale from terrain preset instead of hardcoded values

- [ ] **Task 0.3.2**: Implement terrain positioning from preset ⏳
  - **Effort**: 1 day
  - **Dependencies**: Task 0.3.1
  - **Deliverable**: Correctly positioned terrain mesh
  - **Details**: Use pos.x, pos.y, pos.z from terrain preset for terrain placement

- [ ] **Task 0.3.3**: Enhanced terrain material with opacity maps ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 0.3.2
  - **Deliverable**: Multi-layer terrain materials using opacity maps
  - **Details**: Import and use opacity maps from terrain preset for material blending

---

## Phase 1: Foundation & Research (UPDATED - Weeks 4-5)

### 1.1 Blender Addon Structure 🔴
- [x] **Task 1.1.1**: Create basic addon directory structure ✅
- [x] **Task 1.1.2**: Implement `__init__.py` with addon metadata ✅
- [x] **Task 1.1.3**: Create basic UI panel structure ✅
- [x] **Task 1.1.4**: Implement basic menu integration ✅

### 1.2 Asset Pipeline Research 🔴
- [x] **Task 1.2.1**: Analyze `.ter` terrain format structure ✅
- [ ] **Task 1.2.2**: Document `.prefab` TorqueScript structure ⏳
  - **Updated Priority**: Now HIGH - needed for complete level import
- [ ] **Task 1.2.3**: Research DDS texture pipeline with oiiotool 🔄
  - **Effort**: 2 days
  - **Dependencies**: None
  - **Deliverable**: DDS → EXR/PNG conversion workflow
- [ ] **Task 1.2.4**: Analyze DAE model import requirements ⏳
  - **Effort**: 2 days
  - **Dependencies**: None
  - **Deliverable**: Collada import pipeline documentation

### 1.3 Development Environment 🟡
- [x] **Task 1.3.1**: Set up version control and project structure ✅
- [ ] **Task 1.3.2**: Create comprehensive test level collection ⏳
  - **Effort**: 1 day
  - **Dependencies**: Task 0.1.1
  - **Deliverable**: Test suite with multiple level zips
- [ ] **Task 1.3.3**: Set up automated testing framework ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 1.3.2
  - **Deliverable**: Automated import testing system

---

## Phase 2: Complete Asset Import Pipeline (UPDATED - Weeks 6-8)

### 2.1 Texture Asset Pipeline 🔴
- [ ] **Task 2.1.1**: Implement DDS to EXR conversion ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 1.2.3
  - **Deliverable**: DDS texture converter using oiiotool
  - **Details**: Convert `/art/terrains/` textures to Blender-compatible formats

- [ ] **Task 2.1.2**: Batch texture processing from art directory ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 2.1.1
  - **Deliverable**: Automated texture import from `/art/` directories
  - **Details**: Process textures from terrains/, decals/, skies/, etc.

- [ ] **Task 2.1.3**: Texture organization and naming system ⏳
  - **Effort**: 1 day
  - **Dependencies**: Task 2.1.2
  - **Deliverable**: Organized texture library in Blender
  - **Details**: Maintain BeamNG naming conventions and directory structure

### 2.2 Enhanced Terrain System 🔴
- [x] **Task 2.2.1**: Complete terrain import with EXR displacement ✅
- [x] **Task 2.2.2**: Layermap texture creation with material IDs ✅
- [x] **Task 2.2.3**: Terrain material node group ✅
- [ ] **Task 2.2.4**: Multi-layer terrain material system ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 2.1.1, Task 0.3.3
  - **Deliverable**: Complete terrain material with all texture layers
  - **Details**: Use opacity maps for proper material blending

### 2.3 3D Model Import 🔴
- [ ] **Task 2.3.1**: DAE (Collada) model importer ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 1.2.4
  - **Deliverable**: Import models from `/art/shapes/` directory
  - **Details**: Handle mesh data, UV mapping, material assignments

- [ ] **Task 2.3.2**: Model material assignment system ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 2.3.1, Task 2.1.1
  - **Deliverable**: Automatic material assignment to imported models
  - **Details**: Link DDS textures to model materials

- [ ] **Task 2.3.3**: Model positioning and hierarchy ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 2.3.2
  - **Deliverable**: Organized model hierarchy in Blender scene
  - **Details**: Create logical object grouping and naming

---

## Phase 3: Prefab and Scene Object System (UPDATED - Weeks 9-11)

### 3.1 Prefab Parser 🔴
- [ ] **Task 3.1.1**: TorqueScript prefab parser ⏳
  - **Effort**: 5 days
  - **Dependencies**: Task 1.2.2
  - **Deliverable**: Complete prefab file parser
  - **Details**: Parse object definitions, transforms, properties, materials

- [ ] **Task 3.1.2**: Object transform extraction and conversion ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 3.1.1
  - **Deliverable**: BeamNG to Blender coordinate system conversion
  - **Details**: Handle position, rotation, scale transformations

- [ ] **Task 3.1.3**: Material and texture reference resolution ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 3.1.2, Task 2.1.1
  - **Deliverable**: Automatic material assignment from prefab data
  - **Details**: Link prefab material references to imported textures

### 3.2 Scene Construction 🔴
- [ ] **Task 3.2.1**: Prefab object instantiation system ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 3.1.3, Task 2.3.1
  - **Deliverable**: Create Blender objects from prefab definitions
  - **Details**: Instance models with correct transforms and materials

- [ ] **Task 3.2.2**: Scene hierarchy organization ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 3.2.1
  - **Deliverable**: Logical scene organization with collections
  - **Details**: Group by prefab type, material, or function

- [ ] **Task 3.2.3**: Spawn point creation ⏳
  - **Effort**: 1 day
  - **Dependencies**: Task 0.2.1
  - **Deliverable**: Spawn point objects with metadata
  - **Details**: Create spawn points from info.json with preview images

### 3.3 Advanced Scene Elements 🟡
- [ ] **Task 3.3.1**: Decal system import ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 3.2.1
  - **Deliverable**: Road markings and decal placement
  - **Details**: Import from `*.decals.json` files

- [ ] **Task 3.3.2**: Forest/vegetation system ⏳
  - **Effort**: 4 days
  - **Dependencies**: Task 3.2.1
  - **Deliverable**: Tree and vegetation placement
  - **Details**: Import from `*.forestbrushes*.json` files

- [ ] **Task 3.3.3**: Lighting system import ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 3.2.1
  - **Deliverable**: Scene lighting from prefab light objects
  - **Details**: Convert BeamNG lights to Blender light objects

---

## Phase 4: Advanced Materials and Shading (UPDATED - Weeks 12-13)

### 4.1 Material System Enhancement 🔴
- [ ] **Task 4.1.1**: Advanced material node groups ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 2.1.1
  - **Deliverable**: BeamNG-style material templates
  - **Details**: Create node groups for different BeamNG material types

- [ ] **Task 4.1.2**: PBR material conversion ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 4.1.1
  - **Deliverable**: Convert BeamNG materials to PBR workflow
  - **Details**: Handle diffuse, normal, specular, roughness maps

- [ ] **Task 4.1.3**: Material library system ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 4.1.2
  - **Deliverable**: Reusable material library
  - **Details**: Create library of common BeamNG materials

### 4.2 Skybox and Environment 🟡
- [ ] **Task 4.2.1**: Skybox import from art/skies ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 2.1.1
  - **Deliverable**: World shader with BeamNG skybox
  - **Details**: Import and convert skybox textures

- [ ] **Task 4.2.2**: Environment lighting setup ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 4.2.1
  - **Deliverable**: Realistic environment lighting
  - **Details**: Set up world lighting to match BeamNG

- [ ] **Task 4.2.3**: Atmospheric effects ⏳
  - **Effort**: 1 day
  - **Dependencies**: Task 4.2.2
  - **Deliverable**: Fog, haze, and atmospheric effects
  - **Details**: Recreate BeamNG atmospheric conditions

---

## Phase 5: User Interface and Workflow (UPDATED - Weeks 14-15)

### 5.1 Enhanced Import UI 🔴
- [ ] **Task 5.1.1**: Zip file browser with preview ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 0.1.1
  - **Deliverable**: Level selection UI with previews and metadata
  - **Details**: Show level info, size, preview images before import

- [ ] **Task 5.1.2**: Import options panel ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 5.1.1
  - **Deliverable**: Granular import control
  - **Details**: Toggle terrain, objects, materials, vegetation, etc.

- [ ] **Task 5.1.3**: Progress tracking and logging ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 5.1.2
  - **Deliverable**: Real-time import progress with detailed logging
  - **Details**: Show progress bars, current operation, estimated time

### 5.2 Level Management 🟡
- [ ] **Task 5.2.1**: Level browser and manager ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 5.1.1
  - **Deliverable**: Manage multiple imported levels
  - **Details**: Switch between levels, manage level data

- [ ] **Task 5.2.2**: Asset inspector and editor ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 5.2.1
  - **Deliverable**: Inspect and modify imported assets
  - **Details**: Material editor, object properties, etc.

### 5.3 Error Handling and Validation 🟡
- [ ] **Task 5.3.1**: Comprehensive error handling system ⏳
  - **Effort**: 2 days
  - **Dependencies**: All import tasks
  - **Deliverable**: Robust error handling with recovery
  - **Details**: Handle missing files, corrupted data, format changes

- [ ] **Task 5.3.2**: Import validation and reporting ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 5.3.1
  - **Deliverable**: Validation report with warnings and errors
  - **Details**: Check imported data integrity and completeness

---

## Phase 6: Export and Roundtrip (Weeks 16-18)

### 6.1 Level Export System 🟡
- [ ] **Task 6.1.1**: Terrain export to .ter format ⏳
  - **Effort**: 4 days
  - **Dependencies**: Completed terrain import
  - **Deliverable**: Export modified terrain back to BeamNG format

- [ ] **Task 6.1.2**: Prefab export system ⏳
  - **Effort**: 5 days
  - **Dependencies**: Task 3.1.1
  - **Deliverable**: Generate prefab files from Blender objects

- [ ] **Task 6.1.3**: Asset export pipeline ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 6.1.2
  - **Deliverable**: Export textures and models to BeamNG formats

### 6.2 Package Generation 🟡
- [ ] **Task 6.2.1**: Level package builder ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 6.1.3
  - **Deliverable**: Generate complete level zip packages

- [ ] **Task 6.2.2**: Metadata generation ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 6.2.1
  - **Deliverable**: Generate info.json and configuration files

---

## Phase 7: Testing and Optimization (Weeks 19-20)

### 7.1 Comprehensive Testing 🔴
- [ ] **Task 7.1.1**: Multi-level import testing ⏳
  - **Effort**: 4 days
  - **Dependencies**: All import functionality
  - **Deliverable**: Test with all available BeamNG levels

- [ ] **Task 7.1.2**: Performance optimization ⏳
  - **Effort**: 3 days
  - **Dependencies**: Task 7.1.1
  - **Deliverable**: Optimized import/export performance

- [ ] **Task 7.1.3**: Memory usage optimization ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 7.1.2
  - **Deliverable**: Reduced memory footprint for large levels

### 7.2 BeamNG Integration Testing 🔴
- [ ] **Task 7.2.1**: Exported level validation in BeamNG ⏳
  - **Effort**: 3 days
  - **Dependencies**: All export functionality
  - **Deliverable**: Verify exported levels work in BeamNG

- [ ] **Task 7.2.2**: Roundtrip testing ⏳
  - **Effort**: 2 days
  - **Dependencies**: Task 7.2.1
  - **Deliverable**: Import → Edit → Export → Test workflow validation

---

## Critical Path for Complete Level Import 🔴

### Immediate Priority (Phase 0):
1. **Task 0.1.1**: Zip package handler
2. **Task 0.2.1**: Level metadata parser  
3. **Task 0.2.2**: Height scale detection
4. **Task 0.3.1**: Enhanced terrain import

### Short-term Goals (4 weeks):
1. **Task 1.2.3**: DDS texture pipeline
2. **Task 2.1.1**: DDS to EXR conversion
3. **Task 2.3.1**: DAE model import
4. **Task 3.1.1**: Prefab parser

### Medium-term Goals (8 weeks):
1. **Task 3.2.1**: Complete scene construction
2. **Task 4.1.1**: Material system
3. **Task 5.1.1**: Enhanced UI

## New Feature Highlights

### 🆕 Complete Level Package Import
- **Zip file browser**: Select any BeamNG level zip
- **Automatic extraction**: Safe temp directory handling
- **Metadata parsing**: Level info, spawn points, dimensions
- **Height scale detection**: Automatic terrain scaling

### 🆕 Enhanced Terrain System  
- **Multi-layer materials**: Full opacity map support
- **Correct positioning**: Use terrain preset coordinates
- **Material blending**: Proper layer mixing

### 🆕 Asset Pipeline
- **Batch texture processing**: Convert all DDS textures
- **Model import**: DAE files with materials
- **Organized hierarchy**: Logical scene organization

### 🆕 Advanced Features
- **Decal system**: Road markings and surface details  
- **Vegetation**: Tree and plant placement
- **Lighting**: Scene lighting from BeamNG data
- **Spawn points**: Player spawn locations

## Success Metrics (Updated)

1. **Package Import**: Successfully import any BeamNG level zip file
2. **Complete Scenes**: Terrain + objects + materials + lighting
3. **Performance**: Handle large levels (1-3GB) in reasonable time
4. **Accuracy**: Visual fidelity matching original BeamNG levels
5. **Usability**: One-click import from zip to complete Blender scene
6. **Compatibility**: Support for all major BeamNG level formats

## Technical Requirements (Updated)

### New Dependencies:
- **oiiotool**: DDS texture conversion to EXR/PNG
- **zipfile**: Python built-in for zip handling
- **tempfile**: Secure temporary file management
- **lxml**: Enhanced XML parsing for DAE files

### Performance Targets:
- **Small levels** (< 500MB): < 2 minutes import time
- **Medium levels** (500MB-1GB): < 5 minutes import time  
- **Large levels** (1-3GB): < 15 minutes import time
- **Memory usage**: < 4GB RAM for largest levels

This updated plan provides a comprehensive roadmap for importing complete BeamNG level packages, building on our successful terrain import foundation. 
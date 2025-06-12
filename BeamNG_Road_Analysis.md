# BeamNG Road Data Analysis & NURBS Import Implementation

## Overview
This document analyzes the BeamNG road data structure found in level files and outlines the implementation plan for importing roads as NURBS curves in Blender. Based on research, BeamNG uses a layered road system with collision terrain and visual decals, similar to other automotive simulation platforms.

## BeamNG Road System Architecture

### Road System Components
BeamNG's road system consists of multiple layers:

1. **Base Terrain Mesh**: Smooth collision surface with roads "carved out"
2. **DecalRoad Objects**: Visual road surfaces rendered as decals (no collision)
3. **Road Architect**: World Editor tool for creating roads with edit/render modes
4. **DecalRoad Editor**: Tool for managing road decal properties

### Road Creation Workflow
Roads in BeamNG are created using the [Road Architect](https://documentation.beamng.com/world_editor/tools/road_architect/disk_options/) in the World Editor, which has:
- **Edit Mode**: For designing road geometry and properties
- **Render Mode**: Generates DecalRoad objects in the scene tree for runtime rendering
- **Export Functionality**: Can export road data to JSON format (available in consumer BeamNG versions)

The [DecalRoad Editor](https://documentation.beamng.com/world_editor/tools/decalroad_editor/) manages the visual properties of these road decals.

### Road Architect Export Format
The Road Architect can export road data to JSON format with structure:
```json
{
  "data": {
    "groups": [
      {
        "name": "Urban Block - Single1",
        "roads": [
          {
            "bridgeArch": 1,
            "bridgeDepth": 0.5,
            "bridgeWidth": 5,
            "displayName": "Joined Road",
            "extraE": 2,
            "extraS": 2,
            "forceField": 1,
            "granFactor": 1,
            "groupIdx": [1],
            "isAllowTunnels": false,
            "isArc": false,
            "isBridge": false,
            // ... additional properties
          }
        ]
      }
    ]
  }
}
```

This format contains higher-level road design parameters compared to the final DecalRoad objects.

## BeamNG Road Data Structure

### File Location
Roads are stored in: `levels/{level_name}/main/MissionGroup/roads/items.level.json`

### Road Object Structure
Each road is a JSON object with the `DecalRoad` class containing:

```json
{
  "class": "DecalRoad",
  "persistentId": "unique-uuid",
  "__parent": "roads",
  "position": [x, y, z],
  "improvedSpline": true,
  "material": "material_name",
  "nodes": [[x1, y1, z1, width1], [x2, y2, z2, width2], ...],
  "startEndFade": [start_fade, end_fade],
  "textureLength": number,
  "breakAngle": number (optional),
  "distanceFade": [distance, fade] (optional),
  "renderPriority": number (optional),
  "overObjects": boolean (optional),
  "useTemplate": "true" (optional)
}
```

### Key Properties

#### Essential Properties
- **`nodes`**: Array of control points defining the road path
  - Format: `[x, y, z, width]` for each node
  - These are the actual spline control points
  - Width determines road width at each point

- **`position`**: Base position `[x, y, z]` (usually matches first node)

- **`material`**: Road surface material name
  - Examples: `"utah_asphalt_road_dirt_edge"`, `"Dirt_road_variation_03"`, `"m_sand_variation"`

#### Spline Properties
- **`improvedSpline`**: Boolean indicating enhanced spline interpolation
- **`breakAngle`**: Controls spline smoothness at sharp turns
- **`textureLength`**: UV mapping scale for road texture

#### Visual Properties
- **`startEndFade`**: `[start, end]` fade distances for road endpoints
- **`distanceFade`**: `[distance, fade]` for LOD distance fading
- **`renderPriority`**: Rendering order (higher = rendered on top)
- **`overObjects`**: Whether road renders over other objects

### Road Types by Material
1. **Asphalt Roads**: `AsphaltRoad_variation_*`, `utah_asphalt_road_*`
2. **Dirt Roads**: `Dirt_road_variation_*`, `DirtRoad_variation_*`
3. **Sand Paths**: `m_sand_variation`
4. **Tire Tracks**: `dirt_tiretracks`, `tread_marks_damaged_*`
5. **Erosion/Natural**: `bank_erosion`

## NURBS Curve Import Implementation Plan

### 1. Data Parsing
```python
def parse_road_data(road_json):
    """Extract road information from BeamNG JSON data"""
    return {
        'name': road_json.get('name', road_json['persistentId']),
        'nodes': road_json['nodes'],
        'material': road_json['material'],
        'width_profile': [node[3] for node in road_json['nodes']],
        'properties': {
            'improved_spline': road_json.get('improvedSpline', False),
            'break_angle': road_json.get('breakAngle', 0),
            'texture_length': road_json.get('textureLength', 1),
            'render_priority': road_json.get('renderPriority', 0)
        }
    }
```

### 2. NURBS Curve Creation
```python
def create_nurbs_curve_from_road(road_data, world_scale=1.0):
    """Create NURBS curve from BeamNG road data"""
    
    # Create new curve object
    curve_data = bpy.data.curves.new(road_data['name'], type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 12  # Smooth curve resolution
    
    # Create spline
    spline = curve_data.splines.new('NURBS')
    spline.points.add(len(road_data['nodes']) - 1)  # -1 because one point exists by default
    
    # Set control points
    for i, node in enumerate(road_data['nodes']):
        x, y, z, width = node
        # Apply world scale and coordinate conversion
        spline.points[i].co = (x * world_scale, y * world_scale, z * world_scale, 1.0)
    
    # Configure spline properties
    if road_data['properties']['improved_spline']:
        spline.use_smooth = True
    
    # Create curve object
    curve_obj = bpy.data.objects.new(road_data['name'], curve_data)
    bpy.context.collection.objects.link(curve_obj)
    
    return curve_obj
```

### 3. Road Width Profile
BeamNG roads have variable width along their length. This can be implemented using:

#### Option A: Curve Bevel Object
```python
def create_width_profile_curve(width_profile):
    """Create a curve representing the width profile"""
    profile_curve = bpy.data.curves.new('width_profile', type='CURVE')
    profile_curve.dimensions = '2D'
    
    spline = profile_curve.splines.new('NURBS')
    spline.points.add(len(width_profile) - 1)
    
    for i, width in enumerate(width_profile):
        # Create profile points along curve length
        u = i / (len(width_profile) - 1)  # 0 to 1
        spline.points[i].co = (u, width/2, 0, 1.0)  # Half width for radius
    
    return profile_curve
```

#### Option B: Custom Properties for Width
```python
def add_width_data_to_curve(curve_obj, width_profile):
    """Add width data as custom properties"""
    curve_obj["beamng_width_profile"] = width_profile
    curve_obj["beamng_road_type"] = "variable_width"
```

### 4. Material Assignment
```python
def assign_road_material(curve_obj, material_name):
    """Assign or create material based on BeamNG material name"""
    
    # Material mapping
    material_mapping = {
        'utah_asphalt_road_dirt_edge': 'Asphalt_Road',
        'Dirt_road_variation_03': 'Dirt_Road',
        'm_sand_variation': 'Sand_Path',
        'dirt_tiretracks': 'Tire_Tracks',
        'bank_erosion': 'Natural_Erosion'
    }
    
    blender_material_name = material_mapping.get(material_name, 'Default_Road')
    
    # Create or get material
    if blender_material_name not in bpy.data.materials:
        material = bpy.data.materials.new(name=blender_material_name)
        material.use_nodes = True
        # Configure material nodes based on road type
        setup_road_material_nodes(material, material_name)
    else:
        material = bpy.data.materials[blender_material_name]
    
    # Assign to curve
    if curve_obj.data.materials:
        curve_obj.data.materials[0] = material
    else:
        curve_obj.data.materials.append(material)
```

### 5. Integration with Level Importer
```python
def import_roads_from_level(level_path, world_scale=1.0):
    """Import all roads from BeamNG level"""
    
    roads_file = os.path.join(level_path, "main", "MissionGroup", "roads", "items.level.json")
    
    if not os.path.exists(roads_file):
        print("No roads file found")
        return []
    
    # Parse roads JSON
    with open(roads_file, 'r') as f:
        content = f.read()
        # Split by lines and parse each JSON object
        road_objects = []
        for line in content.strip().split('\n'):
            if line.strip():
                try:
                    road_data = json.loads(line)
                    if road_data.get('class') == 'DecalRoad':
                        road_objects.append(road_data)
                except json.JSONDecodeError:
                    continue
    
    # Create NURBS curves for each road
    imported_roads = []
    for road_json in road_objects:
        road_data = parse_road_data(road_json)
        curve_obj = create_nurbs_curve_from_road(road_data, world_scale)
        assign_road_material(curve_obj, road_data['material'])
        imported_roads.append(curve_obj)
    
    return imported_roads
```

## Related Projects & Standards

### Existing OpenDRIVE Blender Integration
The [Blender Driving Scenario Creator](https://github.com/johschmitz/blender-driving-scenario-creator) addon provides:
- OpenDRIVE and OpenSCENARIO support for automotive scenarios
- NURBS curve-based road creation and editing
- Export to various 3D formats (FBX, glTF, OSGB)
- Integration with automotive simulation tools (CARLA, esmini)

This existing project demonstrates proven approaches for:
- Road geometry representation using NURBS curves
- Automotive-standard file format support
- Integration with simulation platforms

### Potential Integration Opportunities
Our BeamNG road import could complement the existing addon by:
- Importing real-world road data from BeamNG levels
- Converting to OpenDRIVE-compatible format
- Leveraging existing NURBS curve infrastructure

## Implementation Considerations

### Road System Understanding
- **DecalRoad vs. Collision**: DecalRoad objects are visual-only, actual collision is handled by carved terrain
- **Generation Pipeline**: Roads may be generated from Road Architect data, not hand-authored
- **Layered Approach**: Visual and collision geometry are separate systems

### Coordinate System
- BeamNG uses a different coordinate system than Blender
- May need coordinate transformation: `(x, -z, y)` or similar
- World scale factor should be applied consistently

### Performance
- Large levels can have hundreds of roads
- Consider grouping roads by material type
- Option to import only main roads vs. all detail roads

### User Options
- **Import All Roads**: Import every DecalRoad object
- **Filter by Material**: Only import specific road types
- **Minimum Width Filter**: Skip very narrow tire tracks
- **Render Priority Filter**: Only import roads above certain priority
- **OpenDRIVE Export**: Option to export imported roads as OpenDRIVE format

### Road Hierarchy
- Group roads in collections by type:
  - "Main Roads" (asphalt, major dirt roads)
  - "Paths" (narrow dirt paths, sand tracks)
  - "Details" (tire tracks, erosion marks)

### Future Enhancements
1. **Road Mesh Generation**: Convert NURBS to mesh with proper width
2. **Intersection Detection**: Identify and mark road intersections
3. **Road Network Analysis**: Build connectivity graph
4. **Procedural Road Materials**: Generate materials based on BeamNG material names
5. **Animation Support**: Import road-based camera paths for cinematics
6. **OpenDRIVE Integration**: Export BeamNG roads to OpenDRIVE format for automotive tools
7. **Road Architect Import**: Import Road Architect JSON data for higher-level road parameters
8. **Collision Mesh Import**: Import the carved terrain collision mesh alongside visual roads
9. **Dual Import Support**: Support both Road Architect JSON and DecalRoad object import
10. **Format Conversion**: Convert between Road Architect, DecalRoad, and OpenDRIVE formats

## Example Usage
```python
# In the level import operator
def execute(self, context):
    # ... existing terrain import code ...
    
    # Import roads as NURBS curves
    if self.import_roads:
        self.report({'INFO'}, "Importing roads as NURBS curves...")
        imported_roads = import_roads_from_level(self.level_path, world_scale)
        self.report({'INFO'}, f"Imported {len(imported_roads)} roads")
    
    return {'FINISHED'}
```

## Research Questions & Next Steps

### DecalRoad Generation Investigation ✅ CONFIRMED
Key findings from investigation:

1. **Source Data**: ✅ DecalRoad objects ARE generated from Road Architect data when switching to render mode
2. **Generation Process**: ✅ Road Architect → Render Mode → DecalRoad objects appear in scene tree
3. **Export Capability**: ✅ Road Architect can export JSON data (consumer BeamNG versions)
4. **Data Formats**: Road Architect JSON ≠ OpenDRIVE format (different structure and properties)

### Road Architect vs DecalRoad Data
- **Road Architect JSON**: High-level design parameters (bridge settings, display options, grouping)
- **DecalRoad Objects**: Low-level rendering data (nodes, materials, spline properties)
- **Conversion Process**: Road Architect generates DecalRoad objects for runtime rendering

### BeamNG Versions & Access
- **Consumer BeamNG**: Available on Steam, includes Road Architect with export functionality
- **BeamNG.tech**: Professional/enterprise version for automotive industry
  - Enhanced simulation capabilities
  - Advanced development tools
  - Commercial licensing
  - Contact BeamNG directly for access: [BeamNG.tech website](https://www.beamng.tech/)

### Investigation Approach
1. ✅ **Compare Road Architect and DecalRoad data structures**
2. ✅ **Analyze BeamNG World Editor export process** 
3. ✅ **Test road creation workflow in BeamNG World Editor**
4. 🔄 **Document the Road Architect → DecalRoad conversion pipeline** (in progress)

### Integration with Automotive Standards
- **OpenDRIVE Compatibility**: Ensure imported roads can be exported to OpenDRIVE
- **Road Architect vs OpenDRIVE**: Road Architect JSON format is NOT OpenDRIVE (different structure)
- **Format Bridging**: Need conversion layer between BeamNG formats and OpenDRIVE
- **Simulation Tool Support**: Test compatibility with CARLA, esmini, and other simulators
- **Standard Compliance**: Follow automotive industry road representation standards

### Data Import Strategy
Given the confirmed Road Architect → DecalRoad pipeline:

1. **Primary Import**: DecalRoad objects (available in all BeamNG levels)
2. **Enhanced Import**: Road Architect JSON (when available, provides design intent)
3. **Hybrid Approach**: Combine both data sources for complete road information
4. **Format Conversion**: Convert to OpenDRIVE-compatible format for automotive workflows

This implementation will provide a solid foundation for importing BeamNG roads as NURBS curves, preserving their geometric properties and enabling further processing in Blender. The integration with existing OpenDRIVE tools opens possibilities for automotive simulation workflows. 
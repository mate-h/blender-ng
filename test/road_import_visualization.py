#!/usr/bin/env python3
"""
BeamNG Road Import Visualization Script
Imports DecalRoad data from BeamNG level files and creates NURBS curves in Blender
"""

import bpy
import json
import os

# Clear existing mesh objects
def clear_scene():
    """Clear existing curve objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

def parse_road_data(road_json):
    """Extract road information from BeamNG JSON data"""
    return {
        'name': road_json.get('name', f"road_{road_json['persistentId'][:8]}"),
        'persistent_id': road_json['persistentId'],
        'nodes': road_json['nodes'],
        'material': road_json['material'],
        'width_profile': [node[3] for node in road_json['nodes']],
        'properties': {
            'improved_spline': road_json.get('improvedSpline', False),
            'break_angle': road_json.get('breakAngle', 0),
            'texture_length': road_json.get('textureLength', 1),
            'render_priority': road_json.get('renderPriority', 0),
            'start_end_fade': road_json.get('startEndFade', [5, 5]),
            'distance_fade': road_json.get('distanceFade', None),
            'over_objects': road_json.get('overObjects', False)
        }
    }

def create_nurbs_curve_from_road(road_data, world_scale=1.0, coordinate_transform=True):
    """Create NURBS curve from BeamNG road data"""
    
    # Create new curve object
    curve_data = bpy.data.curves.new(road_data['name'], type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 12  # Smooth curve resolution
    
    # Create spline
    spline = curve_data.splines.new('NURBS')
    spline.points.add(len(road_data['nodes']) - 1)  # -1 because one point exists by default
    
    # Set control points with coordinate transformation
    for i, node in enumerate(road_data['nodes']):
        x, y, z, width = node
        
        # Apply coordinate transformation (BeamNG to Blender)
        if coordinate_transform:
            # BeamNG: X=forward, Y=left, Z=up -> Blender: X=right, Y=forward, Z=up
            blender_x = -y * world_scale  # BeamNG Y becomes negative Blender X
            blender_y = x * world_scale   # BeamNG X becomes Blender Y
            blender_z = z * world_scale   # BeamNG Z stays Blender Z
        else:
            blender_x = x * world_scale
            blender_y = y * world_scale
            blender_z = z * world_scale
        
        spline.points[i].co = (blender_x, blender_y, blender_z, 1.0)
    
    # Configure spline properties
    if road_data['properties']['improved_spline']:
        spline.use_smooth = True
    
    # Set spline type based on break angle
    if road_data['properties']['break_angle'] > 0:
        spline.type = 'POLY'  # Use POLY for sharp corners
    else:
        spline.type = 'NURBS'  # Use NURBS for smooth curves
    
    # Create curve object
    curve_obj = bpy.data.objects.new(road_data['name'], curve_data)
    bpy.context.collection.objects.link(curve_obj)
    
    # Add custom properties for road data
    curve_obj["beamng_material"] = road_data['material']
    curve_obj["beamng_width_profile"] = road_data['width_profile']
    curve_obj["beamng_persistent_id"] = road_data['persistent_id']
    curve_obj["beamng_render_priority"] = road_data['properties']['render_priority']
    curve_obj["beamng_texture_length"] = road_data['properties']['texture_length']
    
    return curve_obj

def get_material_color(material_name):
    """Get color for road material visualization"""
    material_colors = {
        # Asphalt roads - dark grays
        'AsphaltRoad_variation_01': (0.15, 0.15, 0.15, 1.0),
        'AsphaltRoad_variation_03': (0.12, 0.12, 0.12, 1.0),
        'utah_asphalt_road_dirt_edge': (0.2, 0.18, 0.15, 1.0),
        'utah_asphalt_road_dirt_wide_edge': (0.18, 0.16, 0.13, 1.0),
        
        # Dirt roads - browns
        'Dirt_road_variation_03': (0.4, 0.25, 0.15, 1.0),
        'DirtRoad_variation_03': (0.35, 0.22, 0.12, 1.0),
        
        # Sand paths - yellows
        'm_sand_variation': (0.8, 0.7, 0.4, 1.0),
        
        # Tire tracks - darker browns
        'dirt_tiretracks': (0.3, 0.2, 0.1, 1.0),
        'tread_marks_damaged_02': (0.25, 0.15, 0.08, 1.0),
        'tread_marks_damaged_03': (0.22, 0.13, 0.07, 1.0),
        
        # Erosion/natural - greens
        'bank_erosion': (0.3, 0.4, 0.2, 1.0),
    }
    
    # Default to gray if material not found
    return material_colors.get(material_name, (0.5, 0.5, 0.5, 1.0))

def assign_road_material(curve_obj, material_name):
    """Assign or create material based on BeamNG material name"""
    
    # Create material name for Blender
    blender_material_name = f"BeamNG_{material_name}"
    
    # Create or get material
    if blender_material_name not in bpy.data.materials:
        material = bpy.data.materials.new(name=blender_material_name)
        material.use_nodes = True
        
        # Get material color
        color = get_material_color(material_name)
        
        # Set up material nodes
        bsdf = material.node_tree.nodes["Principled BSDF"]
        bsdf.inputs[0].default_value = color  # Base Color
        bsdf.inputs[7].default_value = 0.8    # Roughness
        
        # Add emission for better visibility
        bsdf.inputs[17].default_value = color[:3] + (1.0,)  # Emission
        bsdf.inputs[18].default_value = 0.1  # Emission Strength
        
    else:
        material = bpy.data.materials[blender_material_name]
    
    # Assign to curve
    if curve_obj.data.materials:
        curve_obj.data.materials[0] = material
    else:
        curve_obj.data.materials.append(material)

def organize_roads_in_collections(roads_by_type):
    """Organize imported roads into collections by type"""
    
    # Create main collection
    main_collection = bpy.data.collections.new("BeamNG Roads")
    bpy.context.scene.collection.children.link(main_collection)
    
    for road_type, roads in roads_by_type.items():
        if not roads:
            continue
            
        # Create sub-collection for this road type
        type_collection = bpy.data.collections.new(f"Roads - {road_type}")
        main_collection.children.link(type_collection)
        
        # Move roads to appropriate collection
        for road_obj in roads:
            # Remove from scene collection
            bpy.context.scene.collection.objects.unlink(road_obj)
            # Add to type collection
            type_collection.objects.link(road_obj)

def import_roads_from_level(level_path, world_scale=0.1, coordinate_transform=True, filter_materials=None):
    """Import all roads from BeamNG level"""
    
    roads_file = os.path.join(level_path, "main", "MissionGroup", "roads", "items.level.json")
    
    if not os.path.exists(roads_file):
        print(f"No roads file found at: {roads_file}")
        return []
    
    print(f"Reading roads from: {roads_file}")
    
    # Parse roads JSON (each line is a separate JSON object)
    road_objects = []
    with open(roads_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                road_data = json.loads(line)
                if road_data.get('class') == 'DecalRoad':
                    # Filter by material if specified
                    if filter_materials and road_data.get('material') not in filter_materials:
                        continue
                    road_objects.append(road_data)
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    print(f"Found {len(road_objects)} DecalRoad objects")
    
    # Categorize roads by material type
    roads_by_type = {
        'Main Roads': [],
        'Dirt Roads': [],
        'Sand Paths': [],
        'Tire Tracks': [],
        'Natural Features': []
    }
    
    # Create curves for each road
    imported_roads = []
    for road_json in road_objects:
        road_data = parse_road_data(road_json)
        
        # Skip roads with too few nodes
        if len(road_data['nodes']) < 2:
            print(f"Skipping road {road_data['name']} - not enough nodes")
            continue
        
        curve_obj = create_nurbs_curve_from_road(road_data, world_scale, coordinate_transform)
        assign_road_material(curve_obj, road_data['material'])
        
        # Categorize road
        material = road_data['material']
        if 'asphalt' in material.lower() or 'AsphaltRoad' in material:
            roads_by_type['Main Roads'].append(curve_obj)
        elif 'dirt' in material.lower() or 'Dirt' in material:
            roads_by_type['Dirt Roads'].append(curve_obj)
        elif 'sand' in material.lower() or 'm_sand' in material:
            roads_by_type['Sand Paths'].append(curve_obj)
        elif 'track' in material.lower() or 'tread' in material:
            roads_by_type['Tire Tracks'].append(curve_obj)
        elif 'erosion' in material.lower() or 'bank' in material:
            roads_by_type['Natural Features'].append(curve_obj)
        else:
            roads_by_type['Main Roads'].append(curve_obj)  # Default
        
        imported_roads.append(curve_obj)
    
    # Organize in collections
    organize_roads_in_collections(roads_by_type)
    
    # Print summary
    print(f"\nImported {len(imported_roads)} roads:")
    for road_type, roads in roads_by_type.items():
        if roads:
            print(f"  {road_type}: {len(roads)} roads")
    
    return imported_roads

def main():
    """Main function to run the road import"""
    
    # Level path (using symlink in test folder)
    level_path = os.path.join(os.path.dirname(__file__), "small_island")
    
    if not os.path.exists(level_path):
        print(f"Level path not found: {level_path}")
        return
    
    # Clear scene
    clear_scene()
    
    # Import roads
    # Scale down by factor of 10 for better visualization (BeamNG uses large coordinates)
    # Enable coordinate transformation for proper Blender orientation
    imported_roads = import_roads_from_level(
        level_path, 
        world_scale=0.1,  # Scale down for visualization
        coordinate_transform=True,
        filter_materials=None  # Import all materials, or specify list to filter
    )
    
    print(f"Successfully imported {len(imported_roads)} road curves")
    
    # Set viewport to wireframe for better curve visibility
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'WIREFRAME'
                    break

if __name__ == "__main__":
    main() 
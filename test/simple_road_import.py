import bpy
import json
import os

# Configuration
LEVEL_PATH = "/Volumes/Goodboy/github/blend-ng/test/small_island"

def clear_scene():
    """Clear existing objects"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

def create_road_curve(road_data):
    """Create a curve from road control points"""
    name = road_data.get('name', f"road_{road_data['persistentId'][:8]}")
    nodes = road_data['nodes']
    material = road_data['material']
    
    # Create curve
    curve_data = bpy.data.curves.new(name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 12
    
    # Create spline - use appropriate type based on break angle
    break_angle = road_data.get('breakAngle', 0)
    if break_angle > 0:
        spline = curve_data.splines.new('POLY')
    else:
        spline = curve_data.splines.new('NURBS')
    
    spline.points.add(len(nodes) - 1)
    
    # Set control points with coordinate transformation
    for i, node in enumerate(nodes):
        x, y, z, width = node
        # BeamNG to Blender coordinate transformation with -90° Z rotation
        blender_x = x
        blender_y = y
        blender_z = z
        
        spline.points[i].co = (blender_x, blender_y, blender_z, 1.0)
    
    # Create object
    curve_obj = bpy.data.objects.new(name, curve_data)
    
    # Add custom properties
    curve_obj["beamng_material"] = material
    curve_obj["beamng_width_profile"] = [node[3] for node in nodes]
    curve_obj["beamng_break_angle"] = break_angle
    
    # Create material
    create_material(curve_obj, material)
    
    return curve_obj

def create_material(curve_obj, material_name):
    """Create and assign material based on road type"""
    # Material colors
    colors = {
        'AsphaltRoad_variation_01': (0.15, 0.15, 0.15, 1.0),
        'utah_asphalt_road_dirt_edge': (0.2, 0.18, 0.15, 1.0),
        'Dirt_road_variation_03': (0.4, 0.25, 0.15, 1.0),
        'm_sand_variation': (0.8, 0.7, 0.4, 1.0),
        'dirt_tiretracks': (0.3, 0.2, 0.1, 1.0),
        'bank_erosion': (0.3, 0.4, 0.2, 1.0),
    }
    
    color = colors.get(material_name, (0.5, 0.5, 0.5, 1.0))
    
    # Create material
    mat_name = f"BeamNG_{material_name}"
    if mat_name not in bpy.data.materials:
        material = bpy.data.materials.new(name=mat_name)
        material.use_nodes = True
        bsdf = material.node_tree.nodes["Principled BSDF"]
        bsdf.inputs[0].default_value = color
        bsdf.inputs[17].default_value = color[:3] + (1.0,)  # Emission
        bsdf.inputs[18].default_value = 0.1  # Emission Strength
    else:
        material = bpy.data.materials[mat_name]
    
    # Assign to curve
    curve_obj.data.materials.append(material)

def main():
    """Main import function"""
    # Clear scene
    
    # Create Roads collection
    roads_collection = bpy.data.collections.new("Roads")
    bpy.context.scene.collection.children.link(roads_collection)
    
    # Create empty object (null) at origin as parent
    roads_parent = bpy.data.objects.new("Roads_Parent", None)
    roads_parent.location = (0, 0, 0)
    roads_collection.objects.link(roads_parent)
    
    # Read roads file
    roads_file = os.path.join(LEVEL_PATH, "main", "MissionGroup", "roads", "items.level.json")
    
    if not os.path.exists(roads_file):
        print(f"Roads file not found: {roads_file}")
        return
    
    print(f"Importing roads from: {roads_file}")
    
    # Import sample roads
    roads_imported = 0
    with open(roads_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                road_data = json.loads(line)
                if road_data.get('class') == 'DecalRoad' and len(road_data.get('nodes', [])) >= 2:
                    curve_obj = create_road_curve(road_data)
                    # Add to Roads collection
                    roads_collection.objects.link(curve_obj)
                    # Parent to the empty object
                    curve_obj.parent = roads_parent
                    roads_imported += 1
                    print(f"Imported: {road_data.get('material')} road ({len(road_data['nodes'])} nodes)")
            except:
                continue
    
    print(f"Successfully imported {roads_imported} road curves")
    
    # Set wireframe view for better curve visibility
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'WIREFRAME'
                    break

# Run the import
if __name__ == "__main__":
    main() 
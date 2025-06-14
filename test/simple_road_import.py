import bpy
import json
import os

# Configuration
LEVEL_PATH = "/Volumes/Goodboy/github/blend-ng/test/small_island"

def clear_scene():
    """Clear existing objects"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.data.objects['BeamNG_Terrain'].select_set(False)
    bpy.data.objects['BeamNG_Camera'].select_set(False)
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
    spline = curve_data.splines.new('POLY')
    
    spline.points.add(len(nodes) - 1)
    
    # Set control points with coordinate transformation
    for i, node in enumerate(nodes):
        x, y, z, width = node
        # Set the control point coordinates and radius
        spline.points[i].co = (x, y, z, 1.0)  # w=1.0 for NURBS weight
        spline.points[i].radius = width  # Set the radius based on road width
    
    # Create object
    curve_obj = bpy.data.objects.new(name, curve_data)
    
    # Add custom properties
    curve_obj["beamng_material"] = material
    curve_obj["beamng_break_angle"] = road_data.get('breakAngle', 0)
    curve_obj["beamng_improved_spline"] = road_data.get('improvedSpline', True)
    
    return curve_obj

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

# Run the import
if __name__ == "__main__":
    main() 
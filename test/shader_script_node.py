# Blender Shader Editor Script Node - UV Sampler
# This script samples the nearest UV coordinates from an object in the scene
# Compatible with Blender 4.4 Script nodes

import bpy
import bmesh
from mathutils import Vector

# Main function for the script node
# You can connect these inputs to your shader node inputs
target_pos_x = 0.0  # World X position
target_pos_y = 0.0  # World Y position  
target_pos_z = 0.0  # World Z position
object_name = ""    # Object name (empty = active object)

def get_nearest_uv():
    """Sample nearest UV from object surface"""
    
    # Get target object
    if object_name.strip():
        obj = bpy.data.objects.get(object_name.strip())
    else:
        obj = bpy.context.active_object
    
    if not obj or obj.type != 'MESH':
        return 0.0, 0.0
    
    mesh = obj.data
    if not mesh.uv_layers:
        return 0.0, 0.0
    
    # Convert target position to object space
    world_pos = Vector((target_pos_x, target_pos_y, target_pos_z))
    local_pos = obj.matrix_world.inverted() @ world_pos
    
    # Find nearest vertex and face
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()
    
    # Simple nearest vertex search
    min_dist = float('inf')
    nearest_vert = None
    
    for vert in bm.verts:
        dist = (vert.co - local_pos).length
        if dist < min_dist:
            min_dist = dist
            nearest_vert = vert
    
    if not nearest_vert:
        bm.free()
        return 0.0, 0.0
    
    # Find closest face containing this vertex
    uv_layer = mesh.uv_layers.active or mesh.uv_layers[0]
    closest_face = None
    min_face_dist = float('inf')
    
    for face in nearest_vert.link_faces:
        face_center = face.calc_center_median()
        dist = (face_center - local_pos).length
        if dist < min_face_dist:
            min_face_dist = dist
            closest_face = face
    
    if not closest_face:
        bm.free()
        return 0.0, 0.0
    
    # Get UV coordinate from the closest face
    # Use the UV coordinate of the nearest vertex in that face
    result_uv = Vector((0.0, 0.0))
    min_vert_dist = float('inf')
    
    for loop in closest_face.loops:
        vert_dist = (loop.vert.co - local_pos).length
        if vert_dist < min_vert_dist:
            min_vert_dist = vert_dist
            result_uv = uv_layer.data[loop.index].uv
    
    bm.free()
    return result_uv.x, result_uv.y

# Execute and return UV coordinates
u, v = get_nearest_uv()

# These will be the outputs of your script node
# Connect them to your shader inputs
uv_u = u
uv_v = v 
import bpy
import bmesh
from mathutils import Vector, kdtree
import numpy as np

def find_nearest_uv_on_object(target_position, object_name=None):
    """
    Find the nearest UV coordinate on an object's surface to a given world position.
    
    Args:
        target_position: World space position (Vector or tuple)
        object_name: Name of the object to sample from (if None, uses active object)
    
    Returns:
        tuple: (u, v) UV coordinates of the nearest point
    """
    
    # Get the target object
    if object_name:
        obj = bpy.data.objects.get(object_name)
        if not obj:
            print(f"Object '{object_name}' not found")
            return (0.0, 0.0)
    else:
        obj = bpy.context.active_object
        if not obj:
            print("No active object found")
            return (0.0, 0.0)
    
    # Ensure the object has a mesh
    if obj.type != 'MESH':
        print(f"Object '{obj.name}' is not a mesh")
        return (0.0, 0.0)
    
    # Get mesh data
    mesh = obj.data
    
    # Check if the mesh has UV maps
    if not mesh.uv_layers:
        print(f"Object '{obj.name}' has no UV maps")
        return (0.0, 0.0)
    
    # Get the active UV layer
    uv_layer = mesh.uv_layers.active
    if not uv_layer:
        uv_layer = mesh.uv_layers[0]
    
    # Create a bmesh instance for easier manipulation
    bm = bmesh.new()
    bm.from_mesh(mesh)
    
    # Ensure face indices are valid
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()
    
    # Transform target position to object space
    target_local = obj.matrix_world.inverted() @ Vector(target_position)
    
    # Build KD-tree for fast nearest neighbor search
    kd = kdtree.KDTree(len(bm.verts))
    for i, vert in enumerate(bm.verts):
        kd.insert(vert.co, i)
    kd.balance()
    
    # Find nearest vertex
    _, nearest_vert_index, _ = kd.find(target_local)
    nearest_vert = bm.verts[nearest_vert_index]
    
    # Find the face containing this vertex that's closest to the target
    closest_face = None
    closest_distance = float('inf')
    
    for face in nearest_vert.link_faces:
        # Calculate face center
        face_center = face.calc_center_median()
        distance = (face_center - target_local).length
        
        if distance < closest_distance:
            closest_distance = distance
            closest_face = face
    
    if not closest_face:
        print("No suitable face found")
        bm.free()
        return (0.0, 0.0)
    
    # Get UV coordinates for the closest face
    uv_coords = []
    vert_coords = []
    
    for loop in closest_face.loops:
        vert_coords.append(loop.vert.co)
        # Get UV coordinate from the mesh UV layer
        uv_coord = uv_layer.data[loop.index].uv
        uv_coords.append(uv_coord)
    
    # Calculate barycentric coordinates for the target position within the face
    if len(vert_coords) >= 3:
        # Use the first 3 vertices to form a triangle
        v0, v1, v2 = vert_coords[0], vert_coords[1], vert_coords[2]
        uv0, uv1, uv2 = uv_coords[0], uv_coords[1], uv_coords[2]
        
        # Calculate barycentric coordinates
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        v0p = target_local - v0
        
        # Calculate dot products
        d00 = v0v1.dot(v0v1)
        d01 = v0v1.dot(v0v2)
        d11 = v0v2.dot(v0v2)
        d20 = v0p.dot(v0v1)
        d21 = v0p.dot(v0v2)
        
        # Calculate barycentric coordinates
        denom = d00 * d11 - d01 * d01
        if abs(denom) < 1e-8:
            # Degenerate triangle, use first UV coordinate
            result_uv = uv0
        else:
            v = (d11 * d20 - d01 * d21) / denom
            w = (d00 * d21 - d01 * d20) / denom
            u = 1.0 - v - w
            
            # Interpolate UV coordinates
            result_uv = u * uv0 + v * uv1 + w * uv2
    else:
        # Fallback to first UV coordinate
        result_uv = uv_coords[0]
    
    bm.free()
    return (result_uv.x, result_uv.y)

# Shader node script entry point
def shader_script(target_pos_x=0.0, target_pos_y=0.0, target_pos_z=0.0, object_name=""):
    """
    Entry point for the shader script node.
    
    Args:
        target_pos_x, target_pos_y, target_pos_z: World position coordinates
        object_name: Name of the object to sample UV from (empty string uses active object)
    
    Returns:
        tuple: (u, v) UV coordinates
    """
    target_position = Vector((target_pos_x, target_pos_y, target_pos_z))
    obj_name = object_name if object_name.strip() else None
    
    return find_nearest_uv_on_object(target_position, obj_name)

# For direct usage in shader nodes
if __name__ == "__main__":
    # Example usage - you can modify these values or connect them to shader inputs
    target_pos = Vector((0.0, 0.0, 0.0))  # World position to sample from
    object_name = ""  # Leave empty to use active object, or specify object name
    
    u, v = find_nearest_uv_on_object(target_pos, object_name)
    print(f"Nearest UV coordinates: ({u:.4f}, {v:.4f})") 
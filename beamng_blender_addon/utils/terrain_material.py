import bpy
import os

# Remove the global material creation - we'll create it inside the function now
# mat = bpy.data.materials.new(name = "Terrain_Material")
# mat.use_nodes = True

#initialize Terrain_Material node group
def terrain_material_node_group(material_name="Terrain_Material", texture_ao_path=None, texture_base_path=None, texture_roughness_path=None):
    """
    Create a terrain material with node setup
    
    Args:
        material_name: Name for the material
        texture_ao_path: File path to ambient occlusion texture
        texture_base_path: File path to base color texture  
        texture_roughness_path: File path to roughness texture
    """
    
    # Always create a new material - let Blender handle incremental naming (.001, .002, etc.)
    mat = bpy.data.materials.new(name=material_name)
    mat.use_nodes = True

    terrain_material = mat.node_tree
    #start with a clean node tree
    for node in terrain_material.nodes:
        terrain_material.nodes.remove(node)
    terrain_material.color_tag = 'NONE'
    terrain_material.description = ""
    terrain_material.default_group_node_width = 140
    

    #terrain_material interface

    #initialize terrain_material nodes
    #node Principled BSDF
    principled_bsdf = terrain_material.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    #Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    #IOR
    principled_bsdf.inputs[3].default_value = 1.5
    #Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    #Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    #Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    #Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    #Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    #Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    #Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    #Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    #Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    #Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    #Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    #Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    #Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    #Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    #Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    #Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    #Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    #Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    #Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    #Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    #Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    #Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    #Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    #Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    #node Material Output
    material_output = terrain_material.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    #Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Thickness
    material_output.inputs[3].default_value = 0.0

    # Helper function to load image texture
    def load_image_texture(texture_path, image_name_prefix):
        """Load an image texture from file path"""
        if texture_path and os.path.exists(texture_path):
            # Always load a new image - let Blender handle incremental naming
            # This ensures each level gets its own copy of textures even if filenames are the same
            image = bpy.data.images.load(texture_path)
            print(f"📷 Loaded texture: {image.name} from {texture_path}")
            return image
        return None

    #node Image Texture (AO)
    image_texture = terrain_material.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture AO"
    image_texture.extension = 'REPEAT'
    ao_image = load_image_texture(texture_ao_path, "ao")
    if ao_image:
        image_texture.image = ao_image
    image_texture.image_user.frame_current = 0
    image_texture.image_user.frame_duration = 100
    image_texture.image_user.frame_offset = 0
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Linear'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0

    #node Image Texture.001 (Base Color)
    image_texture_001 = terrain_material.nodes.new("ShaderNodeTexImage")
    image_texture_001.name = "Image Texture Base"
    image_texture_001.extension = 'REPEAT'
    base_image = load_image_texture(texture_base_path, "base")
    if base_image:
        image_texture_001.image = base_image
    image_texture_001.image_user.frame_current = 0
    image_texture_001.image_user.frame_duration = 100
    image_texture_001.image_user.frame_offset = 0
    image_texture_001.image_user.frame_start = 1
    image_texture_001.image_user.tile = 0
    image_texture_001.image_user.use_auto_refresh = False
    image_texture_001.image_user.use_cyclic = False
    image_texture_001.interpolation = 'Linear'
    image_texture_001.projection = 'FLAT'
    image_texture_001.projection_blend = 0.0

    #node Image Texture.002 (Roughness)
    image_texture_002 = terrain_material.nodes.new("ShaderNodeTexImage")
    image_texture_002.name = "Image Texture Roughness"
    image_texture_002.extension = 'REPEAT'
    roughness_image = load_image_texture(texture_roughness_path, "roughness")
    if roughness_image:
        image_texture_002.image = roughness_image
    image_texture_002.image_user.frame_current = 0
    image_texture_002.image_user.frame_duration = 100
    image_texture_002.image_user.frame_offset = 0
    image_texture_002.image_user.frame_start = 1
    image_texture_002.image_user.tile = 0
    image_texture_002.image_user.use_auto_refresh = False
    image_texture_002.image_user.use_cyclic = False
    image_texture_002.interpolation = 'Linear'
    image_texture_002.projection = 'FLAT'
    image_texture_002.projection_blend = 0.0

    #node Vector Math
    vector_math = terrain_material.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'MULTIPLY'

    #node Attribute
    attribute = terrain_material.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "UVMap"
    attribute.attribute_type = 'GEOMETRY'


    #Set locations
    principled_bsdf.location = (122.10936737060547, 300.0)
    material_output.location = (412.109375, 300.0)
    image_texture.location = (-358.59405517578125, 464.10614013671875)
    image_texture_001.location = (-358.59405517578125, 164.38784790039062)
    image_texture_002.location = (-358.59405517578125, -135.33038330078125)
    vector_math.location = (-64.9111328125, 405.5472412109375)
    attribute.location = (-546.8926391601562, 322.63507080078125)

    #Set dimensions
    principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
    material_output.width, material_output.height = 140.0, 100.0
    image_texture.width, image_texture.height = 243.36331176757812, 100.0
    image_texture_001.width, image_texture_001.height = 240.0, 100.0
    image_texture_002.width, image_texture_002.height = 240.0, 100.0
    vector_math.width, vector_math.height = 140.0, 100.0
    attribute.width, attribute.height = 140.0, 100.0

    #initialize terrain_material links
    #image_texture.Color -> vector_math.Vector
    terrain_material.links.new(image_texture.outputs[0], vector_math.inputs[0])
    #image_texture_001.Color -> vector_math.Vector
    terrain_material.links.new(image_texture_001.outputs[0], vector_math.inputs[1])
    #vector_math.Vector -> principled_bsdf.Base Color
    terrain_material.links.new(vector_math.outputs[0], principled_bsdf.inputs[0])
    #attribute.Vector -> image_texture.Vector
    terrain_material.links.new(attribute.outputs[1], image_texture.inputs[0])
    #attribute.Vector -> image_texture_001.Vector
    terrain_material.links.new(attribute.outputs[1], image_texture_001.inputs[0])
    #image_texture_002.Color -> principled_bsdf.Roughness
    terrain_material.links.new(image_texture_002.outputs[0], principled_bsdf.inputs[2])
    #attribute.Vector -> image_texture_002.Vector
    terrain_material.links.new(attribute.outputs[1], image_texture_002.inputs[0])
    #principled_bsdf.BSDF -> material_output.Surface
    terrain_material.links.new(principled_bsdf.outputs[0], material_output.inputs[0])

    return mat

# Remove the global creation call since we now create it inside the function
# terrain_material = terrain_material_node_group()


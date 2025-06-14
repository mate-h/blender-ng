import bpy

# mat = bpy.data.materials.new(name = "tread_marks_damaged_02")
# mat.use_nodes = True

#initialize tread_marks_damaged_02 node group
def decal_road_material_node_group(mat: bpy.types.Material) -> bpy.types.ShaderNodeTree:
    group = mat.node_tree
    #start with a clean node tree
    for node in group.nodes:
        group.nodes.remove(node)
    group.color_tag = 'NONE'
    group.description = ""
    group.default_group_node_width = 140

    #initialize tread_marks_damaged_02 nodes
    #node Principled BSDF
    principled_bsdf = group.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    #Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    #IOR
    principled_bsdf.inputs[3].default_value = 1.5
    #Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    #Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    #Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.2, 0.1)
    #Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05
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
    principled_bsdf.inputs[20].default_value = 0.03
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
    principled_bsdf.inputs[30].default_value = 1.33

    #node Attribute
    attribute = group.nodes.new("ShaderNodeAttribute")
    attribute.name = "Attribute"
    attribute.attribute_name = "UVMap"
    attribute.attribute_type = 'GEOMETRY'

    #node Vector Math
    vector_math = group.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'MULTIPLY'

    #node Image Texture
    image_texture = group.nodes.new("ShaderNodeTexImage")
    image_texture.label = "ao"
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    if "t_asphalt_damaged_01_ao.data.DDS" in bpy.data.images:
        image_texture.image = bpy.data.images["t_asphalt_damaged_01_ao.data.DDS"]
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

    #node Image Texture.001
    image_texture_001 = group.nodes.new("ShaderNodeTexImage")
    image_texture_001.label = "color"
    image_texture_001.name = "Image Texture.001"
    image_texture_001.extension = 'REPEAT'
    if "t_asphalt_damaged_01_b.color.DDS" in bpy.data.images:
        image_texture_001.image = bpy.data.images["t_asphalt_damaged_01_b.color.DDS"]
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

    #node Image Texture.002
    image_texture_002 = group.nodes.new("ShaderNodeTexImage")
    image_texture_002.label = "normal"
    image_texture_002.name = "Image Texture.002"
    image_texture_002.extension = 'REPEAT'
    if "t_asphalt_damaged_01_nm.normal.DDS" in bpy.data.images:
        image_texture_002.image = bpy.data.images["t_asphalt_damaged_01_nm.normal.DDS"]
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

    #node Image Texture.003
    image_texture_003 = group.nodes.new("ShaderNodeTexImage")
    image_texture_003.label = "opacity"
    image_texture_003.name = "Image Texture.003"
    image_texture_003.extension = 'REPEAT'
    if "t_asphalt_damaged_01_o.data.DDS" in bpy.data.images:
        image_texture_003.image = bpy.data.images["t_asphalt_damaged_01_o.data.DDS"]
    image_texture_003.image_user.frame_current = 0
    image_texture_003.image_user.frame_duration = 100
    image_texture_003.image_user.frame_offset = 0
    image_texture_003.image_user.frame_start = 1
    image_texture_003.image_user.tile = 0
    image_texture_003.image_user.use_auto_refresh = False
    image_texture_003.image_user.use_cyclic = False
    image_texture_003.interpolation = 'Linear'
    image_texture_003.projection = 'FLAT'
    image_texture_003.projection_blend = 0.0

    #node Image Texture.004
    image_texture_004 = group.nodes.new("ShaderNodeTexImage")
    image_texture_004.label = "roughness"
    image_texture_004.name = "Image Texture.004"
    image_texture_004.extension = 'REPEAT'
    if "t_asphalt_damaged_01_r.data.DDS" in bpy.data.images:
        image_texture_004.image = bpy.data.images["t_asphalt_damaged_01_r.data.DDS"]
    image_texture_004.image_user.frame_current = 0
    image_texture_004.image_user.frame_duration = 100
    image_texture_004.image_user.frame_offset = 0
    image_texture_004.image_user.frame_start = 1
    image_texture_004.image_user.tile = 0
    image_texture_004.image_user.use_auto_refresh = False
    image_texture_004.image_user.use_cyclic = False
    image_texture_004.interpolation = 'Linear'
    image_texture_004.projection = 'FLAT'
    image_texture_004.projection_blend = 0.0

    #node Mix
    mix = group.nodes.new("ShaderNodeMix")
    mix.label = "baseColorFactor"
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    #Factor_Float
    mix.inputs[0].default_value = 1.0
    #B_Color
    mix.inputs[7].default_value = (0.6446059942245483, 0.6446030139923096, 0.6445990204811096, 0.6000000238418579)

    #node Math
    math = group.nodes.new("ShaderNodeMath")
    math.label = "roughnessFactor"
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    #Value_001
    math.inputs[1].default_value = 0.8560000061988831

    #node Math.001
    math_001 = group.nodes.new("ShaderNodeMath")
    math_001.label = "opacityFactor"
    math_001.name = "Math.001"
    math_001.operation = 'MULTIPLY'
    math_001.use_clamp = False
    #Value_001
    math_001.inputs[1].default_value = 0.9010000228881836

    #node Image Texture.005
    image_texture_005 = group.nodes.new("ShaderNodeTexImage")
    image_texture_005.label = "detailNormal"
    image_texture_005.name = "Image Texture.005"
    image_texture_005.extension = 'REPEAT'
    if "t_asphalt_detail_02_nm.normal.DDS" in bpy.data.images:
        image_texture_005.image = bpy.data.images["t_asphalt_detail_02_nm.normal.DDS"]
    image_texture_005.image_user.frame_current = 0
    image_texture_005.image_user.frame_duration = 100
    image_texture_005.image_user.frame_offset = 0
    image_texture_005.image_user.frame_start = 1
    image_texture_005.image_user.tile = 0
    image_texture_005.image_user.use_auto_refresh = False
    image_texture_005.image_user.use_cyclic = False
    image_texture_005.interpolation = 'Linear'
    image_texture_005.projection = 'FLAT'
    image_texture_005.projection_blend = 0.0

    #node Vector Math.001
    vector_math_001 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_001.label = "detailScale"
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'MULTIPLY'
    #Vector_001
    vector_math_001.inputs[1].default_value = (2.0, 8.0, 0.0)

    #node Normal Map
    normal_map = group.nodes.new("ShaderNodeNormalMap")
    normal_map.label = "normalMapStrength"
    normal_map.name = "Normal Map"
    normal_map.space = 'TANGENT'
    normal_map.uv_map = ""
    #Strength
    normal_map.inputs[0].default_value = 1.0

    #node Normal Map.001
    normal_map_001 = group.nodes.new("ShaderNodeNormalMap")
    normal_map_001.label = "detailNormalMapStrengh"
    normal_map_001.name = "Normal Map.001"
    normal_map_001.space = 'TANGENT'
    normal_map_001.uv_map = ""
    #Strength
    normal_map_001.inputs[0].default_value = 2.0

    #node Material Output
    material_output = group.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    #Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Thickness
    material_output.inputs[3].default_value = 0.0

    #node Vector Math.002
    vector_math_002 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'ADD'


    #Set locations
    principled_bsdf.location = (67.19063568115234, -193.85972595214844)
    attribute.location = (-1337.263671875, -288.2535705566406)
    vector_math.location = (-415.93939208984375, 619.888427734375)
    image_texture.location = (-757.0962524414062, 723.2418212890625)
    image_texture_001.location = (-757.0962524414062, 432.2418212890625)
    image_texture_002.location = (-757.0962524414062, -228.50277709960938)
    image_texture_003.location = (-757.0962524414062, -823.27783203125)
    image_texture_004.location = (-757.0962524414062, -525.42333984375)
    mix.location = (-424.9765625, 471.22698974609375)
    math.location = (-470.1828308105469, -430.1927795410156)
    math_001.location = (-471.3009948730469, -726.7727661132812)
    image_texture_005.location = (-764.966796875, 84.22003173828125)
    vector_math_001.location = (-937.6324462890625, -95.35765838623047)
    normal_map.location = (-463.0379638671875, -208.7716064453125)
    normal_map_001.location = (-475.9705810546875, 80.57506561279297)
    material_output.location = (415.7670593261719, -168.20729064941406)
    vector_math_002.location = (-230.37200927734375, -74.58944702148438)

    #Set dimensions
    principled_bsdf.width, principled_bsdf.height = 240.0, 100.0
    attribute.width, attribute.height = 140.0, 100.0
    vector_math.width, vector_math.height = 140.0, 100.0
    image_texture.width, image_texture.height = 240.0, 100.0
    image_texture_001.width, image_texture_001.height = 240.0, 100.0
    image_texture_002.width, image_texture_002.height = 240.0, 100.0
    image_texture_003.width, image_texture_003.height = 240.0, 100.0
    image_texture_004.width, image_texture_004.height = 240.0, 100.0
    mix.width, mix.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    image_texture_005.width, image_texture_005.height = 240.0, 100.0
    vector_math_001.width, vector_math_001.height = 140.0, 100.0
    normal_map.width, normal_map.height = 150.0, 100.0
    normal_map_001.width, normal_map_001.height = 184.2037353515625, 100.0
    material_output.width, material_output.height = 140.0, 100.0
    vector_math_002.width, vector_math_002.height = 140.0, 100.0

    #initialize tread_marks_damaged_02 links
    #image_texture.Color -> vector_math.Vector
    group.links.new(image_texture.outputs[0], vector_math.inputs[0])
    #math.Value -> principled_bsdf.Roughness
    group.links.new(math.outputs[0], principled_bsdf.inputs[2])
    #attribute.Vector -> image_texture.Vector
    group.links.new(attribute.outputs[1], image_texture.inputs[0])
    #attribute.Vector -> image_texture_001.Vector
    group.links.new(attribute.outputs[1], image_texture_001.inputs[0])
    #attribute.Vector -> image_texture_002.Vector
    group.links.new(attribute.outputs[1], image_texture_002.inputs[0])
    #attribute.Vector -> image_texture_003.Vector
    group.links.new(attribute.outputs[1], image_texture_003.inputs[0])
    #attribute.Vector -> image_texture_004.Vector
    group.links.new(attribute.outputs[1], image_texture_004.inputs[0])
    #image_texture_001.Color -> mix.A
    group.links.new(image_texture_001.outputs[0], mix.inputs[6])
    #mix.Result -> vector_math.Vector
    group.links.new(mix.outputs[2], vector_math.inputs[1])
    #image_texture_004.Color -> math.Value
    group.links.new(image_texture_004.outputs[0], math.inputs[0])
    #image_texture_003.Color -> math_001.Value
    group.links.new(image_texture_003.outputs[0], math_001.inputs[0])
    #vector_math_001.Vector -> image_texture_005.Vector
    group.links.new(vector_math_001.outputs[0], image_texture_005.inputs[0])
    #attribute.Vector -> vector_math_001.Vector
    group.links.new(attribute.outputs[1], vector_math_001.inputs[0])
    #vector_math.Vector -> principled_bsdf.Base Color
    group.links.new(vector_math.outputs[0], principled_bsdf.inputs[0])
    #image_texture_002.Color -> normal_map.Color
    group.links.new(image_texture_002.outputs[0], normal_map.inputs[1])
    #image_texture_005.Color -> normal_map_001.Color
    group.links.new(image_texture_005.outputs[0], normal_map_001.inputs[1])
    #principled_bsdf.BSDF -> material_output.Surface
    group.links.new(principled_bsdf.outputs[0], material_output.inputs[0])
    #normal_map_001.Normal -> vector_math_002.Vector
    group.links.new(normal_map_001.outputs[0], vector_math_002.inputs[0])
    #normal_map.Normal -> vector_math_002.Vector
    group.links.new(normal_map.outputs[0], vector_math_002.inputs[1])
    #vector_math_002.Vector -> principled_bsdf.Normal
    group.links.new(vector_math_002.outputs[0], principled_bsdf.inputs[5])
    #math_001.Value -> principled_bsdf.Alpha
    group.links.new(math_001.outputs[0], principled_bsdf.inputs[4])
    return group

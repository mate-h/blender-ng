import bpy

#initialize beamngterrain node group
def beamng_terrain_node_group(displacement_image=None, layermap_image=None, material=None):
    node_group = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "BeamNGTerrain")

    node_group.color_tag = 'NONE'
    node_group.description = ""
    node_group.default_group_node_width = 140
    

    node_group.is_modifier = True

    #beamngterrain interface
    #Socket Geometry
    geometry_socket = node_group.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    #Socket Geometry
    geometry_socket_1 = node_group.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    #Socket Size
    size_socket = node_group.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
    size_socket.default_value = 1024.0
    size_socket.min_value = 0.0
    size_socket.max_value = 3.4028234663852886e+38
    size_socket.subtype = 'DISTANCE'
    size_socket.attribute_domain = 'POINT'

    #Socket Resolution
    resolution_socket = node_group.interface.new_socket(name = "Resolution", in_out='INPUT', socket_type = 'NodeSocketInt')
    resolution_socket.default_value = 1024
    resolution_socket.min_value = -2147483648
    resolution_socket.max_value = 2147483647
    resolution_socket.subtype = 'NONE'
    resolution_socket.attribute_domain = 'POINT'

    #Socket Height
    height_socket = node_group.interface.new_socket(name = "Height", in_out='INPUT', socket_type = 'NodeSocketFloat')
    height_socket.default_value = 100.0
    height_socket.min_value = -10000.0
    height_socket.max_value = 10000.0
    height_socket.subtype = 'DISTANCE'
    height_socket.attribute_domain = 'POINT'


    #initialize beamngterrain nodes
    #node Group Input
    group_input = node_group.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #node Group Output
    group_output = node_group.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    #node Grid
    grid = node_group.nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"

    #node Set Position
    set_position = node_group.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    #Selection
    set_position.inputs[1].default_value = True
    #Position
    set_position.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Image Texture
    image_texture = node_group.nodes.new("GeometryNodeImageTexture")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.interpolation = 'Linear'
    if displacement_image:
        image_texture.inputs[0].default_value = displacement_image
    #Frame
    image_texture.inputs[2].default_value = 0

    #node Layermap Texture
    layermap_texture = node_group.nodes.new("GeometryNodeImageTexture")
    layermap_texture.name = "Layermap Texture"
    layermap_texture.extension = 'REPEAT'
    layermap_texture.interpolation = 'Closest'
    if layermap_image:
        layermap_texture.inputs[0].default_value = layermap_image
    #Frame
    layermap_texture.inputs[2].default_value = 0

    #node Combine XYZ
    combine_xyz = node_group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    #X
    combine_xyz.inputs[0].default_value = 0.0
    #Y
    combine_xyz.inputs[1].default_value = 0.0

    #node Math
    math = node_group.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False

    #node Set Shade Smooth
    set_shade_smooth = node_group.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.domain = 'FACE'
    #Selection
    set_shade_smooth.inputs[1].default_value = True
    #Shade Smooth
    set_shade_smooth.inputs[2].default_value = True

    #node Math.001
    math_001 = node_group.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'ADD'
    math_001.use_clamp = False
    #Value_001
    math_001.inputs[1].default_value = 1.0

    #node Store Layermap Attribute
    store_layermap_attribute = node_group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_layermap_attribute.name = "Store Layermap Attribute"
    store_layermap_attribute.data_type = 'FLOAT'
    store_layermap_attribute.domain = 'POINT'
    #Selection
    store_layermap_attribute.inputs[1].default_value = True
    #Name
    store_layermap_attribute.inputs[2].default_value = "material_layer"

    #node Set Material
    set_material = node_group.nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    #Selection
    set_material.inputs[1].default_value = True
    if material:
        set_material.inputs[2].default_value = material

    #node Named Attribute
    named_attribute = node_group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT'
    #Name
    named_attribute.inputs[0].default_value = "material_layer"

    #node Compare
    compare = node_group.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'EQUAL'
    #B
    compare.inputs[1].default_value = 255.0
    #Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513

    #node Delete Geometry
    delete_geometry = node_group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'POINT'
    delete_geometry.mode = 'ALL'

    #Set locations
    group_input.location = (-445.481689453125, 60.36219787597656)
    group_output.location = (1892.5400390625, 6.232963562011719)
    grid.location = (-52.99237060546875, 149.56451416015625)
    set_position.location = (932.610107421875, 64.8414535522461)
    image_texture.location = (190.7024688720703, 68.13237762451172)
    layermap_texture.location = (172.66714477539062, -171.87030029296875)
    combine_xyz.location = (677.2738647460938, -46.79128646850586)
    math.location = (504.750244140625, -38.489315032958984)
    set_shade_smooth.location = (1547.3326416015625, -3.284168243408203)
    math_001.location = (-222.68728637695312, 1.9558639526367188)
    store_layermap_attribute.location = (1149.5255126953125, -3.6112027168273926)
    set_material.location = (1727.4613037109375, -1.7147369384765625)
    named_attribute.location = (933.9366455078125, -234.52467346191406)
    compare.location = (1142.8494873046875, -224.31651306152344)
    delete_geometry.location = (1347.490966796875, -54.790870666503906)

    #Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    grid.width, grid.height = 140.0, 100.0
    set_position.width, set_position.height = 140.0, 100.0
    image_texture.width, image_texture.height = 226.33042907714844, 100.0
    layermap_texture.width, layermap_texture.height = 226.33042907714844, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    set_shade_smooth.width, set_shade_smooth.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    store_layermap_attribute.width, store_layermap_attribute.height = 140.0, 100.0
    set_material.width, set_material.height = 140.0, 100.0
    named_attribute.width, named_attribute.height = 140.0, 100.0
    compare.width, compare.height = 140.0, 100.0
    delete_geometry.width, delete_geometry.height = 140.0, 100.0

    #initialize beamngterrain links
    #set_material.Geometry -> group_output.Geometry
    node_group.links.new(set_material.outputs[0], group_output.inputs[0])
    #grid.Mesh -> set_position.Geometry
    node_group.links.new(grid.outputs[0], set_position.inputs[0])
    #combine_xyz.Vector -> set_position.Offset
    node_group.links.new(combine_xyz.outputs[0], set_position.inputs[3])
    #math.Value -> combine_xyz.Z
    node_group.links.new(math.outputs[0], combine_xyz.inputs[2])
    #group_input.Resolution -> math_001.Value
    node_group.links.new(group_input.outputs[2], math_001.inputs[0])
    #math_001.Value -> grid.Vertices X
    node_group.links.new(math_001.outputs[0], grid.inputs[2])
    #math_001.Value -> grid.Vertices Y
    node_group.links.new(math_001.outputs[0], grid.inputs[3])
    #group_input.Size -> grid.Size X
    node_group.links.new(group_input.outputs[1], grid.inputs[0])
    #group_input.Size -> grid.Size Y
    node_group.links.new(group_input.outputs[1], grid.inputs[1])
    #image_texture.Color -> math.Value
    node_group.links.new(image_texture.outputs[0], math.inputs[0])
    #group_input.Height -> math.Value
    node_group.links.new(group_input.outputs[3], math.inputs[1])
    #set_shade_smooth.Geometry -> set_material.Geometry
    node_group.links.new(set_shade_smooth.outputs[0], set_material.inputs[0])
    #set_position.Geometry -> store_layermap_attribute.Geometry
    node_group.links.new(set_position.outputs[0], store_layermap_attribute.inputs[0])
    #layermap_texture.Color -> store_layermap_attribute.Value
    node_group.links.new(layermap_texture.outputs[0], store_layermap_attribute.inputs[3])
    #named_attribute.Attribute -> compare.A
    node_group.links.new(named_attribute.outputs[0], compare.inputs[0])
    #grid.UV Map -> image_texture.Vector
    node_group.links.new(grid.outputs[1], image_texture.inputs[1])
    #grid.UV Map -> layermap_texture.Vector
    node_group.links.new(grid.outputs[1], layermap_texture.inputs[1])
    #compare.Result -> delete_geometry.Selection
    node_group.links.new(compare.outputs[0], delete_geometry.inputs[1])
    #store_layermap_attribute.Geometry -> delete_geometry.Geometry
    node_group.links.new(store_layermap_attribute.outputs[0], delete_geometry.inputs[0])
    #delete_geometry.Geometry -> set_shade_smooth.Geometry
    node_group.links.new(delete_geometry.outputs[0], set_shade_smooth.inputs[0])
    return node_group

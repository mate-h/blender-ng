import bpy

#initialize beamngterrain node group
def beamng_terrain_node_group(displacement_image=None, layermap_image=None):
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
    height_socket.default_value = 200.0
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

    #node Image Texture (Displacement)
    image_texture = node_group.nodes.new("GeometryNodeImageTexture")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.interpolation = 'Linear'
    if displacement_image is not None:
        image_texture.inputs[0].default_value = displacement_image
    elif "BeamNG_Terrain_Displacement.exr" in bpy.data.images:
        image_texture.inputs[0].default_value = bpy.data.images["BeamNG_Terrain_Displacement.exr"]
    #Frame
    image_texture.inputs[2].default_value = 0

    # Add layermap image texture node if layermap is provided
    layermap_texture_node = None
    if layermap_image is not None:
        layermap_texture_node = node_group.nodes.new("GeometryNodeImageTexture")
        layermap_texture_node.name = "Layermap Texture"
        layermap_texture_node.extension = 'REPEAT'
        layermap_texture_node.interpolation = 'Closest'  # Use Closest for material IDs
        layermap_texture_node.inputs[0].default_value = layermap_image
        layermap_texture_node.inputs[2].default_value = 0
        layermap_texture_node.location = (241.1028289794922, -200.0)  # Position below displacement texture
        layermap_texture_node.width, layermap_texture_node.height = 226.33042907714844, 100.0

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





    #Set locations
    group_input.location = (-340.3531188964844, 16.491615295410156)
    group_output.location = (1227.301513671875, -26.20293426513672)
    grid.location = (52.136192321777344, 105.69392395019531)
    set_position.location = (866.7385864257812, 20.970867156982422)
    image_texture.location = (241.1028289794922, 3.6049652099609375)
    combine_xyz.location = (688.0914916992188, -124.15180969238281)
    math.location = (515.56787109375, -115.84983825683594)
    set_shade_smooth.location = (1046.9998779296875, 8.62431812286377)
    math_001.location = (-117.55870819091797, -41.91471862792969)

    #Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    grid.width, grid.height = 140.0, 100.0
    set_position.width, set_position.height = 140.0, 100.0
    image_texture.width, image_texture.height = 226.33042907714844, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    set_shade_smooth.width, set_shade_smooth.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0

    #initialize beamngterrain links
    #set_shade_smooth.Geometry -> group_output.Geometry
    node_group.links.new(set_shade_smooth.outputs[0], group_output.inputs[0])
    #grid.Mesh -> set_position.Geometry
    node_group.links.new(grid.outputs[0], set_position.inputs[0])
    #combine_xyz.Vector -> set_position.Offset
    node_group.links.new(combine_xyz.outputs[0], set_position.inputs[3])
    #math.Value -> combine_xyz.Z
    node_group.links.new(math.outputs[0], combine_xyz.inputs[2])
    #set_position.Geometry -> set_shade_smooth.Geometry
    node_group.links.new(set_position.outputs[0], set_shade_smooth.inputs[0])
    #grid.UV Map -> image_texture.Vector
    node_group.links.new(grid.outputs[1], image_texture.inputs[1])
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
    
    # Connect layermap texture to UV coordinates if it exists
    if layermap_texture_node is not None:
        node_group.links.new(grid.outputs[1], layermap_texture_node.inputs[1])
    
    return node_group

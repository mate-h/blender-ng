import bpy

#initialize terrain node group
def terrain_node_group(displacement_image=None, layermap_image=None, material=None, position=(0.0, 0.0, 0.0), size=1024.0, resolution=1024, height=100.0):
    # Always create a new node group - let Blender handle incremental naming
    group = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "BeamNGTerrain")
    print(f"🔧 Created node group: {group.name} (ID: {id(group)})")
    if material:
        print(f"   Using material: {material.name} (ID: {id(material)})")

    group.color_tag = 'NONE'
    group.description = ""
    group.default_group_node_width = 140
    

    group.is_modifier = True

    #beamngterrain interface
    #Socket Geometry
    geometry_socket = group.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    #Socket Geometry
    geometry_socket_1 = group.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    #Socket Size
    size_socket = group.interface.new_socket(name = "Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
    size_socket.default_value = size
    size_socket.min_value = 0.0
    size_socket.max_value = 3.4028234663852886e+38
    size_socket.subtype = 'DISTANCE'
    size_socket.attribute_domain = 'POINT'

    #Socket Resolution
    resolution_socket = group.interface.new_socket(name = "Resolution", in_out='INPUT', socket_type = 'NodeSocketInt')
    resolution_socket.default_value = resolution
    resolution_socket.min_value = -2147483648
    resolution_socket.max_value = 2147483647
    resolution_socket.subtype = 'NONE'
    resolution_socket.attribute_domain = 'POINT'

    #Socket Height
    height_socket = group.interface.new_socket(name = "Height", in_out='INPUT', socket_type = 'NodeSocketFloat')
    height_socket.default_value = height
    height_socket.min_value = -10000.0
    height_socket.max_value = 10000.0
    height_socket.subtype = 'DISTANCE'
    height_socket.attribute_domain = 'POINT'

    #Socket Position
    position_socket = group.interface.new_socket(name = "Position", in_out='INPUT', socket_type = 'NodeSocketVector')
    position_socket.default_value = position
    position_socket.min_value = -3.4028234663852886e+38
    position_socket.max_value = 3.4028234663852886e+38
    position_socket.subtype = 'NONE'
    position_socket.attribute_domain = 'POINT'


    #initialize beamngterrain nodes
    #node Group Input
    group_input = group.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #node Group Output
    group_output = group.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    #node Grid
    grid = group.nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"

    #node Set Position
    set_position = group.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    #Selection
    set_position.inputs[1].default_value = True
    #Position
    set_position.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Image Texture
    image_texture = group.nodes.new("GeometryNodeImageTexture")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    image_texture.interpolation = 'Linear'
    if displacement_image:
        image_texture.inputs[0].default_value = displacement_image
    #Frame
    image_texture.inputs[2].default_value = 0

    #node Layermap Texture
    layermap_texture = group.nodes.new("GeometryNodeImageTexture")
    layermap_texture.name = "Layermap Texture"
    layermap_texture.extension = 'REPEAT'
    layermap_texture.interpolation = 'Closest'
    if layermap_image:
        layermap_texture.inputs[0].default_value = layermap_image
    #Frame
    layermap_texture.inputs[2].default_value = 0

    #node Combine XYZ
    combine_xyz = group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    #X
    combine_xyz.inputs[0].default_value = 0.0
    #Y
    combine_xyz.inputs[1].default_value = 0.0

    #node Math
    math = group.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False

    #node Set Shade Smooth
    set_shade_smooth = group.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.domain = 'FACE'
    #Selection
    set_shade_smooth.inputs[1].default_value = True
    #Shade Smooth
    set_shade_smooth.inputs[2].default_value = True

    #node Math.001
    math_001 = group.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'ADD'
    math_001.use_clamp = False
    #Value_001
    math_001.inputs[1].default_value = 1.0

    #node Store Layermap Attribute
    store_layermap_attribute = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_layermap_attribute.name = "Store Layermap Attribute"
    store_layermap_attribute.data_type = 'FLOAT'
    store_layermap_attribute.domain = 'POINT'
    #Selection
    store_layermap_attribute.inputs[1].default_value = True
    #Name
    store_layermap_attribute.inputs[2].default_value = "material_layer"

    #node Set Material
    set_material = group.nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    #Selection
    set_material.inputs[1].default_value = True
    if material:
        set_material.inputs[2].default_value = material

    #node Named Attribute
    named_attribute = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT'
    #Name
    named_attribute.inputs[0].default_value = "material_layer"

    #node Compare
    compare = group.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'EQUAL'
    #B
    compare.inputs[1].default_value = 255.0
    #Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513

    #node Delete Geometry
    delete_geometry = group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'POINT'
    delete_geometry.mode = 'ALL'

    #node Vector Math
    vector_math = group.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'ADD'

    #node Vector Math.001
    vector_math_001 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'ADD'

    #node Group Input.001
    group_input_001 = group.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"

    #node Math.002
    math_002 = group.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    #Value_001
    math_002.inputs[1].default_value = 0.5

    #node Combine XYZ.001
    combine_xyz_001 = group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.name = "Combine XYZ.001"
    #Z
    combine_xyz_001.inputs[2].default_value = 0.0

    #node Store Named Attribute
    store_named_attribute = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'FLOAT2'
    store_named_attribute.domain = 'CORNER'
    #Selection
    store_named_attribute.inputs[1].default_value = True
    #Name
    store_named_attribute.inputs[2].default_value = "UVMap"





    #Set locations
    group_input.location = (-517.251953125, -36.288307189941406)
    group_output.location = (2177.5400390625, 6.232963562011719)
    grid.location = (-124.76260375976562, 52.91400909423828)
    set_position.location = (1258.742431640625, 46.31529998779297)
    image_texture.location = (155.740234375, 49.381717681884766)
    layermap_texture.location = (151.71380615234375, -178.93560791015625)
    combine_xyz.location = (759.5379638671875, -30.323625564575195)
    math.location = (593.09375, -17.11091423034668)
    set_shade_smooth.location = (1832.332763671875, -3.284168243408203)
    math_001.location = (-294.4574890136719, -94.69464111328125)
    store_layermap_attribute.location = (1434.525634765625, -3.6112027168273926)
    set_material.location = (2012.46142578125, -1.7147369384765625)
    named_attribute.location = (1387.27783203125, -270.93914794921875)
    compare.location = (1596.190673828125, -260.7309875488281)
    delete_geometry.location = (1632.4910888671875, -54.790870666503906)
    vector_math.location = (917.141357421875, -29.272382736206055)
    vector_math_001.location = (1078.6322021484375, -27.7032527923584)
    group_input_001.location = (406.95257568359375, -138.40708923339844)
    math_002.location = (707.1993408203125, -201.60931396484375)
    combine_xyz_001.location = (884.0307006835938, -197.49993896484375)
    store_named_attribute.location = (164.4757843017578, 266.8240661621094)

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
    vector_math.width, vector_math.height = 140.0, 100.0
    vector_math_001.width, vector_math_001.height = 140.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    math_002.width, math_002.height = 140.0, 100.0
    combine_xyz_001.width, combine_xyz_001.height = 140.0, 100.0
    store_named_attribute.width, store_named_attribute.height = 140.0, 100.0

    #initialize beamngterrain links
    #set_material.Geometry -> group_output.Geometry
    group.links.new(set_material.outputs[0], group_output.inputs[0])
    #store_named_attribute.Geometry -> set_position.Geometry
    group.links.new(store_named_attribute.outputs[0], set_position.inputs[0])
    #vector_math_001.Vector -> set_position.Offset
    group.links.new(vector_math_001.outputs[0], set_position.inputs[3])
    #math.Value -> combine_xyz.Z
    group.links.new(math.outputs[0], combine_xyz.inputs[2])
    #group_input.Resolution -> math_001.Value
    group.links.new(group_input.outputs[2], math_001.inputs[0])
    #math_001.Value -> grid.Vertices X
    group.links.new(math_001.outputs[0], grid.inputs[2])
    #math_001.Value -> grid.Vertices Y
    group.links.new(math_001.outputs[0], grid.inputs[3])
    #group_input.Size -> grid.Size X
    group.links.new(group_input.outputs[1], grid.inputs[0])
    #group_input.Size -> grid.Size Y
    group.links.new(group_input.outputs[1], grid.inputs[1])
    #image_texture.Color -> math.Value
    group.links.new(image_texture.outputs[0], math.inputs[0])
    #group_input.Height -> math.Value
    group.links.new(group_input.outputs[3], math.inputs[1])
    #set_shade_smooth.Geometry -> set_material.Geometry
    group.links.new(set_shade_smooth.outputs[0], set_material.inputs[0])
    #set_position.Geometry -> store_layermap_attribute.Geometry
    group.links.new(set_position.outputs[0], store_layermap_attribute.inputs[0])
    #layermap_texture.Color -> store_layermap_attribute.Value
    group.links.new(layermap_texture.outputs[0], store_layermap_attribute.inputs[3])
    #named_attribute.Attribute -> compare.A
    group.links.new(named_attribute.outputs[0], compare.inputs[0])
    #grid.UV Map -> image_texture.Vector
    group.links.new(grid.outputs[1], image_texture.inputs[1])
    #grid.UV Map -> layermap_texture.Vector
    group.links.new(grid.outputs[1], layermap_texture.inputs[1])
    #compare.Result -> delete_geometry.Selection
    group.links.new(compare.outputs[0], delete_geometry.inputs[1])
    #store_layermap_attribute.Geometry -> delete_geometry.Geometry
    group.links.new(store_layermap_attribute.outputs[0], delete_geometry.inputs[0])
    #delete_geometry.Geometry -> set_shade_smooth.Geometry
    group.links.new(delete_geometry.outputs[0], set_shade_smooth.inputs[0])
    #combine_xyz.Vector -> vector_math.Vector
    group.links.new(combine_xyz.outputs[0], vector_math.inputs[0])
    #vector_math.Vector -> vector_math_001.Vector
    group.links.new(vector_math.outputs[0], vector_math_001.inputs[0])
    #group_input_001.Position -> vector_math.Vector
    group.links.new(group_input_001.outputs[4], vector_math.inputs[1])
    #group_input_001.Size -> math_002.Value
    group.links.new(group_input_001.outputs[1], math_002.inputs[0])
    #math_002.Value -> combine_xyz_001.X
    group.links.new(math_002.outputs[0], combine_xyz_001.inputs[0])
    #math_002.Value -> combine_xyz_001.Y
    group.links.new(math_002.outputs[0], combine_xyz_001.inputs[1])
    #combine_xyz_001.Vector -> vector_math_001.Vector
    group.links.new(combine_xyz_001.outputs[0], vector_math_001.inputs[1])
    #grid.Mesh -> store_named_attribute.Geometry
    group.links.new(grid.outputs[0], store_named_attribute.inputs[0])
    #grid.UV Map -> store_named_attribute.Value
    group.links.new(grid.outputs[1], store_named_attribute.inputs[3])
    return group

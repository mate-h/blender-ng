import bpy

#initialize erosion node group
def erosion_node_group():
    group = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Erosion")

    group.color_tag = 'NONE'
    group.description = ""
    group.default_group_node_width = 140
    

    group.is_modifier = True

    #erosion interface
    #Socket Geometry
    geometry_socket = group.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    #Socket Erosion
    erosion_socket = group.interface.new_socket(name = "Erosion", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
    erosion_socket.default_value = 0.0
    erosion_socket.min_value = -3.4028234663852886e+38
    erosion_socket.max_value = 3.4028234663852886e+38
    erosion_socket.subtype = 'NONE'
    erosion_socket.attribute_domain = 'POINT'

    #Socket Sediment
    sediment_socket = group.interface.new_socket(name = "Sediment", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
    sediment_socket.default_value = 0.0
    sediment_socket.min_value = -3.4028234663852886e+38
    sediment_socket.max_value = 3.4028234663852886e+38
    sediment_socket.subtype = 'NONE'
    sediment_socket.attribute_domain = 'POINT'

    #Socket Geometry
    geometry_socket_1 = group.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    #Socket Capacity Factor
    capacity_factor_socket = group.interface.new_socket(name = "Capacity Factor", in_out='INPUT', socket_type = 'NodeSocketFloat')
    capacity_factor_socket.default_value = 3.0
    capacity_factor_socket.min_value = 0.0
    capacity_factor_socket.max_value = 10000.0
    capacity_factor_socket.subtype = 'NONE'
    capacity_factor_socket.attribute_domain = 'POINT'

    #Socket Erode Speed
    erode_speed_socket = group.interface.new_socket(name = "Erode Speed", in_out='INPUT', socket_type = 'NodeSocketFloat')
    erode_speed_socket.default_value = 0.30000001192092896
    erode_speed_socket.min_value = 0.0
    erode_speed_socket.max_value = 10000.0
    erode_speed_socket.subtype = 'NONE'
    erode_speed_socket.attribute_domain = 'POINT'

    #Socket Deposit Speed
    deposit_speed_socket = group.interface.new_socket(name = "Deposit Speed", in_out='INPUT', socket_type = 'NodeSocketFloat')
    deposit_speed_socket.default_value = 0.30000001192092896
    deposit_speed_socket.min_value = 0.0
    deposit_speed_socket.max_value = 10000.0
    deposit_speed_socket.subtype = 'NONE'
    deposit_speed_socket.attribute_domain = 'POINT'

    #Socket Half Size
    half_size_socket = group.interface.new_socket(name = "Half Size", in_out='INPUT', socket_type = 'NodeSocketFloat')
    half_size_socket.default_value = 2.0
    half_size_socket.min_value = 0.0
    half_size_socket.max_value = 10000.0
    half_size_socket.subtype = 'NONE'
    half_size_socket.attribute_domain = 'POINT'

    #Socket Max Age
    max_age_socket = group.interface.new_socket(name = "Max Age", in_out='INPUT', socket_type = 'NodeSocketInt')
    max_age_socket.default_value = 120
    max_age_socket.min_value = 0
    max_age_socket.max_value = 2147483647
    max_age_socket.subtype = 'NONE'
    max_age_socket.attribute_domain = 'POINT'

    #Socket Point Density
    point_density_socket = group.interface.new_socket(name = "Point Density", in_out='INPUT', socket_type = 'NodeSocketFloat')
    point_density_socket.default_value = 5.0
    point_density_socket.min_value = 0.0
    point_density_socket.max_value = 3.4028234663852886e+38
    point_density_socket.subtype = 'NONE'
    point_density_socket.attribute_domain = 'POINT'
    point_density_socket.description = "Distributed each frame for the erosion simulation"

    #Socket Point Gravity
    point_gravity_socket = group.interface.new_socket(name = "Point Gravity", in_out='INPUT', socket_type = 'NodeSocketVector')
    point_gravity_socket.default_value = (0.0, 0.0, -0.0020000000949949026)
    point_gravity_socket.min_value = -10000.0
    point_gravity_socket.max_value = 10000.0
    point_gravity_socket.subtype = 'NONE'
    point_gravity_socket.attribute_domain = 'POINT'
    point_gravity_socket.description = "Point Gravity Acceleration"

    #Socket Show Points
    show_points_socket = group.interface.new_socket(name = "Show Points", in_out='INPUT', socket_type = 'NodeSocketBool')
    show_points_socket.default_value = False
    show_points_socket.attribute_domain = 'POINT'


    #initialize erosion nodes
    #node Group Input.001
    group_input_001 = group.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[4].hide = True
    group_input_001.outputs[5].hide = True
    group_input_001.outputs[6].hide = True
    group_input_001.outputs[7].hide = True
    group_input_001.outputs[8].hide = True

    #node Scene Time
    scene_time = group.nodes.new("GeometryNodeInputSceneTime")
    scene_time.name = "Scene Time"

    #node Simulation Input
    simulation_input = group.nodes.new("GeometryNodeSimulationInput")
    simulation_input.name = "Simulation Input"
    #node Distribute Points on Faces
    distribute_points_on_faces = group.nodes.new("GeometryNodeDistributePointsOnFaces")
    distribute_points_on_faces.name = "Distribute Points on Faces"
    distribute_points_on_faces.distribute_method = 'RANDOM'
    distribute_points_on_faces.use_legacy_normal = False
    #Selection
    distribute_points_on_faces.inputs[1].default_value = True

    #node Join Geometry
    join_geometry = group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    #node Separate Components
    separate_components = group.nodes.new("GeometryNodeSeparateComponents")
    separate_components.name = "Separate Components"

    #node Reroute.002
    reroute_002 = group.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketGeometry"
    #node Math.004
    math_004 = group.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'ADD'
    math_004.use_clamp = False
    #Value_001
    math_004.inputs[1].default_value = 1.0

    #node Named Attribute.001
    named_attribute_001 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.data_type = 'FLOAT'
    #Name
    named_attribute_001.inputs[0].default_value = "age"

    #node Store Named Attribute
    store_named_attribute = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'FLOAT_VECTOR'
    store_named_attribute.domain = 'POINT'
    #Selection
    store_named_attribute.inputs[1].default_value = True
    #Name
    store_named_attribute.inputs[2].default_value = "vel"

    #node Reroute.004
    reroute_004 = group.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    reroute_004.socket_idname = "NodeSocketGeometry"
    #node Vector Math.001
    vector_math_001 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'ADD'

    #node Vector Math.008
    vector_math_008 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.operation = 'CROSS_PRODUCT'

    #node Named Attribute
    named_attribute = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute.inputs[0].default_value = "vel"

    #node Store Named Attribute.001
    store_named_attribute_001 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'FLOAT'
    store_named_attribute_001.domain = 'POINT'
    #Selection
    store_named_attribute_001.inputs[1].default_value = True
    #Name
    store_named_attribute_001.inputs[2].default_value = "age"

    #node Normal
    normal = group.nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    normal.legacy_corner_normals = True

    #node Reroute.007
    reroute_007 = group.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.socket_idname = "NodeSocketGeometry"
    #node Group Output
    group_output = group.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    #Socket_4
    group_output.inputs[1].default_value = 0.0
    #Socket_5
    group_output.inputs[2].default_value = 0.0

    #node Simulation Output
    simulation_output = group.nodes.new("GeometryNodeSimulationOutput")
    simulation_output.name = "Simulation Output"
    simulation_output.active_index = 0
    simulation_output.state_items.clear()
    # Create item "Geometry"
    simulation_output.state_items.new('GEOMETRY', "Geometry")
    simulation_output.state_items[0].attribute_domain = 'POINT'
    #Skip
    simulation_output.inputs[0].default_value = False

    #node Join Geometry.001
    join_geometry_001 = group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"

    #node Reroute
    reroute = group.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    #node Sample Nearest.001
    sample_nearest_001 = group.nodes.new("GeometryNodeSampleNearest")
    sample_nearest_001.name = "Sample Nearest.001"
    sample_nearest_001.domain = 'POINT'
    #Sample Position
    sample_nearest_001.inputs[1].default_value = (0.0, 0.0, 0.0)

    #node Sample Index.001
    sample_index_001 = group.nodes.new("GeometryNodeSampleIndex")
    sample_index_001.name = "Sample Index.001"
    sample_index_001.clamp = False
    sample_index_001.data_type = 'FLOAT_VECTOR'
    sample_index_001.domain = 'POINT'

    #node Vector Math.009
    vector_math_009 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.operation = 'CROSS_PRODUCT'

    #node Reroute.010
    reroute_010 = group.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.socket_idname = "NodeSocketGeometry"
    #node Sample Nearest.004
    sample_nearest_004 = group.nodes.new("GeometryNodeSampleNearest")
    sample_nearest_004.name = "Sample Nearest.004"
    sample_nearest_004.domain = 'POINT'
    #Sample Position
    sample_nearest_004.inputs[1].default_value = (0.0, 0.0, 0.0)

    #node Sample Index.002
    sample_index_002 = group.nodes.new("GeometryNodeSampleIndex")
    sample_index_002.name = "Sample Index.002"
    sample_index_002.clamp = False
    sample_index_002.data_type = 'FLOAT_VECTOR'
    sample_index_002.domain = 'POINT'

    #node Reroute.013
    reroute_013 = group.nodes.new("NodeReroute")
    reroute_013.name = "Reroute.013"
    reroute_013.socket_idname = "NodeSocketGeometry"
    #node Position.001
    position_001 = group.nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"

    #node Store Named Attribute.003
    store_named_attribute_003 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.data_type = 'FLOAT_VECTOR'
    store_named_attribute_003.domain = 'POINT'
    #Selection
    store_named_attribute_003.inputs[1].default_value = True
    #Name
    store_named_attribute_003.inputs[2].default_value = "start_pos"

    #node Reroute.015
    reroute_015 = group.nodes.new("NodeReroute")
    reroute_015.name = "Reroute.015"
    reroute_015.socket_idname = "NodeSocketGeometry"
    #node Sample Nearest.005
    sample_nearest_005 = group.nodes.new("GeometryNodeSampleNearest")
    sample_nearest_005.name = "Sample Nearest.005"
    sample_nearest_005.domain = 'POINT'
    #Sample Position
    sample_nearest_005.inputs[1].default_value = (0.0, 0.0, 0.0)

    #node Sample Index.003
    sample_index_003 = group.nodes.new("GeometryNodeSampleIndex")
    sample_index_003.name = "Sample Index.003"
    sample_index_003.clamp = False
    sample_index_003.data_type = 'FLOAT_VECTOR'
    sample_index_003.domain = 'POINT'

    #node Position.002
    position_002 = group.nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"

    #node Set Position.001
    set_position_001 = group.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    #Selection
    set_position_001.inputs[1].default_value = True
    #Position
    set_position_001.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Reroute.016
    reroute_016 = group.nodes.new("NodeReroute")
    reroute_016.name = "Reroute.016"
    reroute_016.socket_idname = "NodeSocketGeometry"
    #node Store Named Attribute.004
    store_named_attribute_004 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_004.name = "Store Named Attribute.004"
    store_named_attribute_004.data_type = 'FLOAT_VECTOR'
    store_named_attribute_004.domain = 'POINT'
    #Selection
    store_named_attribute_004.inputs[1].default_value = True
    #Name
    store_named_attribute_004.inputs[2].default_value = "end_pos"

    #node Reroute.017
    reroute_017 = group.nodes.new("NodeReroute")
    reroute_017.name = "Reroute.017"
    reroute_017.socket_idname = "NodeSocketGeometry"
    #node Geometry Proximity
    geometry_proximity = group.nodes.new("GeometryNodeProximity")
    geometry_proximity.name = "Geometry Proximity"
    geometry_proximity.target_element = 'POINTS'
    #Group ID
    geometry_proximity.inputs[1].default_value = 0
    #Source Position
    geometry_proximity.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Sample Group ID
    geometry_proximity.inputs[3].default_value = 0

    #node Sample Nearest
    sample_nearest = group.nodes.new("GeometryNodeSampleNearest")
    sample_nearest.name = "Sample Nearest"
    sample_nearest.domain = 'POINT'

    #node Compare.001
    compare_001 = group.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'INT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'EQUAL'

    #node Index
    index = group.nodes.new("GeometryNodeInputIndex")
    index.name = "Index"

    #node Reroute.009
    reroute_009 = group.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.socket_idname = "NodeSocketGeometry"
    #node Reroute.011
    reroute_011 = group.nodes.new("NodeReroute")
    reroute_011.name = "Reroute.011"
    reroute_011.socket_idname = "NodeSocketGeometry"
    #node Geometry Proximity.001
    geometry_proximity_001 = group.nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.target_element = 'POINTS'
    #Group ID
    geometry_proximity_001.inputs[1].default_value = 0
    #Source Position
    geometry_proximity_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Sample Group ID
    geometry_proximity_001.inputs[3].default_value = 0

    #node Sample Nearest.002
    sample_nearest_002 = group.nodes.new("GeometryNodeSampleNearest")
    sample_nearest_002.name = "Sample Nearest.002"
    sample_nearest_002.domain = 'POINT'

    #node Compare.002
    compare_002 = group.nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.data_type = 'INT'
    compare_002.mode = 'ELEMENT'
    compare_002.operation = 'EQUAL'

    #node Index.001
    index_001 = group.nodes.new("GeometryNodeInputIndex")
    index_001.name = "Index.001"

    #node Reroute.014
    reroute_014 = group.nodes.new("NodeReroute")
    reroute_014.name = "Reroute.014"
    reroute_014.socket_idname = "NodeSocketGeometry"
    #node Store Named Attribute.005
    store_named_attribute_005 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_005.name = "Store Named Attribute.005"
    store_named_attribute_005.data_type = 'BOOLEAN'
    store_named_attribute_005.domain = 'POINT'
    #Selection
    store_named_attribute_005.inputs[1].default_value = True
    #Name
    store_named_attribute_005.inputs[2].default_value = "start_selection"

    #node Reroute.018
    reroute_018 = group.nodes.new("NodeReroute")
    reroute_018.name = "Reroute.018"
    reroute_018.socket_idname = "NodeSocketGeometry"
    #node Reroute.020
    reroute_020 = group.nodes.new("NodeReroute")
    reroute_020.name = "Reroute.020"
    reroute_020.socket_idname = "NodeSocketGeometry"
    #node Store Named Attribute.006
    store_named_attribute_006 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_006.name = "Store Named Attribute.006"
    store_named_attribute_006.data_type = 'BOOLEAN'
    store_named_attribute_006.domain = 'POINT'
    #Selection
    store_named_attribute_006.inputs[1].default_value = True
    #Name
    store_named_attribute_006.inputs[2].default_value = "end_selection"

    #node Reroute.021
    reroute_021 = group.nodes.new("NodeReroute")
    reroute_021.name = "Reroute.021"
    reroute_021.socket_idname = "NodeSocketGeometry"
    #node Named Attribute.002
    named_attribute_002 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_002.name = "Named Attribute.002"
    named_attribute_002.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute_002.inputs[0].default_value = "end_pos"

    #node Named Attribute.005
    named_attribute_005 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_005.name = "Named Attribute.005"
    named_attribute_005.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute_005.inputs[0].default_value = "start_pos"

    #node Vector Math.002
    vector_math_002 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SUBTRACT'

    #node Reroute.024
    reroute_024 = group.nodes.new("NodeReroute")
    reroute_024.name = "Reroute.024"
    reroute_024.socket_idname = "NodeSocketGeometry"
    #node Sample Index
    sample_index = group.nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.clamp = False
    sample_index.data_type = 'FLOAT_VECTOR'
    sample_index.domain = 'POINT'

    #node Sample Nearest.003
    sample_nearest_003 = group.nodes.new("GeometryNodeSampleNearest")
    sample_nearest_003.name = "Sample Nearest.003"
    sample_nearest_003.domain = 'POINT'
    #Sample Position
    sample_nearest_003.inputs[1].default_value = (0.0, 0.0, 0.0)

    #node Reroute.023
    reroute_023 = group.nodes.new("NodeReroute")
    reroute_023.name = "Reroute.023"
    reroute_023.socket_idname = "NodeSocketGeometry"
    #node Named Attribute.006
    named_attribute_006 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_006.name = "Named Attribute.006"
    named_attribute_006.data_type = 'BOOLEAN'
    #Name
    named_attribute_006.inputs[0].default_value = "start_selection"

    #node Set Position.002
    set_position_002 = group.nodes.new("GeometryNodeSetPosition")
    set_position_002.name = "Set Position.002"
    #Position
    set_position_002.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Set Position.003
    set_position_003 = group.nodes.new("GeometryNodeSetPosition")
    set_position_003.name = "Set Position.003"
    #Selection
    set_position_003.inputs[1].default_value = True
    #Position
    set_position_003.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Named Attribute.007
    named_attribute_007 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_007.name = "Named Attribute.007"
    named_attribute_007.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute_007.inputs[0].default_value = "vel_surface"

    #node Vector Math.004
    vector_math_004 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.operation = 'SCALE'
    #Scale
    vector_math_004.inputs[3].default_value = -1.0

    #node Reroute.026
    reroute_026 = group.nodes.new("NodeReroute")
    reroute_026.name = "Reroute.026"
    reroute_026.socket_idname = "NodeSocketGeometry"
    #node Named Attribute.008
    named_attribute_008 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_008.name = "Named Attribute.008"
    named_attribute_008.data_type = 'FLOAT'
    #Name
    named_attribute_008.inputs[0].default_value = "age"

    #node Compare.003
    compare_003 = group.nodes.new("FunctionNodeCompare")
    compare_003.name = "Compare.003"
    compare_003.data_type = 'FLOAT'
    compare_003.mode = 'ELEMENT'
    compare_003.operation = 'GREATER_THAN'

    #node Delete Geometry
    delete_geometry = group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'POINT'
    delete_geometry.mode = 'ALL'

    #node Reroute.022
    reroute_022 = group.nodes.new("NodeReroute")
    reroute_022.name = "Reroute.022"
    reroute_022.socket_idname = "NodeSocketGeometry"
    #node Reroute.027
    reroute_027 = group.nodes.new("NodeReroute")
    reroute_027.name = "Reroute.027"
    reroute_027.socket_idname = "NodeSocketGeometry"
    #node Separate Components.001
    separate_components_001 = group.nodes.new("GeometryNodeSeparateComponents")
    separate_components_001.name = "Separate Components.001"

    #node Blur Attribute
    blur_attribute = group.nodes.new("GeometryNodeBlurAttribute")
    blur_attribute.name = "Blur Attribute"
    blur_attribute.data_type = 'FLOAT'
    #Iterations
    blur_attribute.inputs[1].default_value = 0
    #Weight
    blur_attribute.inputs[2].default_value = 1.0

    #node Set Position.004
    set_position_004 = group.nodes.new("GeometryNodeSetPosition")
    set_position_004.name = "Set Position.004"
    #Selection
    set_position_004.inputs[1].default_value = True
    #Offset
    set_position_004.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Position.003
    position_003 = group.nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"

    #node Separate XYZ
    separate_xyz = group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    #node Combine XYZ.001
    combine_xyz_001 = group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.name = "Combine XYZ.001"

    #node Set Shade Smooth
    set_shade_smooth = group.nodes.new("GeometryNodeSetShadeSmooth")
    set_shade_smooth.name = "Set Shade Smooth"
    set_shade_smooth.domain = 'FACE'
    #Selection
    set_shade_smooth.inputs[1].default_value = True
    #Shade Smooth
    set_shade_smooth.inputs[2].default_value = True

    #node Separate XYZ.001
    separate_xyz_001 = group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_001.name = "Separate XYZ.001"

    #node Combine XYZ.002
    combine_xyz_002 = group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_002.name = "Combine XYZ.002"
    #X
    combine_xyz_002.inputs[0].default_value = 0.0
    #Y
    combine_xyz_002.inputs[1].default_value = 0.0

    #node Named Attribute.009
    named_attribute_009 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_009.name = "Named Attribute.009"
    named_attribute_009.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute_009.inputs[0].default_value = "vel_surface"

    #node Vector Math.005
    vector_math_005 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'LENGTH'

    #node Store Named Attribute.007
    store_named_attribute_007 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_007.name = "Store Named Attribute.007"
    store_named_attribute_007.data_type = 'FLOAT'
    store_named_attribute_007.domain = 'POINT'
    #Selection
    store_named_attribute_007.inputs[1].default_value = True
    #Name
    store_named_attribute_007.inputs[2].default_value = "water"
    #Value
    store_named_attribute_007.inputs[3].default_value = 1.0

    #node Named Attribute.010
    named_attribute_010 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_010.name = "Named Attribute.010"
    named_attribute_010.data_type = 'FLOAT'
    #Name
    named_attribute_010.inputs[0].default_value = "water"

    #node Math.009
    math_009 = group.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.operation = 'MULTIPLY'
    math_009.use_clamp = False
    #Value_001
    math_009.inputs[1].default_value = -1.0

    #node Math.010
    math_010 = group.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.operation = 'MULTIPLY'
    math_010.use_clamp = False

    #node Math.011
    math_011 = group.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.operation = 'MULTIPLY'
    math_011.use_clamp = False

    #node Math.012
    math_012 = group.nodes.new("ShaderNodeMath")
    math_012.label = "Capacity Factor"
    math_012.name = "Math.012"
    math_012.use_custom_color = True
    math_012.color = (0.14086699485778809, 0.38403424620628357, 0.5131794214248657)
    math_012.operation = 'MULTIPLY'
    math_012.use_clamp = False

    #node Store Named Attribute.008
    store_named_attribute_008 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_008.name = "Store Named Attribute.008"
    store_named_attribute_008.data_type = 'FLOAT'
    store_named_attribute_008.domain = 'POINT'
    #Selection
    store_named_attribute_008.inputs[1].default_value = True
    #Name
    store_named_attribute_008.inputs[2].default_value = "sediment"
    #Value
    store_named_attribute_008.inputs[3].default_value = 0.0

    #node Set Point Radius
    set_point_radius = group.nodes.new("GeometryNodeSetPointRadius")
    set_point_radius.name = "Set Point Radius"
    #Selection
    set_point_radius.inputs[1].default_value = True
    #Radius
    set_point_radius.inputs[2].default_value = 0.009999999776482582

    #node Reroute.005
    reroute_005 = group.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.socket_idname = "NodeSocketGeometry"
    #node Raycast
    raycast = group.nodes.new("GeometryNodeRaycast")
    raycast.name = "Raycast"
    raycast.data_type = 'FLOAT'
    raycast.mapping = 'INTERPOLATED'
    #Attribute
    raycast.inputs[1].default_value = 0.0
    #Source Position
    raycast.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Ray Length
    raycast.inputs[4].default_value = 0.019999999552965164

    #node Reroute.008
    reroute_008 = group.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.socket_idname = "NodeSocketGeometry"
    #node Reroute.019
    reroute_019 = group.nodes.new("NodeReroute")
    reroute_019.name = "Reroute.019"
    reroute_019.socket_idname = "NodeSocketGeometry"
    #node Raycast.001
    raycast_001 = group.nodes.new("GeometryNodeRaycast")
    raycast_001.name = "Raycast.001"
    raycast_001.data_type = 'FLOAT'
    raycast_001.mapping = 'INTERPOLATED'
    #Attribute
    raycast_001.inputs[1].default_value = 0.0
    #Source Position
    raycast_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Ray Length
    raycast_001.inputs[4].default_value = 0.019999999552965164

    #node Vector Math.003
    vector_math_003 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_003.label = "Geo Normal Inverse"
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'SCALE'
    #Scale
    vector_math_003.inputs[3].default_value = -1.0

    #node Set Position.006
    set_position_006 = group.nodes.new("GeometryNodeSetPosition")
    set_position_006.name = "Set Position.006"
    #Offset
    set_position_006.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Set Position.007
    set_position_007 = group.nodes.new("GeometryNodeSetPosition")
    set_position_007.name = "Set Position.007"
    #Offset
    set_position_007.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Store Named Attribute.002
    store_named_attribute_002 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.data_type = 'FLOAT_VECTOR'
    store_named_attribute_002.domain = 'POINT'
    #Selection
    store_named_attribute_002.inputs[1].default_value = True
    #Name
    store_named_attribute_002.inputs[2].default_value = "current_pos"

    #node Capture Attribute
    capture_attribute = group.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.active_index = 0
    capture_attribute.capture_items.clear()
    capture_attribute.capture_items.new('FLOAT', "Position")
    capture_attribute.capture_items["Position"].data_type = 'FLOAT_VECTOR'
    capture_attribute.domain = 'POINT'

    #node Position.004
    position_004 = group.nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"

    #node Store Named Attribute.009
    store_named_attribute_009 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_009.name = "Store Named Attribute.009"
    store_named_attribute_009.data_type = 'FLOAT_VECTOR'
    store_named_attribute_009.domain = 'POINT'
    #Selection
    store_named_attribute_009.inputs[1].default_value = True
    #Name
    store_named_attribute_009.inputs[2].default_value = "vel_surface"

    #node Position.005
    position_005 = group.nodes.new("GeometryNodeInputPosition")
    position_005.name = "Position.005"

    #node Named Attribute.004
    named_attribute_004 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_004.name = "Named Attribute.004"
    named_attribute_004.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute_004.inputs[0].default_value = "current_pos"

    #node Vector Math.006
    vector_math_006 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.operation = 'SUBTRACT'

    #node Reroute.003
    reroute_003 = group.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    reroute_003.socket_idname = "NodeSocketGeometry"
    #node Reroute.028
    reroute_028 = group.nodes.new("NodeReroute")
    reroute_028.name = "Reroute.028"
    reroute_028.socket_idname = "NodeSocketGeometry"
    #node Reroute.029
    reroute_029 = group.nodes.new("NodeReroute")
    reroute_029.name = "Reroute.029"
    reroute_029.socket_idname = "NodeSocketGeometry"
    #node Reroute.030
    reroute_030 = group.nodes.new("NodeReroute")
    reroute_030.name = "Reroute.030"
    reroute_030.socket_idname = "NodeSocketGeometry"
    #node Frame.001
    frame_001 = group.nodes.new("NodeFrame")
    frame_001.label = "Delta Height"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    #node Frame.002
    frame_002 = group.nodes.new("NodeFrame")
    frame_002.label = "Sediment Capacity"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    #node Math.001
    math_001 = group.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'SUBTRACT'
    math_001.use_clamp = False

    #node Named Attribute.003
    named_attribute_003 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.name = "Named Attribute.003"
    named_attribute_003.data_type = 'FLOAT'
    #Name
    named_attribute_003.inputs[0].default_value = "sediment"

    #node Math.003
    math_003 = group.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'MINIMUM'
    math_003.use_clamp = False

    #node Math.005
    math_005 = group.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'MULTIPLY'
    math_005.use_clamp = False
    #Value_001
    math_005.inputs[1].default_value = -1.0

    #node Math.006
    math_006 = group.nodes.new("ShaderNodeMath")
    math_006.label = "Erode Speed"
    math_006.name = "Math.006"
    math_006.use_custom_color = True
    math_006.color = (0.14086699485778809, 0.38403424620628357, 0.5131794214248657)
    math_006.operation = 'MULTIPLY'
    math_006.use_clamp = False

    #node Store Named Attribute.010
    store_named_attribute_010 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_010.name = "Store Named Attribute.010"
    store_named_attribute_010.data_type = 'FLOAT'
    store_named_attribute_010.domain = 'POINT'
    #Selection
    store_named_attribute_010.inputs[1].default_value = True
    #Name
    store_named_attribute_010.inputs[2].default_value = "sediment"

    #node Named Attribute.011
    named_attribute_011 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_011.name = "Named Attribute.011"
    named_attribute_011.data_type = 'FLOAT'
    #Name
    named_attribute_011.inputs[0].default_value = "sediment"

    #node Math.007
    math_007 = group.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.operation = 'SUBTRACT'
    math_007.use_clamp = False

    #node Reroute.031
    reroute_031 = group.nodes.new("NodeReroute")
    reroute_031.name = "Reroute.031"
    reroute_031.socket_idname = "NodeSocketGeometry"
    #node Reroute.033
    reroute_033 = group.nodes.new("NodeReroute")
    reroute_033.name = "Reroute.033"
    reroute_033.socket_idname = "NodeSocketFloat"
    #node Reroute.034
    reroute_034 = group.nodes.new("NodeReroute")
    reroute_034.name = "Reroute.034"
    reroute_034.socket_idname = "NodeSocketFloat"
    #node Math.014
    math_014 = group.nodes.new("ShaderNodeMath")
    math_014.name = "Math.014"
    math_014.operation = 'MULTIPLY'
    math_014.use_clamp = False
    #Value_001
    math_014.inputs[1].default_value = 48.0

    #node Compare.005
    compare_005 = group.nodes.new("FunctionNodeCompare")
    compare_005.name = "Compare.005"
    compare_005.data_type = 'FLOAT'
    compare_005.mode = 'ELEMENT'
    compare_005.operation = 'GREATER_THAN'
    #B
    compare_005.inputs[1].default_value = 0.0

    #node Named Attribute.012
    named_attribute_012 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_012.name = "Named Attribute.012"
    named_attribute_012.data_type = 'FLOAT'
    #Name
    named_attribute_012.inputs[0].default_value = "sediment"

    #node Compare.004
    compare_004 = group.nodes.new("FunctionNodeCompare")
    compare_004.name = "Compare.004"
    compare_004.data_type = 'FLOAT'
    compare_004.mode = 'ELEMENT'
    compare_004.operation = 'GREATER_THAN'

    #node Boolean Math
    boolean_math = group.nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.operation = 'OR'

    #node Math.015
    math_015 = group.nodes.new("ShaderNodeMath")
    math_015.name = "Math.015"
    math_015.operation = 'MINIMUM'
    math_015.use_clamp = False

    #node Named Attribute.013
    named_attribute_013 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_013.name = "Named Attribute.013"
    named_attribute_013.data_type = 'FLOAT'
    #Name
    named_attribute_013.inputs[0].default_value = "sediment"

    #node Named Attribute.014
    named_attribute_014 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_014.name = "Named Attribute.014"
    named_attribute_014.data_type = 'FLOAT'
    #Name
    named_attribute_014.inputs[0].default_value = "sediment"

    #node Math.016
    math_016 = group.nodes.new("ShaderNodeMath")
    math_016.name = "Math.016"
    math_016.operation = 'SUBTRACT'
    math_016.use_clamp = False

    #node Math.017
    math_017 = group.nodes.new("ShaderNodeMath")
    math_017.label = "Deposit Speed"
    math_017.name = "Math.017"
    math_017.use_custom_color = True
    math_017.color = (0.14086699485778809, 0.38403424620628357, 0.5131794214248657)
    math_017.operation = 'MULTIPLY'
    math_017.use_clamp = False

    #node Reroute.040
    reroute_040 = group.nodes.new("NodeReroute")
    reroute_040.name = "Reroute.040"
    reroute_040.socket_idname = "NodeSocketBool"
    #node Reroute.038
    reroute_038 = group.nodes.new("NodeReroute")
    reroute_038.name = "Reroute.038"
    reroute_038.socket_idname = "NodeSocketFloat"
    #node Switch
    switch = group.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'FLOAT'

    #node Frame.004
    frame_004 = group.nodes.new("NodeFrame")
    frame_004.label = "Deposit Amount"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True

    #node Frame.003
    frame_003 = group.nodes.new("NodeFrame")
    frame_003.label = "Erode Amount"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True

    #node Reroute.039
    reroute_039 = group.nodes.new("NodeReroute")
    reroute_039.name = "Reroute.039"
    reroute_039.socket_idname = "NodeSocketFloat"
    #node Reroute.042
    reroute_042 = group.nodes.new("NodeReroute")
    reroute_042.name = "Reroute.042"
    reroute_042.socket_idname = "NodeSocketBool"
    #node Reroute.043
    reroute_043 = group.nodes.new("NodeReroute")
    reroute_043.name = "Reroute.043"
    reroute_043.socket_idname = "NodeSocketFloat"
    #node Reroute.041
    reroute_041 = group.nodes.new("NodeReroute")
    reroute_041.name = "Reroute.041"
    reroute_041.socket_idname = "NodeSocketBool"
    #node Frame.005
    frame_005 = group.nodes.new("NodeFrame")
    frame_005.label = "Should Deposit"
    frame_005.name = "Frame.005"
    frame_005.label_size = 20
    frame_005.shrink = True

    #node Switch.001
    switch_001 = group.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.input_type = 'FLOAT'

    #node Reroute.044
    reroute_044 = group.nodes.new("NodeReroute")
    reroute_044.name = "Reroute.044"
    reroute_044.socket_idname = "NodeSocketFloat"
    #node Reroute.045
    reroute_045 = group.nodes.new("NodeReroute")
    reroute_045.name = "Reroute.045"
    reroute_045.socket_idname = "NodeSocketFloat"
    #node Reroute.046
    reroute_046 = group.nodes.new("NodeReroute")
    reroute_046.name = "Reroute.046"
    reroute_046.socket_idname = "NodeSocketFloat"
    #node Math.018
    math_018 = group.nodes.new("ShaderNodeMath")
    math_018.name = "Math.018"
    math_018.operation = 'MULTIPLY'
    math_018.use_clamp = False
    #Value_001
    math_018.inputs[1].default_value = -1.0

    #node Store Named Attribute.011
    store_named_attribute_011 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_011.name = "Store Named Attribute.011"
    store_named_attribute_011.data_type = 'FLOAT'
    store_named_attribute_011.domain = 'POINT'
    #Selection
    store_named_attribute_011.inputs[1].default_value = True
    #Name
    store_named_attribute_011.inputs[2].default_value = "water"

    #node Named Attribute.015
    named_attribute_015 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_015.name = "Named Attribute.015"
    named_attribute_015.data_type = 'FLOAT'
    #Name
    named_attribute_015.inputs[0].default_value = "water"

    #node Math.020
    math_020 = group.nodes.new("ShaderNodeMath")
    math_020.label = "Evaporate Speed"
    math_020.name = "Math.020"
    math_020.use_custom_color = True
    math_020.color = (0.14086699485778809, 0.38403424620628357, 0.5131794214248657)
    math_020.operation = 'SUBTRACT'
    math_020.use_clamp = False
    #Value
    math_020.inputs[0].default_value = 1.0
    #Value_001
    math_020.inputs[1].default_value = 0.07999999821186066

    #node Math.019
    math_019 = group.nodes.new("ShaderNodeMath")
    math_019.name = "Math.019"
    math_019.operation = 'MULTIPLY'
    math_019.use_clamp = False

    #node Reroute.006
    reroute_006 = group.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.hide = True
    reroute_006.socket_idname = "NodeSocketFloat"
    #node Reroute.012
    reroute_012 = group.nodes.new("NodeReroute")
    reroute_012.name = "Reroute.012"
    reroute_012.hide = True
    reroute_012.socket_idname = "NodeSocketFloat"
    #node Named Attribute.016
    named_attribute_016 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_016.name = "Named Attribute.016"
    named_attribute_016.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute_016.inputs[0].default_value = "vel_surface"

    #node Named Attribute.017
    named_attribute_017 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_017.name = "Named Attribute.017"
    named_attribute_017.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute_017.inputs[0].default_value = "vel"

    #node Position.006
    position_006 = group.nodes.new("GeometryNodeInputPosition")
    position_006.name = "Position.006"

    #node Separate XYZ.003
    separate_xyz_003 = group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_003.name = "Separate XYZ.003"

    #node Compare
    compare = group.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'GREATER_THAN'

    #node Boolean Math.001
    boolean_math_001 = group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.operation = 'OR'

    #node Compare.006
    compare_006 = group.nodes.new("FunctionNodeCompare")
    compare_006.name = "Compare.006"
    compare_006.data_type = 'FLOAT'
    compare_006.mode = 'ELEMENT'
    compare_006.operation = 'LESS_THAN'

    #node Boolean Math.002
    boolean_math_002 = group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_002.name = "Boolean Math.002"
    boolean_math_002.operation = 'OR'

    #node Compare.007
    compare_007 = group.nodes.new("FunctionNodeCompare")
    compare_007.name = "Compare.007"
    compare_007.data_type = 'FLOAT'
    compare_007.mode = 'ELEMENT'
    compare_007.operation = 'GREATER_THAN'

    #node Compare.008
    compare_008 = group.nodes.new("FunctionNodeCompare")
    compare_008.name = "Compare.008"
    compare_008.data_type = 'FLOAT'
    compare_008.mode = 'ELEMENT'
    compare_008.operation = 'LESS_THAN'

    #node Boolean Math.003
    boolean_math_003 = group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_003.name = "Boolean Math.003"
    boolean_math_003.operation = 'OR'

    #node Boolean Math.004
    boolean_math_004 = group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_004.name = "Boolean Math.004"
    boolean_math_004.operation = 'OR'

    #node Store Named Attribute.012
    store_named_attribute_012 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_012.name = "Store Named Attribute.012"
    store_named_attribute_012.data_type = 'FLOAT'
    store_named_attribute_012.domain = 'POINT'
    #Name
    store_named_attribute_012.inputs[2].default_value = "erosion"

    #node Named Attribute.018
    named_attribute_018 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_018.name = "Named Attribute.018"
    named_attribute_018.data_type = 'FLOAT'
    #Name
    named_attribute_018.inputs[0].default_value = "erosion"

    #node Math.022
    math_022 = group.nodes.new("ShaderNodeMath")
    math_022.name = "Math.022"
    math_022.operation = 'ADD'
    math_022.use_clamp = False

    #node Reroute.001
    reroute_001 = group.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketGeometry"
    #node Sample Index.004
    sample_index_004 = group.nodes.new("GeometryNodeSampleIndex")
    sample_index_004.name = "Sample Index.004"
    sample_index_004.clamp = False
    sample_index_004.data_type = 'FLOAT'
    sample_index_004.domain = 'POINT'

    #node Sample Nearest.006
    sample_nearest_006 = group.nodes.new("GeometryNodeSampleNearest")
    sample_nearest_006.name = "Sample Nearest.006"
    sample_nearest_006.domain = 'POINT'
    #Sample Position
    sample_nearest_006.inputs[1].default_value = (0.0, 0.0, 0.0)

    #node Reroute.025
    reroute_025 = group.nodes.new("NodeReroute")
    reroute_025.name = "Reroute.025"
    reroute_025.socket_idname = "NodeSocketGeometry"
    #node Reroute.032
    reroute_032 = group.nodes.new("NodeReroute")
    reroute_032.name = "Reroute.032"
    reroute_032.socket_idname = "NodeSocketFloat"
    #node Reroute.036
    reroute_036 = group.nodes.new("NodeReroute")
    reroute_036.name = "Reroute.036"
    reroute_036.socket_idname = "NodeSocketFloat"
    #node Named Attribute.019
    named_attribute_019 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_019.name = "Named Attribute.019"
    named_attribute_019.data_type = 'FLOAT'
    #Name
    named_attribute_019.inputs[0].default_value = "erosion"

    #node Attribute Statistic
    attribute_statistic = group.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic.name = "Attribute Statistic"
    attribute_statistic.data_type = 'FLOAT'
    attribute_statistic.domain = 'POINT'
    #Selection
    attribute_statistic.inputs[1].default_value = True

    #node Map Range
    map_range = group.nodes.new("ShaderNodeMapRange")
    map_range.name = "Map Range"
    map_range.clamp = False
    map_range.data_type = 'FLOAT'
    map_range.interpolation_type = 'LINEAR'
    #From Min
    map_range.inputs[1].default_value = 0.0
    #To Min
    map_range.inputs[3].default_value = 0.0
    #To Max
    map_range.inputs[4].default_value = 1.0

    #node Store Named Attribute.013
    store_named_attribute_013 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_013.name = "Store Named Attribute.013"
    store_named_attribute_013.data_type = 'FLOAT'
    store_named_attribute_013.domain = 'POINT'
    #Selection
    store_named_attribute_013.inputs[1].default_value = True
    #Name
    store_named_attribute_013.inputs[2].default_value = "sediment"

    #node Named Attribute.020
    named_attribute_020 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_020.name = "Named Attribute.020"
    named_attribute_020.data_type = 'FLOAT'
    #Name
    named_attribute_020.inputs[0].default_value = "sediment"

    #node Math.023
    math_023 = group.nodes.new("ShaderNodeMath")
    math_023.name = "Math.023"
    math_023.operation = 'ADD'
    math_023.use_clamp = False

    #node Sample Index.005
    sample_index_005 = group.nodes.new("GeometryNodeSampleIndex")
    sample_index_005.name = "Sample Index.005"
    sample_index_005.clamp = False
    sample_index_005.data_type = 'FLOAT'
    sample_index_005.domain = 'POINT'

    #node Sample Nearest.007
    sample_nearest_007 = group.nodes.new("GeometryNodeSampleNearest")
    sample_nearest_007.name = "Sample Nearest.007"
    sample_nearest_007.domain = 'POINT'
    #Sample Position
    sample_nearest_007.inputs[1].default_value = (0.0, 0.0, 0.0)

    #node Reroute.035
    reroute_035 = group.nodes.new("NodeReroute")
    reroute_035.name = "Reroute.035"
    reroute_035.socket_idname = "NodeSocketGeometry"
    #node Reroute.037
    reroute_037 = group.nodes.new("NodeReroute")
    reroute_037.name = "Reroute.037"
    reroute_037.socket_idname = "NodeSocketFloat"
    #node Named Attribute.021
    named_attribute_021 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_021.name = "Named Attribute.021"
    named_attribute_021.data_type = 'FLOAT'
    #Name
    named_attribute_021.inputs[0].default_value = "sediment"

    #node Attribute Statistic.001
    attribute_statistic_001 = group.nodes.new("GeometryNodeAttributeStatistic")
    attribute_statistic_001.name = "Attribute Statistic.001"
    attribute_statistic_001.data_type = 'FLOAT'
    attribute_statistic_001.domain = 'POINT'
    #Selection
    attribute_statistic_001.inputs[1].default_value = True

    #node Map Range.001
    map_range_001 = group.nodes.new("ShaderNodeMapRange")
    map_range_001.name = "Map Range.001"
    map_range_001.clamp = False
    map_range_001.data_type = 'FLOAT'
    map_range_001.interpolation_type = 'LINEAR'
    #From Max
    map_range_001.inputs[2].default_value = 1.0
    #To Min
    map_range_001.inputs[3].default_value = 0.0
    #To Max
    map_range_001.inputs[4].default_value = 1.0

    #node Reroute.047
    reroute_047 = group.nodes.new("NodeReroute")
    reroute_047.name = "Reroute.047"
    reroute_047.socket_idname = "NodeSocketGeometry"
    #node Reroute.048
    reroute_048 = group.nodes.new("NodeReroute")
    reroute_048.name = "Reroute.048"
    reroute_048.socket_idname = "NodeSocketGeometry"
    #node Switch.002
    switch_002 = group.nodes.new("GeometryNodeSwitch")
    switch_002.name = "Switch.002"
    switch_002.input_type = 'FLOAT'
    #True
    switch_002.inputs[2].default_value = 0.0

    #node Switch.003
    switch_003 = group.nodes.new("GeometryNodeSwitch")
    switch_003.name = "Switch.003"
    switch_003.input_type = 'FLOAT'
    #False
    switch_003.inputs[1].default_value = 0.0

    #node Reroute.049
    reroute_049 = group.nodes.new("NodeReroute")
    reroute_049.name = "Reroute.049"
    reroute_049.socket_idname = "NodeSocketFloat"
    #node Delete Geometry.001
    delete_geometry_001 = group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_001.name = "Delete Geometry.001"
    delete_geometry_001.domain = 'POINT'
    delete_geometry_001.mode = 'ALL'

    #node Compare.009
    compare_009 = group.nodes.new("FunctionNodeCompare")
    compare_009.name = "Compare.009"
    compare_009.data_type = 'INT'
    compare_009.mode = 'ELEMENT'
    compare_009.operation = 'NOT_EQUAL'
    #A_INT
    compare_009.inputs[2].default_value = 5923

    #node Index.003
    index_003 = group.nodes.new("GeometryNodeInputIndex")
    index_003.name = "Index.003"

    #node Reroute.051
    reroute_051 = group.nodes.new("NodeReroute")
    reroute_051.name = "Reroute.051"
    reroute_051.socket_idname = "NodeSocketGeometry"
    #node Vector Math.007
    vector_math_007 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.operation = 'SCALE'
    #Scale
    vector_math_007.inputs[3].default_value = 1.0

    #node Separate XYZ.004
    separate_xyz_004 = group.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_004.name = "Separate XYZ.004"

    #node Compare.010
    compare_010 = group.nodes.new("FunctionNodeCompare")
    compare_010.name = "Compare.010"
    compare_010.data_type = 'FLOAT'
    compare_010.mode = 'ELEMENT'
    compare_010.operation = 'LESS_THAN'
    #B
    compare_010.inputs[1].default_value = 0.0

    #node Combine XYZ
    combine_xyz = group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    #X
    combine_xyz.inputs[0].default_value = 0.0
    #Z
    combine_xyz.inputs[2].default_value = 0.0

    #node Switch.004
    switch_004 = group.nodes.new("GeometryNodeSwitch")
    switch_004.name = "Switch.004"
    switch_004.input_type = 'VECTOR'

    #node Combine XYZ.004
    combine_xyz_004 = group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_004.name = "Combine XYZ.004"
    #X
    combine_xyz_004.inputs[0].default_value = 0.0
    #Y
    combine_xyz_004.inputs[1].default_value = 0.0

    #node Math.008
    math_008 = group.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'MULTIPLY'
    math_008.use_clamp = False
    #Value_001
    math_008.inputs[1].default_value = -1.0

    #node Named Attribute.022
    named_attribute_022 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_022.name = "Named Attribute.022"
    named_attribute_022.data_type = 'BOOLEAN'
    #Name
    named_attribute_022.inputs[0].default_value = "start_selection"

    #node Vector Math.010
    vector_math_010 = group.nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.operation = 'SCALE'

    #node Boolean Math.005
    boolean_math_005 = group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_005.name = "Boolean Math.005"
    boolean_math_005.operation = 'NOT'

    #node Boolean Math.006
    boolean_math_006 = group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_006.name = "Boolean Math.006"
    boolean_math_006.operation = 'NOT'

    #node Boolean Math.007
    boolean_math_007 = group.nodes.new("FunctionNodeBooleanMath")
    boolean_math_007.name = "Boolean Math.007"
    boolean_math_007.operation = 'AND'

    #node Delete Geometry.002
    delete_geometry_002 = group.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.domain = 'POINT'
    delete_geometry_002.mode = 'ALL'

    #node Store Named Attribute.014
    store_named_attribute_014 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_014.name = "Store Named Attribute.014"
    store_named_attribute_014.data_type = 'FLOAT'
    store_named_attribute_014.domain = 'POINT'
    #Selection
    store_named_attribute_014.inputs[1].default_value = True
    #Name
    store_named_attribute_014.inputs[2].default_value = "erosion"

    #node Store Named Attribute.015
    store_named_attribute_015 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_015.name = "Store Named Attribute.015"
    store_named_attribute_015.data_type = 'FLOAT'
    store_named_attribute_015.domain = 'POINT'
    #Selection
    store_named_attribute_015.inputs[1].default_value = True
    #Name
    store_named_attribute_015.inputs[2].default_value = "sediment"

    #node Bake
    bake = group.nodes.new("GeometryNodeBake")
    bake.name = "Bake"
    bake.active_index = 0
    bake.bake_items.clear()
    bake.bake_items.new('GEOMETRY', "Geometry")
    bake.bake_items[0].attribute_domain = 'POINT'

    #node Set Material
    set_material = group.nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    #Selection
    set_material.inputs[1].default_value = True
    if "PBR Earth" in bpy.data.materials:
        set_material.inputs[2].default_value = bpy.data.materials["PBR Earth"]

    #node Math
    math = group.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'MULTIPLY'
    math.use_clamp = False
    #Value_001
    math.inputs[1].default_value = -1.0

    #node Reroute.050
    reroute_050 = group.nodes.new("NodeReroute")
    reroute_050.name = "Reroute.050"
    reroute_050.socket_idname = "NodeSocketFloat"
    #node Frame
    frame = group.nodes.new("NodeFrame")
    frame.label = "Delete Out of Bounds Points"
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    #node Group Input
    group_input = group.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[0].hide = True
    group_input.outputs[2].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True
    group_input.outputs[5].hide = True
    group_input.outputs[6].hide = True
    group_input.outputs[7].hide = True
    group_input.outputs[8].hide = True
    group_input.outputs[9].hide = True

    #node Group Input.002
    group_input_002 = group.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[4].hide = True
    group_input_002.outputs[5].hide = True
    group_input_002.outputs[6].hide = True
    group_input_002.outputs[7].hide = True
    group_input_002.outputs[8].hide = True
    group_input_002.outputs[9].hide = True

    #node Group Input.003
    group_input_003 = group.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[2].hide = True
    group_input_003.outputs[4].hide = True
    group_input_003.outputs[5].hide = True
    group_input_003.outputs[6].hide = True
    group_input_003.outputs[7].hide = True
    group_input_003.outputs[8].hide = True
    group_input_003.outputs[9].hide = True

    #node Group Input.004
    group_input_004 = group.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[5].hide = True
    group_input_004.outputs[6].hide = True
    group_input_004.outputs[7].hide = True
    group_input_004.outputs[8].hide = True
    group_input_004.outputs[9].hide = True

    #node Group Input.005
    group_input_005 = group.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.outputs[0].hide = True
    group_input_005.outputs[1].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[3].hide = True
    group_input_005.outputs[4].hide = True
    group_input_005.outputs[6].hide = True
    group_input_005.outputs[7].hide = True
    group_input_005.outputs[8].hide = True
    group_input_005.outputs[9].hide = True

    #node Group Input.006
    group_input_006 = group.nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input.006"
    group_input_006.outputs[0].hide = True
    group_input_006.outputs[1].hide = True
    group_input_006.outputs[2].hide = True
    group_input_006.outputs[3].hide = True
    group_input_006.outputs[4].hide = True
    group_input_006.outputs[5].hide = True
    group_input_006.outputs[7].hide = True
    group_input_006.outputs[8].hide = True
    group_input_006.outputs[9].hide = True

    #node Group Input.007
    group_input_007 = group.nodes.new("NodeGroupInput")
    group_input_007.name = "Group Input.007"
    group_input_007.outputs[0].hide = True
    group_input_007.outputs[1].hide = True
    group_input_007.outputs[2].hide = True
    group_input_007.outputs[3].hide = True
    group_input_007.outputs[4].hide = True
    group_input_007.outputs[5].hide = True
    group_input_007.outputs[6].hide = True
    group_input_007.outputs[8].hide = True
    group_input_007.outputs[9].hide = True

    #node Switch.005
    switch_005 = group.nodes.new("GeometryNodeSwitch")
    switch_005.name = "Switch.005"
    switch_005.input_type = 'GEOMETRY'

    #node Group Input.008
    group_input_008 = group.nodes.new("NodeGroupInput")
    group_input_008.name = "Group Input.008"
    group_input_008.outputs[0].hide = True
    group_input_008.outputs[1].hide = True
    group_input_008.outputs[2].hide = True
    group_input_008.outputs[3].hide = True
    group_input_008.outputs[4].hide = True
    group_input_008.outputs[5].hide = True
    group_input_008.outputs[6].hide = True
    group_input_008.outputs[7].hide = True
    group_input_008.outputs[9].hide = True

    #node Separate Components.002
    separate_components_002 = group.nodes.new("GeometryNodeSeparateComponents")
    separate_components_002.name = "Separate Components.002"

    #node Join Geometry.002
    join_geometry_002 = group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"

    #node Reroute.052
    reroute_052 = group.nodes.new("NodeReroute")
    reroute_052.name = "Reroute.052"
    reroute_052.socket_idname = "NodeSocketGeometry"
    #node Reroute.053
    reroute_053 = group.nodes.new("NodeReroute")
    reroute_053.name = "Reroute.053"
    reroute_053.socket_idname = "NodeSocketGeometry"
    #node Join Geometry.003
    join_geometry_003 = group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_003.name = "Join Geometry.003"

    #Process zone input Simulation Input
    simulation_input.pair_with_output(simulation_output)

    #Skip
    simulation_output.inputs[0].default_value = False




    #Set parents
    named_attribute_002.parent = frame_001
    named_attribute_005.parent = frame_001
    vector_math_002.parent = frame_001
    named_attribute_008.parent = frame
    compare_003.parent = frame
    delete_geometry.parent = frame
    separate_xyz_001.parent = frame_001
    named_attribute_009.parent = frame_002
    vector_math_005.parent = frame_002
    named_attribute_010.parent = frame_002
    math_009.parent = frame_002
    math_010.parent = frame_002
    math_011.parent = frame_002
    math_012.parent = frame_002
    math_001.parent = frame_003
    named_attribute_003.parent = frame_003
    math_003.parent = frame_003
    math_005.parent = frame_003
    math_006.parent = frame_003
    math_014.parent = frame_002
    named_attribute_012.parent = frame_005
    compare_004.parent = frame_005
    boolean_math.parent = frame_005
    math_015.parent = frame_004
    named_attribute_013.parent = frame_004
    named_attribute_014.parent = frame_004
    math_016.parent = frame_004
    math_017.parent = frame_004
    switch.parent = frame_004
    reroute_042.parent = frame_005
    named_attribute_016.parent = frame_001
    position_006.parent = frame
    separate_xyz_003.parent = frame
    compare.parent = frame
    boolean_math_001.parent = frame
    compare_006.parent = frame
    boolean_math_002.parent = frame
    compare_007.parent = frame
    compare_008.parent = frame
    boolean_math_003.parent = frame
    boolean_math_004.parent = frame
    math.parent = frame
    reroute_050.parent = frame
    group_input.parent = frame_002
    group_input_002.parent = frame_003
    group_input_003.parent = frame_004
    group_input_004.parent = frame
    group_input_005.parent = frame

    #Set locations
    group_input_001.location = (-170.03433227539062, -122.71343994140625)
    scene_time.location = (551.5855712890625, -493.7774658203125)
    simulation_input.location = (647.9627685546875, -111.11997985839844)
    distribute_points_on_faces.location = (538.2574462890625, -268.9172058105469)
    join_geometry.location = (1312.196044921875, -210.73397827148438)
    separate_components.location = (1542.723876953125, -214.64979553222656)
    reroute_002.location = (1716.08154296875, -169.5751953125)
    math_004.location = (2016.6953125, -428.8712158203125)
    named_attribute_001.location = (2013.650634765625, -597.5339965820312)
    store_named_attribute.location = (1804.8660888671875, -221.9466094970703)
    reroute_004.location = (2268.453125, -199.00198364257812)
    vector_math_001.location = (1800.987548828125, -436.5976257324219)
    vector_math_008.location = (3949.562255859375, -312.9105224609375)
    named_attribute.location = (1798.7974853515625, -648.2978515625)
    store_named_attribute_001.location = (2019.71923828125, -222.644775390625)
    normal.location = (3761.953369140625, -249.01336669921875)
    reroute_007.location = (2298.95849609375, -169.5751953125)
    group_output.location = (12029.69921875, -739.7587890625)
    simulation_output.location = (9403.0703125, -146.4142303466797)
    join_geometry_001.location = (9226.61328125, -273.4736022949219)
    reroute.location = (9139.224609375, -169.5751953125)
    sample_nearest_001.location = (3751.203369140625, -517.9138793945312)
    sample_index_001.location = (3760.195068359375, -308.20025634765625)
    vector_math_009.location = (3949.522216796875, -491.615966796875)
    reroute_010.location = (2758.451904296875, -169.5751953125)
    sample_nearest_004.location = (2360.00634765625, -448.3284912109375)
    sample_index_002.location = (2361.05810546875, -231.55184936523438)
    reroute_013.location = (4316.01953125, -199.00198364257812)
    position_001.location = (2171.034423828125, -490.83563232421875)
    store_named_attribute_003.location = (2572.611572265625, -234.74822998046875)
    reroute_015.location = (2519.199462890625, -199.00198364257812)
    sample_nearest_005.location = (5313.64013671875, -458.9043884277344)
    sample_index_003.location = (5314.69189453125, -242.1277313232422)
    position_002.location = (5123.91357421875, -462.88507080078125)
    set_position_001.location = (4123.07470703125, -216.64276123046875)
    reroute_016.location = (5199.91455078125, -169.5751953125)
    store_named_attribute_004.location = (5572.9345703125, -253.88832092285156)
    reroute_017.location = (5785.54833984375, -199.00198364257812)
    geometry_proximity.location = (5800.22265625, -391.47467041015625)
    sample_nearest.location = (5803.38427734375, -251.07147216796875)
    compare_001.location = (5996.9970703125, -281.2061462402344)
    index.location = (5991.91015625, -450.3431091308594)
    reroute_009.location = (5746.0390625, -169.5751953125)
    reroute_011.location = (6148.58935546875, -169.5751953125)
    geometry_proximity_001.location = (2792.692138671875, -382.2010498046875)
    sample_nearest_002.location = (2795.853759765625, -241.79786682128906)
    compare_002.location = (2973.644287109375, -277.1072998046875)
    index_001.location = (2972.7333984375, -445.38861083984375)
    reroute_014.location = (2752.221923828125, -204.327392578125)
    store_named_attribute_005.location = (3156.748291015625, -235.90538024902344)
    reroute_018.location = (3106.040771484375, -169.5751953125)
    reroute_020.location = (3348.800537109375, -169.5751953125)
    store_named_attribute_006.location = (6192.5439453125, -222.24676513671875)
    reroute_021.location = (6390.58203125, -169.5751953125)
    named_attribute_002.location = (30.265625, -40.12353515625)
    named_attribute_005.location = (33.794921875, -170.799560546875)
    vector_math_002.location = (219.07177734375, -86.344482421875)
    reroute_024.location = (7847.8701171875, -169.5751953125)
    sample_index.location = (7641.41796875, -223.1723175048828)
    sample_nearest_003.location = (7642.30078125, -436.8452453613281)
    reroute_023.location = (7566.42529296875, -199.00198364257812)
    named_attribute_006.location = (7916.8056640625, -424.9924011230469)
    set_position_002.location = (7915.7607421875, -262.7753601074219)
    set_position_003.location = (7386.18603515625, -239.64413452148438)
    named_attribute_007.location = (7006.95654296875, -264.410888671875)
    vector_math_004.location = (7201.60791015625, -297.4332275390625)
    reroute_026.location = (7315.15673828125, -199.00198364257812)
    named_attribute_008.location = (370.4423828125, -757.177978515625)
    compare_003.location = (536.412109375, -744.8145751953125)
    delete_geometry.location = (1176.05908203125, -778.2161865234375)
    reroute_022.location = (6655.55322265625, -199.00198364257812)
    reroute_027.location = (6893.0615234375, -199.00198364257812)
    separate_components_001.location = (9640.9375, -146.65383911132812)
    blur_attribute.location = (9666.513671875, -477.4272155761719)
    set_position_004.location = (10066.208984375, -215.1748046875)
    position_003.location = (9253.873046875, -484.8003234863281)
    separate_xyz.location = (9452.107421875, -453.01214599609375)
    combine_xyz_001.location = (9888.861328125, -295.83734130859375)
    set_shade_smooth.location = (10264.091796875, -288.6678466796875)
    separate_xyz_001.location = (398.3642578125, -99.314697265625)
    combine_xyz_002.location = (7648.0615234375, -588.759765625)
    named_attribute_009.location = (30.13330078125, -39.94854736328125)
    vector_math_005.location = (218.3984375, -43.86566162109375)
    store_named_attribute_007.location = (954.9766235351562, -264.1739807128906)
    named_attribute_010.location = (583.470703125, -289.01995849609375)
    math_009.location = (417.70166015625, -261.53057861328125)
    math_010.location = (617.21435546875, -105.60162353515625)
    math_011.location = (789.6103515625, -209.84112548828125)
    math_012.location = (973.8564453125, -187.44830322265625)
    store_named_attribute_008.location = (1148.62744140625, -260.35528564453125)
    set_point_radius.location = (764.3028564453125, -305.85089111328125)
    reroute_005.location = (4125.03857421875, -169.5751953125)
    raycast.location = (4364.65771484375, -256.3837585449219)
    reroute_008.location = (4326.00537109375, -169.5751953125)
    reroute_019.location = (4494.2587890625, -199.00198364257812)
    raycast_001.location = (4360.73779296875, -576.6879272460938)
    vector_math_003.location = (4141.33251953125, -521.703125)
    set_position_006.location = (4560.54052734375, -195.98602294921875)
    set_position_007.location = (4742.6123046875, -238.72994995117188)
    store_named_attribute_002.location = (3503.80078125, -242.9504852294922)
    capture_attribute.location = (3329.61083984375, -247.91421508789062)
    position_004.location = (3333.482666015625, -383.5377197265625)
    store_named_attribute_009.location = (5236.76806640625, 89.56702423095703)
    position_005.location = (4836.01220703125, 72.18522644042969)
    named_attribute_004.location = (4836.01171875, 2.0148162841796875)
    vector_math_006.location = (5053.92333984375, 54.59397888183594)
    reroute_003.location = (3292.205078125, -209.5828857421875)
    reroute_028.location = (3677.57861328125, -169.5751953125)
    reroute_029.location = (3671.721923828125, -206.49264526367188)
    reroute_030.location = (4094.643310546875, -205.20034790039062)
    frame_001.location = (4791.0, -1138.0)
    frame_002.location = (5031.0, -682.0)
    math_001.location = (215.94189453125, -209.87554931640625)
    named_attribute_003.location = (29.81982421875, -336.77862548828125)
    math_003.location = (593.0556640625, -77.08746337890625)
    math_005.location = (349.0888671875, -40.34130859375)
    math_006.location = (394.7890625, -213.61041259765625)
    store_named_attribute_010.location = (8743.078125, -240.2434539794922)
    named_attribute_011.location = (8725.423828125, -738.410888671875)
    math_007.location = (8729.798828125, -547.8927612304688)
    reroute_031.location = (8701.16796875, -199.00198364257812)
    reroute_033.location = (6466.80078125, -1154.011474609375)
    reroute_034.location = (5398.95849609375, -1154.011474609375)
    math_014.location = (402.62255859375, -95.56427001953125)
    compare_005.location = (5823.96826171875, -1166.802490234375)
    named_attribute_012.location = (29.8134765625, -95.85693359375)
    compare_004.location = (199.27490234375, -113.3831787109375)
    boolean_math.location = (387.62353515625, -39.9820556640625)
    math_015.location = (239.71044921875, -73.797607421875)
    named_attribute_013.location = (30.02001953125, -87.7703857421875)
    named_attribute_014.location = (39.42431640625, -254.103759765625)
    math_016.location = (243.42822265625, -259.1304931640625)
    math_017.location = (431.46728515625, -238.3238525390625)
    reroute_040.location = (6014.1337890625, -1174.27294921875)
    reroute_038.location = (6169.1279296875, -1154.011474609375)
    switch.location = (637.23095703125, -39.544677734375)
    frame_004.location = (6031.0, -1281.0)
    frame_003.location = (6238.0, -644.0)
    reroute_039.location = (5746.23291015625, -1154.011474609375)
    reroute_042.location = (335.1318359375, -80.27294921875)
    reroute_043.location = (6222.8095703125, -1208.505126953125)
    reroute_041.location = (6598.32763671875, -1174.27294921875)
    frame_005.location = (6886.0, -1094.0)
    switch_001.location = (7471.1201171875, -1078.8671875)
    reroute_044.location = (7421.60498046875, -1424.7720947265625)
    reroute_045.location = (6864.33837890625, -1424.7720947265625)
    reroute_046.location = (6858.251953125, -1208.505126953125)
    math_018.location = (7169.0615234375, -936.0931396484375)
    store_named_attribute_011.location = (8979.287109375, -224.4122772216797)
    named_attribute_015.location = (8960.70703125, -699.4341430664062)
    math_020.location = (8958.0078125, -865.4393310546875)
    math_019.location = (8976.869140625, -493.2763671875)
    reroute_006.location = (7709.94287109375, -950.8627319335938)
    reroute_012.location = (8676.9921875, -950.8627319335938)
    named_attribute_016.location = (191.40576171875, -260.2235107421875)
    named_attribute_017.location = (3504.642822265625, -540.9398193359375)
    position_006.location = (165.89453125, -619.0777587890625)
    separate_xyz_003.location = (337.75439453125, -577.708984375)
    compare.location = (544.61181640625, -583.3834228515625)
    boolean_math_001.location = (736.0185546875, -650.3409423828125)
    compare_006.location = (573.29150390625, -400.1956481933594)
    boolean_math_002.location = (912.2353515625, -417.375732421875)
    compare_007.location = (581.20458984375, -40.471435546875)
    compare_008.location = (567.04443359375, -223.06585693359375)
    boolean_math_003.location = (848.6767578125, -185.28765869140625)
    boolean_math_004.location = (1080.58544921875, -425.2461853027344)
    store_named_attribute_012.location = (8130.99951171875, -267.3162536621094)
    named_attribute_018.location = (8131.17578125, -664.1825561523438)
    math_022.location = (8137.36328125, -480.3013916015625)
    reroute_001.location = (8335.7998046875, -169.5751953125)
    sample_index_004.location = (7906.44970703125, -575.0179443359375)
    sample_nearest_006.location = (7907.33251953125, -788.69091796875)
    reroute_025.location = (7801.77099609375, -237.21517944335938)
    reroute_032.location = (7108.55810546875, -807.4297485351562)
    reroute_036.location = (7796.74072265625, -807.4297485351562)
    named_attribute_019.location = (10229.638671875, -476.2855529785156)
    attribute_statistic.location = (10427.8828125, -553.242919921875)
    map_range.location = (10635.953125, -526.700927734375)
    store_named_attribute_013.location = (8524.3125, -241.59555053710938)
    named_attribute_020.location = (8506.91796875, -653.3528442382812)
    math_023.location = (8513.10546875, -469.4716491699219)
    sample_index_005.location = (8328.1455078125, -297.50543212890625)
    sample_nearest_007.location = (8329.0283203125, -511.17840576171875)
    reroute_035.location = (8284.591796875, -240.26339721679688)
    reroute_037.location = (8234.1279296875, -1316.6240234375)
    named_attribute_021.location = (10220.16015625, -835.441650390625)
    attribute_statistic_001.location = (10414.93359375, -929.76318359375)
    map_range_001.location = (10626.474609375, -885.8569946289062)
    reroute_047.location = (8485.93359375, -169.5751953125)
    reroute_048.location = (8689.79296875, -169.5751953125)
    switch_002.location = (7459.3515625, -909.685302734375)
    switch_003.location = (7475.3994140625, -1280.172607421875)
    reroute_049.location = (7645.05322265625, -1315.076416015625)
    delete_geometry_001.location = (9554.416015625, -721.1368408203125)
    compare_009.location = (9387.869140625, -739.6175537109375)
    index_003.location = (9192.884765625, -826.6572875976562)
    reroute_051.location = (9194.74609375, -661.7731323242188)
    vector_math_007.location = (7740.7412109375, 139.29629516601562)
    separate_xyz_004.location = (7928.810546875, 180.80023193359375)
    compare_010.location = (8132.09228515625, 196.1452178955078)
    combine_xyz.location = (8423.1015625, 2.643217086791992)
    switch_004.location = (8600.744140625, 232.15069580078125)
    combine_xyz_004.location = (8413.4716796875, 137.56832885742188)
    math_008.location = (8201.666015625, 1.9213371276855469)
    named_attribute_022.location = (8785.736328125, 108.89907836914062)
    vector_math_010.location = (8960.40625, 183.59666442871094)
    boolean_math_005.location = (4630.37158203125, -518.30810546875)
    boolean_math_006.location = (4629.38232421875, -642.1319580078125)
    boolean_math_007.location = (4811.49365234375, -543.0729370117188)
    delete_geometry_002.location = (4974.19287109375, -279.2117614746094)
    store_named_attribute_014.location = (10924.4716796875, -413.4552307128906)
    store_named_attribute_015.location = (11112.0380859375, -481.20391845703125)
    bake.location = (11328.6298828125, -429.2044372558594)
    set_material.location = (11514.7890625, -464.0843811035156)
    math.location = (284.6298828125, -317.63934326171875)
    reroute_050.location = (473.14208984375, -181.861328125)
    frame.location = (5531.0, 782.0)
    group_input.location = (973.208984375, -358.92724609375)
    group_input_002.location = (390.97998046875, -399.76513671875)
    group_input_003.location = (424.94140625, -406.171142578125)
    group_input_004.location = (29.72119140625, -326.2218017578125)
    group_input_005.location = (705.3974609375, -834.64892578125)
    group_input_006.location = (550.5271606445312, -603.01806640625)
    group_input_007.location = (1805.4642333984375, -804.4560546875)
    switch_005.location = (9840.1162109375, -18.061386108398438)
    group_input_008.location = (9839.380859375, -180.47802734375)
    separate_components_002.location = (13.0345458984375, -86.63311004638672)
    join_geometry_002.location = (301.9033508300781, -891.2222900390625)
    reroute_052.location = (926.023193359375, -1763.1114501953125)
    reroute_053.location = (11333.4765625, -1853.738037109375)
    join_geometry_003.location = (11744.1796875, -800.4978637695312)

    #Set dimensions
    group_input_001.width, group_input_001.height = 140.0, 100.0
    scene_time.width, scene_time.height = 140.0, 100.0
    simulation_input.width, simulation_input.height = 140.0, 100.0
    distribute_points_on_faces.width, distribute_points_on_faces.height = 167.06024169921875, 100.0
    join_geometry.width, join_geometry.height = 140.0, 100.0
    separate_components.width, separate_components.height = 140.0, 100.0
    reroute_002.width, reroute_002.height = 10.0, 100.0
    math_004.width, math_004.height = 140.0, 100.0
    named_attribute_001.width, named_attribute_001.height = 140.0, 100.0
    store_named_attribute.width, store_named_attribute.height = 140.0, 100.0
    reroute_004.width, reroute_004.height = 10.0, 100.0
    vector_math_001.width, vector_math_001.height = 140.0, 100.0
    vector_math_008.width, vector_math_008.height = 140.0, 100.0
    named_attribute.width, named_attribute.height = 140.0, 100.0
    store_named_attribute_001.width, store_named_attribute_001.height = 140.0, 100.0
    normal.width, normal.height = 140.0, 100.0
    reroute_007.width, reroute_007.height = 10.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    simulation_output.width, simulation_output.height = 140.0, 100.0
    join_geometry_001.width, join_geometry_001.height = 140.0, 100.0
    reroute.width, reroute.height = 10.0, 100.0
    sample_nearest_001.width, sample_nearest_001.height = 140.0, 100.0
    sample_index_001.width, sample_index_001.height = 140.0, 100.0
    vector_math_009.width, vector_math_009.height = 140.0, 100.0
    reroute_010.width, reroute_010.height = 10.0, 100.0
    sample_nearest_004.width, sample_nearest_004.height = 140.0, 100.0
    sample_index_002.width, sample_index_002.height = 140.0, 100.0
    reroute_013.width, reroute_013.height = 10.0, 100.0
    position_001.width, position_001.height = 140.0, 100.0
    store_named_attribute_003.width, store_named_attribute_003.height = 140.0, 100.0
    reroute_015.width, reroute_015.height = 10.0, 100.0
    sample_nearest_005.width, sample_nearest_005.height = 140.0, 100.0
    sample_index_003.width, sample_index_003.height = 140.0, 100.0
    position_002.width, position_002.height = 140.0, 100.0
    set_position_001.width, set_position_001.height = 140.0, 100.0
    reroute_016.width, reroute_016.height = 10.0, 100.0
    store_named_attribute_004.width, store_named_attribute_004.height = 140.0, 100.0
    reroute_017.width, reroute_017.height = 10.0, 100.0
    geometry_proximity.width, geometry_proximity.height = 140.0, 100.0
    sample_nearest.width, sample_nearest.height = 140.0, 100.0
    compare_001.width, compare_001.height = 140.0, 100.0
    index.width, index.height = 140.0, 100.0
    reroute_009.width, reroute_009.height = 10.0, 100.0
    reroute_011.width, reroute_011.height = 10.0, 100.0
    geometry_proximity_001.width, geometry_proximity_001.height = 140.0, 100.0
    sample_nearest_002.width, sample_nearest_002.height = 140.0, 100.0
    compare_002.width, compare_002.height = 140.0, 100.0
    index_001.width, index_001.height = 140.0, 100.0
    reroute_014.width, reroute_014.height = 10.0, 100.0
    store_named_attribute_005.width, store_named_attribute_005.height = 140.0, 100.0
    reroute_018.width, reroute_018.height = 10.0, 100.0
    reroute_020.width, reroute_020.height = 10.0, 100.0
    store_named_attribute_006.width, store_named_attribute_006.height = 140.0, 100.0
    reroute_021.width, reroute_021.height = 10.0, 100.0
    named_attribute_002.width, named_attribute_002.height = 140.0, 100.0
    named_attribute_005.width, named_attribute_005.height = 140.0, 100.0
    vector_math_002.width, vector_math_002.height = 140.0, 100.0
    reroute_024.width, reroute_024.height = 10.0, 100.0
    sample_index.width, sample_index.height = 140.0, 100.0
    sample_nearest_003.width, sample_nearest_003.height = 140.0, 100.0
    reroute_023.width, reroute_023.height = 10.0, 100.0
    named_attribute_006.width, named_attribute_006.height = 140.0, 100.0
    set_position_002.width, set_position_002.height = 140.0, 100.0
    set_position_003.width, set_position_003.height = 140.0, 100.0
    named_attribute_007.width, named_attribute_007.height = 140.0, 100.0
    vector_math_004.width, vector_math_004.height = 140.0, 100.0
    reroute_026.width, reroute_026.height = 10.0, 100.0
    named_attribute_008.width, named_attribute_008.height = 140.0, 100.0
    compare_003.width, compare_003.height = 140.0, 100.0
    delete_geometry.width, delete_geometry.height = 140.0, 100.0
    reroute_022.width, reroute_022.height = 10.0, 100.0
    reroute_027.width, reroute_027.height = 10.0, 100.0
    separate_components_001.width, separate_components_001.height = 140.0, 100.0
    blur_attribute.width, blur_attribute.height = 140.0, 100.0
    set_position_004.width, set_position_004.height = 140.0, 100.0
    position_003.width, position_003.height = 140.0, 100.0
    separate_xyz.width, separate_xyz.height = 140.0, 100.0
    combine_xyz_001.width, combine_xyz_001.height = 140.0, 100.0
    set_shade_smooth.width, set_shade_smooth.height = 140.0, 100.0
    separate_xyz_001.width, separate_xyz_001.height = 140.0, 100.0
    combine_xyz_002.width, combine_xyz_002.height = 140.0, 100.0
    named_attribute_009.width, named_attribute_009.height = 140.0, 100.0
    vector_math_005.width, vector_math_005.height = 140.0, 100.0
    store_named_attribute_007.width, store_named_attribute_007.height = 140.0, 100.0
    named_attribute_010.width, named_attribute_010.height = 140.0, 100.0
    math_009.width, math_009.height = 140.0, 100.0
    math_010.width, math_010.height = 140.0, 100.0
    math_011.width, math_011.height = 140.0, 100.0
    math_012.width, math_012.height = 140.0, 100.0
    store_named_attribute_008.width, store_named_attribute_008.height = 140.0, 100.0
    set_point_radius.width, set_point_radius.height = 140.0, 100.0
    reroute_005.width, reroute_005.height = 10.0, 100.0
    raycast.width, raycast.height = 150.0, 100.0
    reroute_008.width, reroute_008.height = 10.0, 100.0
    reroute_019.width, reroute_019.height = 10.0, 100.0
    raycast_001.width, raycast_001.height = 150.0, 100.0
    vector_math_003.width, vector_math_003.height = 140.0, 100.0
    set_position_006.width, set_position_006.height = 140.0, 100.0
    set_position_007.width, set_position_007.height = 140.0, 100.0
    store_named_attribute_002.width, store_named_attribute_002.height = 140.0, 100.0
    capture_attribute.width, capture_attribute.height = 140.0, 100.0
    position_004.width, position_004.height = 140.0, 100.0
    store_named_attribute_009.width, store_named_attribute_009.height = 140.0, 100.0
    position_005.width, position_005.height = 140.0, 100.0
    named_attribute_004.width, named_attribute_004.height = 140.0, 100.0
    vector_math_006.width, vector_math_006.height = 140.0, 100.0
    reroute_003.width, reroute_003.height = 10.0, 100.0
    reroute_028.width, reroute_028.height = 10.0, 100.0
    reroute_029.width, reroute_029.height = 10.0, 100.0
    reroute_030.width, reroute_030.height = 10.0, 100.0
    frame_001.width, frame_001.height = 568.0, 411.0
    frame_002.width, frame_002.height = 1144.0, 441.0
    math_001.width, math_001.height = 140.0, 100.0
    named_attribute_003.width, named_attribute_003.height = 140.0, 100.0
    math_003.width, math_003.height = 140.0, 100.0
    math_005.width, math_005.height = 140.0, 100.0
    math_006.width, math_006.height = 140.0, 100.0
    store_named_attribute_010.width, store_named_attribute_010.height = 140.0, 100.0
    named_attribute_011.width, named_attribute_011.height = 140.0, 100.0
    math_007.width, math_007.height = 140.0, 100.0
    reroute_031.width, reroute_031.height = 10.0, 100.0
    reroute_033.width, reroute_033.height = 10.0, 100.0
    reroute_034.width, reroute_034.height = 10.0, 100.0
    math_014.width, math_014.height = 140.0, 100.0
    compare_005.width, compare_005.height = 140.0, 100.0
    named_attribute_012.width, named_attribute_012.height = 140.0, 100.0
    compare_004.width, compare_004.height = 140.0, 100.0
    boolean_math.width, boolean_math.height = 140.0, 100.0
    math_015.width, math_015.height = 140.0, 100.0
    named_attribute_013.width, named_attribute_013.height = 140.0, 100.0
    named_attribute_014.width, named_attribute_014.height = 140.0, 100.0
    math_016.width, math_016.height = 140.0, 100.0
    math_017.width, math_017.height = 140.0, 100.0
    reroute_040.width, reroute_040.height = 10.0, 100.0
    reroute_038.width, reroute_038.height = 10.0, 100.0
    switch.width, switch.height = 140.0, 100.0
    frame_004.width, frame_004.height = 807.0, 488.0
    frame_003.width, frame_003.height = 763.0, 488.0
    reroute_039.width, reroute_039.height = 10.0, 100.0
    reroute_042.width, reroute_042.height = 10.0, 100.0
    reroute_043.width, reroute_043.height = 10.0, 100.0
    reroute_041.width, reroute_041.height = 10.0, 100.0
    frame_005.width, frame_005.height = 558.0, 291.0
    switch_001.width, switch_001.height = 140.0, 100.0
    reroute_044.width, reroute_044.height = 10.0, 100.0
    reroute_045.width, reroute_045.height = 10.0, 100.0
    reroute_046.width, reroute_046.height = 10.0, 100.0
    math_018.width, math_018.height = 140.0, 100.0
    store_named_attribute_011.width, store_named_attribute_011.height = 140.0, 100.0
    named_attribute_015.width, named_attribute_015.height = 140.0, 100.0
    math_020.width, math_020.height = 140.0, 100.0
    math_019.width, math_019.height = 140.0, 100.0
    reroute_006.width, reroute_006.height = 10.0, 100.0
    reroute_012.width, reroute_012.height = 10.0, 100.0
    named_attribute_016.width, named_attribute_016.height = 140.0, 100.0
    named_attribute_017.width, named_attribute_017.height = 140.0, 100.0
    position_006.width, position_006.height = 140.0, 100.0
    separate_xyz_003.width, separate_xyz_003.height = 140.0, 100.0
    compare.width, compare.height = 140.0, 100.0
    boolean_math_001.width, boolean_math_001.height = 140.0, 100.0
    compare_006.width, compare_006.height = 140.0, 100.0
    boolean_math_002.width, boolean_math_002.height = 140.0, 100.0
    compare_007.width, compare_007.height = 140.0, 100.0
    compare_008.width, compare_008.height = 140.0, 100.0
    boolean_math_003.width, boolean_math_003.height = 140.0, 100.0
    boolean_math_004.width, boolean_math_004.height = 140.0, 100.0
    store_named_attribute_012.width, store_named_attribute_012.height = 140.0, 100.0
    named_attribute_018.width, named_attribute_018.height = 140.0, 100.0
    math_022.width, math_022.height = 140.0, 100.0
    reroute_001.width, reroute_001.height = 10.0, 100.0
    sample_index_004.width, sample_index_004.height = 140.0, 100.0
    sample_nearest_006.width, sample_nearest_006.height = 140.0, 100.0
    reroute_025.width, reroute_025.height = 10.0, 100.0
    reroute_032.width, reroute_032.height = 10.0, 100.0
    reroute_036.width, reroute_036.height = 10.0, 100.0
    named_attribute_019.width, named_attribute_019.height = 140.0, 100.0
    attribute_statistic.width, attribute_statistic.height = 140.0, 100.0
    map_range.width, map_range.height = 140.0, 100.0
    store_named_attribute_013.width, store_named_attribute_013.height = 140.0, 100.0
    named_attribute_020.width, named_attribute_020.height = 140.0, 100.0
    math_023.width, math_023.height = 140.0, 100.0
    sample_index_005.width, sample_index_005.height = 140.0, 100.0
    sample_nearest_007.width, sample_nearest_007.height = 140.0, 100.0
    reroute_035.width, reroute_035.height = 10.0, 100.0
    reroute_037.width, reroute_037.height = 10.0, 100.0
    named_attribute_021.width, named_attribute_021.height = 140.0, 100.0
    attribute_statistic_001.width, attribute_statistic_001.height = 140.0, 100.0
    map_range_001.width, map_range_001.height = 140.0, 100.0
    reroute_047.width, reroute_047.height = 10.0, 100.0
    reroute_048.width, reroute_048.height = 10.0, 100.0
    switch_002.width, switch_002.height = 140.0, 100.0
    switch_003.width, switch_003.height = 140.0, 100.0
    reroute_049.width, reroute_049.height = 10.0, 100.0
    delete_geometry_001.width, delete_geometry_001.height = 140.0, 100.0
    compare_009.width, compare_009.height = 140.0, 100.0
    index_003.width, index_003.height = 140.0, 100.0
    reroute_051.width, reroute_051.height = 10.0, 100.0
    vector_math_007.width, vector_math_007.height = 140.0, 100.0
    separate_xyz_004.width, separate_xyz_004.height = 140.0, 100.0
    compare_010.width, compare_010.height = 140.0, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    switch_004.width, switch_004.height = 140.0, 100.0
    combine_xyz_004.width, combine_xyz_004.height = 140.0, 100.0
    math_008.width, math_008.height = 140.0, 100.0
    named_attribute_022.width, named_attribute_022.height = 140.0, 100.0
    vector_math_010.width, vector_math_010.height = 140.0, 100.0
    boolean_math_005.width, boolean_math_005.height = 140.0, 100.0
    boolean_math_006.width, boolean_math_006.height = 140.0, 100.0
    boolean_math_007.width, boolean_math_007.height = 140.0, 100.0
    delete_geometry_002.width, delete_geometry_002.height = 140.0, 100.0
    store_named_attribute_014.width, store_named_attribute_014.height = 140.0, 100.0
    store_named_attribute_015.width, store_named_attribute_015.height = 140.0, 100.0
    bake.width, bake.height = 140.0, 100.0
    set_material.width, set_material.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    reroute_050.width, reroute_050.height = 10.0, 100.0
    frame.width, frame.height = 1346.0, 954.0
    group_input.width, group_input.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    group_input_003.width, group_input_003.height = 140.0, 100.0
    group_input_004.width, group_input_004.height = 140.0, 100.0
    group_input_005.width, group_input_005.height = 140.0, 100.0
    group_input_006.width, group_input_006.height = 140.0, 100.0
    group_input_007.width, group_input_007.height = 140.0, 100.0
    switch_005.width, switch_005.height = 140.0, 100.0
    group_input_008.width, group_input_008.height = 140.0, 100.0
    separate_components_002.width, separate_components_002.height = 140.0, 100.0
    join_geometry_002.width, join_geometry_002.height = 140.0, 100.0
    reroute_052.width, reroute_052.height = 10.0, 100.0
    reroute_053.width, reroute_053.height = 10.0, 100.0
    join_geometry_003.width, join_geometry_003.height = 140.0, 100.0

    #initialize erosion links
    #scene_time.Frame -> distribute_points_on_faces.Seed
    group.links.new(scene_time.outputs[1], distribute_points_on_faces.inputs[6])
    #join_geometry_001.Geometry -> simulation_output.Geometry
    group.links.new(join_geometry_001.outputs[0], simulation_output.inputs[1])
    #join_geometry.Geometry -> separate_components.Geometry
    group.links.new(join_geometry.outputs[0], separate_components.inputs[0])
    #separate_components.Mesh -> reroute_002.Input
    group.links.new(separate_components.outputs[0], reroute_002.inputs[0])
    #named_attribute_001.Attribute -> math_004.Value
    group.links.new(named_attribute_001.outputs[0], math_004.inputs[0])
    #math_004.Value -> store_named_attribute_001.Value
    group.links.new(math_004.outputs[0], store_named_attribute_001.inputs[3])
    #separate_components.Point Cloud -> store_named_attribute.Geometry
    group.links.new(separate_components.outputs[3], store_named_attribute.inputs[0])
    #store_named_attribute.Geometry -> store_named_attribute_001.Geometry
    group.links.new(store_named_attribute.outputs[0], store_named_attribute_001.inputs[0])
    #store_named_attribute_001.Geometry -> reroute_004.Input
    group.links.new(store_named_attribute_001.outputs[0], reroute_004.inputs[0])
    #named_attribute.Attribute -> vector_math_001.Vector
    group.links.new(named_attribute.outputs[0], vector_math_001.inputs[0])
    #vector_math_001.Vector -> store_named_attribute.Value
    group.links.new(vector_math_001.outputs[0], store_named_attribute.inputs[3])
    #vector_math_008.Vector -> vector_math_009.Vector
    group.links.new(vector_math_008.outputs[0], vector_math_009.inputs[0])
    #sample_nearest_001.Index -> sample_index_001.Index
    group.links.new(sample_nearest_001.outputs[0], sample_index_001.inputs[2])
    #sample_index_001.Value -> vector_math_008.Vector
    group.links.new(sample_index_001.outputs[0], vector_math_008.inputs[0])
    #sample_index_001.Value -> vector_math_009.Vector
    group.links.new(sample_index_001.outputs[0], vector_math_009.inputs[1])
    #normal.Normal -> sample_index_001.Value
    group.links.new(normal.outputs[0], sample_index_001.inputs[1])
    #reroute_007.Output -> reroute_010.Input
    group.links.new(reroute_007.outputs[0], reroute_010.inputs[0])
    #sample_nearest_004.Index -> sample_index_002.Index
    group.links.new(sample_nearest_004.outputs[0], sample_index_002.inputs[2])
    #set_position_001.Geometry -> reroute_013.Input
    group.links.new(set_position_001.outputs[0], reroute_013.inputs[0])
    #reroute_007.Output -> sample_index_002.Geometry
    group.links.new(reroute_007.outputs[0], sample_index_002.inputs[0])
    #reroute_007.Output -> sample_nearest_004.Geometry
    group.links.new(reroute_007.outputs[0], sample_nearest_004.inputs[0])
    #position_001.Position -> sample_index_002.Value
    group.links.new(position_001.outputs[0], sample_index_002.inputs[1])
    #sample_index_002.Value -> store_named_attribute_003.Value
    group.links.new(sample_index_002.outputs[0], store_named_attribute_003.inputs[3])
    #reroute_015.Output -> store_named_attribute_003.Geometry
    group.links.new(reroute_015.outputs[0], store_named_attribute_003.inputs[0])
    #sample_nearest_005.Index -> sample_index_003.Index
    group.links.new(sample_nearest_005.outputs[0], sample_index_003.inputs[2])
    #position_002.Position -> sample_index_003.Value
    group.links.new(position_002.outputs[0], sample_index_003.inputs[1])
    #reroute_008.Output -> reroute_016.Input
    group.links.new(reroute_008.outputs[0], reroute_016.inputs[0])
    #reroute_016.Output -> sample_index_003.Geometry
    group.links.new(reroute_016.outputs[0], sample_index_003.inputs[0])
    #reroute_016.Output -> sample_nearest_005.Geometry
    group.links.new(reroute_016.outputs[0], sample_nearest_005.inputs[0])
    #store_named_attribute_004.Geometry -> reroute_017.Input
    group.links.new(store_named_attribute_004.outputs[0], reroute_017.inputs[0])
    #store_named_attribute_004.Geometry -> geometry_proximity.Geometry
    group.links.new(store_named_attribute_004.outputs[0], geometry_proximity.inputs[0])
    #geometry_proximity.Position -> sample_nearest.Sample Position
    group.links.new(geometry_proximity.outputs[0], sample_nearest.inputs[1])
    #sample_nearest.Index -> compare_001.A
    group.links.new(sample_nearest.outputs[0], compare_001.inputs[2])
    #index.Index -> compare_001.B
    group.links.new(index.outputs[0], compare_001.inputs[3])
    #reroute_009.Output -> sample_nearest.Geometry
    group.links.new(reroute_009.outputs[0], sample_nearest.inputs[0])
    #reroute_009.Output -> reroute_011.Input
    group.links.new(reroute_009.outputs[0], reroute_011.inputs[0])
    #geometry_proximity_001.Position -> sample_nearest_002.Sample Position
    group.links.new(geometry_proximity_001.outputs[0], sample_nearest_002.inputs[1])
    #sample_nearest_002.Index -> compare_002.A
    group.links.new(sample_nearest_002.outputs[0], compare_002.inputs[2])
    #index_001.Index -> compare_002.B
    group.links.new(index_001.outputs[0], compare_002.inputs[3])
    #store_named_attribute_003.Geometry -> reroute_014.Input
    group.links.new(store_named_attribute_003.outputs[0], reroute_014.inputs[0])
    #reroute_010.Output -> sample_nearest_002.Geometry
    group.links.new(reroute_010.outputs[0], sample_nearest_002.inputs[0])
    #store_named_attribute_003.Geometry -> geometry_proximity_001.Geometry
    group.links.new(store_named_attribute_003.outputs[0], geometry_proximity_001.inputs[0])
    #compare_002.Result -> store_named_attribute_005.Value
    group.links.new(compare_002.outputs[0], store_named_attribute_005.inputs[3])
    #reroute_010.Output -> reroute_018.Input
    group.links.new(reroute_010.outputs[0], reroute_018.inputs[0])
    #reroute_018.Output -> store_named_attribute_005.Geometry
    group.links.new(reroute_018.outputs[0], store_named_attribute_005.inputs[0])
    #store_named_attribute_005.Geometry -> reroute_020.Input
    group.links.new(store_named_attribute_005.outputs[0], reroute_020.inputs[0])
    #reroute_011.Output -> store_named_attribute_006.Geometry
    group.links.new(reroute_011.outputs[0], store_named_attribute_006.inputs[0])
    #compare_001.Result -> store_named_attribute_006.Value
    group.links.new(compare_001.outputs[0], store_named_attribute_006.inputs[3])
    #sample_index_003.Value -> store_named_attribute_004.Value
    group.links.new(sample_index_003.outputs[0], store_named_attribute_004.inputs[3])
    #store_named_attribute_006.Geometry -> reroute_021.Input
    group.links.new(store_named_attribute_006.outputs[0], reroute_021.inputs[0])
    #named_attribute_002.Attribute -> vector_math_002.Vector
    group.links.new(named_attribute_002.outputs[0], vector_math_002.inputs[0])
    #named_attribute_005.Attribute -> vector_math_002.Vector
    group.links.new(named_attribute_005.outputs[0], vector_math_002.inputs[1])
    #reroute_021.Output -> reroute_024.Input
    group.links.new(reroute_021.outputs[0], reroute_024.inputs[0])
    #sample_nearest_003.Index -> sample_index.Index
    group.links.new(sample_nearest_003.outputs[0], sample_index.inputs[2])
    #reroute_026.Output -> reroute_023.Input
    group.links.new(reroute_026.outputs[0], reroute_023.inputs[0])
    #reroute_024.Output -> set_position_002.Geometry
    group.links.new(reroute_024.outputs[0], set_position_002.inputs[0])
    #named_attribute_006.Attribute -> set_position_002.Selection
    group.links.new(named_attribute_006.outputs[0], set_position_002.inputs[1])
    #sample_index.Value -> set_position_002.Offset
    group.links.new(sample_index.outputs[0], set_position_002.inputs[3])
    #named_attribute_007.Attribute -> vector_math_004.Vector
    group.links.new(named_attribute_007.outputs[0], vector_math_004.inputs[0])
    #vector_math_004.Vector -> set_position_003.Offset
    group.links.new(vector_math_004.outputs[0], set_position_003.inputs[3])
    #reroute_026.Output -> set_position_003.Geometry
    group.links.new(reroute_026.outputs[0], set_position_003.inputs[0])
    #reroute_027.Output -> reroute_026.Input
    group.links.new(reroute_027.outputs[0], reroute_026.inputs[0])
    #set_position_003.Geometry -> sample_index.Geometry
    group.links.new(set_position_003.outputs[0], sample_index.inputs[0])
    #set_position_003.Geometry -> sample_nearest_003.Geometry
    group.links.new(set_position_003.outputs[0], sample_nearest_003.inputs[0])
    #named_attribute_008.Attribute -> compare_003.A
    group.links.new(named_attribute_008.outputs[0], compare_003.inputs[0])
    #reroute_017.Output -> reroute_022.Input
    group.links.new(reroute_017.outputs[0], reroute_022.inputs[0])
    #reroute_022.Output -> delete_geometry.Geometry
    group.links.new(reroute_022.outputs[0], delete_geometry.inputs[0])
    #simulation_output.Geometry -> separate_components_001.Geometry
    group.links.new(simulation_output.outputs[0], separate_components_001.inputs[0])
    #position_003.Position -> separate_xyz.Vector
    group.links.new(position_003.outputs[0], separate_xyz.inputs[0])
    #separate_xyz.Z -> blur_attribute.Value
    group.links.new(separate_xyz.outputs[2], blur_attribute.inputs[0])
    #separate_xyz.X -> combine_xyz_001.X
    group.links.new(separate_xyz.outputs[0], combine_xyz_001.inputs[0])
    #combine_xyz_001.Vector -> set_position_004.Position
    group.links.new(combine_xyz_001.outputs[0], set_position_004.inputs[2])
    #separate_xyz.Y -> combine_xyz_001.Y
    group.links.new(separate_xyz.outputs[1], combine_xyz_001.inputs[1])
    #blur_attribute.Value -> combine_xyz_001.Z
    group.links.new(blur_attribute.outputs[0], combine_xyz_001.inputs[2])
    #named_attribute_009.Attribute -> vector_math_005.Vector
    group.links.new(named_attribute_009.outputs[0], vector_math_005.inputs[0])
    #set_point_radius.Points -> store_named_attribute_007.Geometry
    group.links.new(set_point_radius.outputs[0], store_named_attribute_007.inputs[0])
    #store_named_attribute_008.Geometry -> join_geometry.Geometry
    group.links.new(store_named_attribute_008.outputs[0], join_geometry.inputs[0])
    #math_010.Value -> math_011.Value
    group.links.new(math_010.outputs[0], math_011.inputs[0])
    #named_attribute_010.Attribute -> math_011.Value
    group.links.new(named_attribute_010.outputs[0], math_011.inputs[1])
    #math_011.Value -> math_012.Value
    group.links.new(math_011.outputs[0], math_012.inputs[0])
    #store_named_attribute_007.Geometry -> store_named_attribute_008.Geometry
    group.links.new(store_named_attribute_007.outputs[0], store_named_attribute_008.inputs[0])
    #distribute_points_on_faces.Points -> set_point_radius.Points
    group.links.new(distribute_points_on_faces.outputs[0], set_point_radius.inputs[0])
    #reroute_004.Output -> reroute_015.Input
    group.links.new(reroute_004.outputs[0], reroute_015.inputs[0])
    #reroute_002.Output -> reroute_007.Input
    group.links.new(reroute_002.outputs[0], reroute_007.inputs[0])
    #reroute_028.Output -> reroute_005.Input
    group.links.new(reroute_028.outputs[0], reroute_005.inputs[0])
    #reroute_005.Output -> reroute_008.Input
    group.links.new(reroute_005.outputs[0], reroute_008.inputs[0])
    #reroute_008.Output -> raycast.Target Geometry
    group.links.new(reroute_008.outputs[0], raycast.inputs[0])
    #reroute_013.Output -> reroute_019.Input
    group.links.new(reroute_013.outputs[0], reroute_019.inputs[0])
    #sample_index_001.Value -> raycast.Ray Direction
    group.links.new(sample_index_001.outputs[0], raycast.inputs[3])
    #sample_index_001.Value -> vector_math_003.Vector
    group.links.new(sample_index_001.outputs[0], vector_math_003.inputs[0])
    #vector_math_003.Vector -> raycast_001.Ray Direction
    group.links.new(vector_math_003.outputs[0], raycast_001.inputs[3])
    #reroute_008.Output -> raycast_001.Target Geometry
    group.links.new(reroute_008.outputs[0], raycast_001.inputs[0])
    #reroute_019.Output -> set_position_006.Geometry
    group.links.new(reroute_019.outputs[0], set_position_006.inputs[0])
    #raycast.Is Hit -> set_position_006.Selection
    group.links.new(raycast.outputs[0], set_position_006.inputs[1])
    #set_position_006.Geometry -> set_position_007.Geometry
    group.links.new(set_position_006.outputs[0], set_position_007.inputs[0])
    #raycast.Hit Position -> set_position_006.Position
    group.links.new(raycast.outputs[1], set_position_006.inputs[2])
    #raycast_001.Is Hit -> set_position_007.Selection
    group.links.new(raycast_001.outputs[0], set_position_007.inputs[1])
    #raycast_001.Hit Position -> set_position_007.Position
    group.links.new(raycast_001.outputs[1], set_position_007.inputs[2])
    #reroute_003.Output -> capture_attribute.Geometry
    group.links.new(reroute_003.outputs[0], capture_attribute.inputs[0])
    #position_004.Position -> capture_attribute.Position
    group.links.new(position_004.outputs[0], capture_attribute.inputs[1])
    #capture_attribute.Position -> store_named_attribute_002.Value
    group.links.new(capture_attribute.outputs[1], store_named_attribute_002.inputs[3])
    #capture_attribute.Geometry -> store_named_attribute_002.Geometry
    group.links.new(capture_attribute.outputs[0], store_named_attribute_002.inputs[0])
    #reroute_030.Output -> set_position_001.Geometry
    group.links.new(reroute_030.outputs[0], set_position_001.inputs[0])
    #position_005.Position -> vector_math_006.Vector
    group.links.new(position_005.outputs[0], vector_math_006.inputs[0])
    #named_attribute_004.Attribute -> vector_math_006.Vector
    group.links.new(named_attribute_004.outputs[0], vector_math_006.inputs[1])
    #vector_math_006.Vector -> store_named_attribute_009.Value
    group.links.new(vector_math_006.outputs[0], store_named_attribute_009.inputs[3])
    #reroute_014.Output -> reroute_003.Input
    group.links.new(reroute_014.outputs[0], reroute_003.inputs[0])
    #reroute_020.Output -> reroute_028.Input
    group.links.new(reroute_020.outputs[0], reroute_028.inputs[0])
    #reroute_028.Output -> sample_index_001.Geometry
    group.links.new(reroute_028.outputs[0], sample_index_001.inputs[0])
    #reroute_028.Output -> sample_nearest_001.Geometry
    group.links.new(reroute_028.outputs[0], sample_nearest_001.inputs[0])
    #store_named_attribute_002.Geometry -> reroute_029.Input
    group.links.new(store_named_attribute_002.outputs[0], reroute_029.inputs[0])
    #reroute_029.Output -> reroute_030.Input
    group.links.new(reroute_029.outputs[0], reroute_030.inputs[0])
    #math_012.Value -> math_001.Value
    group.links.new(math_012.outputs[0], math_001.inputs[0])
    #named_attribute_003.Attribute -> math_001.Value
    group.links.new(named_attribute_003.outputs[0], math_001.inputs[1])
    #reroute_033.Output -> math_005.Value
    group.links.new(reroute_033.outputs[0], math_005.inputs[0])
    #math_005.Value -> math_003.Value
    group.links.new(math_005.outputs[0], math_003.inputs[0])
    #math_001.Value -> math_006.Value
    group.links.new(math_001.outputs[0], math_006.inputs[0])
    #math_006.Value -> math_003.Value
    group.links.new(math_006.outputs[0], math_003.inputs[1])
    #named_attribute_011.Attribute -> math_007.Value
    group.links.new(named_attribute_011.outputs[0], math_007.inputs[0])
    #math_007.Value -> store_named_attribute_010.Value
    group.links.new(math_007.outputs[0], store_named_attribute_010.inputs[3])
    #reroute_023.Output -> reroute_031.Input
    group.links.new(reroute_023.outputs[0], reroute_031.inputs[0])
    #reroute_031.Output -> store_named_attribute_010.Geometry
    group.links.new(reroute_031.outputs[0], store_named_attribute_010.inputs[0])
    #reroute_038.Output -> reroute_033.Input
    group.links.new(reroute_038.outputs[0], reroute_033.inputs[0])
    #vector_math_005.Value -> math_014.Value
    group.links.new(vector_math_005.outputs[1], math_014.inputs[0])
    #named_attribute_012.Attribute -> compare_004.A
    group.links.new(named_attribute_012.outputs[0], compare_004.inputs[0])
    #reroute_042.Output -> boolean_math.Boolean
    group.links.new(reroute_042.outputs[0], boolean_math.inputs[0])
    #compare_004.Result -> boolean_math.Boolean
    group.links.new(compare_004.outputs[0], boolean_math.inputs[1])
    #named_attribute_014.Attribute -> math_016.Value
    group.links.new(named_attribute_014.outputs[0], math_016.inputs[0])
    #math_016.Value -> math_017.Value
    group.links.new(math_016.outputs[0], math_017.inputs[0])
    #compare_005.Result -> reroute_040.Input
    group.links.new(compare_005.outputs[0], reroute_040.inputs[0])
    #reroute_043.Output -> math_016.Value
    group.links.new(reroute_043.outputs[0], math_016.inputs[1])
    #named_attribute_013.Attribute -> math_015.Value
    group.links.new(named_attribute_013.outputs[0], math_015.inputs[1])
    #reroute_039.Output -> reroute_038.Input
    group.links.new(reroute_039.outputs[0], reroute_038.inputs[0])
    #reroute_038.Output -> math_015.Value
    group.links.new(reroute_038.outputs[0], math_015.inputs[0])
    #math_015.Value -> switch.True
    group.links.new(math_015.outputs[0], switch.inputs[2])
    #math_017.Value -> switch.False
    group.links.new(math_017.outputs[0], switch.inputs[1])
    #reroute_034.Output -> reroute_039.Input
    group.links.new(reroute_034.outputs[0], reroute_039.inputs[0])
    #reroute_039.Output -> compare_005.A
    group.links.new(reroute_039.outputs[0], compare_005.inputs[0])
    #math_009.Value -> math_010.Value
    group.links.new(math_009.outputs[0], math_010.inputs[1])
    #reroute_041.Output -> reroute_042.Input
    group.links.new(reroute_041.outputs[0], reroute_042.inputs[0])
    #math_012.Value -> reroute_043.Input
    group.links.new(math_012.outputs[0], reroute_043.inputs[0])
    #reroute_040.Output -> reroute_041.Input
    group.links.new(reroute_040.outputs[0], reroute_041.inputs[0])
    #reroute_041.Output -> switch.Switch
    group.links.new(reroute_041.outputs[0], switch.inputs[0])
    #reroute_046.Output -> compare_004.B
    group.links.new(reroute_046.outputs[0], compare_004.inputs[1])
    #boolean_math.Boolean -> switch_001.Switch
    group.links.new(boolean_math.outputs[0], switch_001.inputs[0])
    #switch.Output -> reroute_045.Input
    group.links.new(switch.outputs[0], reroute_045.inputs[0])
    #reroute_043.Output -> reroute_046.Input
    group.links.new(reroute_043.outputs[0], reroute_046.inputs[0])
    #named_attribute_015.Attribute -> math_019.Value
    group.links.new(named_attribute_015.outputs[0], math_019.inputs[0])
    #math_020.Value -> math_019.Value
    group.links.new(math_020.outputs[0], math_019.inputs[1])
    #math_019.Value -> store_named_attribute_011.Value
    group.links.new(math_019.outputs[0], store_named_attribute_011.inputs[3])
    #math_003.Value -> math_018.Value
    group.links.new(math_003.outputs[0], math_018.inputs[0])
    #reroute_012.Output -> math_007.Value
    group.links.new(reroute_012.outputs[0], math_007.inputs[1])
    #reroute_048.Output -> reroute.Input
    group.links.new(reroute_048.outputs[0], reroute.inputs[0])
    #reroute_016.Output -> reroute_009.Input
    group.links.new(reroute_016.outputs[0], reroute_009.inputs[0])
    #store_named_attribute_009.Geometry -> store_named_attribute_004.Geometry
    group.links.new(store_named_attribute_009.outputs[0], store_named_attribute_004.inputs[0])
    #switch_001.Output -> reroute_006.Input
    group.links.new(switch_001.outputs[0], reroute_006.inputs[0])
    #reroute_006.Output -> reroute_012.Input
    group.links.new(reroute_006.outputs[0], reroute_012.inputs[0])
    #named_attribute_016.Attribute -> separate_xyz_001.Vector
    group.links.new(named_attribute_016.outputs[0], separate_xyz_001.inputs[0])
    #named_attribute_017.Attribute -> vector_math_008.Vector
    group.links.new(named_attribute_017.outputs[0], vector_math_008.inputs[1])
    #position_006.Position -> separate_xyz_003.Vector
    group.links.new(position_006.outputs[0], separate_xyz_003.inputs[0])
    #separate_xyz_003.X -> compare.A
    group.links.new(separate_xyz_003.outputs[0], compare.inputs[0])
    #delete_geometry.Geometry -> reroute_027.Input
    group.links.new(delete_geometry.outputs[0], reroute_027.inputs[0])
    #compare.Result -> boolean_math_001.Boolean
    group.links.new(compare.outputs[0], boolean_math_001.inputs[0])
    #compare_003.Result -> boolean_math_001.Boolean
    group.links.new(compare_003.outputs[0], boolean_math_001.inputs[1])
    #separate_xyz_003.X -> compare_006.A
    group.links.new(separate_xyz_003.outputs[0], compare_006.inputs[0])
    #compare_006.Result -> boolean_math_002.Boolean
    group.links.new(compare_006.outputs[0], boolean_math_002.inputs[0])
    #boolean_math_001.Boolean -> boolean_math_002.Boolean
    group.links.new(boolean_math_001.outputs[0], boolean_math_002.inputs[1])
    #boolean_math_004.Boolean -> delete_geometry.Selection
    group.links.new(boolean_math_004.outputs[0], delete_geometry.inputs[1])
    #separate_xyz_003.Y -> compare_007.A
    group.links.new(separate_xyz_003.outputs[1], compare_007.inputs[0])
    #separate_xyz_003.Y -> compare_008.A
    group.links.new(separate_xyz_003.outputs[1], compare_008.inputs[0])
    #compare_007.Result -> boolean_math_003.Boolean
    group.links.new(compare_007.outputs[0], boolean_math_003.inputs[0])
    #compare_008.Result -> boolean_math_003.Boolean
    group.links.new(compare_008.outputs[0], boolean_math_003.inputs[1])
    #boolean_math_002.Boolean -> boolean_math_004.Boolean
    group.links.new(boolean_math_002.outputs[0], boolean_math_004.inputs[0])
    #boolean_math_003.Boolean -> boolean_math_004.Boolean
    group.links.new(boolean_math_003.outputs[0], boolean_math_004.inputs[1])
    #store_named_attribute_011.Geometry -> join_geometry_001.Geometry
    group.links.new(store_named_attribute_011.outputs[0], join_geometry_001.inputs[0])
    #store_named_attribute_010.Geometry -> store_named_attribute_011.Geometry
    group.links.new(store_named_attribute_010.outputs[0], store_named_attribute_011.inputs[0])
    #named_attribute_018.Attribute -> math_022.Value
    group.links.new(named_attribute_018.outputs[0], math_022.inputs[0])
    #math_022.Value -> store_named_attribute_012.Value
    group.links.new(math_022.outputs[0], store_named_attribute_012.inputs[3])
    #set_position_002.Geometry -> store_named_attribute_012.Geometry
    group.links.new(set_position_002.outputs[0], store_named_attribute_012.inputs[0])
    #store_named_attribute_012.Geometry -> reroute_001.Input
    group.links.new(store_named_attribute_012.outputs[0], reroute_001.inputs[0])
    #named_attribute_006.Attribute -> store_named_attribute_012.Selection
    group.links.new(named_attribute_006.outputs[0], store_named_attribute_012.inputs[1])
    #sample_nearest_006.Index -> sample_index_004.Index
    group.links.new(sample_nearest_006.outputs[0], sample_index_004.inputs[2])
    #reroute_025.Output -> sample_index_004.Geometry
    group.links.new(reroute_025.outputs[0], sample_index_004.inputs[0])
    #reroute_036.Output -> sample_index_004.Value
    group.links.new(reroute_036.outputs[0], sample_index_004.inputs[1])
    #sample_index_004.Value -> math_022.Value
    group.links.new(sample_index_004.outputs[0], math_022.inputs[1])
    #set_position_003.Geometry -> reroute_025.Input
    group.links.new(set_position_003.outputs[0], reroute_025.inputs[0])
    #reroute_025.Output -> sample_nearest_006.Geometry
    group.links.new(reroute_025.outputs[0], sample_nearest_006.inputs[0])
    #math_003.Value -> reroute_032.Input
    group.links.new(math_003.outputs[0], reroute_032.inputs[0])
    #set_shade_smooth.Geometry -> attribute_statistic.Geometry
    group.links.new(set_shade_smooth.outputs[0], attribute_statistic.inputs[0])
    #attribute_statistic.Max -> map_range.From Max
    group.links.new(attribute_statistic.outputs[4], map_range.inputs[2])
    #named_attribute_019.Attribute -> attribute_statistic.Attribute
    group.links.new(named_attribute_019.outputs[0], attribute_statistic.inputs[2])
    #named_attribute_019.Attribute -> map_range.Value
    group.links.new(named_attribute_019.outputs[0], map_range.inputs[0])
    #math_023.Value -> store_named_attribute_013.Value
    group.links.new(math_023.outputs[0], store_named_attribute_013.inputs[3])
    #sample_nearest_007.Index -> sample_index_005.Index
    group.links.new(sample_nearest_007.outputs[0], sample_index_005.inputs[2])
    #sample_index_005.Value -> math_023.Value
    group.links.new(sample_index_005.outputs[0], math_023.inputs[1])
    #reroute_035.Output -> sample_index_005.Geometry
    group.links.new(reroute_035.outputs[0], sample_index_005.inputs[0])
    #reroute_025.Output -> reroute_035.Input
    group.links.new(reroute_025.outputs[0], reroute_035.inputs[0])
    #reroute_035.Output -> sample_nearest_007.Geometry
    group.links.new(reroute_035.outputs[0], sample_nearest_007.inputs[0])
    #named_attribute_020.Attribute -> math_023.Value
    group.links.new(named_attribute_020.outputs[0], math_023.inputs[0])
    #reroute_037.Output -> sample_index_005.Value
    group.links.new(reroute_037.outputs[0], sample_index_005.inputs[1])
    #named_attribute_021.Attribute -> attribute_statistic_001.Attribute
    group.links.new(named_attribute_021.outputs[0], attribute_statistic_001.inputs[2])
    #named_attribute_021.Attribute -> map_range_001.Value
    group.links.new(named_attribute_021.outputs[0], map_range_001.inputs[0])
    #reroute_001.Output -> reroute_047.Input
    group.links.new(reroute_001.outputs[0], reroute_047.inputs[0])
    #store_named_attribute_013.Geometry -> reroute_048.Input
    group.links.new(store_named_attribute_013.outputs[0], reroute_048.inputs[0])
    #reroute_047.Output -> store_named_attribute_013.Geometry
    group.links.new(reroute_047.outputs[0], store_named_attribute_013.inputs[0])
    #reroute_045.Output -> reroute_044.Input
    group.links.new(reroute_045.outputs[0], reroute_044.inputs[0])
    #boolean_math.Boolean -> switch_002.Switch
    group.links.new(boolean_math.outputs[0], switch_002.inputs[0])
    #reroute_032.Output -> switch_002.False
    group.links.new(reroute_032.outputs[0], switch_002.inputs[1])
    #switch_002.Output -> reroute_036.Input
    group.links.new(switch_002.outputs[0], reroute_036.inputs[0])
    #boolean_math.Boolean -> switch_003.Switch
    group.links.new(boolean_math.outputs[0], switch_003.inputs[0])
    #reroute_044.Output -> switch_003.True
    group.links.new(reroute_044.outputs[0], switch_003.inputs[2])
    #reroute_049.Output -> reroute_037.Input
    group.links.new(reroute_049.outputs[0], reroute_037.inputs[0])
    #switch_003.Output -> reroute_049.Input
    group.links.new(switch_003.outputs[0], reroute_049.inputs[0])
    #reroute_044.Output -> switch_001.True
    group.links.new(reroute_044.outputs[0], switch_001.inputs[2])
    #attribute_statistic_001.Min -> map_range_001.From Min
    group.links.new(attribute_statistic_001.outputs[3], map_range_001.inputs[1])
    #compare_009.Result -> delete_geometry_001.Selection
    group.links.new(compare_009.outputs[0], delete_geometry_001.inputs[1])
    #index_003.Index -> compare_009.B
    group.links.new(index_003.outputs[0], compare_009.inputs[3])
    #reroute_051.Output -> delete_geometry_001.Geometry
    group.links.new(reroute_051.outputs[0], delete_geometry_001.inputs[0])
    #store_named_attribute_011.Geometry -> reroute_051.Input
    group.links.new(store_named_attribute_011.outputs[0], reroute_051.inputs[0])
    #vector_math_007.Vector -> separate_xyz_004.Vector
    group.links.new(vector_math_007.outputs[0], separate_xyz_004.inputs[0])
    #separate_xyz_004.Z -> compare_010.A
    group.links.new(separate_xyz_004.outputs[2], compare_010.inputs[0])
    #compare_010.Result -> switch_004.Switch
    group.links.new(compare_010.outputs[0], switch_004.inputs[0])
    #combine_xyz.Vector -> switch_004.True
    group.links.new(combine_xyz.outputs[0], switch_004.inputs[2])
    #combine_xyz_004.Vector -> switch_004.False
    group.links.new(combine_xyz_004.outputs[0], switch_004.inputs[1])
    #separate_xyz_004.Z -> combine_xyz_004.Z
    group.links.new(separate_xyz_004.outputs[2], combine_xyz_004.inputs[2])
    #separate_xyz_004.Z -> math_008.Value
    group.links.new(separate_xyz_004.outputs[2], math_008.inputs[0])
    #math_008.Value -> combine_xyz.Y
    group.links.new(math_008.outputs[0], combine_xyz.inputs[1])
    #switch_004.Output -> vector_math_010.Vector
    group.links.new(switch_004.outputs[0], vector_math_010.inputs[0])
    #named_attribute_022.Attribute -> vector_math_010.Scale
    group.links.new(named_attribute_022.outputs[0], vector_math_010.inputs[3])
    #sample_index.Value -> vector_math_007.Vector
    group.links.new(sample_index.outputs[0], vector_math_007.inputs[0])
    #math_018.Value -> switch_001.False
    group.links.new(math_018.outputs[0], switch_001.inputs[1])
    #math_014.Value -> math_010.Value
    group.links.new(math_014.outputs[0], math_010.inputs[0])
    #reroute_034.Output -> math_009.Value
    group.links.new(reroute_034.outputs[0], math_009.inputs[0])
    #switch_001.Output -> combine_xyz_002.Z
    group.links.new(switch_001.outputs[0], combine_xyz_002.inputs[2])
    #combine_xyz_002.Vector -> sample_index.Value
    group.links.new(combine_xyz_002.outputs[0], sample_index.inputs[1])
    #separate_xyz_001.Z -> reroute_034.Input
    group.links.new(separate_xyz_001.outputs[2], reroute_034.inputs[0])
    #raycast.Is Hit -> boolean_math_005.Boolean
    group.links.new(raycast.outputs[0], boolean_math_005.inputs[0])
    #raycast_001.Is Hit -> boolean_math_006.Boolean
    group.links.new(raycast_001.outputs[0], boolean_math_006.inputs[0])
    #boolean_math_005.Boolean -> boolean_math_007.Boolean
    group.links.new(boolean_math_005.outputs[0], boolean_math_007.inputs[0])
    #boolean_math_006.Boolean -> boolean_math_007.Boolean
    group.links.new(boolean_math_006.outputs[0], boolean_math_007.inputs[1])
    #boolean_math_007.Boolean -> delete_geometry_002.Selection
    group.links.new(boolean_math_007.outputs[0], delete_geometry_002.inputs[1])
    #set_position_007.Geometry -> delete_geometry_002.Geometry
    group.links.new(set_position_007.outputs[0], delete_geometry_002.inputs[0])
    #delete_geometry_002.Geometry -> store_named_attribute_009.Geometry
    group.links.new(delete_geometry_002.outputs[0], store_named_attribute_009.inputs[0])
    #store_named_attribute_014.Geometry -> store_named_attribute_015.Geometry
    group.links.new(store_named_attribute_014.outputs[0], store_named_attribute_015.inputs[0])
    #map_range.Result -> store_named_attribute_014.Value
    group.links.new(map_range.outputs[0], store_named_attribute_014.inputs[3])
    #map_range_001.Result -> store_named_attribute_015.Value
    group.links.new(map_range_001.outputs[0], store_named_attribute_015.inputs[3])
    #set_shade_smooth.Geometry -> store_named_attribute_014.Geometry
    group.links.new(set_shade_smooth.outputs[0], store_named_attribute_014.inputs[0])
    #store_named_attribute_015.Geometry -> bake.Geometry
    group.links.new(store_named_attribute_015.outputs[0], bake.inputs[0])
    #bake.Geometry -> set_material.Geometry
    group.links.new(bake.outputs[0], set_material.inputs[0])
    #reroute_050.Output -> compare_007.B
    group.links.new(reroute_050.outputs[0], compare_007.inputs[1])
    #math.Value -> compare_008.B
    group.links.new(math.outputs[0], compare_008.inputs[1])
    #math.Value -> compare_006.B
    group.links.new(math.outputs[0], compare_006.inputs[1])
    #reroute_050.Output -> compare.B
    group.links.new(reroute_050.outputs[0], compare.inputs[1])
    #group_input.Capacity Factor -> math_012.Value
    group.links.new(group_input.outputs[1], math_012.inputs[1])
    #group_input_002.Erode Speed -> math_006.Value
    group.links.new(group_input_002.outputs[2], math_006.inputs[1])
    #group_input_003.Deposit Speed -> math_017.Value
    group.links.new(group_input_003.outputs[3], math_017.inputs[1])
    #group_input_004.Half Size -> math.Value
    group.links.new(group_input_004.outputs[4], math.inputs[0])
    #group_input_004.Half Size -> reroute_050.Input
    group.links.new(group_input_004.outputs[4], reroute_050.inputs[0])
    #group_input_005.Max Age -> compare_003.B
    group.links.new(group_input_005.outputs[5], compare_003.inputs[1])
    #group_input_006.Point Density -> distribute_points_on_faces.Density
    group.links.new(group_input_006.outputs[6], distribute_points_on_faces.inputs[4])
    #group_input_007.Point Gravity -> vector_math_001.Vector
    group.links.new(group_input_007.outputs[7], vector_math_001.inputs[1])
    #set_position_004.Geometry -> set_shade_smooth.Geometry
    group.links.new(set_position_004.outputs[0], set_shade_smooth.inputs[0])
    #separate_components_001.Mesh -> switch_005.False
    group.links.new(separate_components_001.outputs[0], switch_005.inputs[1])
    #simulation_output.Geometry -> switch_005.True
    group.links.new(simulation_output.outputs[0], switch_005.inputs[2])
    #switch_005.Output -> set_position_004.Geometry
    group.links.new(switch_005.outputs[0], set_position_004.inputs[0])
    #group_input_008.Show Points -> switch_005.Switch
    group.links.new(group_input_008.outputs[8], switch_005.inputs[0])
    #group_input_001.Geometry -> separate_components_002.Geometry
    group.links.new(group_input_001.outputs[0], separate_components_002.inputs[0])
    #separate_components_002.Mesh -> simulation_input.Geometry
    group.links.new(separate_components_002.outputs[0], simulation_input.inputs[0])
    #separate_components_002.Mesh -> distribute_points_on_faces.Mesh
    group.links.new(separate_components_002.outputs[0], distribute_points_on_faces.inputs[0])
    #separate_components_002.Instances -> join_geometry_002.Geometry
    group.links.new(separate_components_002.outputs[5], join_geometry_002.inputs[0])
    #join_geometry_002.Geometry -> reroute_052.Input
    group.links.new(join_geometry_002.outputs[0], reroute_052.inputs[0])
    #reroute_052.Output -> reroute_053.Input
    group.links.new(reroute_052.outputs[0], reroute_053.inputs[0])
    #reroute_053.Output -> join_geometry_003.Geometry
    group.links.new(reroute_053.outputs[0], join_geometry_003.inputs[0])
    #join_geometry_003.Geometry -> group_output.Geometry
    group.links.new(join_geometry_003.outputs[0], group_output.inputs[0])
    #vector_math_009.Vector -> set_position_001.Offset
    group.links.new(vector_math_009.outputs[0], set_position_001.inputs[3])
    #simulation_input.Geometry -> join_geometry.Geometry
    group.links.new(simulation_input.outputs[1], join_geometry.inputs[0])
    #reroute.Output -> join_geometry_001.Geometry
    group.links.new(reroute.outputs[0], join_geometry_001.inputs[0])
    #separate_components_002.Volume -> join_geometry_002.Geometry
    group.links.new(separate_components_002.outputs[4], join_geometry_002.inputs[0])
    #set_material.Geometry -> join_geometry_003.Geometry
    group.links.new(set_material.outputs[0], join_geometry_003.inputs[0])
    #separate_components_002.Point Cloud -> join_geometry_002.Geometry
    group.links.new(separate_components_002.outputs[3], join_geometry_002.inputs[0])
    #separate_components_002.Grease Pencil -> join_geometry_002.Geometry
    group.links.new(separate_components_002.outputs[2], join_geometry_002.inputs[0])
    #separate_components_002.Curve -> join_geometry_002.Geometry
    group.links.new(separate_components_002.outputs[1], join_geometry_002.inputs[0])
    return group

e = erosion_node_group()
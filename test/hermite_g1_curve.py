import bpy, mathutils

#initialize hermite_math node group
def hermite_math_node_group():
    hermite_math = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Hermite_Math")

    hermite_math.color_tag = 'NONE'
    hermite_math.description = ""
    hermite_math.default_group_node_width = 140
    


    #hermite_math interface
    #Socket Position
    position_socket = hermite_math.interface.new_socket(name = "Position", in_out='OUTPUT', socket_type = 'NodeSocketVector')
    position_socket.default_value = (0.0, 0.0, 0.0)
    position_socket.min_value = -3.4028234663852886e+38
    position_socket.max_value = 3.4028234663852886e+38
    position_socket.subtype = 'NONE'
    position_socket.attribute_domain = 'POINT'

    #Socket t
    t_socket = hermite_math.interface.new_socket(name = "t", in_out='INPUT', socket_type = 'NodeSocketFloat')
    t_socket.default_value = 0.0
    t_socket.min_value = -3.4028234663852886e+38
    t_socket.max_value = 3.4028234663852886e+38
    t_socket.subtype = 'NONE'
    t_socket.attribute_domain = 'POINT'

    #Socket P0
    p0_socket = hermite_math.interface.new_socket(name = "P0", in_out='INPUT', socket_type = 'NodeSocketVector')
    p0_socket.default_value = (0.0, 0.0, 0.0)
    p0_socket.min_value = -3.4028234663852886e+38
    p0_socket.max_value = 3.4028234663852886e+38
    p0_socket.subtype = 'NONE'
    p0_socket.attribute_domain = 'POINT'

    #Socket P1
    p1_socket = hermite_math.interface.new_socket(name = "P1", in_out='INPUT', socket_type = 'NodeSocketVector')
    p1_socket.default_value = (0.0, 0.0, 0.0)
    p1_socket.min_value = -3.4028234663852886e+38
    p1_socket.max_value = 3.4028234663852886e+38
    p1_socket.subtype = 'NONE'
    p1_socket.attribute_domain = 'POINT'

    #Socket T0
    t0_socket = hermite_math.interface.new_socket(name = "T0", in_out='INPUT', socket_type = 'NodeSocketVector')
    t0_socket.default_value = (0.0, 0.0, 0.0)
    t0_socket.min_value = -3.4028234663852886e+38
    t0_socket.max_value = 3.4028234663852886e+38
    t0_socket.subtype = 'NONE'
    t0_socket.attribute_domain = 'POINT'

    #Socket T1
    t1_socket = hermite_math.interface.new_socket(name = "T1", in_out='INPUT', socket_type = 'NodeSocketVector')
    t1_socket.default_value = (0.0, 0.0, 0.0)
    t1_socket.min_value = -3.4028234663852886e+38
    t1_socket.max_value = 3.4028234663852886e+38
    t1_socket.subtype = 'NONE'
    t1_socket.attribute_domain = 'POINT'


    #initialize hermite_math nodes
    #node Group Input
    group_input = hermite_math.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #node Group Output
    group_output = hermite_math.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    #node Math
    math = hermite_math.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'POWER'
    math.use_clamp = False
    #Value_001
    math.inputs[1].default_value = 2.0

    #node Math.001
    math_001 = hermite_math.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'POWER'
    math_001.use_clamp = False
    #Value_001
    math_001.inputs[1].default_value = 3.0

    #node Math.002
    math_002 = hermite_math.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.hide = True
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False
    #Value_001
    math_002.inputs[1].default_value = 2.0

    #node Math.003
    math_003 = hermite_math.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.hide = True
    math_003.operation = 'MULTIPLY'
    math_003.use_clamp = False
    #Value_001
    math_003.inputs[1].default_value = -3.0

    #node Math.004
    math_004 = hermite_math.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.hide = True
    math_004.operation = 'ADD'
    math_004.use_clamp = False

    #node Math.005
    math_005 = hermite_math.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'ADD'
    math_005.use_clamp = False
    #Value_001
    math_005.inputs[1].default_value = 1.0

    #node Math.006
    math_006 = hermite_math.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.hide = True
    math_006.operation = 'MULTIPLY'
    math_006.use_clamp = False
    #Value_001
    math_006.inputs[1].default_value = -2.0

    #node Math.007
    math_007 = hermite_math.nodes.new("ShaderNodeMath")
    math_007.name = "Math.007"
    math_007.hide = True
    math_007.operation = 'ADD'
    math_007.use_clamp = False

    #node Math.008
    math_008 = hermite_math.nodes.new("ShaderNodeMath")
    math_008.name = "Math.008"
    math_008.operation = 'ADD'
    math_008.use_clamp = False

    #node Math.009
    math_009 = hermite_math.nodes.new("ShaderNodeMath")
    math_009.name = "Math.009"
    math_009.hide = True
    math_009.operation = 'MULTIPLY'
    math_009.use_clamp = False
    #Value_001
    math_009.inputs[1].default_value = -2.0

    #node Math.010
    math_010 = hermite_math.nodes.new("ShaderNodeMath")
    math_010.name = "Math.010"
    math_010.hide = True
    math_010.operation = 'MULTIPLY'
    math_010.use_clamp = False
    #Value_001
    math_010.inputs[1].default_value = 3.0

    #node Math.011
    math_011 = hermite_math.nodes.new("ShaderNodeMath")
    math_011.name = "Math.011"
    math_011.hide = True
    math_011.operation = 'ADD'
    math_011.use_clamp = False

    #node Math.012
    math_012 = hermite_math.nodes.new("ShaderNodeMath")
    math_012.name = "Math.012"
    math_012.hide = True
    math_012.operation = 'SUBTRACT'
    math_012.use_clamp = False

    #node Vector Math
    vector_math = hermite_math.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.hide = True
    vector_math.operation = 'SCALE'

    #node Vector Math.001
    vector_math_001 = hermite_math.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.hide = True
    vector_math_001.operation = 'SCALE'

    #node Vector Math.002
    vector_math_002 = hermite_math.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.hide = True
    vector_math_002.operation = 'SCALE'

    #node Vector Math.003
    vector_math_003 = hermite_math.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.hide = True
    vector_math_003.operation = 'SCALE'

    #node Vector Math.004
    vector_math_004 = hermite_math.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.operation = 'ADD'

    #node Vector Math.005
    vector_math_005 = hermite_math.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'ADD'

    #node Vector Math.006
    vector_math_006 = hermite_math.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.operation = 'ADD'

    #node Vector Math.007
    vector_math_007 = hermite_math.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.operation = 'SCALE'
    #Scale
    vector_math_007.inputs[3].default_value = -1.0





    #Set locations
    group_input.location = (-1215.66357421875, -82.28106689453125)
    group_output.location = (400.0, 25.92474365234375)
    math.location = (-1004.3577270507812, 49.85749435424805)
    math_001.location = (-1001.0894165039062, 206.5403289794922)
    math_002.location = (-800.0, 191.34780883789062)
    math_003.location = (-800.0, 145.6739044189453)
    math_004.location = (-600.0, 100.78887939453125)
    math_005.location = (-402.9369201660156, 183.3916778564453)
    math_006.location = (-800.0, 100.0)
    math_007.location = (-600.0, 50.160362243652344)
    math_008.location = (-402.9369201660156, 33.39167785644531)
    math_009.location = (-800.0, 54.32609558105469)
    math_010.location = (-800.0, 8.652191162109375)
    math_011.location = (-600.0, -0.4681549072265625)
    math_012.location = (-604.5782470703125, -46.597686767578125)
    vector_math.location = (-222.51632690429688, -142.94509887695312)
    vector_math_001.location = (-222.51632690429688, -188.345703125)
    vector_math_002.location = (-222.51632690429688, -233.74627685546875)
    vector_math_003.location = (-222.51632690429688, -279.1468811035156)
    vector_math_004.location = (0.0, 184.79595947265625)
    vector_math_005.location = (0.0, 15.204048156738281)
    vector_math_006.location = (195.8870849609375, 31.41179656982422)
    vector_math_007.location = (-931.6860961914062, -210.93019104003906)

    #Set dimensions
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    math_002.width, math_002.height = 140.0, 100.0
    math_003.width, math_003.height = 140.0, 100.0
    math_004.width, math_004.height = 140.0, 100.0
    math_005.width, math_005.height = 140.0, 100.0
    math_006.width, math_006.height = 140.0, 100.0
    math_007.width, math_007.height = 140.0, 100.0
    math_008.width, math_008.height = 140.0, 100.0
    math_009.width, math_009.height = 140.0, 100.0
    math_010.width, math_010.height = 140.0, 100.0
    math_011.width, math_011.height = 140.0, 100.0
    math_012.width, math_012.height = 140.0, 100.0
    vector_math.width, vector_math.height = 140.0, 100.0
    vector_math_001.width, vector_math_001.height = 140.0, 100.0
    vector_math_002.width, vector_math_002.height = 140.0, 100.0
    vector_math_003.width, vector_math_003.height = 140.0, 100.0
    vector_math_004.width, vector_math_004.height = 140.0, 100.0
    vector_math_005.width, vector_math_005.height = 140.0, 100.0
    vector_math_006.width, vector_math_006.height = 140.0, 100.0
    vector_math_007.width, vector_math_007.height = 140.0, 100.0

    #initialize hermite_math links
    #group_input.t -> math.Value
    hermite_math.links.new(group_input.outputs[0], math.inputs[0])
    #group_input.t -> math_001.Value
    hermite_math.links.new(group_input.outputs[0], math_001.inputs[0])
    #math_001.Value -> math_002.Value
    hermite_math.links.new(math_001.outputs[0], math_002.inputs[0])
    #math.Value -> math_003.Value
    hermite_math.links.new(math.outputs[0], math_003.inputs[0])
    #math_002.Value -> math_004.Value
    hermite_math.links.new(math_002.outputs[0], math_004.inputs[0])
    #math_003.Value -> math_004.Value
    hermite_math.links.new(math_003.outputs[0], math_004.inputs[1])
    #math_004.Value -> math_005.Value
    hermite_math.links.new(math_004.outputs[0], math_005.inputs[0])
    #math.Value -> math_006.Value
    hermite_math.links.new(math.outputs[0], math_006.inputs[0])
    #math_001.Value -> math_007.Value
    hermite_math.links.new(math_001.outputs[0], math_007.inputs[0])
    #math_006.Value -> math_007.Value
    hermite_math.links.new(math_006.outputs[0], math_007.inputs[1])
    #math_007.Value -> math_008.Value
    hermite_math.links.new(math_007.outputs[0], math_008.inputs[0])
    #group_input.t -> math_008.Value
    hermite_math.links.new(group_input.outputs[0], math_008.inputs[1])
    #math_001.Value -> math_009.Value
    hermite_math.links.new(math_001.outputs[0], math_009.inputs[0])
    #math.Value -> math_010.Value
    hermite_math.links.new(math.outputs[0], math_010.inputs[0])
    #math_009.Value -> math_011.Value
    hermite_math.links.new(math_009.outputs[0], math_011.inputs[0])
    #math_010.Value -> math_011.Value
    hermite_math.links.new(math_010.outputs[0], math_011.inputs[1])
    #math_001.Value -> math_012.Value
    hermite_math.links.new(math_001.outputs[0], math_012.inputs[0])
    #math.Value -> math_012.Value
    hermite_math.links.new(math.outputs[0], math_012.inputs[1])
    #group_input.P0 -> vector_math.Vector
    hermite_math.links.new(group_input.outputs[1], vector_math.inputs[0])
    #math_005.Value -> vector_math.Scale
    hermite_math.links.new(math_005.outputs[0], vector_math.inputs[3])
    #group_input.T0 -> vector_math_001.Vector
    hermite_math.links.new(group_input.outputs[3], vector_math_001.inputs[0])
    #math_008.Value -> vector_math_001.Scale
    hermite_math.links.new(math_008.outputs[0], vector_math_001.inputs[3])
    #group_input.P1 -> vector_math_002.Vector
    hermite_math.links.new(group_input.outputs[2], vector_math_002.inputs[0])
    #math_011.Value -> vector_math_002.Scale
    hermite_math.links.new(math_011.outputs[0], vector_math_002.inputs[3])
    #vector_math_007.Vector -> vector_math_003.Vector
    hermite_math.links.new(vector_math_007.outputs[0], vector_math_003.inputs[0])
    #math_012.Value -> vector_math_003.Scale
    hermite_math.links.new(math_012.outputs[0], vector_math_003.inputs[3])
    #vector_math.Vector -> vector_math_004.Vector
    hermite_math.links.new(vector_math.outputs[0], vector_math_004.inputs[0])
    #vector_math_001.Vector -> vector_math_004.Vector
    hermite_math.links.new(vector_math_001.outputs[0], vector_math_004.inputs[1])
    #vector_math_004.Vector -> vector_math_005.Vector
    hermite_math.links.new(vector_math_004.outputs[0], vector_math_005.inputs[0])
    #vector_math_002.Vector -> vector_math_005.Vector
    hermite_math.links.new(vector_math_002.outputs[0], vector_math_005.inputs[1])
    #vector_math_005.Vector -> vector_math_006.Vector
    hermite_math.links.new(vector_math_005.outputs[0], vector_math_006.inputs[0])
    #vector_math_003.Vector -> vector_math_006.Vector
    hermite_math.links.new(vector_math_003.outputs[0], vector_math_006.inputs[1])
    #vector_math_006.Vector -> group_output.Position
    hermite_math.links.new(vector_math_006.outputs[0], group_output.inputs[0])
    #group_input.T1 -> vector_math_007.Vector
    hermite_math.links.new(group_input.outputs[4], vector_math_007.inputs[0])
    return hermite_math

hermite_math = hermite_math_node_group()

#initialize hermiteg1curve node group
def hermiteg1curve_node_group():
    hermiteg1curve = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "HermiteG1Curve")

    hermiteg1curve.color_tag = 'NONE'
    hermiteg1curve.description = ""
    hermiteg1curve.default_group_node_width = 140
    

    hermiteg1curve.is_modifier = True

    #hermiteg1curve interface
    #Socket Geometry
    geometry_socket = hermiteg1curve.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    #Socket Geometry
    geometry_socket_1 = hermiteg1curve.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    #Socket Count
    count_socket = hermiteg1curve.interface.new_socket(name = "Count", in_out='INPUT', socket_type = 'NodeSocketInt')
    count_socket.default_value = 16
    count_socket.min_value = 1
    count_socket.max_value = 100000
    count_socket.subtype = 'NONE'
    count_socket.attribute_domain = 'POINT'


    #initialize hermiteg1curve nodes
    #node Group Input
    group_input_1 = hermiteg1curve.nodes.new("NodeGroupInput")
    group_input_1.name = "Group Input"
    group_input_1.outputs[1].hide = True

    #node Group
    group = hermiteg1curve.nodes.new("GeometryNodeGroup")
    group.name = "Group"
    group.node_tree = hermite_math

    #node Curve Line.001
    curve_line_001 = hermiteg1curve.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line_001.name = "Curve Line.001"
    curve_line_001.mode = 'POINTS'

    #node Spline Parameter
    spline_parameter = hermiteg1curve.nodes.new("GeometryNodeSplineParameter")
    spline_parameter.name = "Spline Parameter"

    #node Resample Curve
    resample_curve = hermiteg1curve.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    resample_curve.mode = 'COUNT'
    #Selection
    resample_curve.inputs[1].default_value = True

    #node Set Position
    set_position = hermiteg1curve.nodes.new("GeometryNodeSetPosition")
    set_position.label = "1"
    set_position.name = "Set Position"
    #Selection
    set_position.inputs[1].default_value = True
    #Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Vector
    vector = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector.label = "Current"
    vector.name = "Vector"
    vector.vector = (-1.0, 0.0, 0.0)

    #node Vector.001
    vector_001 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_001.label = "Next"
    vector_001.name = "Vector.001"
    vector_001.vector = (0.0, 1.0, 0.0)

    #node Vector Math.003
    vector_math_003_1 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_003_1.name = "Vector Math.003"
    vector_math_003_1.operation = 'SUBTRACT'

    #node Vector.002
    vector_002 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_002.label = "Next + 1"
    vector_002.name = "Vector.002"
    vector_002.vector = (1.0, 0.0, 0.0)

    #node Vector Math.004
    vector_math_004_1 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_004_1.name = "Vector Math.004"
    vector_math_004_1.operation = 'SUBTRACT'

    #node Vector Math.005
    vector_math_005_1 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_005_1.name = "Vector Math.005"
    vector_math_005_1.operation = 'SCALE'
    #Scale
    vector_math_005_1.inputs[3].default_value = 0.5

    #node Group.001
    group_001 = hermiteg1curve.nodes.new("GeometryNodeGroup")
    group_001.name = "Group.001"
    group_001.node_tree = hermite_math

    #node Curve Line.002
    curve_line_002 = hermiteg1curve.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line_002.name = "Curve Line.002"
    curve_line_002.mode = 'POINTS'

    #node Spline Parameter.001
    spline_parameter_001 = hermiteg1curve.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"

    #node Resample Curve.001
    resample_curve_001 = hermiteg1curve.nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.keep_last_segment = True
    resample_curve_001.mode = 'COUNT'
    #Selection
    resample_curve_001.inputs[1].default_value = True

    #node Set Position.001
    set_position_001 = hermiteg1curve.nodes.new("GeometryNodeSetPosition")
    set_position_001.label = "1"
    set_position_001.name = "Set Position.001"
    #Selection
    set_position_001.inputs[1].default_value = True
    #Offset
    set_position_001.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Vector.003
    vector_003 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_003.label = "Current"
    vector_003.name = "Vector.003"
    vector_003.vector = (0.0, 1.0, 0.0)

    #node Vector.004
    vector_004 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_004.label = "Current + 1"
    vector_004.name = "Vector.004"
    vector_004.vector = (1.0, 0.0, 0.0)

    #node Join Geometry
    join_geometry = hermiteg1curve.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    #node Vector.006
    vector_006 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_006.label = "Current - 1"
    vector_006.name = "Vector.006"
    vector_006.vector = (-1.0, 0.0, 0.0)

    #node Vector Math.009
    vector_math_009 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.operation = 'SUBTRACT'

    #node Vector Math.010
    vector_math_010 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.operation = 'SCALE'
    #Scale
    vector_math_010.inputs[3].default_value = 0.5

    #node Repeat Input
    repeat_input = hermiteg1curve.nodes.new("GeometryNodeRepeatInput")
    repeat_input.name = "Repeat Input"
    #node Repeat Output
    repeat_output = hermiteg1curve.nodes.new("GeometryNodeRepeatOutput")
    repeat_output.name = "Repeat Output"
    repeat_output.active_index = 2
    repeat_output.inspection_index = 0
    repeat_output.repeat_items.clear()
    # Create item "Geometry"
    repeat_output.repeat_items.new('GEOMETRY', "Geometry")
    # Create item "Geometry.001"
    repeat_output.repeat_items.new('GEOMETRY', "Geometry.001")
    # Create item "Point Count"
    repeat_output.repeat_items.new('INT', "Point Count")

    #node Sample Index
    sample_index = hermiteg1curve.nodes.new("GeometryNodeSampleIndex")
    sample_index.label = "Current"
    sample_index.name = "Sample Index"
    sample_index.clamp = False
    sample_index.data_type = 'FLOAT_VECTOR'
    sample_index.domain = 'POINT'

    #node Position
    position = hermiteg1curve.nodes.new("GeometryNodeInputPosition")
    position.name = "Position"

    #node Sample Index.001
    sample_index_001 = hermiteg1curve.nodes.new("GeometryNodeSampleIndex")
    sample_index_001.label = "Current + 1"
    sample_index_001.name = "Sample Index.001"
    sample_index_001.clamp = False
    sample_index_001.data_type = 'FLOAT_VECTOR'
    sample_index_001.domain = 'POINT'

    #node Position.001
    position_001 = hermiteg1curve.nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"

    #node Math
    math_1 = hermiteg1curve.nodes.new("ShaderNodeMath")
    math_1.label = "+ 1"
    math_1.name = "Math"
    math_1.hide = True
    math_1.operation = 'ADD'
    math_1.use_clamp = False
    #Value_001
    math_1.inputs[1].default_value = 1.0

    #node Sample Index.002
    sample_index_002 = hermiteg1curve.nodes.new("GeometryNodeSampleIndex")
    sample_index_002.label = "Current + 2"
    sample_index_002.name = "Sample Index.002"
    sample_index_002.clamp = False
    sample_index_002.data_type = 'FLOAT_VECTOR'
    sample_index_002.domain = 'POINT'

    #node Position.002
    position_002 = hermiteg1curve.nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"

    #node Math.001
    math_001_1 = hermiteg1curve.nodes.new("ShaderNodeMath")
    math_001_1.label = "+ 2"
    math_001_1.name = "Math.001"
    math_001_1.hide = True
    math_001_1.operation = 'ADD'
    math_001_1.use_clamp = False
    #Value_001
    math_001_1.inputs[1].default_value = 2.0

    #node Sample Index.003
    sample_index_003 = hermiteg1curve.nodes.new("GeometryNodeSampleIndex")
    sample_index_003.label = "Current - 1"
    sample_index_003.name = "Sample Index.003"
    sample_index_003.clamp = False
    sample_index_003.data_type = 'FLOAT_VECTOR'
    sample_index_003.domain = 'POINT'

    #node Position.003
    position_003 = hermiteg1curve.nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"

    #node Math.003
    math_003_1 = hermiteg1curve.nodes.new("ShaderNodeMath")
    math_003_1.label = "- 1"
    math_003_1.name = "Math.003"
    math_003_1.hide = True
    math_003_1.operation = 'ADD'
    math_003_1.use_clamp = False
    #Value_001
    math_003_1.inputs[1].default_value = -1.0

    #node Reroute.001
    reroute_001 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_001.label = "-1"
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketVector"
    #node Reroute.002
    reroute_002 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_002.label = "0"
    reroute_002.name = "Reroute.002"
    reroute_002.socket_idname = "NodeSocketVector"
    #node Reroute.003
    reroute_003 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_003.label = "+1"
    reroute_003.name = "Reroute.003"
    reroute_003.socket_idname = "NodeSocketVector"
    #node Reroute.004
    reroute_004 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_004.label = "+2"
    reroute_004.name = "Reroute.004"
    reroute_004.socket_idname = "NodeSocketVector"
    #node Reroute.005
    reroute_005 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    reroute_005.socket_idname = "NodeSocketVector"
    #node Reroute.006
    reroute_006 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    reroute_006.socket_idname = "NodeSocketVector"
    #node Reroute.007
    reroute_007 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    reroute_007.socket_idname = "NodeSocketVector"
    #node Reroute.008
    reroute_008 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    reroute_008.socket_idname = "NodeSocketVector"
    #node Reroute.009
    reroute_009 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    reroute_009.socket_idname = "NodeSocketVector"
    #node Reroute.010
    reroute_010 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    reroute_010.socket_idname = "NodeSocketVector"
    #node Group Output
    group_output_1 = hermiteg1curve.nodes.new("NodeGroupOutput")
    group_output_1.name = "Group Output"
    group_output_1.is_active_output = True

    #node Group Input.001
    group_input_001 = hermiteg1curve.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[2].hide = True

    #node Group Input.002
    group_input_002 = hermiteg1curve.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[2].hide = True

    #node Reroute.011
    reroute_011 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_011.label = "Iteration"
    reroute_011.name = "Reroute.011"
    reroute_011.socket_idname = "NodeSocketInt"
    #node Reroute.012
    reroute_012 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_012.label = "Iteration"
    reroute_012.name = "Reroute.012"
    reroute_012.socket_idname = "NodeSocketInt"
    #node Domain Size
    domain_size = hermiteg1curve.nodes.new("GeometryNodeAttributeDomainSize")
    domain_size.name = "Domain Size"
    domain_size.component = 'CURVE'

    #node Reroute.013
    reroute_013 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_013.label = "Point count"
    reroute_013.name = "Reroute.013"
    reroute_013.socket_idname = "NodeSocketInt"
    #node Reroute.014
    reroute_014 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_014.label = "Point count"
    reroute_014.name = "Reroute.014"
    reroute_014.socket_idname = "NodeSocketInt"
    #node Reroute.017
    reroute_017 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_017.label = "0"
    reroute_017.name = "Reroute.017"
    reroute_017.socket_idname = "NodeSocketGeometry"
    #node Group.002
    group_002 = hermiteg1curve.nodes.new("GeometryNodeGroup")
    group_002.name = "Group.002"
    group_002.node_tree = hermite_math

    #node Curve Line.003
    curve_line_003 = hermiteg1curve.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line_003.name = "Curve Line.003"
    curve_line_003.mode = 'POINTS'

    #node Spline Parameter.002
    spline_parameter_002 = hermiteg1curve.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_002.name = "Spline Parameter.002"

    #node Resample Curve.002
    resample_curve_002 = hermiteg1curve.nodes.new("GeometryNodeResampleCurve")
    resample_curve_002.name = "Resample Curve.002"
    resample_curve_002.keep_last_segment = True
    resample_curve_002.mode = 'COUNT'
    #Selection
    resample_curve_002.inputs[1].default_value = True

    #node Set Position.002
    set_position_002 = hermiteg1curve.nodes.new("GeometryNodeSetPosition")
    set_position_002.label = "2"
    set_position_002.name = "Set Position.002"
    #Selection
    set_position_002.inputs[1].default_value = True
    #Offset
    set_position_002.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Vector.005
    vector_005 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_005.label = "Current"
    vector_005.name = "Vector.005"
    vector_005.vector = (1.0, 0.0, 0.0)

    #node Vector.007
    vector_007 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_007.label = "Next"
    vector_007.name = "Vector.007"
    vector_007.vector = (0.0, -1.0, 0.0)

    #node Vector Math.007
    vector_math_007_1 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_007_1.name = "Vector Math.007"
    vector_math_007_1.hide = True
    vector_math_007_1.operation = 'SUBTRACT'

    #node Vector Math.008
    vector_math_008 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.hide = True
    vector_math_008.operation = 'SUBTRACT'

    #node Vector Math.011
    vector_math_011 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.operation = 'SCALE'
    #Scale
    vector_math_011.inputs[3].default_value = 0.5

    #node Reroute.018
    reroute_018 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_018.name = "Reroute.018"
    reroute_018.socket_idname = "NodeSocketVector"
    #node Reroute.019
    reroute_019 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_019.name = "Reroute.019"
    reroute_019.socket_idname = "NodeSocketVector"
    #node Group Input.003
    group_input_003 = hermiteg1curve.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[2].hide = True

    #node Vector.009
    vector_009 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_009.label = "Current - 1"
    vector_009.name = "Vector.009"
    vector_009.vector = (0.0, 1.0, 0.0)

    #node Frame
    frame = hermiteg1curve.nodes.new("NodeFrame")
    frame.label = "Iteration 0"
    frame.name = "Frame"
    frame.label_size = 20
    frame.shrink = True

    #node Frame.001
    frame_001 = hermiteg1curve.nodes.new("NodeFrame")
    frame_001.label = "Iteration 1"
    frame_001.name = "Frame.001"
    frame_001.label_size = 20
    frame_001.shrink = True

    #node Frame.002
    frame_002 = hermiteg1curve.nodes.new("NodeFrame")
    frame_002.label = "Iteration 2"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True

    #node Index Switch
    index_switch = hermiteg1curve.nodes.new("GeometryNodeIndexSwitch")
    index_switch.name = "Index Switch"
    index_switch.data_type = 'GEOMETRY'
    index_switch.index_switch_items.clear()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()
    index_switch.index_switch_items.new()

    #node Reroute.015
    reroute_015 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_015.label = "2"
    reroute_015.name = "Reroute.015"
    reroute_015.socket_idname = "NodeSocketGeometry"
    #node Reroute.016
    reroute_016 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_016.label = "1"
    reroute_016.name = "Reroute.016"
    reroute_016.socket_idname = "NodeSocketGeometry"
    #node Reroute.021
    reroute_021 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_021.name = "Reroute.021"
    reroute_021.socket_idname = "NodeSocketGeometry"
    #node Reroute.022
    reroute_022 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_022.name = "Reroute.022"
    reroute_022.socket_idname = "NodeSocketGeometry"
    #node Reroute.024
    reroute_024 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_024.name = "Reroute.024"
    reroute_024.socket_idname = "NodeSocketGeometry"
    #node Reroute.025
    reroute_025 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_025.name = "Reroute.025"
    reroute_025.socket_idname = "NodeSocketGeometry"
    #node Reroute.026
    reroute_026 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_026.name = "Reroute.026"
    reroute_026.socket_idname = "NodeSocketGeometry"
    #node Vector Math.012
    vector_math_012 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.operation = 'SUBTRACT'

    #node Vector Math.013
    vector_math_013 = hermiteg1curve.nodes.new("ShaderNodeVectorMath")
    vector_math_013.name = "Vector Math.013"
    vector_math_013.operation = 'SCALE'
    #Scale
    vector_math_013.inputs[3].default_value = 0.5

    #node Vector.008
    vector_008 = hermiteg1curve.nodes.new("FunctionNodeInputVector")
    vector_008.label = "Current + 2"
    vector_008.name = "Vector.008"
    vector_008.vector = (0.0, -1.0, 0.0)

    #node Reroute.020
    reroute_020 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_020.name = "Reroute.020"
    reroute_020.socket_idname = "NodeSocketVector"
    #node Reroute.023
    reroute_023 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_023.name = "Reroute.023"
    reroute_023.socket_idname = "NodeSocketVector"
    #node Reroute.027
    reroute_027 = hermiteg1curve.nodes.new("NodeReroute")
    reroute_027.name = "Reroute.027"
    reroute_027.socket_idname = "NodeSocketInt"
    #node Switch
    switch = hermiteg1curve.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'INT'
    #False
    switch.inputs[1].default_value = 1
    #True
    switch.inputs[2].default_value = 0

    #node Compare
    compare = hermiteg1curve.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'INT'
    compare.mode = 'ELEMENT'
    compare.operation = 'EQUAL'
    #B_INT
    compare.inputs[3].default_value = 0

    #node Compare.001
    compare_001 = hermiteg1curve.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'INT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'EQUAL'

    #node Math.004
    math_004_1 = hermiteg1curve.nodes.new("ShaderNodeMath")
    math_004_1.name = "Math.004"
    math_004_1.operation = 'SUBTRACT'
    math_004_1.use_clamp = False
    #Value_001
    math_004_1.inputs[1].default_value = 2.0

    #node Switch.001
    switch_001 = hermiteg1curve.nodes.new("GeometryNodeSwitch")
    switch_001.name = "Switch.001"
    switch_001.input_type = 'INT'
    #True
    switch_001.inputs[2].default_value = 2

    #node Math.005
    math_005_1 = hermiteg1curve.nodes.new("ShaderNodeMath")
    math_005_1.name = "Math.005"
    math_005_1.operation = 'SUBTRACT'
    math_005_1.use_clamp = False
    #Value_001
    math_005_1.inputs[1].default_value = 1.0


    #Process zone input Repeat Input
    repeat_input.pair_with_output(repeat_output)




    #Set parents
    group.parent = frame
    curve_line_001.parent = frame
    spline_parameter.parent = frame
    resample_curve.parent = frame
    set_position.parent = frame
    vector.parent = frame
    vector_001.parent = frame
    vector_math_003_1.parent = frame
    vector_002.parent = frame
    vector_math_004_1.parent = frame
    vector_math_005_1.parent = frame
    group_001.parent = frame_001
    curve_line_002.parent = frame_001
    spline_parameter_001.parent = frame_001
    resample_curve_001.parent = frame_001
    set_position_001.parent = frame_001
    vector_003.parent = frame_001
    vector_004.parent = frame_001
    vector_006.parent = frame_001
    vector_math_009.parent = frame_001
    vector_math_010.parent = frame_001
    reroute_005.parent = frame
    reroute_006.parent = frame
    reroute_007.parent = frame
    reroute_008.parent = frame_001
    reroute_009.parent = frame_001
    reroute_010.parent = frame_001
    group_input_001.parent = frame
    group_input_002.parent = frame_001
    group_002.parent = frame_002
    curve_line_003.parent = frame_002
    spline_parameter_002.parent = frame_002
    resample_curve_002.parent = frame_002
    set_position_002.parent = frame_002
    vector_005.parent = frame_002
    vector_007.parent = frame_002
    vector_math_007_1.parent = frame_002
    vector_math_008.parent = frame_002
    vector_math_011.parent = frame_002
    reroute_018.parent = frame_002
    reroute_019.parent = frame_002
    group_input_003.parent = frame_002
    vector_009.parent = frame_002
    vector_math_012.parent = frame_001
    vector_math_013.parent = frame_001
    vector_008.parent = frame_001
    reroute_020.parent = frame_001
    reroute_023.parent = frame_002

    #Set locations
    group_input_1.location = (-1786.6361083984375, -440.9237976074219)
    group.location = (501.7665710449219, -156.41961669921875)
    curve_line_001.location = (681.88671875, -298.2283935546875)
    spline_parameter.location = (502.66522216796875, -40.1451416015625)
    resample_curve.location = (679.4761962890625, -130.35586547851562)
    set_position.location = (910.50634765625, -153.3394775390625)
    vector.location = (30.80352783203125, -234.70388793945312)
    vector_001.location = (32.8477783203125, -368.6803894042969)
    vector_math_003_1.location = (260.2437744140625, -258.9957275390625)
    vector_002.location = (29.7813720703125, -503.6808166503906)
    vector_math_004_1.location = (260.76763916015625, -458.0190124511719)
    vector_math_005_1.location = (430.50164794921875, -465.10107421875)
    group_001.location = (578.960205078125, -179.7188720703125)
    curve_line_002.location = (702.22265625, -361.658935546875)
    spline_parameter_001.location = (576.8179321289062, -58.8804931640625)
    resample_curve_001.location = (746.0419921875, -120.10574340820312)
    set_position_001.location = (914.6644287109375, -257.0872802734375)
    vector_003.location = (41.179595947265625, -243.1502685546875)
    vector_004.location = (33.4927978515625, -378.2081298828125)
    join_geometry.location = (1254.2440185546875, -420.3836975097656)
    vector_006.location = (48.715179443359375, -71.54290771484375)
    vector_math_009.location = (237.7310028076172, -110.81341552734375)
    vector_math_010.location = (400.9776611328125, -111.40679931640625)
    repeat_input.location = (-1215.4732666015625, -383.5453186035156)
    repeat_output.location = (1740.638916015625, -403.4732971191406)
    sample_index.location = (-984.7660522460938, -166.28311157226562)
    position.location = (-1062.3848876953125, -376.80670166015625)
    sample_index_001.location = (-988.3659057617188, -461.03240966796875)
    position_001.location = (-1065.9847412109375, -671.5560302734375)
    math_1.location = (-1152.9736328125, -618.5198364257812)
    sample_index_002.location = (-994.3656616210938, -737.1724853515625)
    position_002.location = (-1071.9844970703125, -947.6961059570312)
    math_001_1.location = (-1186.5374755859375, -831.5851440429688)
    sample_index_003.location = (-982.3662109375, 114.66400146484375)
    position_003.location = (-1059.9849853515625, -95.85958862304688)
    math_003_1.location = (-1145.7264404296875, -53.65042495727539)
    reroute_001.location = (-761.8909301757812, 52.788970947265625)
    reroute_002.location = (-748.6072387695312, -207.64730834960938)
    reroute_003.location = (-734.501708984375, -489.57916259765625)
    reroute_004.location = (-759.37890625, -784.0066528320312)
    reroute_005.location = (182.70541381835938, -273.55694580078125)
    reroute_006.location = (187.77078247070312, -401.9033508300781)
    reroute_007.location = (182.70541381835938, -539.884521484375)
    reroute_008.location = (205.29098510742188, -280.633544921875)
    reroute_009.location = (197.22018432617188, -413.9573974609375)
    reroute_010.location = (200.96615600585938, -128.08358764648438)
    group_output_1.location = (1952.5279541015625, -452.369384765625)
    group_input_001.location = (685.0096435546875, -55.866424560546875)
    group_input_002.location = (745.9077758789062, -39.850250244140625)
    reroute_011.location = (-762.8768310546875, -615.3097534179688)
    reroute_012.location = (833.6055908203125, -651.300048828125)
    domain_size.location = (-1575.6431884765625, -270.9859619140625)
    reroute_013.location = (-762.4025268554688, -681.7827758789062)
    reroute_014.location = (1699.4853515625, -483.4669494628906)
    reroute_017.location = (766.8833618164062, -332.4453125)
    group_002.location = (547.939208984375, -156.1810302734375)
    curve_line_003.location = (728.059326171875, -297.9901123046875)
    spline_parameter_002.location = (548.8378295898438, -39.9061279296875)
    resample_curve_002.location = (725.6488037109375, -130.1168212890625)
    set_position_002.location = (907.9555053710938, -181.9051513671875)
    vector_005.location = (29.8558349609375, -237.3519287109375)
    vector_007.location = (29.97674560546875, -377.100830078125)
    vector_math_007_1.location = (305.45477294921875, -303.012451171875)
    vector_math_008.location = (226.16290283203125, -86.4266357421875)
    vector_math_011.location = (384.3572998046875, -107.61328125)
    reroute_018.location = (193.29739379882812, -272.356689453125)
    reroute_019.location = (198.36273193359375, -400.703125)
    group_input_003.location = (731.1823120117188, -55.6273193359375)
    vector_009.location = (35.2469482421875, -95.314208984375)
    frame.location = (-451.5, 382.0)
    frame_001.location = (-454.0, -308.0)
    frame_002.location = (-496.0, -1012.0)
    index_switch.location = (996.7060546875, -230.18414306640625)
    reroute_015.location = (782.6926879882812, -417.8772888183594)
    reroute_016.location = (769.0607299804688, -376.8294677734375)
    reroute_021.location = (1697.2122802734375, -437.8306579589844)
    reroute_022.location = (1699.7403564453125, -457.3897399902344)
    reroute_024.location = (-1026.040771484375, -461.1216735839844)
    reroute_025.location = (-1025.349365234375, -483.1230773925781)
    reroute_026.location = (1213.131103515625, -483.0023498535156)
    vector_math_012.location = (247.7512664794922, -290.1435546875)
    vector_math_013.location = (410.1106262207031, -288.9615478515625)
    vector_008.location = (30.1527099609375, -509.6427001953125)
    reroute_020.location = (188.62640380859375, -533.912353515625)
    reroute_023.location = (201.87799072265625, -125.32080078125)
    reroute_027.location = (789.8018188476562, -709.4142456054688)
    switch.location = (1157.3238525390625, -705.59228515625)
    compare.location = (942.1292724609375, -529.7543334960938)
    compare_001.location = (925.7925415039062, -889.320556640625)
    math_004_1.location = (767.4949951171875, -1009.814453125)
    switch_001.location = (1258.724365234375, -885.93896484375)
    math_005_1.location = (-1395.499755859375, -215.14796447753906)

    #Set dimensions
    group_input_1.width, group_input_1.height = 140.0, 100.0
    group.width, group.height = 140.0, 100.0
    curve_line_001.width, curve_line_001.height = 140.0, 100.0
    spline_parameter.width, spline_parameter.height = 140.0, 100.0
    resample_curve.width, resample_curve.height = 140.0, 100.0
    set_position.width, set_position.height = 140.0, 100.0
    vector.width, vector.height = 140.0, 100.0
    vector_001.width, vector_001.height = 140.0, 100.0
    vector_math_003_1.width, vector_math_003_1.height = 140.0, 100.0
    vector_002.width, vector_002.height = 140.0, 100.0
    vector_math_004_1.width, vector_math_004_1.height = 140.0, 100.0
    vector_math_005_1.width, vector_math_005_1.height = 140.0, 100.0
    group_001.width, group_001.height = 140.0, 100.0
    curve_line_002.width, curve_line_002.height = 140.0, 100.0
    spline_parameter_001.width, spline_parameter_001.height = 140.0, 100.0
    resample_curve_001.width, resample_curve_001.height = 140.0, 100.0
    set_position_001.width, set_position_001.height = 140.0, 100.0
    vector_003.width, vector_003.height = 140.0, 100.0
    vector_004.width, vector_004.height = 140.0, 100.0
    join_geometry.width, join_geometry.height = 140.0, 100.0
    vector_006.width, vector_006.height = 140.0, 100.0
    vector_math_009.width, vector_math_009.height = 140.0, 100.0
    vector_math_010.width, vector_math_010.height = 140.0, 100.0
    repeat_input.width, repeat_input.height = 140.0, 100.0
    repeat_output.width, repeat_output.height = 140.0, 100.0
    sample_index.width, sample_index.height = 140.0, 100.0
    position.width, position.height = 140.0, 100.0
    sample_index_001.width, sample_index_001.height = 140.0, 100.0
    position_001.width, position_001.height = 140.0, 100.0
    math_1.width, math_1.height = 140.0, 100.0
    sample_index_002.width, sample_index_002.height = 140.0, 100.0
    position_002.width, position_002.height = 140.0, 100.0
    math_001_1.width, math_001_1.height = 140.0, 100.0
    sample_index_003.width, sample_index_003.height = 140.0, 100.0
    position_003.width, position_003.height = 140.0, 100.0
    math_003_1.width, math_003_1.height = 140.0, 100.0
    reroute_001.width, reroute_001.height = 20.0, 100.0
    reroute_002.width, reroute_002.height = 20.0, 100.0
    reroute_003.width, reroute_003.height = 20.0, 100.0
    reroute_004.width, reroute_004.height = 20.0, 100.0
    reroute_005.width, reroute_005.height = 20.0, 100.0
    reroute_006.width, reroute_006.height = 20.0, 100.0
    reroute_007.width, reroute_007.height = 20.0, 100.0
    reroute_008.width, reroute_008.height = 20.0, 100.0
    reroute_009.width, reroute_009.height = 20.0, 100.0
    reroute_010.width, reroute_010.height = 20.0, 100.0
    group_output_1.width, group_output_1.height = 140.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    reroute_011.width, reroute_011.height = 20.0, 100.0
    reroute_012.width, reroute_012.height = 20.0, 100.0
    domain_size.width, domain_size.height = 140.0, 100.0
    reroute_013.width, reroute_013.height = 20.0, 100.0
    reroute_014.width, reroute_014.height = 20.0, 100.0
    reroute_017.width, reroute_017.height = 20.0, 100.0
    group_002.width, group_002.height = 140.0, 100.0
    curve_line_003.width, curve_line_003.height = 140.0, 100.0
    spline_parameter_002.width, spline_parameter_002.height = 140.0, 100.0
    resample_curve_002.width, resample_curve_002.height = 140.0, 100.0
    set_position_002.width, set_position_002.height = 140.0, 100.0
    vector_005.width, vector_005.height = 140.0, 100.0
    vector_007.width, vector_007.height = 140.0, 100.0
    vector_math_007_1.width, vector_math_007_1.height = 140.0, 100.0
    vector_math_008.width, vector_math_008.height = 140.0, 100.0
    vector_math_011.width, vector_math_011.height = 140.0, 100.0
    reroute_018.width, reroute_018.height = 20.0, 100.0
    reroute_019.width, reroute_019.height = 20.0, 100.0
    group_input_003.width, group_input_003.height = 140.0, 100.0
    vector_009.width, vector_009.height = 140.0, 100.0
    frame.width, frame.height = 1080.5, 653.5
    frame_001.width, frame_001.height = 1084.5, 659.5
    frame_002.width, frame_002.height = 1078.0, 527.0
    index_switch.width, index_switch.height = 140.0, 100.0
    reroute_015.width, reroute_015.height = 20.0, 100.0
    reroute_016.width, reroute_016.height = 20.0, 100.0
    reroute_021.width, reroute_021.height = 20.0, 100.0
    reroute_022.width, reroute_022.height = 20.0, 100.0
    reroute_024.width, reroute_024.height = 20.0, 100.0
    reroute_025.width, reroute_025.height = 20.0, 100.0
    reroute_026.width, reroute_026.height = 20.0, 100.0
    vector_math_012.width, vector_math_012.height = 140.0, 100.0
    vector_math_013.width, vector_math_013.height = 140.0, 100.0
    vector_008.width, vector_008.height = 140.0, 100.0
    reroute_020.width, reroute_020.height = 20.0, 100.0
    reroute_023.width, reroute_023.height = 20.0, 100.0
    reroute_027.width, reroute_027.height = 20.0, 100.0
    switch.width, switch.height = 140.0, 100.0
    compare.width, compare.height = 140.0, 100.0
    compare_001.width, compare_001.height = 140.0, 100.0
    math_004_1.width, math_004_1.height = 140.0, 100.0
    switch_001.width, switch_001.height = 140.0, 100.0
    math_005_1.width, math_005_1.height = 140.0, 100.0

    #initialize hermiteg1curve links
    #spline_parameter.Factor -> group.t
    hermiteg1curve.links.new(spline_parameter.outputs[0], group.inputs[0])
    #curve_line_001.Curve -> resample_curve.Curve
    hermiteg1curve.links.new(curve_line_001.outputs[0], resample_curve.inputs[0])
    #resample_curve.Curve -> set_position.Geometry
    hermiteg1curve.links.new(resample_curve.outputs[0], set_position.inputs[0])
    #group.Position -> set_position.Position
    hermiteg1curve.links.new(group.outputs[0], set_position.inputs[2])
    #reroute_006.Output -> vector_math_003_1.Vector
    hermiteg1curve.links.new(reroute_006.outputs[0], vector_math_003_1.inputs[0])
    #reroute_005.Output -> vector_math_003_1.Vector
    hermiteg1curve.links.new(reroute_005.outputs[0], vector_math_003_1.inputs[1])
    #reroute_005.Output -> curve_line_001.Start
    hermiteg1curve.links.new(reroute_005.outputs[0], curve_line_001.inputs[0])
    #reroute_006.Output -> curve_line_001.End
    hermiteg1curve.links.new(reroute_006.outputs[0], curve_line_001.inputs[1])
    #reroute_005.Output -> group.P0
    hermiteg1curve.links.new(reroute_005.outputs[0], group.inputs[1])
    #reroute_006.Output -> group.P1
    hermiteg1curve.links.new(reroute_006.outputs[0], group.inputs[2])
    #vector_math_003_1.Vector -> group.T0
    hermiteg1curve.links.new(vector_math_003_1.outputs[0], group.inputs[3])
    #vector_math_004_1.Vector -> vector_math_005_1.Vector
    hermiteg1curve.links.new(vector_math_004_1.outputs[0], vector_math_005_1.inputs[0])
    #vector_math_005_1.Vector -> group.T1
    hermiteg1curve.links.new(vector_math_005_1.outputs[0], group.inputs[4])
    #reroute_005.Output -> vector_math_004_1.Vector
    hermiteg1curve.links.new(reroute_005.outputs[0], vector_math_004_1.inputs[0])
    #reroute_007.Output -> vector_math_004_1.Vector
    hermiteg1curve.links.new(reroute_007.outputs[0], vector_math_004_1.inputs[1])
    #spline_parameter_001.Factor -> group_001.t
    hermiteg1curve.links.new(spline_parameter_001.outputs[0], group_001.inputs[0])
    #curve_line_002.Curve -> resample_curve_001.Curve
    hermiteg1curve.links.new(curve_line_002.outputs[0], resample_curve_001.inputs[0])
    #resample_curve_001.Curve -> set_position_001.Geometry
    hermiteg1curve.links.new(resample_curve_001.outputs[0], set_position_001.inputs[0])
    #group_001.Position -> set_position_001.Position
    hermiteg1curve.links.new(group_001.outputs[0], set_position_001.inputs[2])
    #reroute_008.Output -> curve_line_002.Start
    hermiteg1curve.links.new(reroute_008.outputs[0], curve_line_002.inputs[0])
    #reroute_009.Output -> curve_line_002.End
    hermiteg1curve.links.new(reroute_009.outputs[0], curve_line_002.inputs[1])
    #reroute_008.Output -> group_001.P0
    hermiteg1curve.links.new(reroute_008.outputs[0], group_001.inputs[1])
    #reroute_009.Output -> group_001.P1
    hermiteg1curve.links.new(reroute_009.outputs[0], group_001.inputs[2])
    #vector_math_009.Vector -> vector_math_010.Vector
    hermiteg1curve.links.new(vector_math_009.outputs[0], vector_math_010.inputs[0])
    #reroute_009.Output -> vector_math_009.Vector
    hermiteg1curve.links.new(reroute_009.outputs[0], vector_math_009.inputs[0])
    #vector_math_010.Vector -> group_001.T0
    hermiteg1curve.links.new(vector_math_010.outputs[0], group_001.inputs[3])
    #reroute_021.Output -> repeat_output.Geometry
    hermiteg1curve.links.new(reroute_021.outputs[0], repeat_output.inputs[0])
    #group_input_1.Geometry -> repeat_input.Geometry
    hermiteg1curve.links.new(group_input_1.outputs[0], repeat_input.inputs[1])
    #repeat_input.Geometry -> sample_index.Geometry
    hermiteg1curve.links.new(repeat_input.outputs[1], sample_index.inputs[0])
    #repeat_input.Iteration -> sample_index.Index
    hermiteg1curve.links.new(repeat_input.outputs[0], sample_index.inputs[2])
    #position.Position -> sample_index.Value
    hermiteg1curve.links.new(position.outputs[0], sample_index.inputs[1])
    #position_001.Position -> sample_index_001.Value
    hermiteg1curve.links.new(position_001.outputs[0], sample_index_001.inputs[1])
    #repeat_input.Iteration -> math_1.Value
    hermiteg1curve.links.new(repeat_input.outputs[0], math_1.inputs[0])
    #math_1.Value -> sample_index_001.Index
    hermiteg1curve.links.new(math_1.outputs[0], sample_index_001.inputs[2])
    #repeat_input.Geometry -> sample_index_001.Geometry
    hermiteg1curve.links.new(repeat_input.outputs[1], sample_index_001.inputs[0])
    #position_002.Position -> sample_index_002.Value
    hermiteg1curve.links.new(position_002.outputs[0], sample_index_002.inputs[1])
    #repeat_input.Geometry -> sample_index_002.Geometry
    hermiteg1curve.links.new(repeat_input.outputs[1], sample_index_002.inputs[0])
    #repeat_input.Iteration -> math_001_1.Value
    hermiteg1curve.links.new(repeat_input.outputs[0], math_001_1.inputs[0])
    #math_001_1.Value -> sample_index_002.Index
    hermiteg1curve.links.new(math_001_1.outputs[0], sample_index_002.inputs[2])
    #position_003.Position -> sample_index_003.Value
    hermiteg1curve.links.new(position_003.outputs[0], sample_index_003.inputs[1])
    #repeat_input.Geometry -> sample_index_003.Geometry
    hermiteg1curve.links.new(repeat_input.outputs[1], sample_index_003.inputs[0])
    #repeat_input.Iteration -> math_003_1.Value
    hermiteg1curve.links.new(repeat_input.outputs[0], math_003_1.inputs[0])
    #math_003_1.Value -> sample_index_003.Index
    hermiteg1curve.links.new(math_003_1.outputs[0], sample_index_003.inputs[2])
    #sample_index_003.Value -> reroute_001.Input
    hermiteg1curve.links.new(sample_index_003.outputs[0], reroute_001.inputs[0])
    #sample_index.Value -> reroute_002.Input
    hermiteg1curve.links.new(sample_index.outputs[0], reroute_002.inputs[0])
    #sample_index_001.Value -> reroute_003.Input
    hermiteg1curve.links.new(sample_index_001.outputs[0], reroute_003.inputs[0])
    #sample_index_002.Value -> reroute_004.Input
    hermiteg1curve.links.new(sample_index_002.outputs[0], reroute_004.inputs[0])
    #reroute_022.Output -> repeat_output.Geometry.001
    hermiteg1curve.links.new(reroute_022.outputs[0], repeat_output.inputs[1])
    #reroute_002.Output -> reroute_005.Input
    hermiteg1curve.links.new(reroute_002.outputs[0], reroute_005.inputs[0])
    #reroute_003.Output -> reroute_006.Input
    hermiteg1curve.links.new(reroute_003.outputs[0], reroute_006.inputs[0])
    #reroute_004.Output -> reroute_007.Input
    hermiteg1curve.links.new(reroute_004.outputs[0], reroute_007.inputs[0])
    #reroute_010.Output -> vector_math_009.Vector
    hermiteg1curve.links.new(reroute_010.outputs[0], vector_math_009.inputs[1])
    #reroute_001.Output -> reroute_010.Input
    hermiteg1curve.links.new(reroute_001.outputs[0], reroute_010.inputs[0])
    #reroute_002.Output -> reroute_008.Input
    hermiteg1curve.links.new(reroute_002.outputs[0], reroute_008.inputs[0])
    #reroute_003.Output -> reroute_009.Input
    hermiteg1curve.links.new(reroute_003.outputs[0], reroute_009.inputs[0])
    #reroute_026.Output -> join_geometry.Geometry
    hermiteg1curve.links.new(reroute_026.outputs[0], join_geometry.inputs[0])
    #group_input_001.Count -> resample_curve.Count
    hermiteg1curve.links.new(group_input_001.outputs[1], resample_curve.inputs[2])
    #group_input_002.Count -> resample_curve_001.Count
    hermiteg1curve.links.new(group_input_002.outputs[1], resample_curve_001.inputs[2])
    #repeat_output.Geometry.001 -> group_output_1.Geometry
    hermiteg1curve.links.new(repeat_output.outputs[1], group_output_1.inputs[0])
    #repeat_input.Iteration -> reroute_011.Input
    hermiteg1curve.links.new(repeat_input.outputs[0], reroute_011.inputs[0])
    #reroute_011.Output -> reroute_012.Input
    hermiteg1curve.links.new(reroute_011.outputs[0], reroute_012.inputs[0])
    #domain_size.Point Count -> repeat_input.Point Count
    hermiteg1curve.links.new(domain_size.outputs[0], repeat_input.inputs[3])
    #group_input_1.Geometry -> domain_size.Geometry
    hermiteg1curve.links.new(group_input_1.outputs[0], domain_size.inputs[0])
    #repeat_input.Point Count -> reroute_013.Input
    hermiteg1curve.links.new(repeat_input.outputs[3], reroute_013.inputs[0])
    #reroute_027.Output -> reroute_014.Input
    hermiteg1curve.links.new(reroute_027.outputs[0], reroute_014.inputs[0])
    #set_position.Geometry -> reroute_017.Input
    hermiteg1curve.links.new(set_position.outputs[0], reroute_017.inputs[0])
    #spline_parameter_002.Factor -> group_002.t
    hermiteg1curve.links.new(spline_parameter_002.outputs[0], group_002.inputs[0])
    #curve_line_003.Curve -> resample_curve_002.Curve
    hermiteg1curve.links.new(curve_line_003.outputs[0], resample_curve_002.inputs[0])
    #resample_curve_002.Curve -> set_position_002.Geometry
    hermiteg1curve.links.new(resample_curve_002.outputs[0], set_position_002.inputs[0])
    #group_002.Position -> set_position_002.Position
    hermiteg1curve.links.new(group_002.outputs[0], set_position_002.inputs[2])
    #reroute_018.Output -> curve_line_003.Start
    hermiteg1curve.links.new(reroute_018.outputs[0], curve_line_003.inputs[0])
    #reroute_019.Output -> curve_line_003.End
    hermiteg1curve.links.new(reroute_019.outputs[0], curve_line_003.inputs[1])
    #reroute_018.Output -> group_002.P0
    hermiteg1curve.links.new(reroute_018.outputs[0], group_002.inputs[1])
    #vector_math_008.Vector -> vector_math_011.Vector
    hermiteg1curve.links.new(vector_math_008.outputs[0], vector_math_011.inputs[0])
    #group_input_003.Count -> resample_curve_002.Count
    hermiteg1curve.links.new(group_input_003.outputs[1], resample_curve_002.inputs[2])
    #reroute_017.Output -> index_switch.0
    hermiteg1curve.links.new(reroute_017.outputs[0], index_switch.inputs[1])
    #set_position_002.Geometry -> reroute_015.Input
    hermiteg1curve.links.new(set_position_002.outputs[0], reroute_015.inputs[0])
    #reroute_016.Output -> index_switch.1
    hermiteg1curve.links.new(reroute_016.outputs[0], index_switch.inputs[2])
    #reroute_015.Output -> index_switch.2
    hermiteg1curve.links.new(reroute_015.outputs[0], index_switch.inputs[3])
    #set_position_001.Geometry -> reroute_016.Input
    hermiteg1curve.links.new(set_position_001.outputs[0], reroute_016.inputs[0])
    #reroute_024.Output -> reroute_021.Input
    hermiteg1curve.links.new(reroute_024.outputs[0], reroute_021.inputs[0])
    #join_geometry.Geometry -> reroute_022.Input
    hermiteg1curve.links.new(join_geometry.outputs[0], reroute_022.inputs[0])
    #repeat_input.Geometry -> reroute_024.Input
    hermiteg1curve.links.new(repeat_input.outputs[1], reroute_024.inputs[0])
    #repeat_input.Geometry.001 -> reroute_025.Input
    hermiteg1curve.links.new(repeat_input.outputs[2], reroute_025.inputs[0])
    #reroute_025.Output -> reroute_026.Input
    hermiteg1curve.links.new(reroute_025.outputs[0], reroute_026.inputs[0])
    #reroute_014.Output -> repeat_output.Point Count
    hermiteg1curve.links.new(reroute_014.outputs[0], repeat_output.inputs[2])
    #vector_math_012.Vector -> vector_math_013.Vector
    hermiteg1curve.links.new(vector_math_012.outputs[0], vector_math_013.inputs[0])
    #reroute_004.Output -> reroute_020.Input
    hermiteg1curve.links.new(reroute_004.outputs[0], reroute_020.inputs[0])
    #vector_math_013.Vector -> group_001.T1
    hermiteg1curve.links.new(vector_math_013.outputs[0], group_001.inputs[4])
    #reroute_008.Output -> vector_math_012.Vector
    hermiteg1curve.links.new(reroute_008.outputs[0], vector_math_012.inputs[0])
    #reroute_020.Output -> vector_math_012.Vector
    hermiteg1curve.links.new(reroute_020.outputs[0], vector_math_012.inputs[1])
    #reroute_019.Output -> group_002.P1
    hermiteg1curve.links.new(reroute_019.outputs[0], group_002.inputs[2])
    #vector_math_011.Vector -> group_002.T0
    hermiteg1curve.links.new(vector_math_011.outputs[0], group_002.inputs[3])
    #math_005_1.Value -> repeat_input.Iterations
    hermiteg1curve.links.new(math_005_1.outputs[0], repeat_input.inputs[0])
    #reroute_019.Output -> vector_math_008.Vector
    hermiteg1curve.links.new(reroute_019.outputs[0], vector_math_008.inputs[0])
    #reroute_023.Output -> vector_math_008.Vector
    hermiteg1curve.links.new(reroute_023.outputs[0], vector_math_008.inputs[1])
    #vector_math_007_1.Vector -> group_002.T1
    hermiteg1curve.links.new(vector_math_007_1.outputs[0], group_002.inputs[4])
    #reroute_018.Output -> vector_math_007_1.Vector
    hermiteg1curve.links.new(reroute_018.outputs[0], vector_math_007_1.inputs[0])
    #reroute_019.Output -> vector_math_007_1.Vector
    hermiteg1curve.links.new(reroute_019.outputs[0], vector_math_007_1.inputs[1])
    #reroute_001.Output -> reroute_023.Input
    hermiteg1curve.links.new(reroute_001.outputs[0], reroute_023.inputs[0])
    #reroute_002.Output -> reroute_018.Input
    hermiteg1curve.links.new(reroute_002.outputs[0], reroute_018.inputs[0])
    #reroute_003.Output -> reroute_019.Input
    hermiteg1curve.links.new(reroute_003.outputs[0], reroute_019.inputs[0])
    #reroute_013.Output -> reroute_027.Input
    hermiteg1curve.links.new(reroute_013.outputs[0], reroute_027.inputs[0])
    #reroute_012.Output -> compare.A
    hermiteg1curve.links.new(reroute_012.outputs[0], compare.inputs[2])
    #compare.Result -> switch.Switch
    hermiteg1curve.links.new(compare.outputs[0], switch.inputs[0])
    #reroute_027.Output -> math_004_1.Value
    hermiteg1curve.links.new(reroute_027.outputs[0], math_004_1.inputs[0])
    #math_004_1.Value -> compare_001.B
    hermiteg1curve.links.new(math_004_1.outputs[0], compare_001.inputs[3])
    #reroute_012.Output -> compare_001.A
    hermiteg1curve.links.new(reroute_012.outputs[0], compare_001.inputs[2])
    #switch.Output -> switch_001.False
    hermiteg1curve.links.new(switch.outputs[0], switch_001.inputs[1])
    #compare_001.Result -> switch_001.Switch
    hermiteg1curve.links.new(compare_001.outputs[0], switch_001.inputs[0])
    #switch_001.Output -> index_switch.Index
    hermiteg1curve.links.new(switch_001.outputs[0], index_switch.inputs[0])
    #domain_size.Point Count -> math_005_1.Value
    hermiteg1curve.links.new(domain_size.outputs[0], math_005_1.inputs[0])
    #index_switch.Output -> join_geometry.Geometry
    hermiteg1curve.links.new(index_switch.outputs[0], join_geometry.inputs[0])
    return hermiteg1curve

hermiteg1curve = hermiteg1curve_node_group()


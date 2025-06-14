import bpy

#initialize beamng_decalroad node group
def decal_road_node_group():
    group = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "BeamNG_DecalRoad")

    group.color_tag = 'NONE'
    group.description = ""
    group.default_group_node_width = 140
    

    group.is_modifier = True

    #beamng_decalroad interface
    #Socket Geometry
    geometry_socket = group.interface.new_socket(name = "Geometry", in_out='OUTPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket.attribute_domain = 'POINT'

    #Socket Geometry
    geometry_socket_1 = group.interface.new_socket(name = "Geometry", in_out='INPUT', socket_type = 'NodeSocketGeometry')
    geometry_socket_1.attribute_domain = 'POINT'

    #Socket Geometry Offset
    geometry_offset_socket = group.interface.new_socket(name = "Geometry Offset", in_out='INPUT', socket_type = 'NodeSocketFloat')
    geometry_offset_socket.default_value = 0.10000000149011612
    geometry_offset_socket.min_value = -3.4028234663852886e+38
    geometry_offset_socket.max_value = 3.4028234663852886e+38
    geometry_offset_socket.subtype = 'DISTANCE'
    geometry_offset_socket.attribute_domain = 'POINT'
    geometry_offset_socket.force_non_field = True

    #Socket Show Curves
    show_curves_socket = group.interface.new_socket(name = "Show Curves", in_out='INPUT', socket_type = 'NodeSocketBool')
    show_curves_socket.default_value = False
    show_curves_socket.attribute_domain = 'POINT'

    #Socket Geometry Offset
    geometry_offset_socket_1 = group.interface.new_socket(name = "Geometry Offset", in_out='INPUT', socket_type = 'NodeSocketVector')
    geometry_offset_socket_1.default_value = (0.0, 0.0, 0.014999999664723873)
    geometry_offset_socket_1.min_value = -3.4028234663852886e+38
    geometry_offset_socket_1.max_value = 3.4028234663852886e+38
    geometry_offset_socket_1.subtype = 'TRANSLATION'
    geometry_offset_socket_1.attribute_domain = 'POINT'
    geometry_offset_socket_1.force_non_field = True

    #Socket Material
    material_socket = group.interface.new_socket(name = "Material", in_out='INPUT', socket_type = 'NodeSocketMaterial')
    material_socket.attribute_domain = 'POINT'

    #Socket Texture Length
    texture_length_socket = group.interface.new_socket(name = "Texture Length", in_out='INPUT', socket_type = 'NodeSocketFloat')
    texture_length_socket.default_value = 20.0
    texture_length_socket.min_value = 0.0
    texture_length_socket.max_value = 10000.0
    texture_length_socket.subtype = 'DISTANCE'
    texture_length_socket.attribute_domain = 'POINT'


    #initialize beamng_decalroad nodes
    #node Object Info
    object_info = group.nodes.new("GeometryNodeObjectInfo")
    object_info.name = "Object Info"
    object_info.transform_space = 'ORIGINAL'
    if "BeamNG_Terrain" in bpy.data.objects:
        object_info.inputs[0].default_value = bpy.data.objects["BeamNG_Terrain"]
    #As Instance
    object_info.inputs[1].default_value = False

    #node Raycast.002
    raycast_002 = group.nodes.new("GeometryNodeRaycast")
    raycast_002.name = "Raycast.002"
    raycast_002.data_type = 'FLOAT'
    raycast_002.mapping = 'INTERPOLATED'
    #Attribute
    raycast_002.inputs[1].default_value = 0.0
    #Source Position
    raycast_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Ray Direction
    raycast_002.inputs[3].default_value = (0.0, 0.0, -1.0)
    #Ray Length
    raycast_002.inputs[4].default_value = 100.0

    #node Group Input.001
    group_input_001 = group.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[3].hide = True
    group_input_001.outputs[4].hide = True
    group_input_001.outputs[5].hide = True

    #node Group Output.001
    group_output_001 = group.nodes.new("NodeGroupOutput")
    group_output_001.name = "Group Output.001"
    group_output_001.is_active_output = True

    #node Curve Line.001
    curve_line_001 = group.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line_001.name = "Curve Line.001"
    curve_line_001.mode = 'POINTS'

    #node Position.001
    position_001 = group.nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"

    #node For Each Geometry Element Input
    for_each_geometry_element_input = group.nodes.new("GeometryNodeForeachGeometryElementInput")
    for_each_geometry_element_input.name = "For Each Geometry Element Input"
    #node For Each Geometry Element Output
    for_each_geometry_element_output = group.nodes.new("GeometryNodeForeachGeometryElementOutput")
    for_each_geometry_element_output.name = "For Each Geometry Element Output"
    for_each_geometry_element_output.active_generation_index = 0
    for_each_geometry_element_output.active_input_index = 1
    for_each_geometry_element_output.active_main_index = 0
    for_each_geometry_element_output.domain = 'POINT'
    for_each_geometry_element_output.generation_items.clear()
    for_each_geometry_element_output.generation_items.new('GEOMETRY', "Geometry")
    for_each_geometry_element_output.generation_items[0].domain = 'POINT'
    for_each_geometry_element_output.input_items.clear()
    for_each_geometry_element_output.input_items.new('VECTOR', "Position")
    for_each_geometry_element_output.input_items.new('VECTOR', "Hit Position")
    for_each_geometry_element_output.inspection_index = 0
    for_each_geometry_element_output.main_items.clear()

    #node Set Position.005
    set_position_005 = group.nodes.new("GeometryNodeSetPosition")
    set_position_005.name = "Set Position.005"
    #Selection
    set_position_005.inputs[1].default_value = True
    #Offset
    set_position_005.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Set Position
    set_position = group.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    #Selection
    set_position.inputs[1].default_value = True
    #Position
    set_position.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.10000000149011612)

    #node Mix
    mix = group.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'VECTOR'
    mix.factor_mode = 'UNIFORM'

    #node Raycast.003
    raycast_003 = group.nodes.new("GeometryNodeRaycast")
    raycast_003.name = "Raycast.003"
    raycast_003.data_type = 'FLOAT'
    raycast_003.mapping = 'INTERPOLATED'
    #Attribute
    raycast_003.inputs[1].default_value = 0.0
    #Source Position
    raycast_003.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Ray Direction
    raycast_003.inputs[3].default_value = (0.0, 0.0, 1.0)
    #Ray Length
    raycast_003.inputs[4].default_value = 100.0

    #node Compare
    compare = group.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'GREATER_THAN'

    #node Join Geometry.001
    join_geometry_001 = group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"

    #node Set Spline Type
    set_spline_type = group.nodes.new("GeometryNodeCurveSplineType")
    set_spline_type.name = "Set Spline Type"
    set_spline_type.spline_type = 'CATMULL_ROM'
    #Selection
    set_spline_type.inputs[1].default_value = True

    #node Curve to Mesh
    curve_to_mesh = group.nodes.new("GeometryNodeCurveToMesh")
    curve_to_mesh.name = "Curve to Mesh"
    #Fill Caps
    curve_to_mesh.inputs[2].default_value = False

    #node Curve Line
    curve_line = group.nodes.new("GeometryNodeCurvePrimitiveLine")
    curve_line.name = "Curve Line"
    curve_line.mode = 'POINTS'
    #Start
    curve_line.inputs[0].default_value = (-0.5, 0.0, 0.0)
    #End
    curve_line.inputs[1].default_value = (0.5, 0.0, 0.0)

    #node Join Geometry.002
    join_geometry_002 = group.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_002.name = "Join Geometry.002"

    #node Switch
    switch = group.nodes.new("GeometryNodeSwitch")
    switch.name = "Switch"
    switch.input_type = 'GEOMETRY'

    #node Group Input
    group_input = group.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    group_input.outputs[0].hide = True
    group_input.outputs[1].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True
    group_input.outputs[5].hide = True
    group_input.outputs[6].hide = True

    #node Set Position.001
    set_position_001 = group.nodes.new("GeometryNodeSetPosition")
    set_position_001.name = "Set Position.001"
    #Selection
    set_position_001.inputs[1].default_value = True

    #node Mix.001
    mix_001 = group.nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.blend_type = 'MIX'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.data_type = 'VECTOR'
    mix_001.factor_mode = 'UNIFORM'

    #node Group Input.002
    group_input_002 = group.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    group_input_002.outputs[0].hide = True
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[4].hide = True
    group_input_002.outputs[5].hide = True
    group_input_002.outputs[6].hide = True

    #node Resample Curve
    resample_curve = group.nodes.new("GeometryNodeResampleCurve")
    resample_curve.name = "Resample Curve"
    resample_curve.keep_last_segment = True
    resample_curve.mode = 'LENGTH'
    #Selection
    resample_curve.inputs[1].default_value = True
    #Length
    resample_curve.inputs[3].default_value = 0.6669999957084656

    #node Sample Index
    sample_index = group.nodes.new("GeometryNodeSampleIndex")
    sample_index.name = "Sample Index"
    sample_index.clamp = False
    sample_index.data_type = 'FLOAT'
    sample_index.domain = 'POINT'
    #Index
    sample_index.inputs[2].default_value = 0

    #node Radius
    radius = group.nodes.new("GeometryNodeInputRadius")
    radius.name = "Radius"

    #node Set Material
    set_material = group.nodes.new("GeometryNodeSetMaterial")
    set_material.name = "Set Material"
    #Selection
    set_material.inputs[1].default_value = True

    #node Spline Parameter.001
    spline_parameter_001 = group.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_001.name = "Spline Parameter.001"

    #node Store Named Attribute.001
    store_named_attribute_001 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'FLOAT'
    store_named_attribute_001.domain = 'POINT'
    #Selection
    store_named_attribute_001.inputs[1].default_value = True
    #Name
    store_named_attribute_001.inputs[2].default_value = "v"

    #node Resample Curve.001
    resample_curve_001 = group.nodes.new("GeometryNodeResampleCurve")
    resample_curve_001.name = "Resample Curve.001"
    resample_curve_001.keep_last_segment = True
    resample_curve_001.mode = 'COUNT'
    #Selection
    resample_curve_001.inputs[1].default_value = True

    #node Math
    math = group.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'ADD'
    math.use_clamp = False
    #Value_001
    math.inputs[1].default_value = 1.0

    #node Spline Parameter.003
    spline_parameter_003 = group.nodes.new("GeometryNodeSplineParameter")
    spline_parameter_003.name = "Spline Parameter.003"

    #node Store Named Attribute.003
    store_named_attribute_003 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_003.name = "Store Named Attribute.003"
    store_named_attribute_003.data_type = 'FLOAT'
    store_named_attribute_003.domain = 'POINT'
    #Selection
    store_named_attribute_003.inputs[1].default_value = True
    #Name
    store_named_attribute_003.inputs[2].default_value = "u"

    #node Reroute
    reroute = group.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketGeometry"
    #node Reroute.001
    reroute_001 = group.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    reroute_001.socket_idname = "NodeSocketVector"
    #node Named Attribute
    named_attribute = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT'
    #Name
    named_attribute.inputs[0].default_value = "u"

    #node Named Attribute.001
    named_attribute_001 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.data_type = 'FLOAT'
    #Name
    named_attribute_001.inputs[0].default_value = "v"

    #node Combine XYZ
    combine_xyz = group.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    #Z
    combine_xyz.inputs[2].default_value = 0.0

    #node Store Named Attribute
    store_named_attribute = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"
    store_named_attribute.data_type = 'FLOAT2'
    store_named_attribute.domain = 'CORNER'
    #Selection
    store_named_attribute.inputs[1].default_value = True
    #Name
    store_named_attribute.inputs[2].default_value = "UVMap"

    #node Group Input.003
    group_input_003 = group.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[2].hide = True
    group_input_003.outputs[3].hide = True
    group_input_003.outputs[5].hide = True
    group_input_003.outputs[6].hide = True

    #node Curve Length
    curve_length = group.nodes.new("GeometryNodeCurveLength")
    curve_length.name = "Curve Length"

    #node Store Named Attribute.002
    store_named_attribute_002 = group.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_002.name = "Store Named Attribute.002"
    store_named_attribute_002.data_type = 'FLOAT'
    store_named_attribute_002.domain = 'POINT'
    #Selection
    store_named_attribute_002.inputs[1].default_value = True
    #Name
    store_named_attribute_002.inputs[2].default_value = "curve_length"

    #node Named Attribute.003
    named_attribute_003 = group.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_003.name = "Named Attribute.003"
    named_attribute_003.data_type = 'FLOAT'
    #Name
    named_attribute_003.inputs[0].default_value = "curve_length"

    #node Math.001
    math_001 = group.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'DIVIDE'
    math_001.use_clamp = False

    #node Group Input.004
    group_input_004 = group.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[2].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[4].hide = True
    group_input_004.outputs[6].hide = True

    #node Math.002
    math_002 = group.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'MULTIPLY'
    math_002.use_clamp = False



    #Process zone input For Each Geometry Element Input
    for_each_geometry_element_input.pair_with_output(for_each_geometry_element_output)
    #Selection
    for_each_geometry_element_input.inputs[1].default_value = True




    #Set locations
    object_info.location = (-481.27447509765625, 205.540283203125)
    raycast_002.location = (-201.33657836914062, 433.09674072265625)
    group_input_001.location = (-183.01612854003906, 547.6791381835938)
    group_output_001.location = (2579.149658203125, 300.09039306640625)
    curve_line_001.location = (631.1231079101562, 471.9730224609375)
    position_001.location = (336.4638671875, 315.8575439453125)
    for_each_geometry_element_input.location = (380.9617614746094, 552.783447265625)
    for_each_geometry_element_output.location = (871.6124877929688, 514.4056396484375)
    set_position_005.location = (320.0168151855469, 226.04576110839844)
    set_position.location = (62.89717483520508, 530.445068359375)
    mix.location = (29.53924560546875, 109.18043518066406)
    raycast_003.location = (-195.00473022460938, 17.337371826171875)
    compare.location = (31.9376220703125, 268.76385498046875)
    join_geometry_001.location = (2130.765380859375, 307.8304138183594)
    set_spline_type.location = (507.54876708984375, 231.32130432128906)
    curve_to_mesh.location = (1566.85546875, 235.11216735839844)
    curve_line.location = (772.9236450195312, -33.96175765991211)
    join_geometry_002.location = (1045.7911376953125, 458.4713134765625)
    switch.location = (1210.675048828125, 545.7835083007812)
    group_input.location = (1197.3651123046875, 615.6268920898438)
    set_position_001.location = (1760.5792236328125, 231.38897705078125)
    mix_001.location = (26.53240203857422, -103.50265502929688)
    group_input_002.location = (1749.073486328125, 63.035675048828125)
    resample_curve.location = (885.7139282226562, 194.10723876953125)
    sample_index.location = (1156.786376953125, -271.4029541015625)
    radius.location = (1134.23095703125, -489.4535827636719)
    set_material.location = (2331.9375, 341.00048828125)
    spline_parameter_001.location = (956.41552734375, 307.091796875)
    store_named_attribute_001.location = (1151.8116455078125, 277.8951721191406)
    resample_curve_001.location = (1154.5621337890625, 56.006622314453125)
    math.location = (1146.5260009765625, -103.87480926513672)
    spline_parameter_003.location = (980.4659423828125, -213.34161376953125)
    store_named_attribute_003.location = (981.2427368164062, -4.2393035888671875)
    reroute.location = (524.2794189453125, -406.0030822753906)
    reroute_001.location = (1656.5445556640625, 76.23316955566406)
    named_attribute.location = (1745.0673828125, -5.328437805175781)
    named_attribute_001.location = (1743.8009033203125, -155.71298217773438)
    combine_xyz.location = (1941.3411865234375, 5.928823471069336)
    store_named_attribute.location = (1942.6075439453125, 238.36416625976562)
    group_input_003.location = (2329.378173828125, 194.06192016601562)
    curve_length.location = (683.8497924804688, 63.31126403808594)
    store_named_attribute_002.location = (691.5409545898438, 271.0583801269531)
    named_attribute_003.location = (1730.4517822265625, -335.71923828125)
    math_001.location = (1937.757568359375, -311.8304138183594)
    group_input_004.location = (1936.77099609375, -490.89581298828125)
    math_002.location = (1937.7574462890625, -142.4442138671875)

    #Set dimensions
    object_info.width, object_info.height = 196.1361083984375, 100.0
    raycast_002.width, raycast_002.height = 150.0, 100.0
    group_input_001.width, group_input_001.height = 140.0, 100.0
    group_output_001.width, group_output_001.height = 140.0, 100.0
    curve_line_001.width, curve_line_001.height = 140.0, 100.0
    position_001.width, position_001.height = 140.0, 100.0
    for_each_geometry_element_input.width, for_each_geometry_element_input.height = 140.0, 100.0
    for_each_geometry_element_output.width, for_each_geometry_element_output.height = 140.0, 100.0
    set_position_005.width, set_position_005.height = 140.0, 100.0
    set_position.width, set_position.height = 140.0, 100.0
    mix.width, mix.height = 140.0, 100.0
    raycast_003.width, raycast_003.height = 150.0, 100.0
    compare.width, compare.height = 140.0, 100.0
    join_geometry_001.width, join_geometry_001.height = 140.0, 100.0
    set_spline_type.width, set_spline_type.height = 140.0, 100.0
    curve_to_mesh.width, curve_to_mesh.height = 140.0, 100.0
    curve_line.width, curve_line.height = 140.0, 100.0
    join_geometry_002.width, join_geometry_002.height = 140.0, 100.0
    switch.width, switch.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    set_position_001.width, set_position_001.height = 140.0, 100.0
    mix_001.width, mix_001.height = 140.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    resample_curve.width, resample_curve.height = 140.0, 100.0
    sample_index.width, sample_index.height = 140.0, 100.0
    radius.width, radius.height = 140.0, 100.0
    set_material.width, set_material.height = 140.0, 100.0
    spline_parameter_001.width, spline_parameter_001.height = 140.0, 100.0
    store_named_attribute_001.width, store_named_attribute_001.height = 140.0, 100.0
    resample_curve_001.width, resample_curve_001.height = 140.0, 100.0
    math.width, math.height = 140.0, 100.0
    spline_parameter_003.width, spline_parameter_003.height = 140.0, 100.0
    store_named_attribute_003.width, store_named_attribute_003.height = 140.0, 100.0
    reroute.width, reroute.height = 10.0, 100.0
    reroute_001.width, reroute_001.height = 10.0, 100.0
    named_attribute.width, named_attribute.height = 140.0, 100.0
    named_attribute_001.width, named_attribute_001.height = 140.0, 100.0
    combine_xyz.width, combine_xyz.height = 140.0, 100.0
    store_named_attribute.width, store_named_attribute.height = 140.0, 100.0
    group_input_003.width, group_input_003.height = 140.0, 100.0
    curve_length.width, curve_length.height = 140.0, 100.0
    store_named_attribute_002.width, store_named_attribute_002.height = 140.0, 100.0
    named_attribute_003.width, named_attribute_003.height = 140.0, 100.0
    math_001.width, math_001.height = 140.0, 100.0
    group_input_004.width, group_input_004.height = 140.0, 100.0
    math_002.width, math_002.height = 140.0, 100.0

    #initialize beamng_decalroad links
    #set_position.Geometry -> for_each_geometry_element_input.Geometry
    group.links.new(set_position.outputs[0], for_each_geometry_element_input.inputs[0])
    #position_001.Position -> for_each_geometry_element_input.Position
    group.links.new(position_001.outputs[0], for_each_geometry_element_input.inputs[2])
    #for_each_geometry_element_input.Position -> curve_line_001.Start
    group.links.new(for_each_geometry_element_input.outputs[2], curve_line_001.inputs[0])
    #for_each_geometry_element_input.Hit Position -> curve_line_001.End
    group.links.new(for_each_geometry_element_input.outputs[3], curve_line_001.inputs[1])
    #curve_line_001.Curve -> for_each_geometry_element_output.Geometry
    group.links.new(curve_line_001.outputs[0], for_each_geometry_element_output.inputs[1])
    #set_position.Geometry -> set_position_005.Geometry
    group.links.new(set_position.outputs[0], set_position_005.inputs[0])
    #object_info.Geometry -> raycast_002.Target Geometry
    group.links.new(object_info.outputs[4], raycast_002.inputs[0])
    #object_info.Geometry -> raycast_003.Target Geometry
    group.links.new(object_info.outputs[4], raycast_003.inputs[0])
    #raycast_002.Hit Distance -> compare.A
    group.links.new(raycast_002.outputs[3], compare.inputs[0])
    #raycast_003.Hit Distance -> compare.B
    group.links.new(raycast_003.outputs[3], compare.inputs[1])
    #compare.Result -> mix.Factor
    group.links.new(compare.outputs[0], mix.inputs[0])
    #raycast_002.Hit Position -> mix.A
    group.links.new(raycast_002.outputs[1], mix.inputs[4])
    #raycast_003.Hit Position -> mix.B
    group.links.new(raycast_003.outputs[1], mix.inputs[5])
    #mix.Result -> for_each_geometry_element_input.Hit Position
    group.links.new(mix.outputs[1], for_each_geometry_element_input.inputs[3])
    #mix.Result -> set_position_005.Position
    group.links.new(mix.outputs[1], set_position_005.inputs[2])
    #set_position_005.Geometry -> set_spline_type.Curve
    group.links.new(set_position_005.outputs[0], set_spline_type.inputs[0])
    #group_input.Show Curves -> switch.Switch
    group.links.new(group_input.outputs[2], switch.inputs[0])
    #curve_to_mesh.Mesh -> set_position_001.Geometry
    group.links.new(curve_to_mesh.outputs[0], set_position_001.inputs[0])
    #compare.Result -> mix_001.Factor
    group.links.new(compare.outputs[0], mix_001.inputs[0])
    #raycast_002.Hit Normal -> mix_001.A
    group.links.new(raycast_002.outputs[2], mix_001.inputs[4])
    #raycast_003.Hit Normal -> mix_001.B
    group.links.new(raycast_003.outputs[2], mix_001.inputs[5])
    #group_input_002.Geometry Offset -> set_position_001.Offset
    group.links.new(group_input_002.outputs[3], set_position_001.inputs[3])
    #store_named_attribute_001.Geometry -> curve_to_mesh.Curve
    group.links.new(store_named_attribute_001.outputs[0], curve_to_mesh.inputs[0])
    #reroute_001.Output -> set_position_001.Position
    group.links.new(reroute_001.outputs[0], set_position_001.inputs[2])
    #reroute.Output -> sample_index.Geometry
    group.links.new(reroute.outputs[0], sample_index.inputs[0])
    #radius.Radius -> sample_index.Value
    group.links.new(radius.outputs[0], sample_index.inputs[1])
    #group_input_001.Geometry -> set_position.Geometry
    group.links.new(group_input_001.outputs[0], set_position.inputs[0])
    #join_geometry_001.Geometry -> set_material.Geometry
    group.links.new(join_geometry_001.outputs[0], set_material.inputs[0])
    #resample_curve.Curve -> store_named_attribute_001.Geometry
    group.links.new(resample_curve.outputs[0], store_named_attribute_001.inputs[0])
    #spline_parameter_001.Factor -> store_named_attribute_001.Value
    group.links.new(spline_parameter_001.outputs[0], store_named_attribute_001.inputs[3])
    #sample_index.Value -> math.Value
    group.links.new(sample_index.outputs[0], math.inputs[0])
    #math.Value -> resample_curve_001.Count
    group.links.new(math.outputs[0], resample_curve_001.inputs[2])
    #spline_parameter_003.Factor -> store_named_attribute_003.Value
    group.links.new(spline_parameter_003.outputs[0], store_named_attribute_003.inputs[3])
    #curve_line.Curve -> store_named_attribute_003.Geometry
    group.links.new(curve_line.outputs[0], store_named_attribute_003.inputs[0])
    #store_named_attribute_003.Geometry -> resample_curve_001.Curve
    group.links.new(store_named_attribute_003.outputs[0], resample_curve_001.inputs[0])
    #set_position_005.Geometry -> reroute.Input
    group.links.new(set_position_005.outputs[0], reroute.inputs[0])
    #mix.Result -> reroute_001.Input
    group.links.new(mix.outputs[1], reroute_001.inputs[0])
    #resample_curve_001.Curve -> curve_to_mesh.Profile Curve
    group.links.new(resample_curve_001.outputs[0], curve_to_mesh.inputs[1])
    #named_attribute.Attribute -> combine_xyz.X
    group.links.new(named_attribute.outputs[0], combine_xyz.inputs[0])
    #combine_xyz.Vector -> store_named_attribute.Value
    group.links.new(combine_xyz.outputs[0], store_named_attribute.inputs[3])
    #store_named_attribute.Geometry -> join_geometry_001.Geometry
    group.links.new(store_named_attribute.outputs[0], join_geometry_001.inputs[0])
    #set_position_001.Geometry -> store_named_attribute.Geometry
    group.links.new(set_position_001.outputs[0], store_named_attribute.inputs[0])
    #group_input_003.Material -> set_material.Material
    group.links.new(group_input_003.outputs[4], set_material.inputs[2])
    #curve_length.Length -> store_named_attribute_002.Value
    group.links.new(curve_length.outputs[0], store_named_attribute_002.inputs[3])
    #set_spline_type.Curve -> curve_length.Curve
    group.links.new(set_spline_type.outputs[0], curve_length.inputs[0])
    #store_named_attribute_002.Geometry -> resample_curve.Curve
    group.links.new(store_named_attribute_002.outputs[0], resample_curve.inputs[0])
    #set_spline_type.Curve -> store_named_attribute_002.Geometry
    group.links.new(set_spline_type.outputs[0], store_named_attribute_002.inputs[0])
    #named_attribute_003.Attribute -> math_001.Value
    group.links.new(named_attribute_003.outputs[0], math_001.inputs[0])
    #group_input_004.Texture Length -> math_001.Value
    group.links.new(group_input_004.outputs[5], math_001.inputs[1])
    #named_attribute_001.Attribute -> math_002.Value
    group.links.new(named_attribute_001.outputs[0], math_002.inputs[0])
    #math_001.Value -> math_002.Value
    group.links.new(math_001.outputs[0], math_002.inputs[1])
    #math_002.Value -> combine_xyz.Y
    group.links.new(math_002.outputs[0], combine_xyz.inputs[1])
    #set_material.Geometry -> group_output_001.Geometry
    group.links.new(set_material.outputs[0], group_output_001.inputs[0])
    #store_named_attribute_002.Geometry -> join_geometry_002.Geometry
    group.links.new(store_named_attribute_002.outputs[0], join_geometry_002.inputs[0])
    #join_geometry_002.Geometry -> switch.True
    group.links.new(join_geometry_002.outputs[0], switch.inputs[2])
    #switch.Output -> join_geometry_001.Geometry
    group.links.new(switch.outputs[0], join_geometry_001.inputs[0])
    #for_each_geometry_element_output.Geometry -> join_geometry_002.Geometry
    group.links.new(for_each_geometry_element_output.outputs[2], join_geometry_002.inputs[0])
    return group



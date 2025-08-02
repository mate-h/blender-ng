# Blender 4.4 OSL UV Sampler Guide

This guide explains how to use OSL (Open Shading Language) shaders in Blender 4.4's Shader Editor Script nodes to sample UV coordinates from objects in your scene.

## Files Created

1. **`uv_sampler.osl`** - Advanced UV sampler using OSL trace function (CPU only)
2. **`simple_uv_sampler.osl`** - Simplified UV sampler compatible with OptiX backend

## How to Use in Blender 4.4

### Method 1: Using the Script Node (Recommended)

1. **Enable OSL**: Go to `Render Properties` > `Shading System` > Select `Open Shading Language`
2. **Open Blender 4.4** and switch to the **Shading** workspace
3. **Add a Script node** to your material:
   - In the Shader Editor, press `Shift+A`
   - Go to `Converter` > `Script`
4. **Load the OSL shader**:
   - In the Script node, set mode to `External`
   - Click the folder icon and select `simple_uv_sampler.osl` (or `uv_sampler.osl` for CPU rendering)
   - Click the refresh button to compile the shader
5. **Configure inputs**:
   - `WorldPosition`: Connect a coordinate node or leave as default (P)
   - `UVAttribute`: Specify UV layer name (default: "geom:uv")
   - `BlendFactor`: Scaling factor for UV coordinates
6. **Use outputs**:
   - `UV_U`: U coordinate of the UV map
   - `UV_V`: V coordinate of the UV map
   - `UV_Color`: UV coordinates as color for visualization

### Method 2: Text Editor (Development/Testing)

1. **Open the Text Editor** in Blender
2. **Load the OSL shader**:
   - Click `Open` and select `simple_uv_sampler.osl`
3. **Edit the shader** directly in the text editor
4. **Test in Script node**:
   - Set the Script node to `Internal` mode
   - Select the text block containing your OSL shader
   - Click refresh to compile and test

## OSL Shader Features

### Advanced UV Sampling (`uv_sampler.osl`)
- Uses OSL's `trace()` function for ray-based sampling
- Samples UV coordinates from nearby surfaces
- Supports custom UV layers
- Fallback to generated coordinates
- **CPU rendering only** (trace function not available in OptiX)

### Simple UV Sampling (`simple_uv_sampler.osl`)
- Compatible with both CPU and OptiX backends
- Direct UV attribute access using `getattribute()`
- Supports multiple UV layers
- Lightweight and fast
- Color output for visualization

## Usage Examples

### Example 1: Basic UV Sampling

```
# Shader node setup for basic UV sampling
Texture Coordinate (Object) → Script Node → Separate XYZ → Image Texture
```

### Example 2: Dynamic UV Sampling

1. Connect a **Texture Coordinate** node's **Object** output to provide position
2. Use **Mapping** node to transform coordinates
3. Feed transformed coordinates to the Script node
4. Use the UV output for texture sampling

### Example 3: Multi-Object UV Sampling

Modify the `object_name` parameter to sample from different objects:
```python
object_name = "Terrain"     # Sample UV from terrain object
object_name = "Building"    # Sample UV from building object
object_name = ""           # Sample UV from active object
```

## Troubleshooting

### Common Issues

1. **"Object not found" error**:
   - Check the object name spelling
   - Ensure the object exists in the scene
   - Leave object_name empty to use active object

2. **"No UV maps" error**:
   - Ensure your target object has UV coordinates
   - Go to Edit mode and use `U` to unwrap if needed

3. **Script node not working**:
   - Make sure you're using Blender 4.4 or later
   - Check that the script file path is correct
   - Verify the script syntax in Text Editor first

4. **Performance issues**:
   - Use the simplified `shader_script_node.py` for real-time applications
   - Consider caching results for static scenes

### Performance Tips

- Use the Script node version for better performance in complex shaders
- Limit the frequency of UV sampling updates
- Consider pre-computing UV coordinates for static objects

## Technical Details

### Algorithm Overview

1. **Object Selection**: Gets target object by name or uses active object
2. **Space Conversion**: Transforms world position to object local space
3. **Nearest Search**: Finds closest vertex using distance calculation
4. **Face Selection**: Identifies the best face containing the nearest vertex
5. **UV Extraction**: Retrieves UV coordinates from the mesh UV layer
6. **Result Output**: Returns U and V coordinates for shader use

### Coordinate Systems

- **Input**: World space coordinates (X, Y, Z)
- **Processing**: Object local space for accurate sampling
- **Output**: UV coordinates (0.0-1.0 range typically)

## Integration with BeamNG Project

This UV sampler can be particularly useful for:
- Terrain texture sampling based on vehicle position
- Dynamic decal placement
- Road surface material blending
- Environmental effect mapping

Connect the UV sampler output to your material's texture coordinates for dynamic, position-based texturing effects. 
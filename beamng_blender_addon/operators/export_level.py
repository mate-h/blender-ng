"""
BeamNG Level Export Operator
Handles exporting Blender scene data to BeamNG.drive level format
"""

import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
import os
import sys
import struct
import json
import numpy as np
from pathlib import Path


# Add the addon directory to Python path for imports
addon_dir = Path(__file__).parent.parent
if str(addon_dir) not in sys.path:
    sys.path.append(str(addon_dir))

class ExportBeamNGLevel(Operator, ExportHelper):
    """Export BeamNG.drive Level Data"""
    
    bl_idname = "export_scene.beamng_level"
    bl_label = "Export BeamNG Level"
    bl_description = "Export Blender scene to BeamNG.drive level format"
    bl_options = {'REGISTER', 'UNDO'}
    
    # File browser properties
    filename_ext = ""
    filter_glob: StringProperty(
        default="*",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    # Export options
    export_terrain: BoolProperty(
        name="Export Terrain",
        description="Export terrain mesh as .ter file",
        default=True,
    )
    
    export_objects: BoolProperty(
        name="Export Objects",
        description="Export objects as .prefab files",
        default=True,
    )
    
    export_materials: BoolProperty(
        name="Export Materials",
        description="Export materials and textures",
        default=True,
    )
    
    export_config: BoolProperty(
        name="Export Config",
        description="Generate level configuration files",
        default=True,
    )
    
    level_name: StringProperty(
        name="Level Name",
        description="Name for the exported level",
        default="custom_level",
    )
    
    def execute(self, context):
        """Execute the export operation"""
        try:
            # Get export directory
            export_path = os.path.dirname(self.filepath)
            level_directory = os.path.join(export_path, self.level_name)
            
            # Create level directory structure
            self.create_level_directory(level_directory)
            
            self.report({'INFO'}, f"Starting BeamNG level export to: {level_directory}")
            
            # Export terrain if enabled
            if self.export_terrain:
                self.export_terrain_data(level_directory)
            
            # Export objects if enabled
            if self.export_objects:
                self.export_prefab_objects(level_directory)
            
            # Export materials if enabled
            if self.export_materials:
                self.export_material_data(level_directory)
            
            # Export config files if enabled
            if self.export_config:
                self.export_config_data(level_directory)
            
            self.report({'INFO'}, "BeamNG level export completed successfully")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
    
    def create_level_directory(self, level_path):
        """Create BeamNG level directory structure"""
        directories = [
            level_path,
            os.path.join(level_path, "art"),
            os.path.join(level_path, "art", "shapes"),
            os.path.join(level_path, "art", "terrains"),
            os.path.join(level_path, "art", "skies"),
            os.path.join(level_path, "art", "cubemaps"),
            os.path.join(level_path, "art", "decals"),
            os.path.join(level_path, "main"),
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        self.report({'INFO'}, f"Created level directory structure at: {level_path}")
    
    def export_terrain_data(self, level_path):
        """Export terrain data to .ter files"""
        try:
            self.report({'INFO'}, "Exporting terrain data...")
            
            # Find BeamNG terrain object in scene
            terrain_obj = None
            for obj in bpy.context.scene.objects:
                if obj.name == "BeamNG_Terrain" or obj.get('beamng_type') == 'terrain':
                    terrain_obj = obj
                    break
            
            if not terrain_obj:
                self.report({'WARNING'}, "No BeamNG terrain object found in scene")
                return
            
            # Extract terrain textures from the object
            displacement_image, layermap_image, terrain_config = self.extract_terrain_data(terrain_obj)
            
            if not displacement_image:
                self.report({'ERROR'}, "Could not extract displacement data from terrain object")
                return
            
            # Convert Blender images to numpy arrays
            heightmap = self.image_to_heightmap(displacement_image)
            layermap = self.image_to_layermap(layermap_image) if layermap_image else None
            
            # Generate terrain files
            ter_filename = f"{self.level_name}.ter"
            json_filename = f"{self.level_name}.terrain.json"
            
            ter_path = os.path.join(level_path, ter_filename)
            json_path = os.path.join(level_path, json_filename)
            
            # Write .ter file
            self.write_ter_file(heightmap, layermap, ter_path, terrain_config)
            
            # Write .terrain.json file  
            self.write_terrain_json(json_path, terrain_config, ter_filename)
            
            self.report({'INFO'}, f"Exported terrain: {ter_filename}, {json_filename}")
            
        except Exception as e:
            self.report({'ERROR'}, f"Terrain export failed: {str(e)}")
            print(f"❌ Terrain export error: {e}")
    
    def extract_terrain_data(self, terrain_obj):
        """Extract displacement and layermap images from terrain object"""
        displacement_image = None
        layermap_image = None
        terrain_config = {
            'size': 1024,
            'version': 9,
            'materials': ["Grass", "dirt_grass", "BeachSand", "dirt_rocky_large", "dirt_loose", "dirt_dusty", "groundmodel_asphalt1", "Concrete", "Grass2", "Mud", "Rock"],
            'height_scale': 200.0
        }
        
        # Check if object has geometry nodes modifier
        geo_modifier = None
        for modifier in terrain_obj.modifiers:
            if modifier.type == 'NODES' and modifier.node_group:
                geo_modifier = modifier
                break
        
        if geo_modifier and geo_modifier.node_group:
            node_group = geo_modifier.node_group
            
            # Extract images directly from BeamNG_Terrain modifier inputs
            self.report({'INFO'}, f"Found BeamNG_Terrain modifier: {geo_modifier.name}")
            
            # Common input names to check for
            possible_inputs = [
                'Displacement', 'displacement', 'Height', 'height', 'Heightmap', 'heightmap',
                'Layermap', 'layermap', 'Material', 'material', 'MaterialMap', 'materialmap',
                'Size', 'size', 'Scale', 'scale'
            ]
            
            # Print all available keys for debugging
            all_keys = list(geo_modifier.keys())
            self.report({'INFO'}, f"All modifier keys: {all_keys}")
            
            # Check all available inputs in the modifier (both Input_ and Socket_ naming)
            for key in geo_modifier.keys():
                if (key.startswith('Input_') or key.startswith('Socket_') or key in possible_inputs) and not key.endswith('_use_attribute') and not key.endswith('_attribute_name'):
                    try:
                        input_value = geo_modifier[key]
                        input_name = key.lower()
                        
                        self.report({'INFO'}, f"Checking modifier input: {key} = {type(input_value)}")
                        
                        # Check if it's an image
                        if hasattr(input_value, 'name') and hasattr(input_value, 'pixels'):
                            # Based on debug output: Socket_6 has displacement, Socket_7 has layermap
                            image_name = input_value.name.lower()
                            if (key in ['Input_5', 'Socket_6'] or 'heightmap' in input_name or 'displacement' in input_name or 'displacement' in image_name):
                                displacement_image = input_value
                                self.report({'INFO'}, f"Found displacement/heightmap image: {input_value.name} from {key}")
                            elif (key in ['Input_6', 'Socket_7'] or 'layermap' in input_name or 'material' in input_name or 'layermap' in image_name):
                                layermap_image = input_value
                                self.report({'INFO'}, f"Found layermap image: {input_value.name} from {key}")
                        
                        # Check for numeric parameters
                        elif isinstance(input_value, (int, float)):
                            if key in ['Input_1', 'Socket_1'] or 'size' in input_name:
                                terrain_config['size'] = int(input_value)
                                self.report({'INFO'}, f"Found size parameter: {input_value} from {key}")
                            elif key in ['Input_3', 'Socket_3'] or 'height' in input_name:
                                terrain_config['height_scale'] = float(input_value)
                                self.report({'INFO'}, f"Found height scale: {input_value} from {key}")
                        
                        # Check for other types and print them
                        else:
                            self.report({'INFO'}, f"Input {key} has type {type(input_value)}: {input_value}")
                                
                    except (KeyError, TypeError, AttributeError) as e:
                        self.report({'DEBUG'}, f"Could not access input {key}: {e}")
                        continue
            
            # Also try to access specific socket indices that should contain images
            for i in range(2, 9):  # Check Socket_2 through Socket_8 (based on debug output)
                key = f'Socket_{i}'
                if key in geo_modifier:
                    try:
                        input_value = geo_modifier[key]
                        if hasattr(input_value, 'name') and hasattr(input_value, 'pixels'):
                            self.report({'INFO'}, f"Found image at {key}: {input_value.name}")
                            image_name = input_value.name.lower()
                            if i == 6 or 'displacement' in image_name:  # Displacement at Socket_6
                                displacement_image = input_value
                                self.report({'INFO'}, f"Set displacement_image from {key}")
                            elif i == 7 or 'layermap' in image_name:  # Layermap at Socket_7  
                                layermap_image = input_value
                                self.report({'INFO'}, f"Set layermap_image from {key}")
                    except (KeyError, TypeError, AttributeError):
                        continue
            
            # Fallback: Look for texture nodes in the node group if no images found from inputs
            if not displacement_image and not layermap_image:
                for node in node_group.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        image_name = node.image.name.lower()
                        if 'displacement' in image_name or 'height' in image_name:
                            displacement_image = node.image
                        elif 'layermap' in image_name or 'material' in image_name:
                            layermap_image = node.image
        
        # Also check materials for textures as final fallback
        if (not displacement_image or not layermap_image) and terrain_obj.data and terrain_obj.data.materials:
            for material in terrain_obj.data.materials:
                if material and material.node_tree:
                    for node in material.node_tree.nodes:
                        if node.type == 'TEX_IMAGE' and node.image:
                            image_name = node.image.name.lower()
                            if 'displacement' in image_name or 'height' in image_name:
                                displacement_image = node.image
                            elif 'layermap' in image_name or 'material' in image_name:
                                layermap_image = node.image
        
        # Legacy method: Try to extract from modifier using old input names
        if geo_modifier and not displacement_image:
            try:
                if "Input_2" in geo_modifier:  # Size parameter
                    terrain_config['size'] = int(geo_modifier["Input_2"])
                if "Input_4" in geo_modifier:  # Height parameter
                    terrain_config['height_scale'] = float(geo_modifier["Input_4"])
            except (KeyError, ValueError, TypeError):
                pass
        
        return displacement_image, layermap_image, terrain_config
    
    def image_to_heightmap(self, image):
        """Convert Blender image to heightmap numpy array"""
        if not image:
            return None
        
        # Get image dimensions
        width, height = image.size
        
        # Extract pixel data
        pixels = np.array(image.pixels[:], dtype=np.float32)
        
        # Reshape to image dimensions (RGBA format)
        pixels = pixels.reshape((height, width, 4))
        
        # Use red channel for height data
        heightmap_normalized = pixels[:, :, 0]
        
        # Convert from 0-1 range back to 16-bit values
        heightmap = (heightmap_normalized * 65535.0).astype(np.uint16)
        
        return heightmap
    
    def image_to_layermap(self, image):
        """Convert Blender image to layermap numpy array"""
        if not image:
            return None
        
        # Get image dimensions
        width, height = image.size
        
        # Extract pixel data
        pixels = np.array(image.pixels[:], dtype=np.float32)
        
        # Reshape to image dimensions (RGBA format)
        pixels = pixels.reshape((height, width, 4))
        
        # Use red channel for material ID data
        layermap_float = pixels[:, :, 0]
        
        # Convert to 8-bit material IDs
        layermap = np.round(layermap_float).astype(np.uint8)
        
        return layermap
    
    def write_ter_file(self, heightmap, layermap, output_path, config):
        """Write .ter file in BeamNG format"""
        size = config['size']
        materials = config['materials']
        
        with open(output_path, 'wb') as f:
            # Write header (5 bytes total)
            f.write(struct.pack('B', config['version']))  # Version
            f.write(struct.pack('<I', size))  # Size (little-endian)
            
            # Write heightmap data (little-endian 16-bit values)
            if heightmap is not None:
                heightmap_flat = heightmap.flatten()
                heightmap_bytes = struct.pack(f'<{len(heightmap_flat)}H', *heightmap_flat)
                f.write(heightmap_bytes)
            else:
                # Create empty heightmap
                empty_heightmap = np.zeros((size, size), dtype=np.uint16)
                heightmap_flat = empty_heightmap.flatten()
                heightmap_bytes = struct.pack(f'<{len(heightmap_flat)}H', *heightmap_flat)
                f.write(heightmap_bytes)
            
            # Write layermap data (8-bit values)
            if layermap is not None:
                layermap_flat = layermap.flatten()
                layermap_bytes = struct.pack(f'{len(layermap_flat)}B', *layermap_flat)
                f.write(layermap_bytes)
            else:
                # Create empty layermap
                empty_layermap = np.zeros((size, size), dtype=np.uint8)
                layermap_flat = empty_layermap.flatten()
                layermap_bytes = struct.pack(f'{len(layermap_flat)}B', *layermap_flat)
                f.write(layermap_bytes)
            
            # Write material information (CRITICAL for BeamNG)
            f.write(struct.pack('<I', len(materials)))  # Material count
            
            # Write material names as length-prefixed strings
            for material in materials:
                material_bytes = material.encode('ascii')
                f.write(struct.pack('B', len(material_bytes)))
                f.write(material_bytes)
    
    def write_terrain_json(self, output_path, config, ter_filename):
        """Write .terrain.json configuration file"""
        size = config['size']
        
        terrain_config = {
            "binaryFormat": "version(char), size(unsigned int), heightMap(heightMapSize * heightMapItemSize), layerMap(layerMapSize * layerMapItemSize), materialNames",
            "datafile": f"/{ter_filename}",
            "heightMapItemSize": 2,
            "heightMapSize": size * size,
            "layerMapItemSize": 1,
            "layerMapSize": size * size,
            "materials": config['materials'],
            "size": size,
            "version": config['version']
        }
        
        with open(output_path, 'w') as f:
            json.dump(terrain_config, f, indent=2)
    
    def export_prefab_objects(self, level_path):
        """Export objects to .prefab files"""
        self.report({'INFO'}, "Exporting prefab objects... (placeholder)")
        # TODO: Implement prefab export in Phase 6
        pass
    
    def export_material_data(self, level_path):
        """Export materials and textures"""
        self.report({'INFO'}, "Exporting materials... (placeholder)")
        # TODO: Implement material export in Phase 6
        pass
    
    def export_config_data(self, level_path):
        """Export level configuration files"""
        self.report({'INFO'}, "Exporting configuration... (placeholder)")
        # TODO: Implement config export in Phase 6
        
        # Create basic info.json placeholder
        import json
        info_data = {
            "title": f"levels.{self.level_name}.info.title",
            "description": f"levels.{self.level_name}.info.description",
            "size": [1024, 1024],
            "country": "levels.common.country.usa",
            "defaultSpawnPointName": "spawn_main"
        }
        
        info_path = os.path.join(level_path, "info.json")
        with open(info_path, 'w') as f:
            json.dump(info_data, f, indent=2)
        
        self.report({'INFO'}, f"Created basic info.json at: {info_path}")

def register():
    bpy.utils.register_class(ExportBeamNGLevel)
    
    # Add to File > Export menu
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportBeamNGLevel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

def menu_func_export(self, context):
    """Add export option to File > Export menu"""
    self.layout.operator(ExportBeamNGLevel.bl_idname, text="BeamNG Level") 
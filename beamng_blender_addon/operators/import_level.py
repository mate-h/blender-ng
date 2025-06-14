"""
BeamNG Level Import Operator
Handles importing BeamNG.drive level data into Blender
"""

import bpy
from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
import os
import sys
import struct
import json
import numpy as np
import bmesh
from pathlib import Path

# Add the addon directory to Python path for imports
addon_dir = Path(__file__).parent.parent
if str(addon_dir) not in sys.path:
    sys.path.append(str(addon_dir))

# Import BeamNG terrain node group
from ..utils.terrain_node_group import terrain_node_group
# Import terrain material function
from ..utils.terrain_material import terrain_material_node_group
# Import DecalRoad utilities
from ..parsers.decal_road_parser import DecalRoadParser, DecalRoadData, MaterialData
from ..utils.decal_road_material import create_beamng_decal_road_material
from ..utils.decal_road import decal_road_node_group

class BeamNGTerrainParser:
    """Integrated BeamNG terrain parser for the addon - SOURCE OF TRUTH from ter_parser.py"""
    
    def __init__(self, ter_file: str, json_file: str):
        self.ter_file = Path(ter_file)
        self.json_file = Path(json_file)
        self.level_directory = self.ter_file.parent
        
        # Load JSON configuration
        with open(self.json_file, 'r') as f:
            self.config = json.load(f)
        
        # Extract parameters
        self.version = self.config['version']
        self.size = self.config['size']
        self.heightmap_size = self.config['heightMapSize']
        self.heightmap_item_size = self.config['heightMapItemSize']
        self.layermap_size = self.config['layerMapSize']
        self.layermap_item_size = self.config['layerMapItemSize']
        self.materials = self.config['materials']
        
        # 🆕 Detect height scale from terrain preset files
        self.height_scale = self.detect_height_scale()
        self.terrain_position = self.detect_terrain_position()
        
        print("🏞️  BeamNG Terrain Parser")
        print(f"📁 Terrain: {self.ter_file.name}")
        print(f"📊 Dimensions: {self.size}x{self.size}")
        print(f"🎭 Materials: {len(self.materials)}")
        print(f"⛰️  Height Scale: {self.height_scale}")
        if self.terrain_position:
            print(f"📍 Position: {self.terrain_position}")
        print("✅ Using offset 5 (after header), all data: little-endian")
    
    def detect_height_scale(self):
        """Detect height scale from terrain preset files - Task 0.2.2"""
        try:
            # Look for terrain preset files in level directory
            # Pattern: *terrainPreset.json or *TerrainPreset.json
            preset_files = []
            for pattern in ['*terrainPreset.json', '*TerrainPreset.json', '*terrainpreset.json']:
                preset_files.extend(self.level_directory.glob(pattern))
            
            if not preset_files:
                print("⚠️  No terrain preset files found, using default height scale: 200")
                return 200.0  # Default fallback
            
            # Use the first preset file found
            preset_file = preset_files[0]
            print(f"📄 Found terrain preset: {preset_file.name}")
            
            with open(preset_file, 'r') as f:
                preset_data = json.load(f)
            
            height_scale = preset_data.get('heightScale', 200.0)
            print(f"✅ Detected height scale: {height_scale}")
            return float(height_scale)
            
        except Exception as e:
            print(f"❌ Error detecting height scale: {e}")
            print("⚠️  Using default height scale: 200")
            return 200.0
    
    def detect_terrain_position(self):
        """Detect terrain position from terrain preset files"""
        try:
            # Look for terrain preset files
            preset_files = []
            for pattern in ['*terrainPreset.json', '*TerrainPreset.json', '*terrainpreset.json']:
                preset_files.extend(self.level_directory.glob(pattern))
            
            if not preset_files:
                return None
            
            preset_file = preset_files[0]
            with open(preset_file, 'r') as f:
                preset_data = json.load(f)
            
            pos_data = preset_data.get('pos', {})
            if pos_data:
                position = {
                    'x': pos_data.get('x', 0),
                    'y': pos_data.get('y', 0), 
                    'z': pos_data.get('z', 0)
                }
                print(f"✅ Detected terrain position: {position}")
                return position
            return None
            
        except Exception as e:
            print(f"❌ Error detecting terrain position: {e}")
            return None
    
    def parse_terrain(self):
        """Parse the terrain file using CORRECTED offset and encoding"""
        
        with open(self.ter_file, 'rb') as f:
            # Read header (little-endian)
            version = struct.unpack('B', f.read(1))[0]
            size = struct.unpack('<I', f.read(4))[0]
            
            # Verify header
            if version != self.version or size != self.size:
                raise ValueError(f"Header mismatch: got version={version}, size={size}")
            
            # FIXED: Data starts at offset 5 (immediately after header)
            data_start = 5
            print(f"📍 Using CORRECTED data offset: {data_start} (0x{data_start:x})")
            
            # Read heightmap with LITTLE-ENDIAN encoding
            f.seek(data_start)
            heightmap_bytes = self.heightmap_size * self.heightmap_item_size
            heightmap_data = f.read(heightmap_bytes)
            
            if len(heightmap_data) != heightmap_bytes:
                print(f"⚠️  Warning: Expected {heightmap_bytes} bytes, got {len(heightmap_data)}")
            
            # Parse as 16-bit LITTLE-ENDIAN (CORRECTED)
            num_heights = len(heightmap_data) // 2
            heights = struct.unpack(f'<{num_heights}H', heightmap_data)  # <H = little-endian
            
            # Reshape to 2D
            heightmap = np.array(heights, dtype=np.uint16).reshape((self.size, self.size))
            
            # Calculate layer map position
            layermap_start = data_start + heightmap_bytes
            layermap = None
            
            try:
                f.seek(layermap_start)
                
                # Calculate how much layermap data is actually available
                remaining_file_bytes = len(f.read())  # Read to end to get remaining size
                f.seek(layermap_start)  # Seek back
                
                expected_layermap_bytes = self.layermap_size * self.layermap_item_size
                available_layermap_bytes = min(expected_layermap_bytes, remaining_file_bytes)
                
                print("📊 Layermap info:")
                print(f"   Expected: {expected_layermap_bytes:,} bytes")
                print(f"   Available: {available_layermap_bytes:,} bytes")
                
                if available_layermap_bytes > 0:
                    layermap_data = f.read(available_layermap_bytes)
                    layers = struct.unpack(f'{len(layermap_data)}B', layermap_data)
                    
                    # Calculate how many complete rows we have
                    pixels_available = len(layers)
                    complete_rows = pixels_available // self.size
                    remaining_pixels = pixels_available % self.size
                    
                    print(f"   Pixels available: {pixels_available:,}")
                    print(f"   Complete rows: {complete_rows}")
                    print(f"   Remaining pixels: {remaining_pixels}")
                    
                    if complete_rows > 0:
                        # Create layermap with available data, pad with zeros if needed
                        if pixels_available == self.layermap_size:
                            # Perfect match
                            layermap = np.array(layers, dtype=np.uint8).reshape((self.size, self.size))
                            print(f"✅ Complete layer map loaded: {layermap.shape}")
                        else:
                            # Partial data - pad with zeros or truncate
                            if pixels_available < self.layermap_size:
                                # Pad with zeros
                                padded_layers = list(layers) + [0] * (self.layermap_size - pixels_available)
                                layermap = np.array(padded_layers, dtype=np.uint8).reshape((self.size, self.size))
                                print(f"⚠️  Partial layer map loaded and padded: {layermap.shape}")
                            else:
                                # Truncate to expected size
                                truncated_layers = layers[:self.layermap_size]
                                layermap = np.array(truncated_layers, dtype=np.uint8).reshape((self.size, self.size))
                                print(f"⚠️  Layer map loaded and truncated: {layermap.shape}")
                    else:
                        print("❌ Not enough data for even one complete row")
                        layermap = None
                else:
                    print("❌ No layermap data available")
                    layermap = None
                    
            except Exception as e:
                print(f"❌ Could not read layer map: {e}")
                layermap = None
            
            return {
                'header': {
                    'version': version,
                    'size': size,
                    'data_start': data_start,
                    'encoding': 'all_little_endian'  # CORRECTED encoding description
                },
                'heightmap': heightmap,
                'layermap': layermap,
                'materials': self.materials,
                'config': self.config,
                'height_scale': self.height_scale,  # 🆕 Auto-detected height scale
                'terrain_position': self.terrain_position  # 🆕 Auto-detected position
            }
    
    def get_terrain_stats(self, heightmap: np.ndarray):
        """Calculate terrain statistics"""
        return {
            'shape': heightmap.shape,
            'min_height': int(np.min(heightmap)),
            'max_height': int(np.max(heightmap)),
            'mean_height': float(np.mean(heightmap)),
            'std_height': float(np.std(heightmap)),
            'median_height': float(np.median(heightmap)),
            'unique_values': len(np.unique(heightmap)),
            'zero_count': int(np.sum(heightmap == 0)),
            'zero_percentage': float(np.sum(heightmap == 0) / heightmap.size * 100)
        }

class ImportBeamNGLevel(Operator, ImportHelper):
    """Import BeamNG.drive Level Data"""
    
    bl_idname = "import_scene.beamng_level"
    bl_label = "Import BeamNG Level"
    bl_description = "Import BeamNG.drive level data including terrain, objects, and materials"
    bl_options = {'REGISTER', 'UNDO'}
    
    # File browser properties
    filename_ext = ""
    filter_glob: StringProperty(
        default="*.ter;*.prefab;*.json",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    # Import options
    import_terrain: BoolProperty(
        name="Import Terrain",
        description="Import terrain mesh and materials",
        default=True,
    )
    
    import_objects: BoolProperty(
        name="Import Objects",
        description="Import prefab objects and static meshes",
        default=True,
    )
    
    import_materials: BoolProperty(
        name="Import Materials",
        description="Import and convert materials/textures",
        default=True,
    )
    
    import_lighting: BoolProperty(
        name="Import Lighting",
        description="Import lighting and environment settings",
        default=False,
    )
    
    import_decal_roads: BoolProperty(
        name="Import DecalRoads",
        description="Import DecalRoad objects with materials and geometry nodes",
        default=True,
    )
    
    def execute(self, context):
        """Execute the import operation"""
        try:
            # Get the selected file/directory path
            filepath = self.filepath
            directory = os.path.dirname(filepath)
            
            # Check if this is a BeamNG level directory
            if not self.is_beamng_level(directory):
                self.report({'ERROR'}, "Selected path is not a valid BeamNG level directory")
                return {'CANCELLED'}
            
            # Start import process
            self.report({'INFO'}, f"Starting BeamNG level import from: {directory}")
            
            # Import terrain if enabled
            if self.import_terrain:
                result = self.import_terrain_data(directory)
                if result == {'CANCELLED'}:
                    return {'CANCELLED'}
            
            # Import objects if enabled
            if self.import_objects:
                self.import_prefab_objects(directory)
            
            # Import materials if enabled
            if self.import_materials:
                self.import_material_data(directory)
            
            # Import lighting if enabled
            if self.import_lighting:
                self.import_lighting_data(directory)
            
            # Import DecalRoads if enabled
            if self.import_decal_roads:
                self.import_decal_roads_data(directory)
            
            self.report({'INFO'}, "BeamNG level import completed successfully")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {str(e)}")
            return {'CANCELLED'}
    
    def is_beamng_level(self, directory):
        """Check if directory contains BeamNG level data"""
        # Look for key BeamNG level files
        required_files = ['info.json', 'mainLevel.lua']
        for filename in required_files:
            if os.path.exists(os.path.join(directory, filename)):
                return True
        
        # Check for .ter files (terrain data)
        for file in os.listdir(directory):
            if file.endswith('.ter'):
                return True
        
        return False
    
    def import_terrain_data(self, directory):
        """Import terrain data using EXR displacement mapping"""
        try:
            # Find .ter and .terrain.json files
            ter_file = None
            json_file = None
            
            for file in os.listdir(directory):
                if file.endswith('.ter'):
                    ter_file = os.path.join(directory, file)
                elif file.endswith('.terrain.json'):
                    json_file = os.path.join(directory, file)
            
            if not ter_file or not json_file:
                self.report({'ERROR'}, "Could not find required .ter and .terrain.json files")
                return {'CANCELLED'}
            
            self.report({'INFO'}, f"Parsing terrain files: {os.path.basename(ter_file)}")
            
            # Parse terrain data
            parser = BeamNGTerrainParser(ter_file, json_file)
            terrain_data = parser.parse_terrain()
            # Add level directory to terrain data for texture loading
            terrain_data['level_directory'] = directory
            heightmap = terrain_data['heightmap']
            layermap = terrain_data['layermap']
            
            # Create EXR displacement texture
            self.report({'INFO'}, "Creating 16-bit EXR displacement texture...")
            displacement_texture = self.create_displacement_texture(heightmap)
            
            # Create layermap texture if available
            layermap_texture = None
            if layermap is not None:
                self.report({'INFO'}, "Creating layermap texture...")
                layermap_texture = self.create_layermap_texture(layermap, terrain_data['materials'])
            
            # Create terrain mesh with BeamNG node group
            self.report({'INFO'}, "Creating terrain mesh with BeamNG node group...")
            terrain_obj = self.create_terrain_with_node_group(
                displacement_texture, layermap_texture, terrain_data
            )
            
            # Adjust camera clip planes for large terrain
            self.adjust_camera_clip_planes()
            
            # Adjust 3D viewport clip planes as requested
            self.adjust_viewport_clip_planes()
            
            # Frame the imported terrain in view
            self.frame_imported_terrain(terrain_obj)
            
            self.report({'INFO'}, f"Terrain imported successfully: {terrain_obj.name}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Terrain import failed: {str(e)}")
            return {'CANCELLED'}
    
    def create_displacement_texture(self, heightmap):
        """Create a 16-bit EXR texture for displacement mapping"""
        
        print("🏔️  Converting heightmap to texture...")
        print(f"   Input shape: {heightmap.shape}")
        print(f"   Value range: {heightmap.min()} - {heightmap.max()}")
        
        # Normalize heightmap to 0-1 range for displacement (matching npy_to_exr.py)
        heightmap_normalized = heightmap.astype(np.float32) / 65535.0
        
        print(f"   Normalized range: {heightmap_normalized.min():.1f} - {heightmap_normalized.max():.1f}")
        
        # Create Blender image
        image_name = "BeamNG_Terrain_Displacement.exr"
        
        # Remove existing image if it exists
        if image_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[image_name])
        
        # Create new image
        height, width = heightmap_normalized.shape
        displacement_image = bpy.data.images.new(
            name=image_name,
            width=width,
            height=height,
            alpha=False,
            float_buffer=True  # Use float buffer for 16-bit precision
        )
        
        # Convert heightmap to RGBA format for Blender (R=height, G=height, B=height, A=1)
        rgba_data = np.zeros((height, width, 4), dtype=np.float32)
        rgba_data[:, :, 0] = heightmap_normalized  # Red channel
        rgba_data[:, :, 1] = heightmap_normalized  # Green channel  
        rgba_data[:, :, 2] = heightmap_normalized  # Blue channel
        rgba_data[:, :, 3] = 1.0  # Alpha channel
        
        # Flatten for Blender (Blender expects flattened RGBA array)
        displacement_image.pixels = rgba_data.flatten()
        
        # Update image
        displacement_image.update()
        displacement_image.pack()
        
        # Save as EXR file
        displacement_image.file_format = 'OPEN_EXR'
        
        print(f"✅ Created displacement texture: {image_name} ({width}x{height})")
        print(f"   Size: {width}x{height}")
        print(f"   Value range: {heightmap_normalized.min():.1f} - {heightmap_normalized.max():.1f}")
        return displacement_image
    
    def create_layermap_texture(self, layermap, materials):
        """Create a texture for the layermap (material indices)"""
        
        print("🎨 Converting layermap to texture...")
        print(f"   Input shape: {layermap.shape}")
        print(f"   Value range: {layermap.min()} - {layermap.max()}")
        print(f"   Unique materials: {len(np.unique(layermap))}")
        
        # Create Blender image
        image_name = "BeamNG_Terrain_Layermap"
        
        # Remove existing image if it exists
        if image_name in bpy.data.images:
            bpy.data.images.remove(bpy.data.images[image_name])
        
        # Create new image
        height, width = layermap.shape
        layermap_image = bpy.data.images.new(
            name=image_name,
            width=width,
            height=height,
            alpha=False,
            float_buffer=True  # Use float buffer for better precision
        )
        
        # DO NOT normalize layermap - keep raw material ID values (matching npy_to_exr.py)
        layermap_normalized = layermap.astype(np.float32)
        if layermap.max() == 0:
            print("⚠️  WARNING: Layermap is all zeros")
        
        # Convert layermap to RGBA format for Blender (R=G=B=material_id, A=1)
        rgba_data = np.zeros((height, width, 4), dtype=np.float32)
        rgba_data[:, :, 0] = layermap_normalized  # Red channel
        rgba_data[:, :, 1] = layermap_normalized  # Green channel  
        rgba_data[:, :, 2] = layermap_normalized  # Blue channel
        rgba_data[:, :, 3] = 1.0  # Alpha channel
        
        # Keep it simple - just flatten the RGBA data directly (like npy_to_exr.py)
        pixel_data = rgba_data.flatten()
        
        # Set pixels to Blender image
        layermap_image.pixels = pixel_data
        
        # Force update and pack the image
        layermap_image.update()
        layermap_image.pack()
        
        # Set colorspace to Non-Color for data textures
        layermap_image.colorspace_settings.name = 'Non-Color'
        
        # Save as EXR file
        layermap_image.file_format = 'OPEN_EXR'
        
        # Force another update after format change
        layermap_image.update()
                
        print(f"✅ Created layermap texture: {image_name} ({width}x{height})")
        
        # Print material mapping (like in npy_to_exr.py)
        unique_values = np.unique(layermap)
        print("   Material mapping:")
        for mat_id in unique_values[:10]:  # Show first 10
            if mat_id < len(materials):
                material_name = materials[mat_id]
                print(f"     ID {mat_id} → {material_name}")
        
        return layermap_image
    
    def create_terrain_with_node_group(self, displacement_texture, layermap_texture, terrain_data):
        """Create terrain mesh using BeamNG geometry node group with auto-detected settings"""
        
        # Get terrain dimensions and settings
        config = terrain_data['config']
        terrain_size = config['size']
        
        # 🆕 Use auto-detected height scale instead of hardcoded displacement strength
        displacement_strength =  terrain_data['height_scale']
        
        # Apply terrain position offset if detected
        terrain_position = terrain_data.get('terrain_position', None)

        print(f"🆕 Would use the following terrain position: {terrain_position}")
        
        # Calculate resolution early for use in node group
        heightmap_resolution = config.get('heightMapSize', 1024)
        # Calculate resolution as square root since heightMapSize is total pixels
        vertex_resolution = int(np.sqrt(heightmap_resolution))
        
        # Create base plane mesh
        bpy.ops.mesh.primitive_plane_add(size=1.0)  # Unit size, will be scaled by node group
        terrain_obj = bpy.context.active_object
        terrain_obj.name = "BeamNG_Terrain"
        
        # Prepare terrain position (convert to tuple if available)
        terrain_pos = (0.0, 0.0, 0.0)
        if terrain_position:
            terrain_pos = (
                terrain_position.get('x', 0.0),
                terrain_position.get('y', 0.0),
                terrain_position.get('z', 0.0)
            )
        
        # Create advanced terrain material with textures
        material_name = "BeamNG_Terrain_Material"
        
        # Find terrain texture files in the level directory
        # Get level directory from terrain data
        level_dir = Path(terrain_data.get('level_directory', ''))
        terrain_textures_dir = level_dir / "art" / "terrains"
        
        # Look for common terrain texture patterns
        texture_ao_path = None
        texture_base_path = None  
        texture_roughness_path = None
        
        if terrain_textures_dir.exists():
            # Find texture files - prioritize terrain_base textures first
            texture_patterns = {
                'ao': ['t_terrain_base_ao.png', 't_terrain_base02_ao.png'],
                'base': ['t_terrain_base_b.png', 't_terrain_base02_b.png'],
                'roughness': ['t_terrain_base_r.png', 't_terrain_base02_r.png']
            }
            
            for tex_type, patterns in texture_patterns.items():
                for pattern in patterns:
                    tex_path = terrain_textures_dir / pattern
                    if tex_path.exists():
                        if tex_type == 'ao':
                            texture_ao_path = str(tex_path)
                        elif tex_type == 'base':
                            texture_base_path = str(tex_path)
                        elif tex_type == 'roughness':
                            texture_roughness_path = str(tex_path)
                        print(f"📁 Found terrain texture ({tex_type}): {pattern}")
                        break
        
        # Create terrain material with found textures
        terrain_material = terrain_material_node_group(
            material_name=material_name,
            texture_ao_path=texture_ao_path,
            texture_base_path=texture_base_path,
            texture_roughness_path=texture_roughness_path
        )
        
        print(f"✅ Created terrain material: {terrain_material.name}")
        print(f"   Material ID: {id(terrain_material)}")
        if texture_ao_path:
            print(f"   AO texture: {Path(texture_ao_path).name}")
        if texture_base_path:
            print(f"   Base texture: {Path(texture_base_path).name}")
        if texture_roughness_path:
            print(f"   Roughness texture: {Path(texture_roughness_path).name}")
        
        # Assign material directly to the terrain object as well
        if terrain_obj.data.materials:
            terrain_obj.data.materials[0] = terrain_material
        else:
            terrain_obj.data.materials.append(terrain_material)
        print(f"✅ Assigned material to terrain object: {terrain_obj.name}")
        
        # Create or get the BeamNG terrain node group with all parameters
        node_group = terrain_node_group(
            displacement_image=displacement_texture,
            layermap_image=layermap_texture,
            material=terrain_material,
            position=terrain_pos,
            size=terrain_size,
            resolution=vertex_resolution,
            height=displacement_strength
        )
        
        # Add geometry nodes modifier
        geo_nodes_mod = terrain_obj.modifiers.new(name="BeamNG_Terrain", type='NODES')
        geo_nodes_mod.node_group = node_group
        
        # Set node group parameters
        # Size (terrain dimensions in world units)
        geo_nodes_mod["Input_2"] = terrain_size
        
        # Resolution (number of vertices per axis)
        geo_nodes_mod["Input_3"] = vertex_resolution
        
        # Height (displacement strength)
        geo_nodes_mod["Input_4"] = displacement_strength
        
        print(f"✅ Created terrain mesh with BeamNG node group: {terrain_obj.name}")
        print(f"   Size: {terrain_size} units")
        print(f"   Resolution: {vertex_resolution}x{vertex_resolution}")
        print(f"   Height: {displacement_strength}")
        
        return terrain_obj
    
    def adjust_camera_clip_planes(self):
        """Adjust camera clip planes to handle large terrain better"""
        
        # Get the active scene
        scene = bpy.context.scene
        
        # Adjust clip planes for all cameras in the scene
        cameras_adjusted = 0
        for obj in scene.objects:
            if obj.type == 'CAMERA':
                camera_data = obj.data
                
                # Adjust near clip plane (increase by one order of magnitude if < 0.1)
                if camera_data.clip_start < 0.1:
                    old_near = camera_data.clip_start
                    camera_data.clip_start = min(old_near * 10, 0.1)
                    print(f"📷 Camera '{obj.name}' near clip: {old_near} → {camera_data.clip_start}")
                
                # Adjust far clip plane (increase by one order of magnitude if < 10000)
                if camera_data.clip_end < 10000:
                    old_far = camera_data.clip_end
                    camera_data.clip_end = min(old_far * 10, 100000)
                    print(f"📷 Camera '{obj.name}' far clip: {old_far} → {camera_data.clip_end}")
                
                cameras_adjusted += 1
        
        # If no cameras exist, create a default camera with appropriate clip planes
        if cameras_adjusted == 0:
            bpy.ops.object.camera_add()
            camera_obj = bpy.context.active_object
            camera_obj.name = "BeamNG_Camera"
            camera_data = camera_obj.data
            
            # Set appropriate clip planes for large terrain
            camera_data.clip_start = 0.1
            camera_data.clip_end = 100000
            
            # Position camera above terrain center
            camera_obj.location = (0, 0, 1000)
            camera_obj.rotation_euler = (0, 0, 0)
            
            print(f"📷 Created camera '{camera_obj.name}' with clip planes: {camera_data.clip_start} - {camera_data.clip_end}")
            cameras_adjusted += 1
        
        print(f"✅ Adjusted clip planes for {cameras_adjusted} camera(s)")
    
    def adjust_viewport_clip_planes(self):
        """Adjust 3D viewport clip planes for large terrain viewing"""
        
        # Iterate through all 3D viewports in all areas and screens
        viewports_adjusted = 0
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for space in area.spaces:
                        if space.type == 'VIEW_3D':
                            old_near = space.clip_start
                            old_far = space.clip_end
                            
                            # Set viewport clip planes as requested
                            space.clip_start = 0.1  # 0.1 meters
                            space.clip_end = 10000  # 10000 meters
                            
                            print(f"🖥️  Viewport clip planes: {old_near} - {old_far} → {space.clip_start} - {space.clip_end}")
                            viewports_adjusted += 1
        
        if viewports_adjusted == 0:
            print("⚠️  No 3D viewports found to adjust")
        else:
            print(f"✅ Adjusted clip planes for {viewports_adjusted} 3D viewport(s)")
    
    def frame_imported_terrain(self, terrain_obj):
        """Frame the imported terrain in the 3D viewport"""
        
        try:
            # Ensure the terrain object is selected and active
            bpy.ops.object.select_all(action='DESELECT')
            terrain_obj.select_set(True)
            bpy.context.view_layer.objects.active = terrain_obj
            
            # Frame the selected terrain object in all 3D viewports
            # Use override context to ensure it works across all viewports
            for screen in bpy.data.screens:
                for area in screen.areas:
                    if area.type == 'VIEW_3D':
                        for region in area.regions:
                            if region.type == 'WINDOW':
                                # Override context for this specific viewport
                                override_context = {
                                    'screen': screen,
                                    'area': area,
                                    'region': region,
                                    'scene': bpy.context.scene,
                                    'view_layer': bpy.context.view_layer,
                                    'active_object': terrain_obj,
                                    'selected_objects': [terrain_obj]
                                }
                                
                                # Frame the selected object in this viewport
                                with bpy.context.temp_override(**override_context):
                                    bpy.ops.view3d.view_selected()
                                
                                print(f"🎯 Framed terrain in viewport")
                                break
            
            print(f"✅ Framed terrain '{terrain_obj.name}' in view")
            
        except Exception as e:
            print(f"⚠️  Could not frame terrain in view: {e}")
    
    def import_prefab_objects(self, directory):
        """Import prefab objects from .prefab files"""
        self.report({'INFO'}, "Importing prefab objects... (placeholder)")
        # TODO: Implement prefab import in Phase 3
        pass
    
    def import_material_data(self, directory):
        """Import material and texture data"""
        self.report({'INFO'}, "Importing materials... (placeholder)")
        # TODO: Implement material import in Phase 4
        pass
    
    def import_lighting_data(self, directory):
        """Import lighting and environment data"""
        self.report({'INFO'}, "Importing lighting... (placeholder)")
        # TODO: Implement lighting import in Phase 5
        pass
    
    def import_decal_roads_data(self, directory):
        """Import DecalRoad objects from level data"""
        try:
            self.report({'INFO'}, "Importing DecalRoad objects...")
            
            # Parse DecalRoad data
            parser = DecalRoadParser(directory)
            parser.parse_level()
            
            roads_data = parser.get_roads_data()
            if not roads_data:
                self.report({'INFO'}, "No DecalRoad objects found in level")
                return
            
            # Create or get DecalRoads collection
            roads_collection = self.get_or_create_collection("DecalRoads")
            
            # Get existing road persistent IDs to avoid duplicates
            existing_road_ids = set()
            for obj in bpy.data.objects:
                if obj.get('beamng_type') == 'DecalRoad':
                    existing_id = obj.get('beamng_persistent_id')
                    if existing_id:
                        existing_road_ids.add(existing_id)
            
            print(f"🔍 Found {len(existing_road_ids)} existing DecalRoad objects")
            
            # Create materials if materials import is enabled
            if self.import_materials:
                self.create_decal_road_materials(parser, directory)
            
            # Create geometry node group
            self.ensure_decal_road_node_group()
            
            # Import each road
            imported_count = 0
            skipped_count = 0
            for road_data in roads_data:
                try:
                    # Skip if road already exists
                    if road_data.persistent_id in existing_road_ids:
                        print(f"⏭️  Skipping duplicate road: {road_data.persistent_id[:8]}")
                        skipped_count += 1
                        continue
                    
                    road_obj = self.create_decal_road_object(road_data, parser, directory)
                    if road_obj:
                        roads_collection.objects.link(road_obj)
                        imported_count += 1
                        
                except Exception as e:
                    print(f"❌ Failed to import road {road_data.persistent_id}: {e}")
                    continue
            
            # Report results
            stats = parser.get_stats()
            message = f"Imported {imported_count} DecalRoad objects ({stats['unique_materials_used']} unique materials)"
            if skipped_count > 0:
                message += f", skipped {skipped_count} duplicates"
            self.report({'INFO'}, message)
            
        except Exception as e:
            self.report({'WARNING'}, f"DecalRoad import failed: {str(e)}")
            print(f"❌ DecalRoad import error: {e}")
    
    def get_or_create_collection(self, name: str) -> bpy.types.Collection:
        """Get or create a collection"""
        if name in bpy.data.collections:
            return bpy.data.collections[name]
        
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        return collection
    
    def create_decal_road_materials(self, parser: DecalRoadParser, level_path: str):
        """Create materials for all roads"""
        unique_materials = parser.get_unique_materials()
        
        print(f"🎨 Creating {len(unique_materials)} DecalRoad materials...")
        
        for material_name in unique_materials:
            material_data = parser.get_material(material_name)
            
            # Create material with BeamNG data
            mat = create_beamng_decal_road_material(
                material_name, 
                material_data.__dict__ if material_data else None,
                Path(level_path)
            )
            
            print(f"  ✅ Created material: {material_name}")
    
    def ensure_decal_road_node_group(self):
        """Ensure the DecalRoad geometry node group exists"""
        if "BeamNG_DecalRoad" not in bpy.data.node_groups:
            decal_road_node_group()
            print("✅ Created BeamNG_DecalRoad geometry node group")
    
    def create_decal_road_object(self, road_data: DecalRoadData, parser: DecalRoadParser, level_path: str) -> bpy.types.Object:
        """Create a Blender curve object from DecalRoad data"""
        
        # Create curve with unique name
        curve_name = f"DecalRoad_{road_data.persistent_id[:8]}"
        
        # Ensure unique curve data name
        curve_data_name = curve_name
        counter = 1
        while curve_data_name in bpy.data.curves:
            curve_data_name = f"{curve_name}.{counter:03d}"
            counter += 1
            
        curve_data = bpy.data.curves.new(curve_data_name, type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = 12
        
        # Create spline
        spline = curve_data.splines.new('POLY')
        spline.points.add(len(road_data.nodes) - 1)
        
        # Set control points
        for i, node in enumerate(road_data.nodes):
            x, y, z, width = node
            spline.points[i].co = (x, y, z, 1.0)
            spline.points[i].radius = width
        
        # Create object with unique name
        object_name = curve_name
        counter = 1
        while object_name in bpy.data.objects:
            object_name = f"{curve_name}.{counter:03d}"
            counter += 1
            
        curve_obj = bpy.data.objects.new(object_name, curve_data)
        
        # Set custom properties
        curve_obj["beamng_type"] = "DecalRoad"
        curve_obj["beamng_material"] = road_data.material
        curve_obj["beamng_persistent_id"] = road_data.persistent_id
        curve_obj["beamng_texture_length"] = road_data.texture_length
        curve_obj["beamng_break_angle"] = road_data.break_angle
        curve_obj["beamng_improved_spline"] = road_data.improved_spline
        curve_obj["beamng_render_priority"] = road_data.render_priority
        curve_obj["beamng_start_end_fade"] = road_data.start_end_fade
        curve_obj["beamng_distance_fade"] = road_data.distance_fade
        
        # Apply material if available and requested
        if self.import_materials and road_data.material in bpy.data.materials:
            material = bpy.data.materials[road_data.material]
            curve_data.materials.append(material)
        
        # Apply geometry nodes
        if "BeamNG_DecalRoad" in bpy.data.node_groups:
            modifier = curve_obj.modifiers.new(name="DecalRoad_GeometryNodes", type='NODES')
            modifier.node_group = bpy.data.node_groups["BeamNG_DecalRoad"]
            
            # Set geometry node modifier inputs using socket indices
            # Based on the node group interface: Socket 5 = Material, Socket 6 = Texture Length
            try:
                # Set texture length parameter (Socket 6)
                modifier["Socket_6"] = road_data.texture_length
            except Exception as e:
                print(f"⚠️  Could not set texture length for {curve_obj.name}: {e}")
            
            # Set material if available (Socket 5)
            if self.import_materials and road_data.material in bpy.data.materials:
                try:
                    modifier["Socket_5"] = bpy.data.materials[road_data.material]
                except Exception as e:
                    print(f"⚠️  Could not set material {road_data.material} for {curve_obj.name}: {e}")
        
        return curve_obj

def register():
    bpy.utils.register_class(ImportBeamNGLevel)
    
    # Add to File > Import menu
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportBeamNGLevel)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)

def menu_func_import(self, context):
    """Add import option to File > Import menu"""
    self.layout.operator(ImportBeamNGLevel.bl_idname, text="BeamNG Level (.ter, .prefab)") 
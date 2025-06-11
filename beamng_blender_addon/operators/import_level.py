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
from ..utils.beamng_terrain_node_group import beamng_terrain_node_group

class BeamNGTerrainParser:
    """Integrated BeamNG terrain parser for the addon - SOURCE OF TRUTH from ter_parser.py"""
    
    def __init__(self, ter_file: str, json_file: str):
        self.ter_file = Path(ter_file)
        self.json_file = Path(json_file)
        
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
        
        print("🏞️  BeamNG Terrain Parser")
        print(f"📁 Terrain: {self.ter_file.name}")
        print(f"📊 Dimensions: {self.size}x{self.size}")
        print(f"🎭 Materials: {len(self.materials)}")
        print("✅ Using offset 5 (after header), all data: little-endian")
    
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
                'config': self.config
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
    
    # Terrain displacement options
    terrain_scale: bpy.props.FloatProperty(
        name="Terrain Scale",
        description="Scale factor for terrain size",
        default=1.0,
        min=0.1,
        max=10.0,
    )
    
    displacement_strength: bpy.props.FloatProperty(
        name="Displacement Strength",
        description="Strength of displacement effect",
        default=200.0,
        min=1.0,
        max=1000.0,
    )
    
    subdivision_levels: bpy.props.IntProperty(
        name="Subdivision Levels",
        description="Number of subdivision levels for terrain detail",
        default=6,
        min=2,
        max=10,
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
                displacement_texture, layermap_texture, terrain_data['config']
            )
            
            # Adjust camera clip planes for large terrain
            self.adjust_camera_clip_planes()
            
            self.report({'INFO'}, f"Terrain imported successfully: {terrain_obj.name}")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Terrain import failed: {str(e)}")
            return {'CANCELLED'}
    
    def create_displacement_texture(self, heightmap):
        """Create a 16-bit EXR texture for displacement mapping"""
        
        # Normalize heightmap to 0-1 range for displacement
        heightmap_normalized = heightmap.astype(np.float32) / 65535.0
        
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
        
        # Save as EXR file
        displacement_image.file_format = 'OPEN_EXR'
        
        print(f"✅ Created displacement texture: {image_name} ({width}x{height})")
        return displacement_image
    
    def create_layermap_texture(self, layermap, materials):
        """Create a texture for the layermap (material indices)"""
        
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
            float_buffer=False  # Use 8-bit for material indices
        )
        
        # Normalize layermap to 0-1 range for material IDs
        # Convert material indices to normalized values (0-1)
        max_material_id = len(materials) - 1 if materials else 255
        layermap_normalized = layermap.astype(np.float32) / max_material_id
        
        # Convert layermap to RGBA format for Blender (R=material_id, G=material_id, B=material_id, A=1)
        rgba_data = np.zeros((height, width, 4), dtype=np.float32)
        rgba_data[:, :, 0] = layermap_normalized  # Red channel
        rgba_data[:, :, 1] = layermap_normalized  # Green channel  
        rgba_data[:, :, 2] = layermap_normalized  # Blue channel
        rgba_data[:, :, 3] = 1.0  # Alpha channel
        
        # Flatten for Blender (Blender expects flattened RGBA array)
        layermap_image.pixels = rgba_data.flatten()
        
        # Update image
        layermap_image.update()
        
        # Set colorspace to Non-Color for data textures
        layermap_image.colorspace_settings.name = 'Non-Color'
        
        print(f"✅ Created layermap texture: {image_name} ({width}x{height})")
        print(f"   Materials: {len(materials)} ({max_material_id} max ID)")
        
        return layermap_image
    
    def create_terrain_with_node_group(self, displacement_texture, layermap_texture, config):
        """Create terrain mesh using BeamNG geometry node group"""
        
        # Get terrain dimensions and settings
        terrain_size = config['size']
        world_scale = getattr(bpy.context.scene, 'beamng_terrain_scale', self.terrain_scale)
        displacement_strength = getattr(bpy.context.scene, 'beamng_displacement_strength', self.displacement_strength)
        
        # Create base plane mesh
        bpy.ops.mesh.primitive_plane_add(size=1.0)  # Unit size, will be scaled by node group
        terrain_obj = bpy.context.active_object
        terrain_obj.name = "BeamNG_Terrain"
        
        # Create or get the BeamNG terrain node group
        node_group = beamng_terrain_node_group(displacement_texture, layermap_texture)
        
        # Add geometry nodes modifier
        geo_nodes_mod = terrain_obj.modifiers.new(name="BeamNG_Terrain", type='NODES')
        geo_nodes_mod.node_group = node_group
        
        # Set node group parameters
        # Size (terrain dimensions in world units)
        geo_nodes_mod["Input_2"] = terrain_size * world_scale
        
        # Resolution (number of vertices per axis, calculated from heightmap)
        heightmap_resolution = config.get('heightMapSize', 1024)
        # Calculate resolution as square root since heightMapSize is total pixels
        vertex_resolution = int(np.sqrt(heightmap_resolution))
        geo_nodes_mod["Input_3"] = vertex_resolution
        
        # Height (displacement strength)
        geo_nodes_mod["Input_4"] = displacement_strength
        
        print(f"✅ Created terrain mesh with BeamNG node group: {terrain_obj.name}")
        print(f"   Size: {terrain_size * world_scale} units")
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
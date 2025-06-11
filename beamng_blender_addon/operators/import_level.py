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

class BeamNGTerrainParser:
    """Integrated BeamNG terrain parser for the addon"""
    
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
        
        print(f"🏞️  BeamNG Terrain Parser")
        print(f"📁 Terrain: {self.ter_file.name}")
        print(f"📊 Dimensions: {self.size}x{self.size}")
    
    def parse_terrain(self):
        """Parse the terrain file using corrected offset and encoding"""
        
        with open(self.ter_file, 'rb') as f:
            # Read header (little-endian)
            version = struct.unpack('B', f.read(1))[0]
            size = struct.unpack('<I', f.read(4))[0]
            
            # Verify header
            if version != self.version or size != self.size:
                raise ValueError(f"Header mismatch: got version={version}, size={size}")
            
            # CORRECTED: Data starts at offset 2048, big-endian
            data_start = 2048
            print(f"📍 Using corrected data offset: {data_start}")
            
            # Read heightmap with big-endian encoding
            f.seek(data_start)
            heightmap_bytes = self.heightmap_size * self.heightmap_item_size
            heightmap_data = f.read(heightmap_bytes)
            
            if len(heightmap_data) != heightmap_bytes:
                print(f"⚠️  Warning: Expected {heightmap_bytes} bytes, got {len(heightmap_data)}")
            
            # Parse as 16-bit BIG-ENDIAN
            num_heights = len(heightmap_data) // 2
            heights = struct.unpack(f'>{num_heights}H', heightmap_data)  # >H = big-endian
            
            # Reshape to 2D
            heightmap = np.array(heights, dtype=np.uint16).reshape((self.size, self.size))
            
            return {
                'header': {
                    'version': version,
                    'size': size,
                    'data_start': data_start,
                },
                'heightmap': heightmap,
                'config': self.config
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
            
            # Create EXR displacement texture
            self.report({'INFO'}, "Creating 16-bit EXR displacement texture...")
            displacement_texture = self.create_displacement_texture(heightmap)
            
            # Create terrain mesh with displacement
            self.report({'INFO'}, "Creating terrain mesh with displacement...")
            terrain_obj = self.create_terrain_with_displacement(
                heightmap, displacement_texture, terrain_data['config']
            )
            
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
    
    def create_terrain_with_displacement(self, heightmap, displacement_texture, config):
        """Create terrain mesh using displacement modifier"""
        
        # Get terrain dimensions and settings from scene properties
        terrain_size = config['size']
        world_scale = bpy.context.scene.beamng_terrain_scale if hasattr(bpy.context.scene, 'beamng_terrain_scale') else self.terrain_scale
        displacement_strength = bpy.context.scene.beamng_displacement_strength if hasattr(bpy.context.scene, 'beamng_displacement_strength') else self.displacement_strength
        subdivision_levels = bpy.context.scene.beamng_subdivision_levels if hasattr(bpy.context.scene, 'beamng_subdivision_levels') else self.subdivision_levels
        
        # Create base plane mesh
        bpy.ops.mesh.primitive_plane_add(size=terrain_size * world_scale)
        terrain_obj = bpy.context.active_object
        terrain_obj.name = "BeamNG_Terrain"
        
        # Add subdivision surface modifier for detail
        subdiv_mod = terrain_obj.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv_mod.levels = subdivision_levels
        subdiv_mod.render_levels = subdivision_levels
        
        # Create material with displacement
        material = bpy.data.materials.new(name="BeamNG_Terrain_Material")
        material.use_nodes = True
        nodes = material.node_tree.nodes
        links = material.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        # Add material output
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (300, 0)
        
        # Add principled BSDF
        bsdf_node = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf_node.location = (0, 0)
        
        # Add texture coordinate node
        tex_coord_node = nodes.new(type='ShaderNodeTexCoord')
        tex_coord_node.location = (-600, 0)
        
        # Add image texture node for displacement
        image_node = nodes.new(type='ShaderNodeTexImage')
        image_node.location = (-300, -200)
        image_node.image = displacement_texture
        
        # Add displacement node
        displacement_node = nodes.new(type='ShaderNodeDisplacement')
        displacement_node.location = (0, -200)
        displacement_node.inputs['Scale'].default_value = displacement_strength
        
        # Connect nodes
        links.new(tex_coord_node.outputs['Generated'], image_node.inputs['Vector'])
        links.new(image_node.outputs['Color'], displacement_node.inputs['Height'])
        links.new(bsdf_node.outputs['BSDF'], output_node.inputs['Surface'])
        links.new(displacement_node.outputs['Displacement'], output_node.inputs['Displacement'])
        
        # Set material color to terrain-like green
        bsdf_node.inputs['Base Color'].default_value = (0.2, 0.6, 0.1, 1.0)  # Green
        bsdf_node.inputs['Roughness'].default_value = 0.8
        
        # Assign material to object
        terrain_obj.data.materials.append(material)
        
        # Set subdivision surface to smooth
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.faces_shade_smooth()
        bpy.ops.object.mode_set(mode='OBJECT')
        
        print(f"✅ Created terrain mesh with displacement: {terrain_obj.name}")
        print(f"   Size: {terrain_size * world_scale} units")
        print(f"   Subdivision levels: {subdivision_levels}")
        print(f"   Displacement strength: {displacement_strength}")
        
        return terrain_obj
    
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
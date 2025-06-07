"""
Properties module for BeamNG Blender addon
Manages addon-specific properties and settings
"""

import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty

def register_properties():
    """Register addon properties to scene"""
    
    # Level information properties
    bpy.types.Scene.beamng_level_name = StringProperty(
        name="Level Name",
        description="Name of the BeamNG level",
        default="custom_level",
    )
    
    bpy.types.Scene.beamng_level_path = StringProperty(
        name="Level Path",
        description="Path to the BeamNG level directory",
        subtype='DIR_PATH',
        default="",
    )
    
    # Import/Export settings
    bpy.types.Scene.beamng_import_terrain = BoolProperty(
        name="Import Terrain",
        description="Import terrain data when importing a level",
        default=True,
    )
    
    bpy.types.Scene.beamng_import_objects = BoolProperty(
        name="Import Objects",
        description="Import prefab objects when importing a level",
        default=True,
    )
    
    bpy.types.Scene.beamng_import_materials = BoolProperty(
        name="Import Materials",
        description="Import materials and textures when importing a level",
        default=True,
    )
    
    # Terrain settings
    bpy.types.Scene.beamng_terrain_scale = FloatProperty(
        name="Terrain Scale",
        description="Scale factor for imported terrain",
        default=1.0,
        min=0.1,
        max=10.0,
    )
    
    bpy.types.Scene.beamng_terrain_subdivision = IntProperty(
        name="Terrain Subdivision",
        description="Subdivision level for terrain mesh",
        default=1,
        min=0,
        max=5,
    )
    
    print("BeamNG Properties: Registered")

def unregister_properties():
    """Unregister addon properties from scene"""
    
    # Remove all custom properties
    properties_to_remove = [
        'beamng_level_name',
        'beamng_level_path',
        'beamng_import_terrain',
        'beamng_import_objects',
        'beamng_import_materials',
        'beamng_terrain_scale',
        'beamng_terrain_subdivision',
    ]
    
    for prop in properties_to_remove:
        if hasattr(bpy.types.Scene, prop):
            delattr(bpy.types.Scene, prop)
    
    print("BeamNG Properties: Unregistered") 
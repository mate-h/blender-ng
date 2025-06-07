"""
BeamNG.drive Level Data Importer/Exporter for Blender

This addon allows importing and exporting BeamNG.drive level data
including terrain, prefabs, materials, and configurations.
"""

bl_info = {
    "name": "BeamNG.drive Level Importer/Exporter",
    "author": "BeamNG Blender Tools",
    "version": (0, 1, 0),
    "blender": (4, 0, 0),
    "location": "File > Import/Export",
    "description": "Import and export BeamNG.drive level data",
    "category": "Import-Export",
    "support": "COMMUNITY",
    "doc_url": "https://github.com/your-repo/beamng-blender-addon",
    "tracker_url": "https://github.com/your-repo/beamng-blender-addon/issues",
}

import bpy
from bpy.utils import register_class, unregister_class

# Import addon modules
from . import operators
from . import ui
from . import utils

# List of classes to register
classes = []

def register():
    """Register all addon classes and handlers"""
    # Register operators
    operators.register()
    
    # Register UI panels
    ui.register()
    
    # Register any scene properties
    from .utils.properties import register_properties
    register_properties()
    
    print("BeamNG Blender Addon: Registered successfully")

def unregister():
    """Unregister all addon classes and handlers"""
    # Unregister in reverse order
    from .utils.properties import unregister_properties
    unregister_properties()
    
    ui.unregister()
    operators.unregister()
    
    print("BeamNG Blender Addon: Unregistered successfully")

if __name__ == "__main__":
    register() 
"""
UI module for BeamNG Blender addon
Contains all user interface panels and elements
"""

from .main_panel import BeamNGMainPanel, BeamNGTerrainPanel
from . import main_panel

# List of UI classes
classes = [
    BeamNGMainPanel,
    BeamNGTerrainPanel,
]

def register():
    """Register all UI classes"""
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    # Register terrain panel properties
    main_panel.register()
    
    print("BeamNG UI: Registered")

def unregister():
    """Unregister all UI classes"""
    from bpy.utils import unregister_class
    
    # Unregister terrain panel properties
    main_panel.unregister()
    
    for cls in reversed(classes):
        unregister_class(cls)
    print("BeamNG UI: Unregistered") 
"""
UI module for BeamNG Blender addon
Contains all user interface panels and elements
"""

from .main_panel import BeamNGMainPanel

# List of UI classes
classes = [
    BeamNGMainPanel,
]

def register():
    """Register all UI classes"""
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    print("BeamNG UI: Registered")

def unregister():
    """Unregister all UI classes"""
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    print("BeamNG UI: Unregistered") 
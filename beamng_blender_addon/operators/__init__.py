"""
Operators module for BeamNG Blender addon
Contains all import/export operations
"""

from .import_level import ImportBeamNGLevel
from .export_level import ExportBeamNGLevel

# List of operator classes
classes = [
    ImportBeamNGLevel,
    ExportBeamNGLevel,
]

def register():
    """Register all operators"""
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    print("BeamNG Operators: Registered")

def unregister():
    """Unregister all operators"""
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    print("BeamNG Operators: Unregistered") 
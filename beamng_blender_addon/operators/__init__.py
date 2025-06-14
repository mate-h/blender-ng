"""
Operators module for BeamNG Blender addon
Contains all import/export operations
"""

from .import_level import ImportBeamNGLevel
from .export_level import ExportBeamNGLevel
from .import_decal_roads import ImportBeamNGDecalRoads

# List of operator classes - DecalRoad import is now integrated into main level import
classes = [
    ImportBeamNGLevel,
    ExportBeamNGLevel,
    # ImportBeamNGDecalRoads,  # Keep available but not registered - integrated into main import
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
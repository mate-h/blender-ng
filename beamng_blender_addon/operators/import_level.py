"""
BeamNG Level Import Operator
Handles importing BeamNG.drive level data into Blender
"""

import bpy
from bpy.props import StringProperty, BoolProperty, CollectionProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
import os

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
                self.import_terrain_data(directory)
            
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
        """Import terrain data from .ter files"""
        self.report({'INFO'}, "Importing terrain data... (placeholder)")
        # TODO: Implement terrain import in Phase 2
        pass
    
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
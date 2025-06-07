"""
BeamNG Level Export Operator
Handles exporting Blender scene data to BeamNG.drive level format
"""

import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
import os

class ExportBeamNGLevel(Operator, ExportHelper):
    """Export BeamNG.drive Level Data"""
    
    bl_idname = "export_scene.beamng_level"
    bl_label = "Export BeamNG Level"
    bl_description = "Export Blender scene to BeamNG.drive level format"
    bl_options = {'REGISTER', 'UNDO'}
    
    # File browser properties
    filename_ext = ""
    filter_glob: StringProperty(
        default="*",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    # Export options
    export_terrain: BoolProperty(
        name="Export Terrain",
        description="Export terrain mesh as .ter file",
        default=True,
    )
    
    export_objects: BoolProperty(
        name="Export Objects",
        description="Export objects as .prefab files",
        default=True,
    )
    
    export_materials: BoolProperty(
        name="Export Materials",
        description="Export materials and textures",
        default=True,
    )
    
    export_config: BoolProperty(
        name="Export Config",
        description="Generate level configuration files",
        default=True,
    )
    
    level_name: StringProperty(
        name="Level Name",
        description="Name for the exported level",
        default="custom_level",
    )
    
    def execute(self, context):
        """Execute the export operation"""
        try:
            # Get export directory
            export_path = os.path.dirname(self.filepath)
            level_directory = os.path.join(export_path, self.level_name)
            
            # Create level directory structure
            self.create_level_directory(level_directory)
            
            self.report({'INFO'}, f"Starting BeamNG level export to: {level_directory}")
            
            # Export terrain if enabled
            if self.export_terrain:
                self.export_terrain_data(level_directory)
            
            # Export objects if enabled
            if self.export_objects:
                self.export_prefab_objects(level_directory)
            
            # Export materials if enabled
            if self.export_materials:
                self.export_material_data(level_directory)
            
            # Export config files if enabled
            if self.export_config:
                self.export_config_data(level_directory)
            
            self.report({'INFO'}, "BeamNG level export completed successfully")
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
    
    def create_level_directory(self, level_path):
        """Create BeamNG level directory structure"""
        directories = [
            level_path,
            os.path.join(level_path, "art"),
            os.path.join(level_path, "art", "shapes"),
            os.path.join(level_path, "art", "terrains"),
            os.path.join(level_path, "art", "skies"),
            os.path.join(level_path, "art", "cubemaps"),
            os.path.join(level_path, "art", "decals"),
            os.path.join(level_path, "main"),
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        self.report({'INFO'}, f"Created level directory structure at: {level_path}")
    
    def export_terrain_data(self, level_path):
        """Export terrain data to .ter files"""
        self.report({'INFO'}, "Exporting terrain data... (placeholder)")
        # TODO: Implement terrain export in Phase 6
        pass
    
    def export_prefab_objects(self, level_path):
        """Export objects to .prefab files"""
        self.report({'INFO'}, "Exporting prefab objects... (placeholder)")
        # TODO: Implement prefab export in Phase 6
        pass
    
    def export_material_data(self, level_path):
        """Export materials and textures"""
        self.report({'INFO'}, "Exporting materials... (placeholder)")
        # TODO: Implement material export in Phase 6
        pass
    
    def export_config_data(self, level_path):
        """Export level configuration files"""
        self.report({'INFO'}, "Exporting configuration... (placeholder)")
        # TODO: Implement config export in Phase 6
        
        # Create basic info.json placeholder
        import json
        info_data = {
            "title": f"levels.{self.level_name}.info.title",
            "description": f"levels.{self.level_name}.info.description",
            "size": [1024, 1024],
            "country": "levels.common.country.usa",
            "defaultSpawnPointName": "spawn_main"
        }
        
        info_path = os.path.join(level_path, "info.json")
        with open(info_path, 'w') as f:
            json.dump(info_data, f, indent=2)
        
        self.report({'INFO'}, f"Created basic info.json at: {info_path}")

def register():
    bpy.utils.register_class(ExportBeamNGLevel)
    
    # Add to File > Export menu
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportBeamNGLevel)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

def menu_func_export(self, context):
    """Add export option to File > Export menu"""
    self.layout.operator(ExportBeamNGLevel.bl_idname, text="BeamNG Level") 
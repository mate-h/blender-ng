"""
Main UI Panel for BeamNG Blender addon
Provides quick access to import/export functionality
"""

import bpy
from bpy.types import Panel

class BeamNGMainPanel(Panel):
    """Main panel for BeamNG level tools"""
    
    bl_label = "BeamNG Level Tools"
    bl_idname = "VIEW3D_PT_beamng_main"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BeamNG'
    bl_context = "objectmode"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Header
        row = layout.row()
        row.label(text="BeamNG.drive Level Tools", icon='WORLD')
        
        layout.separator()
        
        # Import section
        box = layout.box()
        row = box.row()
        row.label(text="Import", icon='IMPORT')
        
        row = box.row()
        row.operator("import_scene.beamng_level", text="Import Level", icon='FILEBROWSER')
        
        # Quick info about import
        row = box.row()
        row.label(text="Supports: .ter terrain files", icon='INFO')
        
        layout.separator()
        
        # Export section
        box = layout.box()
        row = box.row()
        row.label(text="Export", icon='EXPORT')
        
        row = box.row()
        row.operator("export_scene.beamng_level", text="Export Level", icon='FILEBROWSER')
        
        # Quick info about export
        row = box.row()
        row.label(text="Exports to BeamNG level format", icon='INFO')
        
        layout.separator()
        
        col = box.column(align=True)
        col.label(text="Version: 0.2.5")

def register():
    pass

def unregister():
    pass
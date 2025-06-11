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
        row.label(text="Supports: .ter terrain + EXR displacement", icon='INFO')
        
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
        
        # Tools section (for future development)
        box = layout.box()
        row = box.row()
        row.label(text="Tools", icon='TOOL_SETTINGS')
        
        row = box.row()
        row.label(text="Coming in future updates:", icon='TIME')
        
        col = box.column(align=True)
        col.label(text="• Terrain editing tools")
        col.label(text="• Material converter")
        col.label(text="• Prefab builder")
        col.label(text="• Level validator")
        
        layout.separator()
        
        # Development info
        box = layout.box()
        row = box.row()
        row.label(text="Development Status", icon='EXPERIMENTAL')
        
        col = box.column(align=True)
        col.label(text="Version: 0.2.0 (Alpha)")
        col.label(text="✅ Phase 1: Foundation Complete")
        col.label(text="🔄 Phase 2: Terrain Import (EXR)")

class BeamNGTerrainPanel(Panel):
    """Panel for terrain-specific import settings"""
    
    bl_label = "Terrain Import Settings"
    bl_idname = "VIEW3D_PT_beamng_terrain"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BeamNG'
    bl_context = "objectmode"
    bl_parent_id = "VIEW3D_PT_beamng_main"
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Add properties to scene if they don't exist
        if not hasattr(scene, 'beamng_terrain_scale'):
            scene.beamng_terrain_scale = 1.0
        if not hasattr(scene, 'beamng_displacement_strength'):
            scene.beamng_displacement_strength = 200.0
        if not hasattr(scene, 'beamng_subdivision_levels'):
            scene.beamng_subdivision_levels = 6
        
        # Terrain displacement settings
        box = layout.box()
        row = box.row()
        row.label(text="EXR Displacement Settings", icon='TEXTURE')
        
        col = box.column(align=True)
        col.prop(scene, "beamng_terrain_scale", text="Terrain Scale")
        col.prop(scene, "beamng_displacement_strength", text="Displacement Strength")
        col.prop(scene, "beamng_subdivision_levels", text="Subdivision Levels")
        
        layout.separator()
        
        # Info about EXR approach
        box = layout.box()
        row = box.row()
        row.label(text="About EXR Displacement", icon='INFO')
        
        col = box.column(align=True)
        col.label(text="• 16-bit precision heightmaps")
        col.label(text="• Real-time viewport preview")
        col.label(text="• Non-destructive workflow")
        col.label(text="• High subdivision for detail")

def register():
    # Add scene properties for terrain settings
    bpy.types.Scene.beamng_terrain_scale = bpy.props.FloatProperty(
        name="Terrain Scale",
        description="Scale factor for terrain size",
        default=1.0,
        min=0.1,
        max=10.0,
    )
    
    bpy.types.Scene.beamng_displacement_strength = bpy.props.FloatProperty(
        name="Displacement Strength", 
        description="Strength of displacement effect",
        default=200.0,
        min=1.0,
        max=1000.0,
    )
    
    bpy.types.Scene.beamng_subdivision_levels = bpy.props.IntProperty(
        name="Subdivision Levels",
        description="Number of subdivision levels for terrain detail",
        default=6,
        min=2,
        max=10,
    )

def unregister():
    # Remove scene properties
    del bpy.types.Scene.beamng_terrain_scale
    del bpy.types.Scene.beamng_displacement_strength 
    del bpy.types.Scene.beamng_subdivision_levels 
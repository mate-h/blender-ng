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
        row.operator("import_scene.beamng_level", text="Import BeamNG Level", icon='FILEBROWSER')
        
        # Quick info about imports
        col = box.column(align=True)
        col.label(text="Imports: Terrain + DecalRoads + Materials", icon='INFO')
        col.label(text="Supports: .ter, .json level data", icon='INFO')
        
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
        
        # Level content section
        box = layout.box()
        row = box.row()
        row.label(text="Level Content", icon='OUTLINER')
        
        # Check if there are any DecalRoad objects in scene
        decal_roads = [obj for obj in bpy.data.objects if obj.get('beamng_type') == 'DecalRoad']
        terrain_objects = [obj for obj in bpy.data.objects if obj.name.startswith('BeamNG_Terrain')]
        
        col = box.column(align=True)
        
        if terrain_objects:
            col.label(text=f"Terrain objects: {len(terrain_objects)}", icon='MESH_PLANE')
        
        if decal_roads:
            col.label(text=f"DecalRoads: {len(decal_roads)}", icon='CURVE_BEZCURVE')
            
            # Show material info for first road
            if len(decal_roads) > 0:
                road = decal_roads[0]
                material_name = road.get('beamng_material', 'No material')
                col.label(text=f"Road material: {material_name[:20]}...")
                
        if not terrain_objects and not decal_roads:
            col.label(text="No BeamNG objects in scene")
        
        layout.separator()
        
        col = layout.column(align=True)
        col.label(text="Version: 0.3.0")

def register():
    pass

def unregister():
    pass
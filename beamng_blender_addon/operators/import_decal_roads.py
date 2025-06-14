"""
BeamNG DecalRoad Import Operator
Handles importing DecalRoad objects from BeamNG level data into Blender
"""

import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add the addon directory to Python path for imports
addon_dir = Path(__file__).parent.parent
if str(addon_dir) not in sys.path:
    sys.path.append(str(addon_dir))

# Import BeamNG utilities
from ..parsers.decal_road_parser import DecalRoadParser, DecalRoadData, MaterialData
from ..utils.decal_road_material import create_beamng_decal_road_material
from ..utils.decal_road import decal_road_node_group


class ImportBeamNGDecalRoads(Operator, ImportHelper):
    """Import BeamNG DecalRoad objects with materials and geometry nodes"""
    
    bl_idname = "import_scene.beamng_decal_roads"
    bl_label = "Import BeamNG DecalRoads"
    bl_description = "Import BeamNG DecalRoad objects with automatic material and geometry node creation"
    bl_options = {'REGISTER', 'UNDO'}
    
    # File browser properties
    filename_ext = ""
    filter_glob: StringProperty(
        default="*.json;*.ter;*.prefab",
        options={'HIDDEN'},
        maxlen=255,
    )
    
    # Import options
    import_materials: BoolProperty(
        name="Import Materials",
        description="Create and configure materials for roads",
        default=True,
    )
    
    create_geometry_nodes: BoolProperty(
        name="Create Geometry Nodes",
        description="Apply decal road geometry node groups to imported roads",
        default=True,
    )
    
    clear_existing: BoolProperty(
        name="Clear Existing Roads",
        description="Remove existing road objects before importing",
        default=False,
    )
    
    resample_resolution: BoolProperty(
        name="High Resolution Resampling",
        description="Use higher resolution for road curve resampling",
        default=False,
    )
    
    road_width_scale: BoolProperty(
        name="Scale Road Width",
        description="Scale road width from BeamNG values",
        default=True,
    )
    
    def execute(self, context):
        """Execute the import operation"""
        try:
            # Determine level path
            level_path = self.get_level_path()
            if not level_path:
                self.report({'ERROR'}, "Could not determine level path. Please select a BeamNG level directory.")
                return {'CANCELLED'}
            
            # Parse DecalRoad data
            parser = DecalRoadParser(str(level_path))
            parser.parse_level()
            
            if not parser.roads:
                self.report({'WARNING'}, f"No DecalRoad objects found in {level_path}")
                return {'CANCELLED'}
            
            # Clear existing roads if requested
            if self.clear_existing:
                self.clear_existing_roads()
            
            # Import roads
            imported_count = self.import_roads(parser, level_path)
            
            # Report results
            stats = parser.get_stats()
            self.report({'INFO'}, 
                       f"Successfully imported {imported_count} DecalRoad objects "
                       f"({stats['unique_materials_used']} unique materials)")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {str(e)}")
            return {'CANCELLED'}
    
    def get_level_path(self) -> Optional[Path]:
        """Determine the BeamNG level path from the selected file/directory"""
        filepath = Path(self.filepath)
        
        # If a file was selected, use its directory
        if filepath.is_file():
            current_dir = filepath.parent
        else:
            current_dir = filepath
        
        # Look for level indicators
        level_indicators = [
            "main.level.json",
            "terrain.ter",
            "info.json"
        ]
        
        # Check current directory and parent directories
        for i in range(5):  # Limit search depth
            for indicator in level_indicators:
                if (current_dir / indicator).exists():
                    return current_dir
            
            # Move up one level
            parent = current_dir.parent
            if parent == current_dir:  # Root reached
                break
            current_dir = parent
        
        return None
    
    def clear_existing_roads(self):
        """Remove existing road objects from the scene"""
        roads_to_remove = []
        
        for obj in bpy.data.objects:
            if (obj.type == 'CURVE' and 
                obj.get('beamng_type') == 'DecalRoad'):
                roads_to_remove.append(obj)
        
        # Remove objects
        for obj in roads_to_remove:
            bpy.data.objects.remove(obj, do_unlink=True)
        
        print(f"🗑️  Removed {len(roads_to_remove)} existing DecalRoad objects")
    
    def import_roads(self, parser: DecalRoadParser, level_path: Path) -> int:
        """Import all DecalRoad objects"""
        imported_count = 0
        
        # Create or get Roads collection
        roads_collection = self.get_or_create_collection("DecalRoads")
        
        # Create materials if requested
        if self.import_materials:
            self.create_materials(parser, level_path)
        
        # Create geometry node group if requested
        if self.create_geometry_nodes:
            self.ensure_decal_road_node_group()
        
        # Import each road
        for road_data in parser.roads:
            try:
                road_obj = self.create_road_object(road_data, parser, level_path)
                if road_obj:
                    roads_collection.objects.link(road_obj)
                    imported_count += 1
                    
            except Exception as e:
                print(f"❌ Failed to import road {road_data.persistent_id}: {e}")
                continue
        
        return imported_count
    
    def get_or_create_collection(self, name: str) -> bpy.types.Collection:
        """Get or create a collection"""
        if name in bpy.data.collections:
            return bpy.data.collections[name]
        
        collection = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(collection)
        return collection
    
    def create_materials(self, parser: DecalRoadParser, level_path: Path):
        """Create materials for all roads"""
        unique_materials = parser.get_unique_materials()
        
        print(f"🎨 Creating {len(unique_materials)} DecalRoad materials...")
        
        for material_name in unique_materials:
            material_data = parser.get_material(material_name)
            
            # Create material with BeamNG data
            mat = create_beamng_decal_road_material(
                material_name, 
                material_data.__dict__ if material_data else None,
                level_path
            )
            
            print(f"  ✅ Created material: {material_name}")
    
    def ensure_decal_road_node_group(self):
        """Ensure the DecalRoad geometry node group exists"""
        if "BeamNG_DecalRoad" not in bpy.data.node_groups:
            decal_road_node_group()
            print("✅ Created BeamNG_DecalRoad geometry node group")
    
    def create_road_object(self, road_data: DecalRoadData, parser: DecalRoadParser, level_path: Path) -> Optional[bpy.types.Object]:
        """Create a Blender curve object from DecalRoad data"""
        
        # Create curve
        curve_name = f"DecalRoad_{road_data.persistent_id[:8]}"
        curve_data = bpy.data.curves.new(curve_name, type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = 12 if not self.resample_resolution else 24
        
        # Create spline
        spline = curve_data.splines.new('POLY')
        spline.points.add(len(road_data.nodes) - 1)
        
        # Set control points
        for i, node in enumerate(road_data.nodes):
            x, y, z, width = node
            spline.points[i].co = (x, y, z, 1.0)
            
            # Apply width scaling if enabled
            if self.road_width_scale:
                spline.points[i].radius = width
            else:
                spline.points[i].radius = 1.0
        
        # Create object
        curve_obj = bpy.data.objects.new(curve_name, curve_data)
        
        # Set custom properties
        curve_obj["beamng_type"] = "DecalRoad"
        curve_obj["beamng_material"] = road_data.material
        curve_obj["beamng_persistent_id"] = road_data.persistent_id
        curve_obj["beamng_texture_length"] = road_data.texture_length
        curve_obj["beamng_break_angle"] = road_data.break_angle
        curve_obj["beamng_improved_spline"] = road_data.improved_spline
        curve_obj["beamng_render_priority"] = road_data.render_priority
        curve_obj["beamng_start_end_fade"] = road_data.start_end_fade
        curve_obj["beamng_distance_fade"] = road_data.distance_fade
        
        # Apply material if available and requested
        if self.import_materials and road_data.material in bpy.data.materials:
            material = bpy.data.materials[road_data.material]
            curve_data.materials.append(material)
        
        # Apply geometry nodes if requested
        if self.create_geometry_nodes and "BeamNG_DecalRoad" in bpy.data.node_groups:
            modifier = curve_obj.modifiers.new(name="DecalRoad_GeometryNodes", type='NODES')
            modifier.node_group = bpy.data.node_groups["BeamNG_DecalRoad"]
            
            # Set texture length parameter
            if "Texture Length" in modifier:
                modifier["Texture Length"] = road_data.texture_length
            
            # Set material if available
            if self.import_materials and road_data.material in bpy.data.materials:
                if "Material" in modifier:
                    modifier["Material"] = bpy.data.materials[road_data.material]
        
        return curve_obj
    
    def draw(self, context):
        """Draw the import options in the file browser"""
        layout = self.layout
        
        layout.prop(self, "import_materials")
        layout.prop(self, "create_geometry_nodes")
        layout.prop(self, "clear_existing")
        
        layout.separator()
        layout.label(text="Advanced Options:")
        layout.prop(self, "resample_resolution")
        layout.prop(self, "road_width_scale")


def register():
    """Register the operator"""
    bpy.utils.register_class(ImportBeamNGDecalRoads)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    """Unregister the operator"""
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(ImportBeamNGDecalRoads)


def menu_func_import(self, context):
    """Add the import operator to the File > Import menu"""
    self.layout.operator(ImportBeamNGDecalRoads.bl_idname, text="BeamNG DecalRoads (.json)")


if __name__ == "__main__":
    register()
    bpy.ops.import_scene.beamng_decal_roads('INVOKE_DEFAULT') 
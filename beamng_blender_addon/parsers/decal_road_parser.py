"""
BeamNG DecalRoad Parser
Handles parsing DecalRoad objects and their materials from BeamNG level data
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional


class DecalRoadData:
    """Container for DecalRoad data"""
    
    def __init__(self, road_dict: Dict[str, Any]):
        self.class_name = road_dict.get('class', '')
        self.persistent_id = road_dict.get('persistentId', '')
        self.parent = road_dict.get('__parent', '')
        self.position = road_dict.get('position', [0, 0, 0])
        self.nodes = road_dict.get('nodes', [])
        self.material = road_dict.get('material', '')
        self.texture_length = road_dict.get('textureLength', 20.0)
        self.break_angle = road_dict.get('breakAngle', 1.0)
        self.improved_spline = road_dict.get('improvedSpline', True)
        self.render_priority = road_dict.get('renderPriority', 9)
        self.start_end_fade = road_dict.get('startEndFade', [5, 5])
        self.distance_fade = road_dict.get('distanceFade', [300, 50])
        
        # Validate that we have minimum required data
        if not self.nodes or len(self.nodes) < 2:
            raise ValueError(f"DecalRoad {self.persistent_id} has insufficient nodes: {len(self.nodes)}")
        
        if not self.material:
            raise ValueError(f"DecalRoad {self.persistent_id} has no material assigned")


class MaterialData:
    """Container for BeamNG material data"""
    
    def __init__(self, mat_name: str, mat_dict: Dict[str, Any]):
        self.name = mat_name
        self.class_name = mat_dict.get('class', 'Material')
        self.persistent_id = mat_dict.get('persistentId', '')
        self.map_to = mat_dict.get('mapTo', 'unmapped_mat')
        self.stages = mat_dict.get('Stages', [])
        self.alpha_ref = mat_dict.get('alphaRef', 0)
        self.alpha_test = mat_dict.get('alphaTest', False)
        self.annotation = mat_dict.get('annotation', '')
        self.cast_shadows = mat_dict.get('castShadows', True)
        self.translucent = mat_dict.get('translucent', False)
        self.translucent_z_write = mat_dict.get('translucentZWrite', False)
        self.version = mat_dict.get('version', 1.5)
        
        # Material tags
        self.material_tags = {}
        for i in range(5):
            tag_key = f'materialTag{i}'
            if tag_key in mat_dict:
                self.material_tags[i] = mat_dict[tag_key]
    
    def get_primary_stage(self) -> Optional[Dict[str, Any]]:
        """Get the primary material stage (first non-null stage)"""
        if not self.stages:
            return None
        
        for stage in self.stages:
            if stage and any(v is not None for v in stage.values()):
                return stage
        
        return None


class DecalRoadParser:
    """Parser for BeamNG DecalRoad data"""
    
    def __init__(self, level_path: str):
        self.level_path = Path(level_path)
        self.roads: List[DecalRoadData] = []
        self.materials: Dict[str, MaterialData] = {}
        self._processed_files: set = set()  # Track processed files to avoid duplicates
        
        if not self.level_path.exists():
            raise FileNotFoundError(f"Level path does not exist: {level_path}")
    
    def parse_level(self) -> None:
        """Parse the entire level for DecalRoad data"""
        print(f"🛣️  Parsing DecalRoad data from: {self.level_path}")
        
        # Parse roads
        roads_parsed = self._parse_roads()
        
        # Deduplicate roads after parsing all files
        original_count = len(self.roads)
        self._deduplicate_roads()
        final_count = len(self.roads)
        
        if original_count != final_count:
            print(f"🔄 Deduplicated {original_count - final_count} duplicate roads")
        
        print(f"✅ Found {final_count} unique DecalRoad objects")
        
        # Parse materials
        materials_parsed = self._parse_materials()
        print(f"✅ Found {materials_parsed} materials")
        
        # Validate that all road materials exist
        self._validate_road_materials()
    
    def _parse_roads(self) -> int:
        """Parse DecalRoad objects from level files"""
        roads_count = 0
        
        # Look for road item files
        road_patterns = [
            "main/MissionGroup/roads/items.level.json",
            "main/MissionGroup/*/roads/items.level.json",
            "**/roads/items.level.json",
            "**/*roads*.json"
        ]
        
        for pattern in road_patterns:
            for road_file in self.level_path.glob(pattern):
                # Skip if we've already processed this file
                file_key = str(road_file.resolve())
                if file_key in self._processed_files:
                    continue
                
                try:
                    roads_count += self._parse_road_file(road_file)
                    self._processed_files.add(file_key)
                except Exception as e:
                    print(f"❌ Error parsing road file {road_file}: {e}")
        
        return roads_count
    
    def _parse_road_file(self, road_file: Path) -> int:
        """Parse a single road file"""
        roads_found = 0
        
        print(f"📁 Parsing road file: {road_file.relative_to(self.level_path)}")
        
        try:
            with open(road_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
                # Handle different JSON formats
                if content.startswith('['):
                    # JSON array format
                    data = json.loads(content)
                    for item in data:
                        if self._is_decal_road(item):
                            try:
                                road = DecalRoadData(item)
                                self.roads.append(road)
                                roads_found += 1
                            except ValueError as e:
                                print(f"⚠️  Skipping invalid road: {e}")
                
                else:
                    # Line-by-line JSON format
                    for line_num, line in enumerate(content.split('\n'), 1):
                        line = line.strip()
                        if not line:
                            continue
                        
                        try:
                            item = json.loads(line)
                            if self._is_decal_road(item):
                                try:
                                    road = DecalRoadData(item)
                                    self.roads.append(road)
                                    roads_found += 1
                                except ValueError as e:
                                    print(f"⚠️  Skipping invalid road on line {line_num}: {e}")
                        except json.JSONDecodeError:
                            # Skip invalid JSON lines
                            continue
        
        except Exception as e:
            print(f"❌ Error reading road file {road_file}: {e}")
            raise
        
        if roads_found > 0:
            print(f"  ✅ Found {roads_found} DecalRoad objects")
        
        return roads_found
    
    def _parse_materials(self) -> int:
        """Parse material definitions from level files"""
        materials_count = 0
        
        # Look for material files
        material_patterns = [
            "art/road/*.materials.json",
            "art/**/*.materials.json", 
            "**/*.materials.json"
        ]
        
        for pattern in material_patterns:
            for material_file in self.level_path.glob(pattern):
                try:
                    materials_count += self._parse_material_file(material_file)
                except Exception as e:
                    print(f"❌ Error parsing material file {material_file}: {e}")
        
        return materials_count
    
    def _parse_material_file(self, material_file: Path) -> int:
        """Parse a single material file"""
        materials_found = 0
        
        print(f"📁 Parsing material file: {material_file.relative_to(self.level_path)}")
        
        try:
            with open(material_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if isinstance(data, dict):
                    for mat_name, mat_data in data.items():
                        if isinstance(mat_data, dict) and mat_data.get('class') == 'Material':
                            try:
                                material = MaterialData(mat_name, mat_data)
                                self.materials[mat_name] = material
                                materials_found += 1
                            except Exception as e:
                                print(f"⚠️  Error parsing material {mat_name}: {e}")
        
        except Exception as e:
            print(f"❌ Error reading material file {material_file}: {e}")
            raise
        
        if materials_found > 0:
            print(f"  ✅ Found {materials_found} materials")
        
        return materials_found
    
    def _is_decal_road(self, item: Dict[str, Any]) -> bool:
        """Check if an item is a DecalRoad"""
        return (isinstance(item, dict) and 
                item.get('class') == 'DecalRoad' and
                'nodes' in item and
                len(item.get('nodes', [])) >= 2)
    
    def _deduplicate_roads(self) -> None:
        """Remove duplicate roads based on persistent ID"""
        unique_roads = []
        seen_ids = set()
        
        for road in self.roads:
            if road.persistent_id not in seen_ids:
                unique_roads.append(road)
                seen_ids.add(road.persistent_id)
        
        self.roads = unique_roads
    
    def _validate_road_materials(self) -> None:
        """Validate that all road materials exist"""
        missing_materials = set()
        
        for road in self.roads:
            if road.material not in self.materials:
                missing_materials.add(road.material)
        
        if missing_materials:
            print(f"⚠️  Warning: {len(missing_materials)} road materials not found:")
            for mat in sorted(missing_materials):
                print(f"    - {mat}")
    
    def get_road_by_id(self, persistent_id: str) -> Optional[DecalRoadData]:
        """Get a road by its persistent ID"""
        for road in self.roads:
            if road.persistent_id == persistent_id:
                return road
        return None
    
    def get_roads_by_material(self, material_name: str) -> List[DecalRoadData]:
        """Get all roads using a specific material"""
        return [road for road in self.roads if road.material == material_name]
    
    def get_material(self, material_name: str) -> Optional[MaterialData]:
        """Get material data by name"""
        return self.materials.get(material_name)
    
    def get_unique_materials(self) -> List[str]:
        """Get list of unique material names used by roads"""
        return list(set(road.material for road in self.roads))
    
    def get_roads_data(self) -> List[DecalRoadData]:
        """Get all parsed road data"""
        return self.roads
    
    def get_stats(self) -> Dict[str, Any]:
        """Get parsing statistics"""
        unique_materials = self.get_unique_materials()
        material_usage = {}
        
        for material in unique_materials:
            roads_using = len(self.get_roads_by_material(material))
            material_usage[material] = roads_using
        
        return {
            'total_roads': len(self.roads),
            'total_materials': len(self.materials),
            'unique_materials_used': len(unique_materials),
            'material_usage': material_usage,
            'level_path': str(self.level_path)
        } 
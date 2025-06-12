#!/usr/bin/env python3
"""
BeamNG Road Data Analysis Script
Analyzes DecalRoad data from BeamNG level files to understand structure and patterns
"""

import json
import os
from collections import defaultdict

def analyze_roads_from_level(level_path):
    """Analyze road data from BeamNG level"""
    
    roads_file = os.path.join(level_path, "main", "MissionGroup", "roads", "items.level.json")
    
    if not os.path.exists(roads_file):
        print(f"No roads file found at: {roads_file}")
        return
    
    print(f"Analyzing roads from: {roads_file}")
    print("=" * 80)
    
    # Statistics
    total_roads = 0
    materials = defaultdict(int)
    spline_types = defaultdict(int)
    node_counts = defaultdict(int)
    properties_used = defaultdict(int)
    break_angles = defaultdict(int)
    render_priorities = defaultdict(int)
    
    # Sample road data for inspection
    sample_roads = []
    
    # Parse roads JSON
    with open(roads_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
                
            try:
                road_data = json.loads(line)
                if road_data.get('class') == 'DecalRoad':
                    total_roads += 1
                    
                    # Material analysis
                    material = road_data.get('material', 'unknown')
                    materials[material] += 1
                    
                    # Node count analysis
                    nodes = road_data.get('nodes', [])
                    node_count = len(nodes)
                    node_counts[f"{node_count} nodes"] += 1
                    
                    # Spline type analysis
                    improved_spline = road_data.get('improvedSpline', False)
                    break_angle = road_data.get('breakAngle', 0)
                    
                    if break_angle > 0:
                        spline_types['Has break angle'] += 1
                        break_angles[str(break_angle)] += 1
                    else:
                        spline_types['No break angle'] += 1
                    
                    if improved_spline:
                        spline_types['Improved spline'] += 1
                    else:
                        spline_types['Basic spline'] += 1
                    
                    # Properties analysis
                    if 'startEndFade' in road_data:
                        properties_used['startEndFade'] += 1
                    if 'textureLength' in road_data:
                        properties_used['textureLength'] += 1
                    if 'renderPriority' in road_data:
                        properties_used['renderPriority'] += 1
                        render_priorities[str(road_data['renderPriority'])] += 1
                    if 'distanceFade' in road_data:
                        properties_used['distanceFade'] += 1
                    if 'overObjects' in road_data:
                        properties_used['overObjects'] += 1
                    if 'useTemplate' in road_data:
                        properties_used['useTemplate'] += 1
                    
                    # Collect sample roads
                    if len(sample_roads) < 5:
                        sample_roads.append(road_data)
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    # Print analysis results
    print(f"TOTAL ROADS: {total_roads}")
    print()
    
    print("MATERIALS:")
    for material, count in sorted(materials.items(), key=lambda x: x[1], reverse=True):
        print(f"  {material}: {count}")
    print()
    
    print("NODE COUNTS:")
    for node_count, count in sorted(node_counts.items()):
        print(f"  {node_count}: {count}")
    print()
    
    print("SPLINE TYPES:")
    for spline_type, count in sorted(spline_types.items()):
        print(f"  {spline_type}: {count}")
    print()
    
    if break_angles:
        print("BREAK ANGLES:")
        for angle, count in sorted(break_angles.items()):
            print(f"  {angle}: {count}")
        print()
    
    if render_priorities:
        print("RENDER PRIORITIES:")
        for priority, count in sorted(render_priorities.items()):
            print(f"  Priority {priority}: {count}")
        print()
    
    print("PROPERTIES USAGE:")
    for prop, count in sorted(properties_used.items()):
        print(f"  {prop}: {count} roads")
    print()
    
    # Show sample road structures
    print("SAMPLE ROAD STRUCTURES:")
    print("-" * 40)
    for i, road in enumerate(sample_roads[:3], 1):
        print(f"Sample Road {i}:")
        print(f"  Material: {road.get('material')}")
        print(f"  Nodes: {len(road.get('nodes', []))}")
        print(f"  Improved Spline: {road.get('improvedSpline', False)}")
        print(f"  Break Angle: {road.get('breakAngle', 0)}")
        
        # Show first few nodes
        nodes = road.get('nodes', [])
        if nodes:
            print(f"  First node: {nodes[0]} (x, y, z, width)")
            if len(nodes) > 1:
                print(f"  Second node: {nodes[1]}")
            if len(nodes) > 2:
                print(f"  Last node: {nodes[-1]}")
        
        print(f"  All properties: {list(road.keys())}")
        print()
    
    # Coordinate analysis
    print("COORDINATE ANALYSIS:")
    print("-" * 20)
    
    all_x, all_y, all_z, all_widths = [], [], [], []
    
    with open(roads_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            try:
                road_data = json.loads(line)
                if road_data.get('class') == 'DecalRoad':
                    nodes = road_data.get('nodes', [])
                    for node in nodes:
                        if len(node) >= 4:
                            x, y, z, width = node[:4]
                            all_x.append(x)
                            all_y.append(y)
                            all_z.append(z)
                            all_widths.append(width)
            except:
                continue
    
    if all_x:
        print(f"X coordinates: {min(all_x):.1f} to {max(all_x):.1f}")
        print(f"Y coordinates: {min(all_y):.1f} to {max(all_y):.1f}")
        print(f"Z coordinates: {min(all_z):.1f} to {max(all_z):.1f}")
        print(f"Widths: {min(all_widths):.1f} to {max(all_widths):.1f}")
        print(f"Coordinate scale suggests world units are meters")
        print()

def main():
    """Main analysis function"""
    
    # Level path (using symlink in test folder)
    level_path = os.path.join(os.path.dirname(__file__), "small_island")
    
    if not os.path.exists(level_path):
        print(f"Level path not found: {level_path}")
        return
    
    analyze_roads_from_level(level_path)

if __name__ == "__main__":
    main() 
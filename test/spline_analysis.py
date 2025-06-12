#!/usr/bin/env python3
"""
BeamNG Road Spline Analysis Script
Analyzes the mathematical properties of road splines to understand curve interpolation
"""

import json
import os
import math
from collections import defaultdict

def calculate_distance(p1, p2):
    """Calculate 3D distance between two points"""
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1[:3], p2[:3])))

def calculate_angle_change(p1, p2, p3):
    """Calculate the angle change at point p2 between segments p1->p2 and p2->p3"""
    # Vectors
    v1 = [p2[i] - p1[i] for i in range(3)]
    v2 = [p3[i] - p2[i] for i in range(3)]
    
    # Magnitudes
    mag1 = math.sqrt(sum(x**2 for x in v1))
    mag2 = math.sqrt(sum(x**2 for x in v2))
    
    if mag1 == 0 or mag2 == 0:
        return 0
    
    # Normalize
    v1 = [x / mag1 for x in v1]
    v2 = [x / mag2 for x in v2]
    
    # Dot product
    dot = sum(a * b for a, b in zip(v1, v2))
    dot = max(-1, min(1, dot))  # Clamp to avoid numerical errors
    
    # Angle in radians
    angle = math.acos(dot)
    return math.degrees(angle)

def analyze_spline_characteristics(road_data):
    """Analyze the mathematical characteristics of a road spline"""
    nodes = road_data.get('nodes', [])
    if len(nodes) < 3:
        return None
    
    analysis = {
        'total_length': 0,
        'segment_lengths': [],
        'angle_changes': [],
        'curvature_changes': [],
        'width_changes': [],
        'uniform_spacing': True,
        'smooth_curvature': True,
        'constant_width': True
    }
    
    # Analyze segments
    for i in range(len(nodes) - 1):
        p1, p2 = nodes[i], nodes[i + 1]
        segment_length = calculate_distance(p1, p2)
        analysis['segment_lengths'].append(segment_length)
        analysis['total_length'] += segment_length
        
        # Width change
        width_change = abs(p2[3] - p1[3])
        analysis['width_changes'].append(width_change)
        if width_change > 0.1:  # Threshold for "constant"
            analysis['constant_width'] = False
    
    # Analyze angles and curvature
    for i in range(1, len(nodes) - 1):
        p1, p2, p3 = nodes[i-1], nodes[i], nodes[i+1]
        angle_change = calculate_angle_change(p1, p2, p3)
        analysis['angle_changes'].append(angle_change)
    
    # Check spacing uniformity
    if analysis['segment_lengths']:
        avg_length = sum(analysis['segment_lengths']) / len(analysis['segment_lengths'])
        for length in analysis['segment_lengths']:
            if abs(length - avg_length) > avg_length * 0.3:  # 30% tolerance
                analysis['uniform_spacing'] = False
                break
    
    # Check curvature smoothness
    if len(analysis['angle_changes']) > 1:
        for i in range(len(analysis['angle_changes']) - 1):
            curr_angle = analysis['angle_changes'][i]
            next_angle = analysis['angle_changes'][i + 1]
            curvature_change = abs(curr_angle - next_angle)
            analysis['curvature_changes'].append(curvature_change)
            
            if curvature_change > 20:  # Threshold for "smooth"
                analysis['smooth_curvature'] = False
    
    return analysis

def analyze_spline_types(level_path):
    """Analyze spline characteristics across all roads"""
    
    roads_file = os.path.join(level_path, "main", "MissionGroup", "roads", "items.level.json")
    
    if not os.path.exists(roads_file):
        print(f"No roads file found at: {roads_file}")
        return
    
    print(f"Analyzing spline characteristics from: {roads_file}")
    print("=" * 80)
    
    # Statistics
    spline_characteristics = defaultdict(list)
    material_characteristics = defaultdict(lambda: defaultdict(list))
    
    total_roads = 0
    analyzed_roads = 0
    
    # Sample detailed analysis
    detailed_samples = []
    
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
                    
                    analysis = analyze_spline_characteristics(road_data)
                    if analysis:
                        analyzed_roads += 1
                        material = road_data.get('material', 'unknown')
                        
                        # Collect statistics
                        spline_characteristics['total_length'].append(analysis['total_length'])
                        spline_characteristics['uniform_spacing'].append(analysis['uniform_spacing'])
                        spline_characteristics['smooth_curvature'].append(analysis['smooth_curvature'])
                        spline_characteristics['constant_width'].append(analysis['constant_width'])
                        
                        # Material-specific characteristics
                        material_characteristics[material]['total_length'].append(analysis['total_length'])
                        material_characteristics[material]['segment_count'].append(len(analysis['segment_lengths']))
                        
                        # Collect detailed samples
                        if len(detailed_samples) < 3:
                            detailed_samples.append({
                                'road_data': road_data,
                                'analysis': analysis
                            })
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
                continue
    
    # Print analysis results
    print(f"ANALYZED: {analyzed_roads} out of {total_roads} roads")
    print()
    
    # Spline characteristics summary
    if spline_characteristics['total_length']:
        lengths = spline_characteristics['total_length']
        print(f"ROAD LENGTHS:")
        print(f"  Range: {min(lengths):.1f}m to {max(lengths):.1f}m")
        print(f"  Average: {sum(lengths)/len(lengths):.1f}m")
        print()
        
        uniform_count = sum(spline_characteristics['uniform_spacing'])
        smooth_count = sum(spline_characteristics['smooth_curvature'])
        constant_width_count = sum(spline_characteristics['constant_width'])
        
        print(f"SPLINE CHARACTERISTICS:")
        print(f"  Uniform spacing: {uniform_count}/{analyzed_roads} ({uniform_count/analyzed_roads*100:.1f}%)")
        print(f"  Smooth curvature: {smooth_count}/{analyzed_roads} ({smooth_count/analyzed_roads*100:.1f}%)")
        print(f"  Constant width: {constant_width_count}/{analyzed_roads} ({constant_width_count/analyzed_roads*100:.1f}%)")
        print()
    
    # Material-specific analysis
    print("MATERIAL-SPECIFIC CHARACTERISTICS:")
    for material, chars in sorted(material_characteristics.items()):
        if chars['total_length']:
            avg_length = sum(chars['total_length']) / len(chars['total_length'])
            avg_segments = sum(chars['segment_count']) / len(chars['segment_count'])
            print(f"  {material}:")
            print(f"    Average length: {avg_length:.1f}m")
            print(f"    Average segments: {avg_segments:.1f}")
    print()
    
    # Detailed sample analysis
    print("DETAILED SPLINE ANALYSIS SAMPLES:")
    print("-" * 50)
    
    for i, sample in enumerate(detailed_samples, 1):
        road = sample['road_data']
        analysis = sample['analysis']
        
        print(f"Sample {i}: {road.get('material')} road")
        print(f"  Nodes: {len(road.get('nodes', []))}")
        print(f"  Total length: {analysis['total_length']:.1f}m")
        print(f"  Break angle: {road.get('breakAngle', 0)}")
        print(f"  Improved spline: {road.get('improvedSpline', False)}")
        
        print(f"  Segment lengths: {[f'{x:.1f}' for x in analysis['segment_lengths'][:5]]}{'...' if len(analysis['segment_lengths']) > 5 else ''}")
        if analysis['angle_changes']:
            print(f"  Angle changes: {[f'{x:.1f}°' for x in analysis['angle_changes'][:5]]}{'...' if len(analysis['angle_changes']) > 5 else ''}")
        
        print(f"  Uniform spacing: {analysis['uniform_spacing']}")
        print(f"  Smooth curvature: {analysis['smooth_curvature']}")
        print(f"  Constant width: {analysis['constant_width']}")
        
        # Width profile
        nodes = road.get('nodes', [])
        widths = [node[3] for node in nodes]
        print(f"  Width profile: {[f'{x:.1f}' for x in widths[:5]]}{'...' if len(widths) > 5 else ''}")
        print()
    
    # Spline type inference
    print("SPLINE TYPE INFERENCE:")
    print("-" * 25)
    print("Based on the analysis, BeamNG roads appear to use:")
    print("1. Control point-based splines (not direct coordinates)")
    print("2. Variable width along path (stored per control point)")
    print("3. Smooth interpolation with break angle control")
    print("4. Likely Hermite or similar parametric curves for 'improvedSpline'")
    print("5. Possibly linear interpolation for non-improved splines")
    print()
    print("The 'nodes' array represents control points, not sampled curve points.")
    print("Width variation suggests the curves are designed for road mesh generation.")

def main():
    """Main analysis function"""
    
    # Level path (using symlink in test folder)
    level_path = os.path.join(os.path.dirname(__file__), "small_island")
    
    if not os.path.exists(level_path):
        print(f"Level path not found: {level_path}")
        return
    
    analyze_spline_types(level_path)

if __name__ == "__main__":
    main() 
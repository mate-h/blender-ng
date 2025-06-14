#!/usr/bin/env python3
"""
Simple test script for creating clothoid curves using G1 Hermite interpolation.
Uses pyclothoids library to generate points and creates Blender curve objects.
"""

import bpy
import math
from mathutils import Vector
from pyclothoids import Clothoid

def create_clothoid_curve(name, x0, y0, t0, x1, y1, t1, num_points=50):
    """Create a clothoid curve using G1 Hermite interpolation"""
    try:
        # Generate clothoid using G1 Hermite interpolation
        clothoid = Clothoid.G1Hermite(x0, y0, t0, x1, y1, t1)
        
        # Create curve data
        curve_data = bpy.data.curves.new(name=name, type='CURVE')
        curve_data.dimensions = '3D'
        
        # Create spline
        spline = curve_data.splines.new('POLY')  # Using poly line for simplicity
        
        # Sample points along the clothoid
        length = clothoid.length
        points = []
        for i in range(num_points):
            s = (i / (num_points - 1)) * length
            x = clothoid.X(s)
            y = clothoid.Y(s)
            points.append(Vector((x, y, 0.0)))
        
        # Add points to spline
        spline.points.add(len(points) - 1)
        for i, point in enumerate(points):
            spline.points[i].co = (point.x, point.y, point.z, 1.0)
        
        # Create curve object
        curve_obj = bpy.data.objects.new(name, curve_data)
        
        # Link curve to scene
        bpy.context.collection.objects.link(curve_obj)
        
        # Store clothoid parameters as custom properties
        curve_obj["clothoid_length"] = length
        curve_obj["clothoid_start_x"] = x0
        curve_obj["clothoid_start_y"] = y0
        curve_obj["clothoid_start_angle"] = t0
        curve_obj["clothoid_end_x"] = x1
        curve_obj["clothoid_end_y"] = y1
        curve_obj["clothoid_end_angle"] = t1
        curve_obj["clothoid_start_curvature"] = clothoid.KappaStart
        curve_obj["clothoid_end_curvature"] = clothoid.KappaEnd
        
        return curve_obj
    
    except Exception as e:
        print(f"Error creating clothoid curve: {e}")
        return None

def create_test_curves():
    """Create a few test clothoid curves"""
    # Clear existing test curves
    for obj in bpy.data.objects:
        if obj.name.startswith("Clothoid"):
            bpy.data.objects.remove(obj, do_unlink=True)
    
    # Test case 1: Simple S-curve
    curve1 = create_clothoid_curve(
        name="Clothoid_S_Curve",
        x0=0, y0=0, t0=0,           # Start at origin, horizontal
        x1=10, y1=5, t1=math.pi/4,  # End above and right, 45 degrees
        num_points=50
    )
    if curve1:
        curve1.location.x = 0
    
    # Test case 2: Quarter turn
    curve2 = create_clothoid_curve(
        name="Clothoid_Quarter_Turn",
        x0=0, y0=0, t0=0,           # Start at origin, horizontal
        x1=5, y1=5, t1=math.pi/2,   # End with vertical tangent
        num_points=50
    )
    if curve2:
        curve2.location.x = 15
    
    # Test case 3: Gentle curve
    curve3 = create_clothoid_curve(
        name="Clothoid_Gentle_Curve",
        x0=0, y0=0, t0=0,           # Start at origin, horizontal
        x1=10, y1=2, t1=math.pi/6,  # End with 30 degree angle
        num_points=50
    )
    if curve3:
        curve3.location.x = 30

def main():
    """Main function"""
    print("Creating test clothoid curves...")
    create_test_curves()
    print("Done!")

if __name__ == "__main__":
    main() 
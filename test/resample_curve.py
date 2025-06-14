import bpy
import mathutils

def hermite_interp(p0, p1, t0, t1, t):
    """Cubic Hermite interpolation for a single t in [0,1]."""
    h00 = 2*t**3 - 3*t**2 + 1
    h10 = t**3 - 2*t**2 + t
    h01 = -2*t**3 + 3*t**2
    h11 = t**3 - t**2
    return h00 * p0 + h10 * t0 + h01 * p1 + h11 * t1

def compute_tangents(points):
    """Compute tangents for G1 continuity (central difference for interior, forward/backward for ends)."""
    tangents = []
    n = len(points)
    for i in range(n):
        if i == 0:
            tangent = points[1] - points[0]
        elif i == n - 1:
            tangent = points[-1] - points[-2]
        else:
            tangent = 0.5 * (points[i+1] - points[i-1])
        tangents.append(tangent)
    return tangents

class CURVE_OT_resample_hermite(bpy.types.Operator):
    """Resample active curve with G1 Hermite interpolation"""
    bl_idname = "curve.resample_hermite"
    bl_label = "Resample Curve (Hermite)"
    bl_options = {'REGISTER', 'UNDO'}

    samples_per_segment: bpy.props.IntProperty(
        name="Samples Per Segment",
        default=10,
        min=2,
        max=100
    )

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'CURVE':
            self.report({'ERROR'}, "Active object is not a curve")
            return {'CANCELLED'}

        curve = obj.data
        spline = curve.splines[0]
        if spline.type != 'BEZIER' and spline.type != 'POLY':
            self.report({'ERROR'}, "Only Bezier or Poly splines supported")
            return {'CANCELLED'}

        # Get points as vectors
        if spline.type == 'BEZIER':
            points = [p.co.to_3d() for p in spline.bezier_points]
        else:
            points = [p.co.to_3d() for p in spline.points]

        tangents = compute_tangents(points)
        new_points = []

        for i in range(len(points) - 1):
            p0, p1 = points[i], points[i+1]
            t0, t1 = tangents[i], tangents[i+1]
            for s in range(self.samples_per_segment):
                t = s / (self.samples_per_segment - 1)
                pt = hermite_interp(p0, p1, t0, t1, t)
                new_points.append(pt)

        # Replace spline with new points
        spline.points.add(len(new_points) - len(spline.points))
        for i, pt in enumerate(new_points):
            spline.points[i].co = (pt.x, pt.y, pt.z, 1.0)

        # Remove extra points if any
        if len(spline.points) > len(new_points):
            spline.points.resize(len(new_points))

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(CURVE_OT_resample_hermite.bl_idname)

def register():
    bpy.utils.register_class(CURVE_OT_resample_hermite)
    bpy.types.VIEW3D_MT_curve_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(CURVE_OT_resample_hermite)
    bpy.types.VIEW3D_MT_curve_add.remove(menu_func)

if __name__ == "__main__":
    register()
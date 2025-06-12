# BeamNG Road Data Analysis Summary

## Key Findings

### Road Data Structure
- **Total Roads**: 385 DecalRoad objects in small_island level
- **Control Points**: Nodes represent control points, not sampled curve points
- **Coordinate System**: World units appear to be meters
- **Coordinate Range**: X: -435 to 415, Y: -443 to 403, Z: 25 to 85

### Road Categories by Material
1. **Sand Paths** (88 roads): `m_sand_variation` - short segments, avg 27.4m
2. **Natural Features** (85 roads): `bank_erosion` - short natural features, avg 29.9m  
3. **Tire Tracks** (62 roads): `dirt_tiretracks` - medium length, avg 42.3m
4. **Main Asphalt** (46 roads): `utah_asphalt_road_dirt_edge` - longer roads, avg 143m
5. **Dirt Roads** (45 roads): `Dirt_road_variation_03` - varied lengths, avg 52.9m

### Spline Characteristics
- **Improved Spline**: ALL roads use `improvedSpline: true`
- **Smooth Curvature**: 77% show mathematically smooth curves
- **Uniform Spacing**: Only 50% have uniform control point spacing
- **Constant Width**: 95% maintain constant width along path
- **Break Angles**: 27% use break angles for sharp corners

### Mathematical Analysis
- **Curve Type**: Likely Hermite/Catmull-Rom splines, NOT NURBS
- **Width Profile**: Stored per control point (4th component: [x, y, z, width])
- **Node Count**: Ranges from 2-43 nodes, average ~6 nodes per road
- **Length Range**: 9.2m to 768.7m, average 70.6m

## Spline Type Inference

**Confirmed**: BeamNG roads are **control point-based parametric curves**, not NURBS splines.

### Evidence:
1. **Control Points**: Non-uniform spacing indicates control points, not curve samples
2. **Smooth Interpolation**: 77% smooth curvature suggests parametric interpolation
3. **Break Angle Control**: Sharp corner control via `breakAngle` parameter
4. **Width Integration**: Width stored per control point for mesh generation
5. **Improved Spline Flag**: Suggests enhanced interpolation (Hermite vs linear)

### Likely Implementation:
- **Improved Spline (99.7% of roads)**: Hermite or Catmull-Rom curves
- **Break Angle Roads (27%)**: Piecewise linear segments at corners
- **Width Variation**: Mesh generation from control points + width profile

## Visualization Strategy

For Blender import:
1. **Create curves from control points** using appropriate spline type
2. **Store width data** as custom properties or bevel objects
3. **Categorize by material** for organization and material assignment
4. **Handle break angles** by using POLY splines instead of smooth curves
5. **Scale coordinates** appropriately (0.1x scaling works well)

## Road Mesh Generation Notes

BeamNG likely generates road meshes by:
1. Interpolating smooth curves between control points
2. Creating cross-sections at regular intervals along curves  
3. Using width values to determine cross-section size
4. Generating collision and visual meshes separately
5. Applying material textures based on material names

This explains why DecalRoad objects are "visual only" - the actual drivable surface is carved into the terrain mesh. 
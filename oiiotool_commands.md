# OIIO Image Processing Commands

This document records the oiiotool commands used to process the satellite image from the original download to the final 4K texture.

## Original Image Processing Workflow

### 1. Scale Original to 10K
```bash
oiiotool /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_49.3375_-123.2065_1ppm_9.765625km.jpg --resize 10000x10000 -o /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_49.3375_-123.2065_1ppm_9.765625km_10k.jpg
```
- **Purpose**: Scale the original satellite image to exactly 10000x10000 pixels
- **Input**: Original satellite image (variable dimensions)
- **Output**: 10000x10000 scaled image

### 2. Center Crop 10K to 8K
```bash
oiiotool /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_10k.jpg --cut 8192x8192+904+904 -o /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_8k_center.jpg
```
- **Purpose**: Extract a center 8192x8192 section from the 10K image
- **Key Points**: 
  - Used `--cut` instead of `--crop` to avoid black borders
  - Offset calculation: (10000 - 8192) / 2 = 904
  - `--cut` extracts the region and repositions to origin
- **Input**: 10000x10000 image
- **Output**: 8192x8192 center-cropped image

### 3. Scale 8K to 4K
```bash
oiiotool /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_8k_center.jpg --resize 4096x4096 -o /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_4k_center.jpg
```
- **Purpose**: Scale the 8K texture down to 4K for better performance
- **Input**: 8192x8192 center-cropped image
- **Output**: 4096x4096 final texture

## Key Learnings

### Crop vs Cut
- `--crop GEOM`: Sets pixel data resolution and offset, may pad with black if crop area extends beyond image
- `--cut GEOM`: Cuts out the ROI and repositions to origin, gives exactly the pixels you want
- **Recommendation**: Use `--cut` when you want to extract a specific region without padding

### Geometry Format
- Format: `WxH+X+Y` (width x height + x_offset + y_offset)
- Example: `8192x8192+904+904` means 8192x8192 pixels starting at position (904, 904)

### File Verification
```bash
oiiotool --info filename.jpg
```
Use this command to verify image dimensions and properties after processing.

## Final Output Files
- `satellite_8k_center.jpg`: 8192x8192 center-cropped satellite texture
- `satellite_4k_center.jpg`: 4096x4096 downscaled satellite texture

Both files are clean textures without black borders, suitable for use in 3D applications.

## GDAL Coordinate Transformation

### Transform from WGS84 to UTM Zone 10N

#### Step 1: Georeference the image in WGS84
```bash
gdal_translate -a_srs EPSG:4326 -a_ullr -123.2565 49.3875 -122.7565 48.8875 /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_10k.jpg /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_10k_wgs84.tif
```
- **Purpose**: Add WGS84 georeferencing to the satellite image
- **Parameters**:
  - `-a_srs EPSG:4326`: Assign WGS84 coordinate system
  - `-a_ullr`: Set Upper Left/Lower Right coordinates (west, north, east, south)
  - Bounds cover Vancouver area with ~9.765km extent

#### Step 2: Transform to UTM Zone 10N
```bash
gdalwarp -s_srs EPSG:4326 -t_srs EPSG:32610 /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_10k_wgs84.tif /Volumes/Goodboy/github/blend-ng/map-browser/downloads/satellite_10k_utm10.tif
```
- **Purpose**: Transform from WGS84 to UTM Zone 10N projection
- **Parameters**:
  - `-s_srs EPSG:4326`: Source coordinate system (WGS84)
  - `-t_srs EPSG:32610`: Target coordinate system (UTM Zone 10N)
- **Result**: 7797 x 11831 pixels in UTM coordinates
- **Pixel Size**: ~4.7 meters per pixel

### Verification
```bash
gdalinfo filename.tif
```
Use this command to verify coordinate system and georeferencing information.

## Output Files Summary
- `satellite_10k_wgs84.tif`: Georeferenced in WGS84 (10000x10000)
- `satellite_10k_utm10.tif`: Transformed to UTM Zone 10N (7797x11831)
- `satellite_8k_center.jpg`: 8192x8192 center-cropped texture
- `satellite_4k_center.jpg`: 4096x4096 downscaled texture

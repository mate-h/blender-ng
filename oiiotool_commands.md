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

## DTM-Matched Satellite Imagery Workflow

### 1. Download and Align Satellite to DTM
The system automatically downloads satellite imagery that matches a DTM file's projection and bounds:

#### Backend Process (Automated):
```bash
# 1. Analyze remote DTM file
gdalinfo "/vsicurl/https://ftp.maps.canada.ca/pub/elevation/dem_mne/highresolution_hauteresolution/dtm_mnt/1m/BC/Lower_Mainland_2016/utm10/dtm_1m_utm10_w_1_146.tif"

# 2. Transform DTM bounds to WGS84 for Mapbox API
echo "480000 5470000" | gdaltransform -s_srs EPSG:3157 -t_srs EPSG:4326
echo "490000 5460000" | gdaltransform -s_srs EPSG:3157 -t_srs EPSG:4326

# 3. Download high-resolution satellite imagery (10000+ pixels)
# [Mapbox API calls with tiling - handled by backend]

# 4. Georeference satellite image in WGS84
gdal_translate -a_srs EPSG:4326 -a_ullr -123.275569857435 49.3826223105414 -123.137542365707 49.2924261665239 satellite_raw.jpg satellite_wgs84.tif

# 5. Transform to match DTM projection (EPSG:3157)
gdalwarp -t_srs EPSG:3157 -tr 1 1 -r cubic satellite_wgs84.tif satellite_projected.tif

# 6. Align exactly to DTM bounds and dimensions
gdalwarp -te 480000 5460000 490000 5470000 -ts 10000 10000 -r cubic satellite_projected.tif satellite_aligned.tif

# 7. Convert to JPEG
oiiotool satellite_aligned.tif -o satellite_aligned.jpg
```

### 2. Process for BeamNG Import

#### Center Crop 10K to 8K
```bash
oiiotool satellite_dtm_1m_utm10_w_1_146_aligned.jpg --cut 8192x8192+904+904 -o satellite_dtm_1m_utm10_w_1_146_8k_center.jpg
```
- **Purpose**: Extract center 8192x8192 section from 10K aligned satellite image
- **Key Points**: 
  - Offset calculation: (10000 - 8192) / 2 = 904
  - `--cut` extracts the region and repositions to origin
  - Maintains perfect DTM alignment in the center region

#### Scale 8K to 4K
```bash
oiiotool satellite_dtm_1m_utm10_w_1_146_8k_center.jpg --resize 4096x4096 -o satellite_dtm_1m_utm10_w_1_146_4k_center.jpg
```
- **Purpose**: Scale to 4K for optimal BeamNG performance
- **Result**: 9.0MB texture suitable for game engine use

## Output Files Summary

### DTM-Matched Satellite Files
- `satellite_dtm_1m_utm10_w_1_146_aligned.tif`: Perfect DTM alignment (10000x10000, 286MB)
- `satellite_dtm_1m_utm10_w_1_146_aligned.jpg`: JPEG version (10000x10000, 43MB)
- `satellite_dtm_1m_utm10_w_1_146_8k_center.jpg`: Center-cropped (8192x8192, 28MB)
- `satellite_dtm_1m_utm10_w_1_146_4k_center.jpg`: BeamNG-ready (4096x4096, 9MB)

### Legacy Files (Previous Workflow)
- `satellite_10k_wgs84.tif`: Georeferenced in WGS84 (10000x10000)
- `satellite_10k_utm10.tif`: Transformed to UTM Zone 10N (7797x11831)
- `satellite_8k_center.jpg`: 8192x8192 center-cropped texture
- `satellite_4k_center.jpg`: 4096x4096 downscaled texture

## Key Advantages of DTM-Matched Workflow

1. **Perfect Alignment**: Satellite and DTM have identical bounds and projection
2. **Automated Process**: Frontend integration allows one-click download from any DTM layer
3. **High Resolution**: Uses Mapbox tiling for maximum detail (1+ pixels per meter)
4. **Coordinate Accuracy**: Handles remote DTM files and complex coordinate transformations
5. **BeamNG Ready**: Direct workflow from DTM selection to game-ready textures

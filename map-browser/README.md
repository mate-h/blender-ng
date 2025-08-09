# Map Browser

## Data Sources

https://geo.ca/imagery/high-resolution-digital-elevation-model-hrdem-canelevation-series/

https://app.geo.ca/en-ca/map-browser/record/957782bf-847c-4644-a757-e383c0057995

https://opentopography.org/

https://opendata.vancouver.ca/explore/dataset/public-trees

## Coordinate System Reprojection

Many GIS datasets come in UTM (Universal Transverse Mercator) coordinate systems, which use meter-based coordinates that are not compatible with web mapping libraries like Mapbox. This project includes several layers that required coordinate system transformation.

### Converting UTM to Web-Compatible Coordinates

Use `ogr2ogr` to convert shapefiles from UTM projections to WGS84 (EPSG:4326) for web mapping:

#### UTM Zone 9 (EPSG:3156) → WGS84
```bash
ogr2ogr -f GeoJSON -s_srs EPSG:3156 -t_srs EPSG:4326 \
  output_reprojected.geojson input.shp
```

#### UTM Zone 10 (EPSG:3157) → WGS84
```bash
ogr2ogr -f GeoJSON -s_srs EPSG:3157 -t_srs EPSG:4326 \
  output_reprojected.geojson input.shp
```

#### Example Commands Used in This Project
```bash
# Convert BC Vancouver Island UTM Zone 9 data
ogr2ogr -f GeoJSON -s_srs EPSG:3156 -t_srs EPSG:4326 \
  ./INDEX_utm9_BC_Vancouver_Island_Sunshine_Coast_2018/INDEX_utm9_BC_Vancouver_Island_Sunshine_Coast_2018_reprojected.geojson \
  ./INDEX_utm9_BC_Vancouver_Island_Sunshine_Coast_2018/INDEX_utm9_BC_Vancouver_Island_Sunshine_Coast_2018.shp

# Convert BC Vancouver Island UTM Zone 10 data  
ogr2ogr -f GeoJSON -s_srs EPSG:3157 -t_srs EPSG:4326 \
  ./INDEX_utm10_BC_Vancouver_Island_Sunshine_Coast_2018/INDEX_utm10_BC_Vancouver_Island_Sunshine_Coast_2018_reprojected.geojson \
  ./INDEX_utm10_BC_Vancouver_Island_Sunshine_Coast_2018/INDEX_utm10_BC_Vancouver_Island_Sunshine_Coast_2018.shp
```

### Common UTM Zone EPSG Codes for Canada

| UTM Zone | EPSG Code | Coverage Area |
|----------|-----------|---------------|
| UTM 9N   | EPSG:3156 | BC West Coast |
| UTM 10N  | EPSG:3157 | BC Vancouver Island/Lower Mainland |
| UTM 11N  | EPSG:3158 | BC Interior/Alberta West |
| UTM 12N  | EPSG:3159 | Alberta/Saskatchewan |

### Parameters Explained

- `-f GeoJSON`: Output format (GeoJSON for web compatibility)
- `-s_srs EPSG:XXXX`: Source coordinate reference system
- `-t_srs EPSG:4326`: Target CRS (WGS84 - standard for web maps)
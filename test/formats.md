# Decal Road Format

First one is a road, second one is the edge.

```json
[
  {
    "class": "DecalRoad",
    "persistentId": "6b579ce6-b349-4cbc-aa8b-39c63daa063c",
    "__parent": "roads",
    "position": [35.8802986, 382.663361, 27.4080429],
    "breakAngle": 1,
    "distanceFade": [300, 50],
    "improvedSpline": true,
    "material": "tread_marks_damaged_02",
    "nodes": [
      [35.8802986, 382.663361, 27.4080429, 5],
      [58.4397202, 372.257996, 28.571701, 5],
      [79.0960312, 361.109406, 30.0621185, 5],
      [102.277512, 350.699646, 31.395731, 5],
      [118.533463, 344.776398, 31.6648598, 5],
      [147.436981, 343.794739, 32.6167793, 5],
      [166.396545, 342.495056, 33.3655281, 5],
      [194.439407, 332.39505, 32.9403191, 5],
      [211.663895, 325.339508, 31.8235359, 5],
      [235.075974, 308.716309, 31.1900978, 5],
      [258.419006, 294.452332, 31.161171, 5],
      [277.371674, 282.909454, 31.2063732, 5],
      [287.104034, 263.945374, 31.9606209, 5],
      [287.654144, 238.168579, 33.4012337, 5],
      [279.97406, 211.316254, 34.9670219, 5]
    ],
    "renderPriority": 9,
    "startEndFade": [5, 5],
    "textureLength": 20
  },
  {
    "class": "DecalRoad",
    "persistentId": "97b1a4c0-5d01-4305-bc59-2706715af998",
    "__parent": "roads",
    "position": [101.832893, 354.487366, 31.1592731],
    "breakAngle": 1,
    "improvedSpline": true,
    "material": "utah_asphalt_road_dirt_edge",
    "nodes": [
      [101.832893, 354.487366, 31.1592731, 2],
      [114.398682, 349.070526, 31.4381332, 2],
      [124.851654, 347.081573, 31.5214672, 2],
      [133.421021, 346.811737, 31.7815571, 2],
      [146.35788, 346.966492, 32.4120865, 2],
      [156.524139, 346.8815, 33.0453224, 2],
      [162.907654, 345.999756, 33.3274918, 2],
      [168.44165, 344.890076, 33.4738655, 2],
      [179.103149, 341.447052, 33.4154205, 2],
      [189.700394, 337.561798, 33.1592789, 2],
      [200.553558, 333.304871, 32.7333107, 2],
      [211.937347, 328.824677, 32.0009651, 2],
      [222.106308, 321.883392, 31.4045868, 2],
      [234.425095, 312.873932, 31.186718, 2],
      [248.748138, 303.775879, 31.1718636, 2],
      [265.015076, 294.124237, 31.1212921, 2],
      [274.929321, 288.70932, 31.1245079, 2],
      [284.429749, 278.746582, 31.4546051, 2],
      [289.693695, 266.670166, 31.9251232, 2],
      [291.082611, 252.611725, 32.4946861, 2],
      [290.88089, 239.590576, 33.3285713, 2],
      [288.991089, 228.019073, 34.176754, 2],
      [287.05304, 219.108475, 34.5670662, 2],
      [288.711609, 207.17662, 34.9129601, 2],
      [286.509918, 192.852905, 34.808075, 2],
      [287.843811, 179.621826, 33.2125015, 2],
      [292.057648, 168.173386, 31.0823441, 2],
      [302.089844, 159.55661, 29.3047371, 1.89999998],
      [311.58374, 159.275452, 28.0455437, 1.89999998],
      [318.125366, 164.301834, 27.9998779, 1.89999998],
      [319.164642, 177.944885, 28.0133572, 1.89999998]
    ],
    "startEndFade": [3, 3],
    "textureLength": 8
  }
]
```

## Material

```json
{
  "tread_marks_damaged_02": {
    "name": "tread_marks_damaged_02",
    "mapTo": "unmapped_mat",
    "class": "Material",
    "persistentId": "19b08db8-996a-481d-8cd9-6ef8135ddeaa",
    "Stages": [
      {
        "ambientOcclusionMap": "/levels/small_island/art/road/t_asphalt_damaged_01_ao.data.png",
        "baseColorFactor": [0.644605994, 0.644603014, 0.64459902, 0.600000024],
        "baseColorMap": "/levels/small_island/art/road/t_asphalt_damaged_01_b.color.png",
        "detailNormalMap": "/levels/small_island/art/road/detailed_normals/t_asphalt_detail_02_nm.normal.png",
        "detailNormalMapStrength": 2,
        "detailScale": [2, 8],
        "normalMap": "/levels/small_island/art/road/t_asphalt_damaged_01_nm.normal.png",
        "opacityFactor": 0.856000006,
        "opacityMap": "/levels/small_island/art/road/t_asphalt_damaged_01_o.data.png",
        "roughnessFactor": 0.901000023,
        "roughnessMap": "/levels/small_island/art/road/t_asphalt_damaged_01_r.data.png"
      },
      {
        "baseColorFactor": null,
        "detailNormalMapStrength": null,
        "detailScale": null,
        "opacityFactor": null,
        "roughnessFactor": null
      },
      {
        "baseColorFactor": null,
        "detailNormalMapStrength": null,
        "detailScale": null,
        "opacityFactor": null,
        "roughnessFactor": null
      },
      {
        "baseColorFactor": null,
        "detailNormalMapStrength": null,
        "detailScale": null,
        "opacityFactor": null,
        "roughnessFactor": null
      }
    ],
    "alphaRef": 0,
    "annotation": "ASPHALT",
    "castShadows": false,
    "materialTag0": "RoadAndPath",
    "materialTag1": "beamng",
    "materialTag2": "Natural",
    "materialTag3": "Natural",
    "materialTag4": "east_coast_usa",
    "specularStrength0": "0",
    "translucent": true,
    "translucentZWrite": true,
    "version": 1.5
  },
  "utah_asphalt_road_dirt_wide_edge": {
    "name": "utah_asphalt_road_dirt_wide_edge",
    "mapTo": "unmapped_mat",
    "class": "Material",
    "persistentId": "d5adca0a-ecc5-4ef1-900f-7ac12b69f0bd",
    "Stages": [
      {
        "ambientOcclusionMap": "/levels/small_island/art/road/t_si_asphalt_dirt_wide_edge_ao.data.png",
        "baseColorFactor": [1, 0.999998987, 0.999989986, 0.699999988],
        "baseColorMap": "/levels/small_island/art/road/t_si_asphalt_dirt_wide_edge_b.color.png",
        "normalMap": "/levels/small_island/art/road/t_si_asphalt_dirt_wide_edge_nm.normal.png",
        "opacityFactor": 0.77700001,
        "opacityMap": "/levels/small_island/art/road/t_si_asphalt_dirt_wide_edge_o.data.png",
        "roughnessFactor": 0.848999977,
        "roughnessMap": "/levels/small_island/art/road/t_si_asphalt_dirt_wide_edge_r.data.png",
        "scrollSpeed": 4.11800003,
        "specular": [0.992156982, 0.992156982, 0.992156982, 1]
      },
      {
        "baseColorFactor": null,
        "opacityFactor": null,
        "roughnessFactor": null,
        "scrollSpeed": null,
        "specular": null
      },
      {
        "baseColorFactor": null,
        "opacityFactor": null,
        "roughnessFactor": null,
        "scrollSpeed": null,
        "specular": null
      },
      {
        "baseColorFactor": null,
        "opacityFactor": null,
        "roughnessFactor": null,
        "scrollSpeed": null,
        "specular": null
      }
    ],
    "alphaRef": 100,
    "alphaTest": true,
    "annotation": "NATURE",
    "materialTag0": "RoadAndPath",
    "materialTag1": "beamng",
    "specularStrength0": "0.490196",
    "translucent": true,
    "translucentZWrite": true,
    "version": 1.5
  }
}
```

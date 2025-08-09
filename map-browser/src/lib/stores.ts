import { writable } from 'svelte/store';
import type { LatLng } from './coordinateUtils';

export const defaultCenter: LatLng = {
  // 49.337545, -123.206493
  lng: -123.206493,
  lat: 49.337545
};

// Store for current grid center location
export const gridCenter = writable<LatLng>({ 
  lng: defaultCenter.lng,
  lat: defaultCenter.lat
});

// Store for current grid scale
export const gridScale = writable<number>(9.765625);

// Store for current grid size
export const gridSize = writable<number>(3);

// Layer definition interface
export interface LayerConfig {
  id: string;
  name: string;
  url: string;
  visible: boolean;
  fillColor: string;
  lineColor: string;
  fillOpacity: number;
  lineWidth: number;
  lineOpacity: number;
}

// Available layers
export const availableLayers: LayerConfig[] = [
  {
    id: 'public-trees',
    name: 'Public Trees',
    url: '/downloads/public-trees.geojson',
    visible: false,
    fillColor: '#228B22',
    lineColor: '#006400',
    fillOpacity: 0.7,
    lineWidth: 1,
    lineOpacity: 1.0
  },
  {
    id: 'projects-footprints',
    name: 'Projects Footprints',
    url: '/downloads/Projects_Footprints/Projects_Footprints.geojson',
    visible: false,
    fillColor: '#00ff00',
    lineColor: '#00aa00',
    fillOpacity: 0.2,
    lineWidth: 2,
    lineOpacity: 0.8
  },
  {
    id: 'bc-vancouver-island-utm9',
    name: 'BC Vancouver Island UTM9 (2018)',
    url: '/downloads/INDEX_utm9_BC_Vancouver_Island_Sunshine_Coast_2018/INDEX_utm9_BC_Vancouver_Island_Sunshine_Coast_2018_reprojected.geojson',
    visible: false,
    fillColor: '#ff6600',
    lineColor: '#cc4400',
    fillOpacity: 0.15,
    lineWidth: 1.5,
    lineOpacity: 0.7
  },
  {
    id: 'bc-vancouver-island-utm10',
    name: 'BC Vancouver Island UTM10 (2018)',
    url: '/downloads/INDEX_utm10_BC_Vancouver_Island_Sunshine_Coast_2018/INDEX_utm10_BC_Vancouver_Island_Sunshine_Coast_2018_reprojected.geojson',
    visible: false,
    fillColor: '#0066ff',
    lineColor: '#004499',
    fillOpacity: 0.15,
    lineWidth: 1.5,
    lineOpacity: 0.7
  },
  {
    id: 'bc-lower-mainland-2016',
    name: 'BC Lower Mainland (2016)',
    url: '/downloads/INDEX_utm10_BC_Lower_Mainland_2016/INDEX_utm10_BC_Lower_Mainland_2016.geojson',
    visible: false,
    fillColor: '#9966ff',
    lineColor: '#7744cc',
    fillOpacity: 0.15,
    lineWidth: 1.5,
    lineOpacity: 0.7
  },
  {
    id: 'roadways',
    name: 'Roadways',
    url: '/downloads/ways.geojson',
    visible: false,
    fillColor: '#ff4444',
    lineColor: '#cc0000',
    fillOpacity: 0.8,
    lineWidth: 2,
    lineOpacity: 0.9
  },
  {
    id: 'street-outlines',
    name: 'Street Outlines',
    url: '', // Handled internally by StreetOutlinesLayer component
    visible: true,
    fillColor: '#333333',
    lineColor: '#333333',
    fillOpacity: 0.7,
    lineWidth: 2,
    lineOpacity: 0.8
  }
];

// Layer visibility store
export const layerVisibility = writable<Record<string, boolean>>(
  availableLayers.reduce((acc, layer) => {
    acc[layer.id] = layer.visible;
    return acc;
  }, {} as Record<string, boolean>)
);

// Project labels visibility store (off by default)
export const projectLabelsVisible = writable<boolean>(false);

// Elevation marker interface
export interface ElevationMarker {
  id: string;
  position: LatLng;
  elevation: number | null;
  isLoading: boolean;
  error?: string;
}

// Elevation markers store
export const elevationMarkers = writable<ElevationMarker[]>([]);

// Elevation query mode (toggle between feature info and elevation query)
export const elevationQueryMode = writable<boolean>(false);

// 3D terrain visualization mode
export const terrainMode = writable<boolean>(false);

// Selected tree interface
export interface SelectedTree {
  id: string;
  properties: any;
  coordinates: [number, number];
}

// Selected trees store
export const selectedTrees = writable<SelectedTree[]>([]);
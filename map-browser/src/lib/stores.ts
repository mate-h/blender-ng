import { writable } from 'svelte/store';
import type { LatLng } from './coordinateUtils';

export const defaultCenter: LatLng = {
  lng: -123.2720,
  lat: 49.3634
};

// Store for current grid center location
export const gridCenter = writable<LatLng>({ 
  lng: defaultCenter.lng,
  lat: defaultCenter.lat
});

// Store for current grid scale
export const gridScale = writable<number>(1);

// Store for current grid size
export const gridSize = writable<number>(3);
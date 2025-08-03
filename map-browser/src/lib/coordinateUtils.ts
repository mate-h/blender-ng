import proj4 from 'proj4';

export interface LatLng {
  lat: number;
  lng: number;
}

export interface UTMCoordinate {
  x: number;
  y: number;
  zone: number;
}

export interface BoundingBox {
  southwest: LatLng;
  northeast: LatLng;
}

/**
 * Calculate UTM zone from longitude
 * UTM zones are 6 degrees wide, starting from -180°
 */
export function getUTMZone(lng: number): number {
  return Math.floor((lng + 180) / 6) + 1;
}

/**
 * Get UTM projection string for a given zone
 */
export function getUTMProjection(zone: number): string {
  return `+proj=utm +zone=${zone} +datum=WGS84 +units=m +no_defs`;
}

/**
 * Convert lat/lng coordinates to UTM
 */
export function latLngToUTM(latLng: LatLng): UTMCoordinate {
  const zone = getUTMZone(latLng.lng);
  const utm = getUTMProjection(zone);
  const wgs84 = 'EPSG:4326';
  
  const [x, y] = proj4(wgs84, utm, [latLng.lng, latLng.lat]);
  
  return { x, y, zone };
}

/**
 * Convert UTM coordinates to lat/lng
 */
export function utmToLatLng(utmCoord: UTMCoordinate): LatLng {
  const utm = getUTMProjection(utmCoord.zone);
  const wgs84 = 'EPSG:4326';
  
  const [lng, lat] = proj4(utm, wgs84, [utmCoord.x, utmCoord.y]);
  
  return { lat, lng };
}

/**
 * Create a square polygon in UTM coordinates
 */
export function createUTMSquare(center: UTMCoordinate, sizeInMeters: number): UTMCoordinate[] {
  const halfSize = sizeInMeters / 2;
  
  return [
    { x: center.x - halfSize, y: center.y - halfSize, zone: center.zone }, // SW
    { x: center.x + halfSize, y: center.y - halfSize, zone: center.zone }, // SE
    { x: center.x + halfSize, y: center.y + halfSize, zone: center.zone }, // NE
    { x: center.x - halfSize, y: center.y + halfSize, zone: center.zone }, // NW
    { x: center.x - halfSize, y: center.y - halfSize, zone: center.zone }  // Close polygon
  ];
}

/**
 * Convert UTM polygon to GeoJSON coordinates format
 */
export function utmPolygonToGeoJSON(utmCoords: UTMCoordinate[]): number[][][] {
  const latLngCoords = utmCoords.map(coord => {
    const latLng = utmToLatLng(coord);
    return [latLng.lng, latLng.lat]; // GeoJSON format: [lng, lat]
  });
  
  return [latLngCoords];
}

/**
 * Calculate bounding box for a set of coordinates
 */
export function calculateBoundingBox(coords: LatLng[]): BoundingBox {
  const lats = coords.map(c => c.lat);
  const lngs = coords.map(c => c.lng);
  
  return {
    southwest: {
      lat: Math.min(...lats),
      lng: Math.min(...lngs)
    },
    northeast: {
      lat: Math.max(...lats),
      lng: Math.max(...lngs)
    }
  };
}

/**
 * Calculate precise square bounds from center point and size in meters
 * Uses UTM projection to ensure true square dimensions
 */
export function calculateSquareBounds(center: LatLng, sizeInMeters: number): {
  north: number;
  south: number;
  east: number;
  west: number;
} {
  // Convert center to UTM coordinates
  const utmCenter = latLngToUTM(center);
  
  // Create a square in UTM coordinates (true square in meters)
  const utmSquare = createUTMSquare(utmCenter, sizeInMeters);
  
  // Convert back to lat/lng coordinates
  const latLngSquare = utmSquare.map(utmCoord => utmToLatLng(utmCoord));
  
  // Calculate the bounding box
  const bbox = calculateBoundingBox(latLngSquare);
  
  return {
    north: bbox.northeast.lat,
    south: bbox.southwest.lat,
    east: bbox.northeast.lng,
    west: bbox.southwest.lng
  };
}
import type { LatLng, UTMCoordinate } from './coordinateUtils';
import { latLngToUTM, utmToLatLng, createUTMSquare, utmPolygonToGeoJSON } from './coordinateUtils';

export interface GridConfig {
  center: LatLng;
  scale: number; // Multiplier for 1024m base unit (1 = 1024m, 2 = 2048m, etc.)
  gridSize: number; // Number of grid cells per side (e.g., 3x3, 5x5)
}

export interface GridCell {
  id: string;
  center: LatLng;
  coordinates: number[][][]; // GeoJSON polygon coordinates
  bounds: {
    utmBounds: {
      minX: number;
      maxX: number;
      minY: number;
      maxY: number;
    };
  };
}

export interface GridData {
  mainSquare: {
    coordinates: number[][][];
    sizeInMeters: number;
  };
  gridCells: GridCell[];
  gridLines: {
    horizontal: number[][];
    vertical: number[][];
  };
}

const BASE_UNIT = 1024; // Base unit in meters

/**
 * Calculate the total size in meters for a given scale
 */
export function getScaledSize(scale: number): number {
  return BASE_UNIT * scale;
}

/**
 * Generate grid data for a given configuration
 */
export function generateGrid(config: GridConfig): GridData {
  const totalSize = getScaledSize(config.scale);
  const cellSize = totalSize / config.gridSize;
  
  // Convert center to UTM for calculations
  const centerUTM = latLngToUTM(config.center);
  
  // Create main square
  const mainSquareUTM = createUTMSquare(centerUTM, totalSize);
  const mainSquareCoords = utmPolygonToGeoJSON(mainSquareUTM);
  
  // Generate grid cells
  const gridCells: GridCell[] = [];
  const halfSize = totalSize / 2;
  const halfCellSize = cellSize / 2;
  
  for (let row = 0; row < config.gridSize; row++) {
    for (let col = 0; col < config.gridSize; col++) {
      // Calculate cell center in UTM coordinates
      const cellCenterX = centerUTM.x - halfSize + (col * cellSize) + halfCellSize;
      const cellCenterY = centerUTM.y + halfSize - (row * cellSize) - halfCellSize;
      
      const cellCenterUTM: UTMCoordinate = {
        x: cellCenterX,
        y: cellCenterY,
        zone: centerUTM.zone
      };
      
      // Create cell polygon
      const cellPolygonUTM = createUTMSquare(cellCenterUTM, cellSize);
      const cellCoords = utmPolygonToGeoJSON(cellPolygonUTM);
      
      // Convert center back to lat/lng
      const cellCenterLatLng = utmToLatLng(cellCenterUTM);
      
      gridCells.push({
        id: `cell-${row}-${col}`,
        center: cellCenterLatLng,
        coordinates: cellCoords,
        bounds: {
          utmBounds: {
            minX: cellCenterX - halfCellSize,
            maxX: cellCenterX + halfCellSize,
            minY: cellCenterY - halfCellSize,
            maxY: cellCenterY + halfCellSize
          }
        }
      });
    }
  }
  
  // Generate grid lines
  const gridLines = generateGridLines(centerUTM, totalSize, config.gridSize);
  
  return {
    mainSquare: {
      coordinates: mainSquareCoords,
      sizeInMeters: totalSize
    },
    gridCells,
    gridLines
  };
}

/**
 * Generate grid lines for the grid
 */
function generateGridLines(centerUTM: UTMCoordinate, totalSize: number, gridSize: number): {
  horizontal: number[][];
  vertical: number[][];
} {
  const halfSize = totalSize / 2;
  const cellSize = totalSize / gridSize;
  
  const horizontal: number[][] = [];
  const vertical: number[][] = [];
  
  // Generate horizontal lines
  for (let i = 0; i <= gridSize; i++) {
    const y = centerUTM.y + halfSize - (i * cellSize);
    const startPoint = utmToLatLng({ x: centerUTM.x - halfSize, y, zone: centerUTM.zone });
    const endPoint = utmToLatLng({ x: centerUTM.x + halfSize, y, zone: centerUTM.zone });
    
    horizontal.push([
      [startPoint.lng, startPoint.lat],
      [endPoint.lng, endPoint.lat]
    ]);
  }
  
  // Generate vertical lines
  for (let i = 0; i <= gridSize; i++) {
    const x = centerUTM.x - halfSize + (i * cellSize);
    const startPoint = utmToLatLng({ x, y: centerUTM.y - halfSize, zone: centerUTM.zone });
    const endPoint = utmToLatLng({ x, y: centerUTM.y + halfSize, zone: centerUTM.zone });
    
    vertical.push([
      [startPoint.lng, startPoint.lat],
      [endPoint.lng, endPoint.lat]
    ]);
  }
  
  return { horizontal, vertical };
}

/**
 * Generate handle positions for drag interaction
 */
export function generateHandles(center: LatLng, scale: number): Array<{
  id: string;
  position: LatLng;
  color: string;
  radius: number;
}> {
  const totalSize = getScaledSize(scale);
  const centerUTM = latLngToUTM(center);
  const handleOffset = (totalSize / 2) + 40; // Slightly outside the main square
  
  const handlePositions = [
    { id: 'center', x: centerUTM.x, y: centerUTM.y, color: '#ff0000', radius: 12 },
    { id: 'nw', x: centerUTM.x - handleOffset, y: centerUTM.y + handleOffset, color: '#00ff00', radius: 8 },
    { id: 'ne', x: centerUTM.x + handleOffset, y: centerUTM.y + handleOffset, color: '#00ff00', radius: 8 },
    { id: 'sw', x: centerUTM.x - handleOffset, y: centerUTM.y - handleOffset, color: '#00ff00', radius: 8 },
    { id: 'se', x: centerUTM.x + handleOffset, y: centerUTM.y - handleOffset, color: '#00ff00', radius: 8 }
  ];
  
  return handlePositions.map(handle => {
    const position = utmToLatLng({ x: handle.x, y: handle.y, zone: centerUTM.zone });
    return {
      id: handle.id,
      position,
      color: handle.color,
      radius: handle.radius
    };
  });
}

/**
 * Get available scale options
 */
export function getScaleOptions(): Array<{ value: number; label: string; sizeMeters: number }> {
  return [
    { value: 1, label: '1x (1024m)', sizeMeters: 1024 },
    { value: 2, label: '2x (2048m)', sizeMeters: 2048 },
    { value: 3, label: '3x (3072m)', sizeMeters: 3072 },
    { value: 4, label: '4x (4096m)', sizeMeters: 4096 },
    { value: 5, label: '5x (5120m)', sizeMeters: 5120 },
    { value: 8, label: '8x (8192m)', sizeMeters: 8192 },
    { value: 9.765625, label: '10km (exactly)', sizeMeters: 10000 },
    { value: 10, label: '10x (10240m)', sizeMeters: 10240 }
  ];
}
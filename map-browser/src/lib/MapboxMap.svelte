<script lang="ts">
  import { onMount } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import { defaultCenter } from './stores';
  
  import type { LatLng } from './coordinateUtils';
  import { generateGrid, generateHandles, type GridConfig, type GridData } from './gridUtils';
  import GridControls from './GridControls.svelte';
  import { gridCenter, gridScale, gridSize } from './stores';

  export let accessToken: string;
  export let style: string = 'mapbox://styles/mapbox/streets-v12';
  export let center: [number, number] = [defaultCenter.lng, defaultCenter.lat];
  export let zoom: number = 11;

  let mapContainer: HTMLDivElement;
  let map: mapboxgl.Map;
  
  // Grid state
  let gridData: GridData;

  // Reactive statements to automatically update grid when scale or size changes
  $: if (map && gridData && ($gridScale || $gridSize)) {
    updateGrid();
  }
  
  // Dragging state
  let isDragging = false;
  let dragStart: { x: number; y: number } | null = null;
  let dragUpdateFrame: number | null = null;

  onMount(() => {
    mapboxgl.accessToken = accessToken;

    map = new mapboxgl.Map({
      container: mapContainer,
      style: style,
      center: center,
      zoom: zoom
    });

    // Add navigation control (zoom buttons)
    map.addControl(new mapboxgl.NavigationControl());

    // Add fullscreen control
    map.addControl(new mapboxgl.FullscreenControl());

    // Wait for map to load before adding the grid
    map.on('load', () => {
      updateGrid();
    });

    // Clean up on component destroy
    return () => {
      if (dragUpdateFrame) {
        cancelAnimationFrame(dragUpdateFrame);
      }
      map?.remove();
    };
  });

  function updateGrid() {
    const config: GridConfig = {
      center: $gridCenter,
      scale: $gridScale,
      gridSize: $gridSize
    };
    
    gridData = generateGrid(config);
    renderGrid();
    addInteractionHandlers();
  }

  function updateGridPositions() {
    if (!gridData) return;
    
    // Regenerate grid data with new center position
    const config: GridConfig = {
      center: $gridCenter,
      scale: $gridScale,
      gridSize: $gridSize
    };
    
    gridData = generateGrid(config);
    
    // During drag, only update essential elements for real-time feedback
    updateEssentialElements();
  }

  function updateEssentialElements() {
    if (!gridData) return;
    
    // Update main square (most important visual feedback)
    const mainSquareSource = map.getSource('main-square') as mapboxgl.GeoJSONSource;
    if (mainSquareSource) {
      mainSquareSource.setData({
        'type': 'Feature',
        'properties': {},
        'geometry': {
          'type': 'Polygon',
          'coordinates': gridData.mainSquare.coordinates
        }
      });
    }

    // Update handles (essential for interaction)
    const handles = generateHandles($gridCenter, $gridScale);
    handles.forEach(handle => {
      const source = map.getSource(`handle-${handle.id}`) as mapboxgl.GeoJSONSource;
      if (source) {
        source.setData({
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'type': 'Point',
            'coordinates': [handle.position.lng, handle.position.lat]
          }
        });
      }
    });
  }

  function renderGrid() {
    if (!gridData) return;
    
    // Render main square
    renderMainSquare();
    
    // Render grid cells
    renderGridCells();
    
    // Render grid lines
    renderGridLines();
    
    // Render handles
    renderHandles();
  }

  function renderMainSquare() {
    const sourceId = 'main-square';
    const fillLayerId = 'main-square-fill';
    const lineLayerId = 'main-square-outline';

    if (map.getSource(sourceId)) {
      (map.getSource(sourceId) as mapboxgl.GeoJSONSource).setData({
        'type': 'Feature',
        'properties': {},
        'geometry': {
          'type': 'Polygon',
          'coordinates': gridData.mainSquare.coordinates
        }
      });
    } else {
      map.addSource(sourceId, {
        'type': 'geojson',
        'data': {
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'type': 'Polygon',
            'coordinates': gridData.mainSquare.coordinates
          }
        }
      });

      map.addLayer({
        'id': fillLayerId,
        'type': 'fill',
        'source': sourceId,
        'paint': {
          'fill-color': '#ff0000',
          'fill-opacity': 0.05
        }
      });

      map.addLayer({
        'id': lineLayerId,
        'type': 'line',
        'source': sourceId,
        'paint': {
          'line-color': '#ff0000',
          'line-width': 3,
          'line-opacity': 0.8
        }
      });
    }
  }

  function renderGridCells() {
    const sourceId = 'grid-cells';
    const layerId = 'grid-cells-layer';

    const featureCollection = {
      'type': 'FeatureCollection' as const,
      'features': gridData.gridCells.map(cell => ({
        'type': 'Feature' as const,
        'properties': { id: cell.id },
        'geometry': {
          'type': 'Polygon' as const,
          'coordinates': cell.coordinates
        }
      }))
    };

    if (map.getSource(sourceId)) {
      (map.getSource(sourceId) as mapboxgl.GeoJSONSource).setData(featureCollection);
    } else {
      map.addSource(sourceId, {
        'type': 'geojson',
        'data': featureCollection
      });

      map.addLayer({
        'id': layerId,
        'type': 'line',
        'source': sourceId,
        'paint': {
          'line-color': '#0066ff',
          'line-width': 1,
          'line-opacity': 0.6
        }
      });
    }
  }

  function renderGridLines() {
    renderGridLineSet('horizontal', gridData.gridLines.horizontal);
    renderGridLineSet('vertical', gridData.gridLines.vertical);
  }

  function renderGridLineSet(type: 'horizontal' | 'vertical', lines: number[][]) {
    const sourceId = `grid-lines-${type}`;
    const layerId = `grid-lines-${type}-layer`;
    const prefix = type === 'horizontal' ? 'h' : 'v';
    
    const features = {
      'type': 'FeatureCollection' as const,
      'features': lines.map((line, index) => ({
        'type': 'Feature' as const,
        'properties': { id: `${prefix}-${index}` },
        'geometry': {
          'type': 'LineString' as const,
          'coordinates': line
        }
      }))
    } as unknown as GeoJSON.GeoJSON;

    if (map.getSource(sourceId)) {
      (map.getSource(sourceId) as mapboxgl.GeoJSONSource).setData(features);
    } else {
      map.addSource(sourceId, {
        'type': 'geojson',
        'data': features
      });

      map.addLayer({
        'id': layerId,
        'type': 'line',
        'source': sourceId,
        'paint': {
          'line-color': '#888888',
          'line-width': 0.5,
          'line-opacity': 0.4
        }
      });
    }
  }

  function renderHandles() {
    const handles = generateHandles($gridCenter, $gridScale);
    
    handles.forEach(handle => {
      const sourceId = `handle-${handle.id}`;
      const layerId = `handle-${handle.id}-layer`;

      if (map.getSource(sourceId)) {
        (map.getSource(sourceId) as mapboxgl.GeoJSONSource).setData({
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'type': 'Point',
            'coordinates': [handle.position.lng, handle.position.lat]
          }
        });
      } else {
        map.addSource(sourceId, {
          'type': 'geojson',
          'data': {
            'type': 'Feature',
            'properties': {},
            'geometry': {
              'type': 'Point',
              'coordinates': [handle.position.lng, handle.position.lat]
            }
          }
        });

        map.addLayer({
          'id': layerId,
          'type': 'circle',
          'source': sourceId,
          'paint': {
            'circle-radius': handle.radius,
            'circle-color': handle.color,
            'circle-stroke-color': '#ffffff',
            'circle-stroke-width': 2,
            'circle-opacity': 0.8
          }
        });
      }
    });
  }

  function addInteractionHandlers() {
    // Make handles draggable
    const handleIds = ['handle-center-layer', 'handle-nw-layer', 'handle-ne-layer', 'handle-sw-layer', 'handle-se-layer'];
    
    handleIds.forEach(layerId => {
      // Change cursor on hover
      map.on('mouseenter', layerId, () => {
        map.getCanvas().style.cursor = 'grab';
      });

      map.on('mouseleave', layerId, () => {
        map.getCanvas().style.cursor = '';
      });

      // Handle drag start
      map.on('mousedown', layerId, (e) => {
        e.preventDefault();
        isDragging = true;
        dragStart = { x: e.point.x, y: e.point.y };
        map.getCanvas().style.cursor = 'grabbing';
        
        // Disable map drag while dragging handle
        map.dragPan.disable();
      });
    });

    // Handle drag move
    map.on('mousemove', (e) => {
      if (!isDragging || !dragStart) return;

      const deltaX = e.point.x - dragStart.x;
      const deltaY = e.point.y - dragStart.y;

      // Convert pixel movement to lat/lng
      const startLatLng = map.unproject([dragStart.x, dragStart.y]);
      const endLatLng = map.unproject([dragStart.x + deltaX, dragStart.y + deltaY]);

      const deltaLng = endLatLng.lng - startLatLng.lng;
      const deltaLat = endLatLng.lat - startLatLng.lat;

      // Update center position in store
      gridCenter.update(center => ({
        lng: center.lng + deltaLng,
        lat: center.lat + deltaLat
      }));

      // Update drag start for next frame
      dragStart = { x: e.point.x, y: e.point.y };

      // Real-time updates using requestAnimationFrame
      if (dragUpdateFrame) {
        cancelAnimationFrame(dragUpdateFrame);
      }
      
      dragUpdateFrame = requestAnimationFrame(() => {
        updateGridPositions();
        dragUpdateFrame = null;
      });
    });

    // Handle drag end
    map.on('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        dragStart = null;
        map.getCanvas().style.cursor = '';
        map.dragPan.enable();
        
        // Clear any pending frame update
        if (dragUpdateFrame) {
          cancelAnimationFrame(dragUpdateFrame);
          dragUpdateFrame = null;
        }
        
        // Do a full grid update when dragging ends (includes all grid lines and cells)
        updateGrid();
      }
    });
  }
</script>

<div bind:this={mapContainer} class="map-container"></div>

<GridControls />

<style>
  .map-container {
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
  }

  :global(.mapboxgl-canvas) {
    cursor: grab;
  }

  :global(.mapboxgl-canvas:active) {
    cursor: grabbing;
  }
</style>
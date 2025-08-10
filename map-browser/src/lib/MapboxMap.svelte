<script lang="ts">
  import { onMount } from 'svelte';
  import mapboxgl from 'mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import { defaultCenter } from './stores';
  import RoadwaysLayer from './roadways/RoadwaysLayer.svelte';
  import StreetOutlinesLayer from './roadways/StreetOutlinesLayer.svelte';
  
  import { generateGrid, generateHandles, type GridConfig, type GridData } from './gridUtils';
  import GridControls from './GridControls.svelte';
  import FeatureInfoPanel from './FeatureInfoPanel.svelte';
  import { gridCenter, gridScale, gridSize, availableLayers, layerVisibility, projectLabelsVisible, elevationQueryMode, elevationMarkers, terrainMode, selectedTrees, type LayerConfig, type ElevationMarker, type SelectedTree } from './stores';

  export let accessToken: string;
  export let style = 'mapbox://styles/mapbox/streets-v12';
  export let center: [number, number] = [defaultCenter.lng, defaultCenter.lat];
  export let zoom = 11;

  let mapContainer: HTMLDivElement;
  let map: mapboxgl.Map;
  let roadwaysLayer: RoadwaysLayer;
  let streetOutlinesLayer: StreetOutlinesLayer;
  
  // Expose roadwaysLayer globally for debugging
  $: if (roadwaysLayer && typeof window !== 'undefined') {
    (window as any).roadwaysLayer = roadwaysLayer;
  }
  
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

  // Feature info panel state
  let featureInfoVisible = false;
  let clickedFeatures: any[] = [];
  let clickPosition: { x: number; y: number } | null = null;

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

    // Wait for map to load before adding the layers and grid
    map.on('load', () => {
      // Add Mapbox terrain for elevation queries
      map.addSource('mapbox-dem', {
        'type': 'raster-dem',
        'url': 'mapbox://mapbox.mapbox-terrain-dem-v1',
        'tileSize': 512,
        'maxzoom': 14
      });
      
      // Enable terrain on the map (optional - for 3D visualization)
      // map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 1.5 });
      
      // Load GeoJSON layers first (background layers)
      loadAllLayers().then(() => {
        // Then load grid layers on top (interactive foreground layers)
        // This ensures the interactive grid is always above data layers
        updateGrid();
        
        // Add click handler for feature information
        addFeatureClickHandler();
      });
    });

    // Subscribe to layer visibility changes
    layerVisibility.subscribe(($layerVisibility) => {
      if (map?.isStyleLoaded()) {
        updateLayerVisibility($layerVisibility);
      }
    });

    // Subscribe to project labels visibility changes
    projectLabelsVisible.subscribe(($projectLabelsVisible) => {
      if (map?.isStyleLoaded()) {
        updateProjectLabelsVisibility($projectLabelsVisible);
      }
    });

    // Subscribe to terrain mode changes
    terrainMode.subscribe(($terrainMode) => {
      if (map?.isStyleLoaded()) {
        if ($terrainMode) {
          map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 1.0 });
        } else {
          map.setTerrain(null);
        }
      }
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

  async function loadAllLayers() {
    for (const layer of availableLayers) {
      await loadLayer(layer);
    }
  }

  async function loadLayer(layerConfig: LayerConfig) {
    try {
      // Skip layers with empty URLs (handled by custom components)
      if (!layerConfig.url || layerConfig.url.trim() === '') {
        console.log(`Skipping layer '${layerConfig.name}' - no URL provided (handled by custom component)`);
        return;
      }
      
      const response = await fetch(layerConfig.url);
      const geojsonData = await response.json();
      
      const sourceId = layerConfig.id;
      
      // Add the source
      map.addSource(sourceId, {
        'type': 'geojson',
        'data': geojsonData
      });
      
      // Check layer type based on geometry
      const isPointLayer = layerConfig.id === 'public-trees';
      const isLineLayer = layerConfig.id === 'roadways';
      const isStreetOutlines = layerConfig.id === 'street-outlines';
      
      if (isLineLayer) {
        // Skip roadways here - handled by advanced RoadwaysLayer component
        console.log(`Skipping roadways layer - handled by advanced component`);
        return;
      } else if (isStreetOutlines) {
        // Skip street outlines here - handled by StreetOutlinesLayer component
        console.log(`Skipping street outlines layer - handled by advanced component`);
        return;
      } else if (isPointLayer) {
        // For point layers (trees), use circle layers
        const circleLayerId = `${layerConfig.id}-circle`;
        const selectedCircleLayerId = `${layerConfig.id}-selected`;
        
        // Add main circle layer
        map.addLayer({
          'id': circleLayerId,
          'type': 'circle',
          'source': sourceId,
          'paint': {
            'circle-radius': [
              'case',
              ['boolean', ['feature-state', 'selected'], false],
              8, // Selected size
              5  // Normal size
            ],
            'circle-color': [
              'case',
              ['boolean', ['feature-state', 'selected'], false],
              '#FF6B35', // Selected color (orange)
              layerConfig.fillColor // Normal color (green)
            ],
            'circle-stroke-color': layerConfig.lineColor,
            'circle-stroke-width': [
              'case',
              ['boolean', ['feature-state', 'selected'], false],
              3, // Selected stroke width
              1  // Normal stroke width
            ],
            'circle-opacity': layerConfig.fillOpacity
          },
          'layout': {
            'visibility': layerConfig.visible ? 'visible' : 'none'
          }
        });
        
      } else {
        // For polygon layers, use the existing fill/line approach
        const fillLayerId = `${layerConfig.id}-fill`;
        const lineLayerId = `${layerConfig.id}-line`;
        
        // Add fill layer
        map.addLayer({
          'id': fillLayerId,
          'type': 'fill',
          'source': sourceId,
          'paint': {
            'fill-color': layerConfig.fillColor,
            'fill-opacity': layerConfig.fillOpacity
          },
          'layout': {
            'visibility': layerConfig.visible ? 'visible' : 'none'
          }
        });
        
        // Add outline layer
        map.addLayer({
          'id': lineLayerId,
          'type': 'line',
          'source': sourceId,
          'paint': {
            'line-color': layerConfig.lineColor,
            'line-width': layerConfig.lineWidth,
            'line-opacity': layerConfig.lineOpacity
          },
          'layout': {
            'visibility': layerConfig.visible ? 'visible' : 'none'
          }
        });
        
        // Add text labels for Projects Footprints layer
        if (layerConfig.id === 'projects-footprints') {
          const labelLayerId = `${layerConfig.id}-labels`;
          map.addLayer({
            'id': labelLayerId,
            'type': 'symbol',
            'source': sourceId,
            'layout': {
              'text-field': ['get', 'Project'],
              'text-font': ['Open Sans Regular', 'Arial Unicode MS Regular'],
              'text-size': 10,
              'text-anchor': 'center',
              'text-offset': [0, 0],
              'visibility': 'none' // Labels start hidden by default
            },
            'paint': {
              'text-color': '#ffffff',
              'text-halo-color': 'rgba(0, 0, 0, 1.0)',
              'text-halo-width': 1,
              'text-opacity': 1.0
            }
          });
        }
      }
      
      console.log(`Layer '${layerConfig.name}' loaded successfully`);
    } catch (error) {
      console.error(`Error loading layer '${layerConfig.name}':`, error);
    }
  }

  function updateLayerVisibility(visibility: Record<string, boolean>) {
    availableLayers.forEach(layerConfig => {
      const isVisible = visibility[layerConfig.id];
      const isPointLayer = layerConfig.id === 'public-trees';
      const isLineLayer = layerConfig.id === 'roadways';
      const isStreetOutlines = layerConfig.id === 'street-outlines';
      
      if (isPointLayer) {
        // Handle point layers (trees)
        const circleLayerId = `${layerConfig.id}-circle`;
        if (map.getLayer(circleLayerId)) {
          map.setLayoutProperty(circleLayerId, 'visibility', isVisible ? 'visible' : 'none');
        }
      } else if (isLineLayer) {
        // Skip roadways visibility handling - managed by RoadwaysLayer component
        return;
      } else if (isStreetOutlines) {
        // Skip street outlines visibility handling - managed by StreetOutlinesLayer component
        return;
      } else {
        // Handle polygon layers
        const fillLayerId = `${layerConfig.id}-fill`;
        const lineLayerId = `${layerConfig.id}-line`;
        
        if (map.getLayer(fillLayerId)) {
          map.setLayoutProperty(fillLayerId, 'visibility', isVisible ? 'visible' : 'none');
        }
        if (map.getLayer(lineLayerId)) {
          map.setLayoutProperty(lineLayerId, 'visibility', isVisible ? 'visible' : 'none');
        }
      }
    });
    
    // Also update label visibility when layer visibility changes
    updateProjectLabelsVisibility($projectLabelsVisible);
  }

  function updateProjectLabelsVisibility(visible: boolean) {
    availableLayers.forEach(layerConfig => {
      // Only update labels for projects-footprints layer
      if (layerConfig.id === 'projects-footprints') {
        const labelLayerId = `${layerConfig.id}-labels`;
        const layerVisible = $layerVisibility[layerConfig.id];
        
        if (map.getLayer(labelLayerId)) {
          // Labels are only visible if both the layer and labels toggle are on
          map.setLayoutProperty(labelLayerId, 'visibility', 
            (visible && layerVisible) ? 'visible' : 'none');
        }
      }
    });
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

  function addFeatureClickHandler() {
    map.on('click', (e) => {
      // Don't show feature info if we're dragging
      if (isDragging) return;
      
      // Check if we're in elevation query mode
      if ($elevationQueryMode) {
        addElevationMarker(e.lngLat);
        return;
      }
      
      // Query all visible layers at the click point
      const features = map.queryRenderedFeatures(e.point);
      
      // Filter to only show GeoJSON data layers (not grid layers or labels)
      const dataLayerFeatures = features.filter(feature => {
        const layerId = feature.layer?.id;
        if (!layerId) return false;
        
        return (layerId.includes('projects-footprints') || 
                layerId.includes('bc-vancouver-island') ||
                layerId.includes('bc-lower-mainland') ||
                layerId.includes('public-trees') ||
                layerId.includes('roadways')) &&
               !layerId.includes('-labels'); // Exclude label layers
      });
      
      // Handle tree selection separately
      const treeFeatures = dataLayerFeatures.filter(feature => 
        feature.layer?.id?.includes('public-trees')
      );
      
      if (treeFeatures.length > 0) {
        handleTreeSelection(treeFeatures[0], e.lngLat);
        return; // Don't show feature info panel for trees
      }
      
      if (dataLayerFeatures.length > 0) {
        clickedFeatures = dataLayerFeatures;
        clickPosition = { x: e.point.x, y: e.point.y };
        featureInfoVisible = true;
      } else {
        featureInfoVisible = false;
      }
    });
    
    // Hide feature info panel when map is moved
    map.on('move', () => {
      featureInfoVisible = false;
    });
  }

  function handleTreeSelection(feature: any, lngLat: mapboxgl.LngLat) {
    const treeId = feature.properties?.tree_id;
    if (!treeId) return;
    
    const coordinates: [number, number] = [lngLat.lng, lngLat.lat];
    
    // Check if tree is already selected
    const isAlreadySelected = $selectedTrees.some(tree => tree.id === treeId);
    
    if (isAlreadySelected) {
      // Deselect the tree
      selectedTrees.update(trees => trees.filter(tree => tree.id !== treeId));
      // Remove feature state
      map.setFeatureState(
        { source: 'public-trees', id: feature.id },
        { selected: false }
      );
    } else {
      // Select the tree
      const selectedTree: SelectedTree = {
        id: treeId,
        properties: feature.properties,
        coordinates
      };
      
      selectedTrees.update(trees => [...trees, selectedTree]);
      // Set feature state
      map.setFeatureState(
        { source: 'public-trees', id: feature.id },
        { selected: true }
      );
    }
    
    console.log(`Tree ${isAlreadySelected ? 'deselected' : 'selected'}:`, feature.properties);
  }

  // Subscribe to selectedTrees changes to update feature states
  $: if (map && map.isStyleLoaded()) {
    // Clear all feature states first
    if (map.getSource('public-trees')) {
      // We need to clear all feature states when trees are cleared
      // This is a bit tricky since we can't enumerate all features easily
      // So we'll rely on the reactive statement to handle this
    }
  }

  async function addElevationMarker(lngLat: mapboxgl.LngLat) {
    const markerId = `elevation-${Date.now()}`;
    const position = { lat: lngLat.lat, lng: lngLat.lng };
    
    // Add marker with loading state
    const newMarker: ElevationMarker = {
      id: markerId,
      position,
      elevation: null,
      isLoading: true
    };
    
    elevationMarkers.update(markers => [...markers, newMarker]);
    
    // Render the marker on the map
    renderElevationMarker(newMarker);
    
    // Query elevation using Mapbox's built-in method
    try {
      // Use Mapbox GL JS queryTerrainElevation for instant elevation data
      const elevation = map.queryTerrainElevation([lngLat.lng, lngLat.lat]);
      
      if (elevation !== null && elevation !== undefined) {
        // Update marker with elevation data
        elevationMarkers.update(markers => 
          markers.map(marker => 
            marker.id === markerId 
              ? { ...marker, elevation: Math.round(elevation), isLoading: false }
              : marker
          )
        );
        
        // Update the marker display
        updateElevationMarkerDisplay(markerId, Math.round(elevation));
      } else {
        // Fallback to SRTM file query if Mapbox terrain not available
        await queryElevationFromFiles(markerId, lngLat);
      }
      
    } catch (error) {
      console.error('Error querying elevation with Mapbox:', error);
      
      // Fallback to SRTM file query
      await queryElevationFromFiles(markerId, lngLat);
    }
  }

  async function queryElevationFromFiles(markerId: string, lngLat: mapboxgl.LngLat) {
    try {
      const response = await fetch('/api/query-elevation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          lat: lngLat.lat,
          lng: lngLat.lng
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      
      // Update marker with elevation data
      elevationMarkers.update(markers => 
        markers.map(marker => 
          marker.id === markerId 
            ? { ...marker, elevation: result.elevation, isLoading: false }
            : marker
        )
      );
      
      // Update the marker display
      updateElevationMarkerDisplay(markerId, result.elevation);
      
    } catch (error) {
      console.error('Error querying elevation from files:', error);
      
      // Update marker with error state
      elevationMarkers.update(markers => 
        markers.map(marker => 
          marker.id === markerId 
            ? { ...marker, error: 'No elevation data available', isLoading: false }
            : marker
        )
      );
      
      // Update the marker display with error
      updateElevationMarkerDisplay(markerId, null, 'No data');
    }
  }

  function renderElevationMarker(marker: ElevationMarker) {
    const sourceId = `elevation-marker-${marker.id}`;
    const layerId = `elevation-marker-${marker.id}-layer`;
    const labelLayerId = `elevation-marker-${marker.id}-label`;

    // Add marker point
    map.addSource(sourceId, {
      'type': 'geojson',
      'data': {
        'type': 'Feature',
        'properties': {
          'elevation': marker.elevation,
          'isLoading': marker.isLoading,
          'error': marker.error
        },
        'geometry': {
          'type': 'Point',
          'coordinates': [marker.position.lng, marker.position.lat]
        }
      }
    });

    // Add marker circle
    map.addLayer({
      'id': layerId,
      'type': 'circle',
      'source': sourceId,
      'paint': {
        'circle-radius': 8,
        'circle-color': marker.isLoading ? '#ffc107' : (marker.error ? '#dc3545' : '#007bff'),
        'circle-stroke-color': '#ffffff',
        'circle-stroke-width': 2,
        'circle-opacity': 0.9
      }
    });

    // Add label
    map.addLayer({
      'id': labelLayerId,
      'type': 'symbol',
      'source': sourceId,
      'layout': {
        'text-field': marker.isLoading ? 'Loading...' : (marker.error ? 'Error' : `${marker.elevation?.toFixed(0)}m`),
        'text-font': ['Open Sans Semibold', 'Arial Unicode MS Bold'],
        'text-size': 12,
        'text-offset': [0, -2],
        'text-anchor': 'bottom'
      },
      'paint': {
        'text-color': '#333333',
        'text-halo-color': '#ffffff',
        'text-halo-width': 1
      }
    });
  }

  function updateElevationMarkerDisplay(markerId: string, elevation: number | null, error?: string) {
    const sourceId = `elevation-marker-${markerId}`;
    const layerId = `elevation-marker-${markerId}-layer`;
    const labelLayerId = `elevation-marker-${markerId}-label`;

    if (map.getSource(sourceId)) {
      // Update marker color
      map.setPaintProperty(layerId, 'circle-color', error ? '#dc3545' : '#28a745');
      
      // Update label text
      const labelText = error ? error : (elevation !== null ? `${elevation.toFixed(0)}m` : 'Unknown');
      map.setLayoutProperty(labelLayerId, 'text-field', labelText);
    }
  }

  // Subscribe to elevation markers changes to render/remove markers
  $: if (map && $elevationMarkers) {
    renderElevationMarkers();
  }

  function renderElevationMarkers() {
    if (!map || !map.isStyleLoaded()) return;

    // Remove existing elevation markers
    const existingSources = Object.keys(map.getStyle().sources);
    existingSources.forEach(sourceId => {
      if (sourceId.startsWith('elevation-marker-')) {
        const layerId = `${sourceId}-layer`;
        const labelLayerId = `${sourceId}-label`;
        
        if (map.getLayer(labelLayerId)) map.removeLayer(labelLayerId);
        if (map.getLayer(layerId)) map.removeLayer(layerId);
        if (map.getSource(sourceId)) map.removeSource(sourceId);
      }
    });

    // Add current markers
    $elevationMarkers.forEach(marker => {
      renderElevationMarker(marker);
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

{#if map}
  <RoadwaysLayer bind:this={roadwaysLayer} {map} />
  <StreetOutlinesLayer bind:this={streetOutlinesLayer} {map} />
{/if}

<GridControls mapboxToken={accessToken} />

<FeatureInfoPanel 
  bind:isVisible={featureInfoVisible}
  features={clickedFeatures}
  clickPosition={clickPosition}
  mapboxToken={accessToken}
/>

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
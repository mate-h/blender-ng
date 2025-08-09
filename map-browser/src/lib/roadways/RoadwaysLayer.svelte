<script lang="ts">
  import type mapboxgl from 'mapbox-gl';
  import { layerVisibility } from '../stores';
  import RoadwaysInfoPanel from './RoadwaysInfoPanel.svelte';
  
  const { map }: { map: mapboxgl.Map } = $props();
  
  let roadwaysData = $state<GeoJSON.FeatureCollection | null>(null);
  let layersAdded = $state(false);
  let lastVisibilityState = $state<boolean | undefined>(undefined);
  
  // State for the info panel
  let selectedRoad = $state<GeoJSON.Feature | null>(null);
  let infoPanelVisible = $state(false);
  
  // Derived state for roadways visibility
  const isRoadwaysVisible = $derived($layerVisibility['roadways'] ?? true);
  

  
  // Advanced styling configuration
  const roadwayStyles = {
    // Route-based styling (bicycle routes, etc.)
    route: {
      'bicycle': {
        color: '#0F7D4B',
        width: 3,
        opacity: 0.9,
        dashArray: [2, 2]
      },
      'road': {
        color: '#333333',
        width: 4,
        opacity: 0.8,
        dashArray: null
      }
    },
    // Highway classification styling
    highway: {
      'motorway': {
        color: '#E892A2',
        width: 6,
        opacity: 0.9,
        dashArray: null
      },
      'motorway_link': {
        color: '#E892A2',
        width: 4,
        opacity: 0.8,
        dashArray: null
      },
      'trunk': {
        color: '#F9B29C',
        width: 5,
        opacity: 0.9,
        dashArray: null
      },
      'primary': {
        color: '#FCD6A4',
        width: 4,
        opacity: 0.8,
        dashArray: null
      },
      'secondary': {
        color: '#F7FABF',
        width: 3,
        opacity: 0.8,
        dashArray: null
      },
      'tertiary': {
        color: '#C8E6C9',
        width: 2.5,
        opacity: 0.8,
        dashArray: null
      },
      'residential': {
        color: '#BBDEFB',
        width: 2,
        opacity: 0.7,
        dashArray: null
      },
      'service': {
        color: '#E1BEE7',
        width: 1.5,
        opacity: 0.6,
        dashArray: null
      }
    },
    // Default fallback
    default: {
      color: '#999999',
      width: 2,
      opacity: 0.6,
      dashArray: null
    }
  };

  // Effect to load roadways data when component mounts
  $effect(() => {

    if (!map || roadwaysData) return;
    
    console.log('Loading roadways data...');
    loadRoadwaysData();
  });

  // Effect to add layers when map and data are ready
  $effect(() => {

    if (!map || !roadwaysData || layersAdded) return;
    
    console.log('Map and data ready, checking if style is loaded...');
    
    const addLayers = () => {
      console.log('addLayers called - roadwaysData:', !!roadwaysData, 'layersAdded:', layersAdded);
      if (roadwaysData && !layersAdded) {
        console.log('Adding roadways layers...');
        try {
          addRoadwaysLayers();
          layersAdded = true;
          console.log('Roadways layers added successfully');
        } catch (error) {
          console.error('Error adding roadways layers:', error);
        }
      }
    };

    // Try multiple approaches to ensure layers get added
    console.log('Setting up layer addition triggers...');
    
    // Immediate attempt
    setTimeout(() => {
      console.log('Timeout attempt to add layers');
      addLayers();
    }, 100);
    
    // Listen for styledata event
    const onStyleLoad = () => {
      console.log('styledata event fired, attempting to add layers');
      addLayers();
    };
    
    // Listen for load event
    const onLoad = () => {
      console.log('load event fired, attempting to add layers');
      addLayers();
    };
    
    // Listen for idle event (when map is fully loaded)
    const onIdle = () => {
      console.log('idle event fired, attempting to add layers');
      addLayers();
      map.off('idle', onIdle); // Only listen once
    };
    
    map.on('styledata', onStyleLoad);
    map.on('load', onLoad);
    map.on('idle', onIdle);
    
    // Cleanup function
    const cleanup = () => {
      map.off('styledata', onStyleLoad);
      map.off('load', onLoad);
      map.off('idle', onIdle);
    };
    
    // Clean up after 5 seconds
    setTimeout(cleanup, 5000);
  });

  // Effect to handle visibility changes
  $effect(() => {
    if (!map || !layersAdded) return;
    
    // Prevent infinite loops by checking if visibility actually changed
    if (lastVisibilityState === isRoadwaysVisible) return;
    
    console.log('Updating roadways visibility:', isRoadwaysVisible, 'from:', lastVisibilityState);
    lastVisibilityState = isRoadwaysVisible;
    updateLayerVisibility(isRoadwaysVisible);
  });

  async function loadRoadwaysData() {
    try {
      const response = await fetch('/downloads/ways.geojson');
      const data = await response.json();
      roadwaysData = data;
      console.log('Roadways data loaded:', roadwaysData?.features?.length, 'features');
    } catch (error) {
      console.error('Error loading roadways data:', error);
    }
  }

  function addRoadwaysLayers() {
    if (!roadwaysData || !map) {
      console.log('addRoadwaysLayers - missing data or map:', { roadwaysData: !!roadwaysData, map: !!map });
      return;
    }

    // Check if layers already exist
    if (map.getSource('roadways-advanced')) {
      console.log('Roadways layers already exist, skipping...');
      return;
    }

    console.log('Adding roadways layers to map...', 'Style loaded:', map.loaded());

    // Add the roadways source
    try {
      map.addSource('roadways-advanced', {
        type: 'geojson',
        data: roadwaysData,
        generateId: true  // Enable automatic ID generation for features
      });
      console.log('Added roadways-advanced source with', roadwaysData.features?.length, 'features');
    } catch (error) {
      console.error('Error adding roadways source:', error);
      return;
    }

    // Create color expression for route-based styling
    const routeColorExpression = [
      'case',
      ['==', ['get', 'route'], 'bicycle'], roadwayStyles.route.bicycle.color,
      ['==', ['get', 'route'], 'road'], roadwayStyles.route.road.color,
      roadwayStyles.default.color
    ];

    // Create width expression for route-based styling
    const routeWidthExpression = [
      'case',
      ['==', ['get', 'route'], 'bicycle'], roadwayStyles.route.bicycle.width,
      ['==', ['get', 'route'], 'road'], roadwayStyles.route.road.width,
      roadwayStyles.default.width
    ];

    // Create highway-based color expression
    const highwayColorExpression = [
      'case',
      ['==', ['get', 'highway'], 'motorway'], roadwayStyles.highway.motorway.color,
      ['==', ['get', 'highway'], 'motorway_link'], roadwayStyles.highway.motorway_link.color,
      ['==', ['get', 'highway'], 'trunk'], roadwayStyles.highway.trunk.color,
      ['==', ['get', 'highway'], 'primary'], roadwayStyles.highway.primary.color,
      ['==', ['get', 'highway'], 'secondary'], roadwayStyles.highway.secondary.color,
      ['==', ['get', 'highway'], 'tertiary'], roadwayStyles.highway.tertiary.color,
      ['==', ['get', 'highway'], 'residential'], roadwayStyles.highway.residential.color,
      ['==', ['get', 'highway'], 'service'], roadwayStyles.highway.service.color,
      roadwayStyles.default.color
    ];

    // Create highway-based width expression
    const highwayWidthExpression = [
      'case',
      ['==', ['get', 'highway'], 'motorway'], roadwayStyles.highway.motorway.width,
      ['==', ['get', 'highway'], 'motorway_link'], roadwayStyles.highway.motorway_link.width,
      ['==', ['get', 'highway'], 'trunk'], roadwayStyles.highway.trunk.width,
      ['==', ['get', 'highway'], 'primary'], roadwayStyles.highway.primary.width,
      ['==', ['get', 'highway'], 'secondary'], roadwayStyles.highway.secondary.width,
      ['==', ['get', 'highway'], 'tertiary'], roadwayStyles.highway.tertiary.width,
      ['==', ['get', 'highway'], 'residential'], roadwayStyles.highway.residential.width,
      ['==', ['get', 'highway'], 'service'], roadwayStyles.highway.service.width,
      roadwayStyles.default.width
    ];

    // Final color expression - prioritize highway classification over route
    const finalColorExpression: mapboxgl.DataDrivenPropertyValueSpecification<mapboxgl.ColorSpecification> = [
      'case',
      ['has', 'highway'], highwayColorExpression,
      ['has', 'route'], routeColorExpression,
      roadwayStyles.default.color
    ];

    // Final width expression - prioritize highway classification over route
    const finalWidthExpression = [
      'case',
      ['has', 'highway'], highwayWidthExpression,
      ['has', 'route'], routeWidthExpression,
      roadwayStyles.default.width
    ];

    // Add main roadways layer with advanced styling
    try {
      map.addLayer({
        id: 'roadways-advanced-main',
        type: 'line',
        source: 'roadways-advanced',
        paint: {
          'line-color': finalColorExpression,
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            8, ['*', finalWidthExpression, 0.5],
            12, finalWidthExpression,
            16, ['*', finalWidthExpression, 1.5]
          ],
          'line-opacity': 0.8
        },
        layout: {
          'line-cap': 'round',
          'line-join': 'round',
          visibility: isRoadwaysVisible ? 'visible' : 'none'
        }
      });
      console.log('Added roadways-advanced-main layer');
    } catch (error) {
      console.error('Error adding roadways-advanced-main layer:', error);
    }

    // Add bicycle route overlay with dashed lines
    map.addLayer({
      id: 'roadways-advanced-bicycle',
      type: 'line',
      source: 'roadways-advanced',
      filter: ['==', ['get', 'route'], 'bicycle'],
      paint: {
        'line-color': roadwayStyles.route.bicycle.color,
        'line-width': [
          'interpolate',
          ['linear'],
          ['zoom'],
          8, 1,
          12, 2,
          16, 3
        ],
        'line-opacity': 0.9,
        'line-dasharray': [2, 2]
      },
      layout: {
        'line-cap': 'round',
        'line-join': 'round',
        visibility: isRoadwaysVisible ? 'visible' : 'none'
      }
    });

    // Add hover effect layer
    map.addLayer({
      id: 'roadways-advanced-hover',
      type: 'line',
      source: 'roadways-advanced',
      paint: {
        'line-color': '#ffff00',
        'line-width': [
          'interpolate',
          ['linear'],
          ['zoom'],
          8, 2,
          12, 4,
          16, 6
        ],
        'line-opacity': [
          'case',
          ['boolean', ['feature-state', 'hover'], false],
          0.8,
          0
        ]
      },
      layout: {
        'line-cap': 'round',
        'line-join': 'round',
        visibility: isRoadwaysVisible ? 'visible' : 'none'
      }
    });

    // Add click handlers for interactivity
    addInteractivity();

    console.log('Advanced roadways layers added successfully');
  }

  function addInteractivity() {
    if (!map) return;

    // Change cursor on hover
    map.on('mouseenter', 'roadways-advanced-main', () => {
      map.getCanvas().style.cursor = 'pointer';
    });

    map.on('mouseleave', 'roadways-advanced-main', () => {
      map.getCanvas().style.cursor = '';
      // Clear hover state
      map.removeFeatureState({ source: 'roadways-advanced' });
    });

    // Handle hover state
    map.on('mousemove', 'roadways-advanced-main', (e) => {
      if (e.features && e.features.length > 0) {
        const feature = e.features[0];
        
        // Clear previous hover state
        map.removeFeatureState({ source: 'roadways-advanced' });
        
        // Set new hover state only if feature has an ID
        if (feature.id !== undefined) {
          map.setFeatureState(
            { source: 'roadways-advanced', id: feature.id },
            { hover: true }
          );
        }
      }
    });

    // Handle click events
    map.on('click', 'roadways-advanced-main', (e) => {
      if (e.features && e.features.length > 0) {
        const feature = e.features[0];
        console.log('Roadway clicked:', feature.properties);
        
        // Show the info panel with road details
        selectedRoad = feature;
        infoPanelVisible = true;
      }
    });
    
    // Add general map click handler to close info panel when clicking elsewhere
    map.on('click', (e) => {
      // Check if click was on a roadway layer
      const features = map.queryRenderedFeatures(e.point, { 
        layers: ['roadways-advanced-main'] 
      });
      
      // If no roadway features at click point, close info panel
      if (features.length === 0) {
        infoPanelVisible = false;
        selectedRoad = null;
      }
    });
  }

 

  function updateLayerVisibility(visible: boolean) {
    if (!map) return;
    
    try {
      const layerIds = ['roadways-advanced-main', 'roadways-advanced-bicycle', 'roadways-advanced-hover'];
      layerIds.forEach(layerId => {
        if (map.getLayer(layerId)) {
          map.setLayoutProperty(layerId, 'visibility', visible ? 'visible' : 'none');
          console.log(`Set ${layerId} visibility to:`, visible ? 'visible' : 'none');
        }
      });
    } catch (error) {
      console.error('Error updating layer visibility:', error);  
    }
  }

  // Manual trigger for debugging - can be called from browser console
  export function forceAddLayers() {
    console.log('forceAddLayers called - map:', !!map, 'roadwaysData:', !!roadwaysData, 'layersAdded:', layersAdded);
    if (map && roadwaysData) {
      layersAdded = false; // Reset to allow re-adding
      addRoadwaysLayers();
      layersAdded = true;
    }
  }

  // Clean up on component destroy
  export function destroy() {
    if (!map) return;
    
    try {
      const layerIds = ['roadways-advanced-main', 'roadways-advanced-bicycle', 'roadways-advanced-hover'];
      layerIds.forEach(layerId => {
        if (map.getLayer(layerId)) {
          map.removeLayer(layerId);
        }
      });
      
      if (map.getSource('roadways-advanced')) {
        map.removeSource('roadways-advanced');
      }
      
      // Reset state
      layersAdded = false;
      lastVisibilityState = undefined;
    } catch (error) {
      console.error('Error during cleanup:', error);
    }
  }
</script>

<RoadwaysInfoPanel 
  bind:selectedRoad={selectedRoad}
  bind:isVisible={infoPanelVisible}
/>

<script lang="ts">
  import type mapboxgl from 'mapbox-gl';
  import { layerVisibility } from '../stores';
  
  const { map }: { map: mapboxgl.Map } = $props();
  
  let layersAdded = $state(false);
  let dataLoaded = $state(false);
  
  // Combined data from all sources
  let combinedData = $state<GeoJSON.FeatureCollection | null>(null);
  
  // Derived state for street outlines visibility
  const isVisible = $derived($layerVisibility['street-outlines'] ?? true);
  
  // Data sources configuration
  const dataSources = [
    {
      name: 'roadways',
      url: '/downloads/ways.geojson',
      type: 'roadway'
    },
    {
      name: 'intersection-markings',
      url: '/downloads/Intersection markings.geojson',
      type: 'intersection-marking'
    },
    {
      name: 'intersection-polygons', 
      url: '/downloads/Intersection polygons.geojson',
      type: 'intersection-polygon'
    },
    {
      name: 'lane-polygons',
      url: '/downloads/Lane polygons.geojson', 
      type: 'lane-polygon'
    }
  ];

  // Styling configuration for different feature types
  const styleConfig = {
    'roadway': {
      color: '#333333',
      width: 2,
      opacity: 0.8,
      type: 'line'
    },
    'intersection-marking': {
      color: '#FFFFFF',
      opacity: 0.9,
      type: 'fill'
    },
    'intersection-polygon': {
      color: '#666666',
      opacity: 0.7,
      type: 'fill'
    },
    'lane-polygon': {
      // Color by lane type
      colors: {
        'Driving': '#444444',
        'Biking': '#0F7D4B',
        'Sidewalk': '#CCCCCC',
        'Parking': '#8B4513',
        'Bus': '#BE4A4C',
        'SharedLeftTurn': '#555555',
        'Construction': '#FF6D00',
        'LightRail': '#844204',
        'Footway': '#DDDDE8',
        'SharedUse': '#DED68A'
      },
      defaultColor: '#999999',
      opacity: 0.6,
      type: 'fill'
    }
  };

  // Effect to load data when component mounts
  $effect(() => {
    if (!map || dataLoaded) return;
    
    console.log('Loading street outlines data...');
    loadAllData();
  });

  // Effect to add layers when map and data are ready
  $effect(() => {
    if (!map || !combinedData || layersAdded) return;
    
    console.log('Adding street outlines layers...');
    
    // Try multiple approaches to ensure layers get added
    const addLayers = () => {
      if (combinedData && !layersAdded) {
        try {
          addStreetOutlineLayers();
          layersAdded = true;
          console.log('Street outline layers added successfully');
        } catch (error) {
          console.error('Error adding street outline layers:', error);
        }
      }
    };

    // Immediate attempt
    setTimeout(addLayers, 100);
    
    // Listen for various map events
    const onStyleLoad = () => addLayers();
    const onLoad = () => addLayers();
    const onIdle = () => {
      addLayers();
      map.off('idle', onIdle);
    };
    
    map.on('styledata', onStyleLoad);
    map.on('load', onLoad);
    map.on('idle', onIdle);
    
    // Cleanup after 5 seconds
    setTimeout(() => {
      map.off('styledata', onStyleLoad);
      map.off('load', onLoad);
      map.off('idle', onIdle);
    }, 5000);
  });

  // Effect to handle visibility changes
  $effect(() => {
    if (!map || !layersAdded) return;
    
    console.log('Updating street outlines visibility:', isVisible);
    updateLayerVisibility(isVisible);
  });

  async function loadAllData() {
    try {
      console.log('Loading data from', dataSources.length, 'sources...');
      
      const dataPromises = dataSources.map(async (source) => {
        console.log(`Loading ${source.name}...`);
        const response = await fetch(source.url);
        const data = await response.json();
        
        // Add source type to each feature's properties
        data.features = data.features.map((feature: GeoJSON.Feature) => ({
          ...feature,
          properties: {
            ...feature.properties,
            _sourceType: source.type,
            _sourceName: source.name
          }
        }));
        
        console.log(`Loaded ${source.name}: ${data.features?.length} features`);
        return data;
      });
      
      const allData = await Promise.all(dataPromises);
      
      // Combine all features into one FeatureCollection
      const allFeatures = allData.flatMap(data => data.features);
      
      combinedData = {
        type: 'FeatureCollection',
        features: allFeatures
      };
      
      console.log('Combined street outlines data:', allFeatures.length, 'total features');
      dataLoaded = true;
      
    } catch (error) {
      console.error('Error loading street outlines data:', error);
    }
  }

  function addStreetOutlineLayers() {
    if (!combinedData || !map) return;

    // Check if layers already exist
    if (map.getSource('street-outlines')) {
      console.log('Street outline layers already exist, skipping...');
      return;
    }

    console.log('Adding street outlines layers to map...');

    // Add the combined source
    try {
      map.addSource('street-outlines', {
        type: 'geojson',
        data: combinedData,
        generateId: true
      });
      console.log('Added street-outlines source with', combinedData.features?.length, 'features');
    } catch (error) {
      console.error('Error adding street outlines source:', error);
      return;
    }

    // Add lane polygons layer (fill)
    try {
      map.addLayer({
        id: 'street-outlines-lanes',
        type: 'fill',
        source: 'street-outlines',
        filter: ['==', ['get', '_sourceType'], 'lane-polygon'],
        paint: {
          'fill-color': [
            'case',
            ['has', 'type'],
            [
              'case',
              ['==', ['get', 'type'], 'Driving'], styleConfig['lane-polygon'].colors.Driving,
              ['==', ['get', 'type'], 'Biking'], styleConfig['lane-polygon'].colors.Biking,
              ['==', ['get', 'type'], 'Sidewalk'], styleConfig['lane-polygon'].colors.Sidewalk,
              ['==', ['get', 'type'], 'Parking'], styleConfig['lane-polygon'].colors.Parking,
              ['==', ['get', 'type'], 'Bus'], styleConfig['lane-polygon'].colors.Bus,
              ['==', ['get', 'type'], 'SharedLeftTurn'], styleConfig['lane-polygon'].colors.SharedLeftTurn,
              ['==', ['get', 'type'], 'Construction'], styleConfig['lane-polygon'].colors.Construction,
              ['==', ['get', 'type'], 'LightRail'], styleConfig['lane-polygon'].colors.LightRail,
              ['==', ['get', 'type'], 'Footway'], styleConfig['lane-polygon'].colors.Footway,
              ['==', ['get', 'type'], 'SharedUse'], styleConfig['lane-polygon'].colors.SharedUse,
              styleConfig['lane-polygon'].defaultColor
            ],
            styleConfig['lane-polygon'].defaultColor
          ],
          'fill-opacity': styleConfig['lane-polygon'].opacity
        },
        layout: {
          visibility: isVisible ? 'visible' : 'none'
        }
      });
      console.log('Added lane polygons layer');
    } catch (error) {
      console.error('Error adding lane polygons layer:', error);
    }

    // Add intersection polygons layer (fill)
    try {
      map.addLayer({
        id: 'street-outlines-intersections',
        type: 'fill',
        source: 'street-outlines',
        filter: ['==', ['get', '_sourceType'], 'intersection-polygon'],
        paint: {
          'fill-color': styleConfig['intersection-polygon'].color,
          'fill-opacity': styleConfig['intersection-polygon'].opacity
        },
        layout: {
          visibility: isVisible ? 'visible' : 'none'
        }
      });
      console.log('Added intersection polygons layer');
    } catch (error) {
      console.error('Error adding intersection polygons layer:', error);
    }

    // Add intersection markings layer (fill)
    try {
      map.addLayer({
        id: 'street-outlines-markings',
        type: 'fill',
        source: 'street-outlines',
        filter: ['==', ['get', '_sourceType'], 'intersection-marking'],
        paint: {
          'fill-color': styleConfig['intersection-marking'].color,
          'fill-opacity': styleConfig['intersection-marking'].opacity
        },
        layout: {
          visibility: isVisible ? 'visible' : 'none'
        }
      });
      console.log('Added intersection markings layer');
    } catch (error) {
      console.error('Error adding intersection markings layer:', error);
    }

    // Add roadways layer (line) - on top
    try {
      map.addLayer({
        id: 'street-outlines-roadways',
        type: 'line',
        source: 'street-outlines',
        filter: ['==', ['get', '_sourceType'], 'roadway'],
        paint: {
          'line-color': styleConfig.roadway.color,
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            8, styleConfig.roadway.width * 0.5,
            12, styleConfig.roadway.width,
            16, styleConfig.roadway.width * 1.5
          ],
          'line-opacity': styleConfig.roadway.opacity
        },
        layout: {
          'line-cap': 'round',
          'line-join': 'round',
          visibility: isVisible ? 'visible' : 'none'
        }
      });
      console.log('Added roadways layer');
    } catch (error) {
      console.error('Error adding roadways layer:', error);
    }

    // Add hover effect layer
    try {
      map.addLayer({
        id: 'street-outlines-hover',
        type: 'line',
        source: 'street-outlines',
        paint: {
          'line-color': '#ffff00',
          'line-width': [
            'interpolate',
            ['linear'],
            ['zoom'],
            8, 3,
            12, 5,
            16, 7
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
          visibility: isVisible ? 'visible' : 'none'
        }
      });
      console.log('Added hover layer');
    } catch (error) {
      console.error('Error adding hover layer:', error);
    }

    // Add interactivity
    addInteractivity();
  }

  function addInteractivity() {
    if (!map) return;

    const interactiveLayers = ['street-outlines-lanes', 'street-outlines-intersections', 'street-outlines-roadways'];

    interactiveLayers.forEach(layerId => {
      // Change cursor on hover
      map.on('mouseenter', layerId, () => {
        map.getCanvas().style.cursor = 'pointer';
      });

      map.on('mouseleave', layerId, () => {
        map.getCanvas().style.cursor = '';
        map.removeFeatureState({ source: 'street-outlines' });
      });

      // Handle hover state
      map.on('mousemove', layerId, (e) => {
        if (e.features && e.features.length > 0) {
          const feature = e.features[0];
          
          // Clear previous hover state
          map.removeFeatureState({ source: 'street-outlines' });
          
          // Set new hover state only if feature has an ID
          if (feature.id !== undefined) {
            map.setFeatureState(
              { source: 'street-outlines', id: feature.id },
              { hover: true }
            );
          }
        }
      });

      // Handle click events
      map.on('click', layerId, (e) => {
        if (e.features && e.features.length > 0) {
          const feature = e.features[0];
          console.log('Street outline feature clicked:', {
            type: feature.properties?._sourceType,
            properties: feature.properties
          });
        }
      });
    });
  }

  function updateLayerVisibility(visible: boolean) {
    if (!map) return;
    
    try {
      const layerIds = [
        'street-outlines-lanes',
        'street-outlines-intersections', 
        'street-outlines-markings',
        'street-outlines-roadways',
        'street-outlines-hover'
      ];
      
      layerIds.forEach(layerId => {
        if (map.getLayer(layerId)) {
          map.setLayoutProperty(layerId, 'visibility', visible ? 'visible' : 'none');
        }
      });
    } catch (error) {
      console.error('Error updating street outlines visibility:', error);
    }
  }

  // Clean up on component destroy
  export function destroy() {
    if (!map) return;
    
    try {
      const layerIds = [
        'street-outlines-lanes',
        'street-outlines-intersections',
        'street-outlines-markings', 
        'street-outlines-roadways',
        'street-outlines-hover'
      ];
      
      layerIds.forEach(layerId => {
        if (map.getLayer(layerId)) {
          map.removeLayer(layerId);
        }
      });
      
      if (map.getSource('street-outlines')) {
        map.removeSource('street-outlines');
      }
      
      // Reset state
      layersAdded = false;
      dataLoaded = false;
    } catch (error) {
      console.error('Error during street outlines cleanup:', error);
    }
  }
</script>

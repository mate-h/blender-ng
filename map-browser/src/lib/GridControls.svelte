<script lang="ts">
  import { getScaleOptions } from './gridUtils';
  import { gridCenter, gridScale, gridSize, availableLayers, layerVisibility, projectLabelsVisible, elevationQueryMode, elevationMarkers, terrainMode } from './stores';
  import { calculateSquareBounds } from './coordinateUtils';
  
  const scaleOptions = getScaleOptions();
  const gridSizeOptions = [
    { value: 1, label: '1x1' },
    { value: 2, label: '2x2' },
    { value: 3, label: '3x3' },
    { value: 4, label: '4x4' },
    { value: 5, label: '5x5' },
    { value: 8, label: '8x8' },
    { value: 10, label: '10x10' }
  ];

  const resolutionOptions = [
    { value: 'SRTMGL1', label: 'SRTM 30m', description: 'Global coverage, 30m resolution' },
    { value: 'SRTMGL3', label: 'SRTM 90m', description: 'Global coverage, 90m resolution' },
    { value: 'COP30', label: 'Copernicus 30m', description: 'High quality, limited coverage' },
    { value: 'COP90', label: 'Copernicus 90m', description: 'High quality, global coverage' },
    { value: 'NASADEM', label: 'NASADEM 30m', description: 'Improved SRTM, 30m resolution' },
    { value: 'CA_HDREM', label: 'Canada HDREM', description: 'High-resolution DEM for Canada' }
  ];

  const satelliteResolutionOptions = [
    { value: 2, label: '2 pixels/meter', description: 'Maximum resolution - uses tiling for large areas' },
    { value: 1, label: '1 pixel/meter', description: 'High resolution - uses tiling for large areas' },
    { value: 0.5, label: '0.5 pixel/meter', description: 'Medium resolution - good balance' },
    { value: 0.25, label: '0.25 pixel/meter', description: 'Standard resolution - faster download' },
    { value: 0.1, label: '0.1 pixel/meter', description: 'Low resolution - very fast download' }
  ];

  // Download state
  let isDownloading = false;
  let downloadStatus = '';
  let downloadError = '';
  let selectedResolution = 'SRTMGL1'; // Default to SRTM 30m
  
  // Satellite download state
  let isSatelliteDownloading = false;
  let satelliteDownloadStatus = '';
  let satelliteDownloadError = '';
  let selectedSatelliteResolution = 1; // Default to 1 pixel per meter
  
  // Mapbox token from the app (we'll need to pass this from the parent)
  export let mapboxToken: string;

  // Layer management
  function toggleLayerVisibility(layerId: string) {
    layerVisibility.update(visibility => ({
      ...visibility,
      [layerId]: !visibility[layerId]
    }));
  }

  // Elevation marker management
  function clearElevationMarkers() {
    elevationMarkers.set([]);
  }

  // Format coordinates for display
  function formatCoordinate(value: number, decimals: number = 4): string {
    return value.toFixed(decimals);
  }

  function formatDMS(degrees: number, isLongitude: boolean = false): string {
    const direction = isLongitude 
      ? (degrees >= 0 ? 'E' : 'W')
      : (degrees >= 0 ? 'N' : 'S');
    
    const abs = Math.abs(degrees);
    const deg = Math.floor(abs);
    const min = Math.floor((abs - deg) * 60);
    const sec = ((abs - deg) * 60 - min) * 60;
    
    return `${deg}°${min}'${sec.toFixed(2)}"${direction}`;
  }

  // Calculate bounds from current grid settings using proper UTM projection
  function calculateBounds() {
    const totalSizeMeters = $gridScale * 1024; // Total area in meters
    
    // Use precise UTM-based calculation for square bounds
    return calculateSquareBounds(
      { lat: $gridCenter.lat, lng: $gridCenter.lng },
      totalSizeMeters
    );
  }

  // Download terrain data
  async function downloadTerrain() {
    if (isDownloading) return;
    
    isDownloading = true;
    downloadStatus = 'Preparing download...';
    downloadError = '';
    
    try {
      const bounds = calculateBounds();
      
      downloadStatus = 'Requesting terrain data...';
      
      const response = await fetch('/api/download-terrain', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          bounds,
          center: {
            lat: $gridCenter.lat,
            lng: $gridCenter.lng
          },
          scale: $gridScale,
          gridSize: $gridSize,
          resolution: selectedResolution
        })
      });
      
      if (!response.ok) {
        let errorMessage = `Server error (${response.status})`;
        try {
          const errorResult = await response.json();
          if (errorResult.error) {
            errorMessage = errorResult.error;
          }
        } catch (e) {
          // If we can't parse the error response, use the status text
          errorMessage = `${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }
      
      const result = await response.json();
      
      if (result.success) {
        downloadStatus = `Downloaded: ${result.filename} (${result.fileSize})`;
        setTimeout(() => {
          downloadStatus = '';
        }, 5000);
      } else {
        throw new Error(result.error || 'Download failed');
      }
      
    } catch (error) {
      console.error('Download error:', error);
      
      // Try to get more detailed error from the response
      let errorMessage = 'Download failed';
      
      if (error instanceof Error) {
        if (error.message.includes('Failed to fetch')) {
          errorMessage = 'Network error: Unable to connect to server';
        } else if (error.message.includes('HTTP')) {
          errorMessage = error.message; // This will include the detailed HTTP error
        } else {
          errorMessage = error.message;
        }
      }
      
      downloadError = `Error: ${errorMessage}`;
      setTimeout(() => {
        downloadError = '';
      }, 15000); // Show error for 15 seconds instead of 10
    } finally {
      isDownloading = false;
    }
  }

  // Download satellite imagery
  async function downloadSatellite() {
    if (isSatelliteDownloading) return;
    
    isSatelliteDownloading = true;
    satelliteDownloadStatus = 'Preparing satellite download...';
    satelliteDownloadError = '';
    
    try {
      const bounds = calculateBounds();
      
      satelliteDownloadStatus = 'Requesting satellite imagery...';
      
      const response = await fetch('/api/download-satellite', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          bounds,
          center: {
            lat: $gridCenter.lat,
            lng: $gridCenter.lng
          },
          scale: $gridScale,
          gridSize: $gridSize,
          resolution: selectedSatelliteResolution,
          mapboxToken
        })
      });
      
      if (!response.ok) {
        let errorMessage = `Server error (${response.status})`;
        try {
          const errorResult = await response.json();
          if (errorResult.error) {
            errorMessage = errorResult.error;
          }
        } catch (e) {
          errorMessage = `${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }
      
      const result = await response.json();
      
      if (result.success) {
        satelliteDownloadStatus = `Downloaded: ${result.filename} (${result.fileSize}) - ${result.resolution}`;
        setTimeout(() => {
          satelliteDownloadStatus = '';
        }, 5000);
      } else {
        throw new Error(result.error || 'Satellite download failed');
      }
      
    } catch (error) {
      console.error('Satellite download error:', error);
      
      let errorMessage = 'Satellite download failed';
      
      if (error instanceof Error) {
        if (error.message.includes('Failed to fetch')) {
          errorMessage = 'Network error: Unable to connect to server';
        } else if (error.message.includes('HTTP') || error.message.includes('Mapbox')) {
          errorMessage = error.message;
        } else {
          errorMessage = error.message;
        }
      }
      
      satelliteDownloadError = `Error: ${errorMessage}`;
      setTimeout(() => {
        satelliteDownloadError = '';
      }, 15000);
    } finally {
      isSatelliteDownloading = false;
    }
  }
</script>

<div class="grid-controls">
  <div class="control-group">
    <label for="scale-select">Scale:</label>
    <select id="scale-select" bind:value={$gridScale}>
      {#each scaleOptions as option}
        <option value={option.value}>{option.label}</option>
      {/each}
    </select>
  </div>
  
  <div class="control-group">
    <label for="grid-size-select">Grid:</label>
    <select id="grid-size-select" bind:value={$gridSize}>
      {#each gridSizeOptions as option}
        <option value={option.value}>{option.label}</option>
      {/each}
    </select>
  </div>
  
  <div class="control-group">
    <label for="resolution-select">Resolution:</label>
    <select id="resolution-select" bind:value={selectedResolution}>
      {#each resolutionOptions as option}
        <option value={option.value} title={option.description}>{option.label}</option>
      {/each}
    </select>
  </div>
  
  <div class="resolution-info">
    <span class="resolution-description">
      {resolutionOptions.find(r => r.value === selectedResolution)?.description || ''}
    </span>
  </div>
  
  <div class="layers-section">
    <div class="layers-title">Map Layers:</div>
    {#each availableLayers as layer}
      <div class="layer-control">
        <label class="layer-checkbox">
          <input 
            type="checkbox" 
            checked={$layerVisibility[layer.id]} 
            on:change={() => toggleLayerVisibility(layer.id)}
          />
          <span class="layer-name">{layer.name}</span>
          <span 
            class="layer-color-indicator" 
            style="background-color: {layer.fillColor};"
          ></span>
        </label>
      </div>
    {/each}
    
    <div class="labels-control">
      <label class="layer-checkbox">
        <input 
          type="checkbox" 
          bind:checked={$projectLabelsVisible}
        />
        <span class="layer-name">Project Labels</span>
        <span class="labels-icon">🏷️</span>
      </label>
    </div>
  </div>
  
  <div class="elevation-section">
    <div class="elevation-title">Elevation Tools:</div>
    <div class="elevation-controls">
      <label class="layer-checkbox">
        <input 
          type="checkbox" 
          bind:checked={$elevationQueryMode}
        />
        <span class="layer-name">Click for Elevation</span>
        <span class="elevation-icon">📏</span>
      </label>
      
      <label class="layer-checkbox">
        <input 
          type="checkbox" 
          bind:checked={$terrainMode}
        />
        <span class="layer-name">3D Terrain View</span>
        <span class="elevation-icon">🏔️</span>
      </label>
      
      {#if $elevationMarkers.length > 0}
        <button 
          class="clear-markers-btn"
          on:click={clearElevationMarkers}
        >
          Clear Markers ({$elevationMarkers.length})
        </button>
      {/if}
    </div>
  </div>
  
  <div class="location-info">
    <div class="location-title">Current Location:</div>
    <div class="coordinate-group">
      <span class="coordinate-label">Decimal:</span>
      <span class="coordinate-value">
        {formatCoordinate($gridCenter.lat)}, {formatCoordinate($gridCenter.lng)}
      </span>
    </div>
    <div class="coordinate-group">
      <span class="coordinate-label">DMS:</span>
      <span class="coordinate-value">
        {formatDMS($gridCenter.lat)} {formatDMS($gridCenter.lng, true)}
      </span>
    </div>
  </div>
  
  <div class="info">
    <span class="info-text">
      Total: {$gridScale * 1024}m × {$gridScale * 1024}m
    </span>
    <span class="info-text">
      Cell: {Math.round(($gridScale * 1024) / $gridSize)}m × {Math.round(($gridScale * 1024) / $gridSize)}m
    </span>
  </div>

  <div class="download-section">
    <div class="download-title">Download Terrain Data:</div>
    <button 
      class="download-btn" 
      class:downloading={isDownloading}
      disabled={isDownloading}
      on:click={downloadTerrain}
    >
      {#if isDownloading}
        <span class="spinner"></span>
        Downloading...
      {:else}
        Download {resolutionOptions.find(r => r.value === selectedResolution)?.label || 'Terrain'}
      {/if}
    </button>
    
    {#if downloadStatus}
      <div class="download-status success">{downloadStatus}</div>
    {/if}
    
    {#if downloadError}
      <div class="download-status error">{downloadError}</div>
    {/if}
  </div>

  <div class="satellite-section">
    <div class="satellite-title">Download Satellite Imagery:</div>
    
    <div class="control-group">
      <label for="satellite-resolution-select">Resolution:</label>
      <select id="satellite-resolution-select" bind:value={selectedSatelliteResolution}>
        {#each satelliteResolutionOptions as option}
          <option value={option.value} title={option.description}>{option.label}</option>
        {/each}
      </select>
    </div>
    
    <div class="resolution-info">
      <span class="resolution-description">
        {satelliteResolutionOptions.find(r => r.value === selectedSatelliteResolution)?.description || ''}
      </span>
    </div>
    
    <button 
      class="download-btn satellite-btn" 
      class:downloading={isSatelliteDownloading}
      disabled={isSatelliteDownloading}
      on:click={downloadSatellite}
    >
      {#if isSatelliteDownloading}
        <span class="spinner"></span>
        Downloading...
      {:else}
        🛰️ Download Satellite Image
      {/if}
    </button>
    
    {#if satelliteDownloadStatus}
      <div class="download-status success">{satelliteDownloadStatus}</div>
    {/if}
    
    {#if satelliteDownloadError}
      <div class="download-status error">{satelliteDownloadError}</div>
    {/if}
  </div>
</div>

<style>
  .grid-controls {
    position: absolute;
    top: 20px;
    left: 20px;
    background: rgba(255, 255, 255, 0.95);
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    width: 280px;
    max-width: 280px;
  }
  
  .control-group {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
    gap: 10px;
  }
  
  .control-group:last-of-type {
    margin-bottom: 15px;
  }
  
  label {
    font-weight: 600;
    color: #333;
    min-width: 60px;
    font-size: 14px;
  }
  
  select {
    flex: 1;
    padding: 6px 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
    font-size: 14px;
    cursor: pointer;
    color: black;
  }
  
  select:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }
  
  .location-info {
    border-top: 1px solid #eee;
    border-bottom: 1px solid #eee;
    padding: 12px 0;
    margin: 12px 0;
  }

  .location-title {
    font-weight: 600;
    font-size: 13px;
    color: #333;
    margin-bottom: 8px;
  }

  .coordinate-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
  }

  .coordinate-label {
    font-size: 11px;
    color: #666;
    font-weight: 500;
    min-width: 50px;
  }

  .coordinate-value {
    font-size: 11px;
    color: #333;
    font-family: 'Monaco', 'Consolas', monospace;
    text-align: right;
    flex: 1;
  }

  .info {
    padding-top: 8px;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .info-text {
    font-size: 12px;
    color: #666;
    font-weight: 500;
  }

  .download-section {
    border-top: 1px solid #eee;
    padding-top: 12px;
    margin-top: 12px;
  }

  .download-btn {
    width: 100%;
    padding: 10px 16px;
    background: linear-gradient(135deg, #28a745, #20c997);
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    transition: all 0.3s ease;
  }

  .download-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #218838, #1ea085);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
  }

  .download-btn:active:not(:disabled) {
    transform: translateY(0);
  }

  .download-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }

  .download-btn.downloading {
    background: linear-gradient(135deg, #6c757d, #495057);
  }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .download-status {
    margin-top: 8px;
    padding: 8px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    word-wrap: break-word;
    overflow-wrap: break-word;
    line-height: 1.3;
  }

  .download-status.success {
    background: rgba(40, 167, 69, 0.1);
    color: #28a745;
    border: 1px solid rgba(40, 167, 69, 0.2);
  }

  .download-status.error {
    background: rgba(220, 53, 69, 0.1);
    color: #dc3545;
    border: 1px solid rgba(220, 53, 69, 0.2);
    font-size: 11px; /* Smaller font for potentially longer error messages */
    max-height: 60px;
    overflow-y: auto;
  }

  .resolution-info {
    margin-top: -8px;
    margin-bottom: 10px;
  }

  .resolution-description {
    font-size: 11px;
    color: #666;
    font-style: italic;
  }

  .layers-section {
    border-top: 1px solid #eee;
    border-bottom: 1px solid #eee;
    padding: 12px 0;
    margin: 12px 0;
  }

  .layers-title {
    font-weight: 600;
    font-size: 13px;
    color: #333;
    margin-bottom: 8px;
  }

  .layer-control {
    margin-bottom: 6px;
  }

  .layer-checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 12px;
    color: #333;
    width: 100%;
  }

  .layer-checkbox input[type="checkbox"] {
    width: 14px;
    height: 14px;
    cursor: pointer;
    accent-color: #007bff;
  }

  .layer-name {
    flex: 1;
    font-weight: 500;
  }

  .layer-color-indicator {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    flex-shrink: 0;
  }

  .layer-checkbox:hover .layer-name {
    color: #007bff;
  }

  .labels-control {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #eee;
  }

  .labels-icon {
    font-size: 14px;
    opacity: 0.8;
  }

  .elevation-section {
    border-top: 1px solid #eee;
    border-bottom: 1px solid #eee;
    padding: 12px 0;
    margin: 12px 0;
  }

  .elevation-title {
    font-weight: 600;
    font-size: 13px;
    color: #333;
    margin-bottom: 8px;
  }

  .elevation-controls {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .elevation-icon {
    font-size: 14px;
    opacity: 0.8;
  }

  .clear-markers-btn {
    padding: 6px 12px;
    background: linear-gradient(135deg, #dc3545, #c82333);
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .clear-markers-btn:hover {
    background: linear-gradient(135deg, #c82333, #a71e2a);
    transform: translateY(-1px);
  }

  .clear-markers-btn:active {
    transform: translateY(0);
  }

  .satellite-section {
    border-top: 1px solid #eee;
    padding-top: 12px;
    margin-top: 12px;
  }

  .satellite-title, .download-title {
    font-weight: 600;
    font-size: 13px;
    color: #333;
    margin-bottom: 12px;
  }

  .satellite-btn {
    background: linear-gradient(135deg, #007bff, #0056b3);
  }

  .satellite-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #0056b3, #004085);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
  }

  .satellite-btn.downloading {
    background: linear-gradient(135deg, #6c757d, #495057);
  }
</style>
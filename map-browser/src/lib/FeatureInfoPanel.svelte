<script lang="ts">
  export let features: any[] = [];
  export let clickPosition: { x: number; y: number } | null = null;
  export let isVisible: boolean = false;
  export let mapboxToken: string = '';

  let panelElement: HTMLDivElement;
  
  // Satellite download state
  let satelliteDownloadStates: Record<string, {
    isDownloading: boolean;
    status: string;
    error: string;
  }> = {};

  function closePanel() {
    isVisible = false;
  }

  function getOptimalPosition() {
    if (!clickPosition || !panelElement) return { left: 0, top: 0 };
    
    const rect = panelElement.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    let left = clickPosition.x + 10; // Offset from cursor
    let top = clickPosition.y + 10;
    
    // Adjust if panel would go off-screen horizontally
    if (left + rect.width > viewportWidth) {
      left = clickPosition.x - rect.width - 10;
    }
    
    // Adjust if panel would go off-screen vertically
    if (top + rect.height > viewportHeight) {
      top = clickPosition.y - rect.height - 10;
    }
    
    // Ensure minimum margins
    left = Math.max(16, left);
    top = Math.max(16, top);
    
    return { left, top };
  }

  $: position = { left: 16, top: 16 };

  function formatDownloadLinks(properties: any) {
    const links = [];
    
    // DTM (Digital Terrain Model) links
    if (properties.Ftp_dtm) {
      links.push({ 
        name: 'DTM (Digital Terrain Model)', 
        url: properties.Ftp_dtm,
        description: '1m resolution elevation data'
      });
    }
    
    if (properties.Ftp_dtmHS) {
      links.push({ 
        name: 'DTM Hillshade', 
        url: properties.Ftp_dtmHS,
        description: 'Shaded relief visualization'
      });
    }
    
    if (properties.Ftp_dtmAsp) {
      links.push({ 
        name: 'DTM Aspect', 
        url: properties.Ftp_dtmAsp,
        description: 'Slope direction data'
      });
    }
    
    if (properties.Ftp_dtmSlo) {
      links.push({ 
        name: 'DTM Slope', 
        url: properties.Ftp_dtmSlo,
        description: 'Slope steepness data'
      });
    }

    // DSM (Digital Surface Model) links
    if (properties.Ftp_dsm) {
      links.push({ 
        name: 'DSM (Digital Surface Model)', 
        url: properties.Ftp_dsm,
        description: '1m resolution surface data'
      });
    }
    
    if (properties.Ftp_dsmHS) {
      links.push({ 
        name: 'DSM Hillshade', 
        url: properties.Ftp_dsmHS,
        description: 'Surface hillshade visualization'
      });
    }

    return links;
  }

  function formatTileName(tileName: string) {
    // Convert technical tile names to more readable format
    return tileName.replace(/_/g, ' ').toUpperCase();
  }

  function getLayerColor(layerId: string) {
    // Match colors from stores.ts
    const layerColors: Record<string, string> = {
      'projects-footprints': '#00ff00',
      'bc-vancouver-island-utm9': '#ff6600', 
      'bc-vancouver-island-utm10': '#0066ff',
      'bc-lower-mainland-2016': '#9966ff'
    };
    return layerColors[layerId] || '#666666';
  }

  // Download satellite imagery to match DTM
  async function downloadMatchingSatellite(dtmUrl: string, featureId: string) {
    if (!mapboxToken) {
      alert('Mapbox token is required for satellite imagery download');
      return;
    }

    const stateKey = `${featureId}-${dtmUrl}`;
    satelliteDownloadStates[stateKey] = {
      isDownloading: true,
      status: 'Preparing satellite download to match DTM...',
      error: ''
    };
    
    try {
      const response = await fetch('/api/download-satellite-dtm-matched', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          dtmFilePath: dtmUrl,
          mapboxToken: mapboxToken,
          targetResolution: 1 // 1 pixel per meter default
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
        let statusMessage = `✅ Complete processing finished!\n`;
        statusMessage += `🎮 BeamNG ready: ${result.filename} (${result.fileSize})\n`;
        if (result.additionalFiles) {
          statusMessage += `📦 Additional files generated:\n`;
          statusMessage += `   • ${result.additionalFiles.aligned} (10K TIFF)\n`;
          statusMessage += `   • ${result.additionalFiles.alignedJpeg} (10K JPEG)\n`;
          statusMessage += `   • ${result.additionalFiles.crop8k} (8K JPEG)\n`;
        }
        
        satelliteDownloadStates[stateKey] = {
          isDownloading: false,
          status: statusMessage,
          error: ''
        };
        setTimeout(() => {
          if (satelliteDownloadStates[stateKey]) {
            satelliteDownloadStates[stateKey].status = '';
          }
        }, 12000); // Show longer for more detailed info
      } else {
        throw new Error(result.error || 'DTM-matched satellite download failed');
      }
      
    } catch (error) {
      console.error('DTM-matched satellite download error:', error);
      
      let errorMessage = 'DTM-matched satellite download failed';
      
      if (error instanceof Error) {
        if (error.message.includes('Failed to fetch')) {
          errorMessage = 'Network error: Unable to connect to server';
        } else if (error.message.includes('HTTP') || error.message.includes('Mapbox')) {
          errorMessage = error.message;
        } else {
          errorMessage = error.message;
        }
      }
      
      satelliteDownloadStates[stateKey] = {
        isDownloading: false,
        status: '',
        error: `Error: ${errorMessage}`
      };
      setTimeout(() => {
        if (satelliteDownloadStates[stateKey]) {
          satelliteDownloadStates[stateKey].error = '';
        }
      }, 15000);
    }
  }

  // Check if a URL is a DTM file
  function isDTMFile(url: string): boolean {
    return url.includes('dtm') && !url.includes('dtmHS') && !url.includes('dtmAsp') && !url.includes('dtmSlo');
  }
</script>

{#if isVisible && features.length > 0}
  <div 
    bind:this={panelElement}
    class="feature-info-panel"
    style="left: {position.left}px; top: {position.top}px;"
  >
    <div class="panel-header">
      <h3>Feature Information</h3>
      <button class="close-btn" on:click={closePanel}>&times;</button>
    </div>
    
    <div class="panel-content">
      {#each features as feature, index}
        <div class="feature-item" style="border-left-color: {getLayerColor(feature.layer.id)};">
          <div class="feature-header">
            <div class="layer-name">{feature.layer.id}</div>
            {#if feature.properties.Tile_name}
              <div class="tile-name">{formatTileName(feature.properties.Tile_name)}</div>
            {/if}
          </div>
          
          <div class="feature-details">
            {#if feature.properties.Provider}
              <div class="detail-row">
                <span class="label">Provider:</span>
                <span class="value">{feature.properties.Provider}</span>
              </div>
            {/if}
            
            {#if feature.properties.Project}
              <div class="detail-row">
                <span class="label">Project:</span>
                <span class="value">{feature.properties.Project}</span>
              </div>
            {/if}
            
            {#if feature.properties.Year_min && feature.properties.Year_max}
              <div class="detail-row">
                <span class="label">Year:</span>
                <span class="value">
                  {feature.properties.Year_min === feature.properties.Year_max 
                    ? feature.properties.Year_min 
                    : `${feature.properties.Year_min}-${feature.properties.Year_max}`}
                </span>
              </div>
            {/if}
            
            {#if feature.properties.Coord_Sys}
              <div class="detail-row">
                <span class="label">Coordinate System:</span>
                <span class="value">{feature.properties.Coord_Sys}</span>
              </div>
            {/if}
          </div>

          {#if formatDownloadLinks(feature.properties).length > 0}
            <div class="downloads-section">
              <h4>Download GeoTIFF Files:</h4>
              <div class="download-links">
                {#each formatDownloadLinks(feature.properties) as link}
                  <div class="download-item">
                    <a href={link.url} target="_blank" rel="noopener noreferrer" class="download-link">
                      <span class="download-name">{link.name}</span>
                      <span class="download-icon">⬇</span>
                    </a>
                    <span class="download-description">{link.description}</span>
                    
                    <!-- Add satellite download button for DTM files -->
                    {#if isDTMFile(link.url) && mapboxToken}
                      {@const stateKey = `${feature.properties.Tile_name || index}-${link.url}`}
                      {@const downloadState = satelliteDownloadStates[stateKey] || { isDownloading: false, status: '', error: '' }}
                      
                      <div class="satellite-download-section">
                        <button 
                          class="satellite-download-btn" 
                          class:downloading={downloadState.isDownloading}
                          disabled={downloadState.isDownloading}
                          on:click={() => downloadMatchingSatellite(link.url, feature.properties.Tile_name || String(index))}
                        >
                          {#if downloadState.isDownloading}
                            <span class="spinner"></span>
                            Downloading Satellite...
                          {:else}
                            🛰️ Download Matching Satellite
                          {/if}
                        </button>
                        
                        {#if downloadState.status}
                          <div class="satellite-status success">{downloadState.status}</div>
                        {/if}
                        
                        {#if downloadState.error}
                          <div class="satellite-status error">{downloadState.error}</div>
                        {/if}
                      </div>
                    {/if}
                  </div>
                {/each}
              </div>
            </div>
          {/if}
          
          {#if feature.properties.Preview}
            <div class="preview-section">
              <h4>Preview:</h4>
              <a href={feature.properties.Preview} target="_blank" rel="noopener noreferrer" class="preview-link">
                View Thumbnail
              </a>
            </div>
          {/if}
        </div>
        
        {#if index < features.length - 1}
          <div class="feature-separator"></div>
        {/if}
      {/each}
    </div>
  </div>
{/if}

<style>
  .feature-info-panel {
    position: absolute;
    background: white;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 2000;
    max-width: 400px;
    max-height: 500px;
    overflow-y: auto;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid #eee;
    background: #f8f9fa;
    border-radius: 8px 8px 0 0;
  }

  .panel-header h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
    color: #333;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    color: #666;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
  }

  .close-btn:hover {
    background: #eee;
    color: #333;
  }

  .panel-content {
    padding: 16px;
  }

  .feature-item {
    border-left: 4px solid #666;
    padding-left: 12px;
    margin-bottom: 16px;
  }

  .feature-header {
    margin-bottom: 12px;
  }

  .layer-name {
    font-weight: 600;
    color: #333;
    font-size: 14px;
    text-transform: capitalize;
  }

  .tile-name {
    font-size: 12px;
    color: #666;
    margin-top: 2px;
  }

  .feature-details {
    margin-bottom: 12px;
  }

  .detail-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 13px;
  }

  .label {
    font-weight: 500;
    color: #555;
    min-width: 120px;
  }

  .value {
    color: #333;
    text-align: right;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .downloads-section {
    margin-top: 16px;
  }

  .downloads-section h4 {
    margin: 0 0 8px 0;
    font-size: 14px;
    font-weight: 600;
    color: #333;
  }

  .download-links {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .download-item {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
  }

  .download-link {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    text-decoration: none;
    color: #007bff;
    background: #f8f9fa;
    transition: background-color 0.2s;
  }

  .download-link:hover {
    background: #e9ecef;
    color: #0056b3;
  }

  .download-name {
    font-weight: 500;
    font-size: 13px;
  }

  .download-icon {
    font-size: 16px;
    opacity: 0.7;
  }

  .download-description {
    display: block;
    padding: 4px 12px 8px;
    font-size: 11px;
    color: #666;
    font-style: italic;
  }

  .preview-section {
    margin-top: 16px;
    padding-top: 12px;
    border-top: 1px solid #eee;
  }

  .preview-section h4 {
    margin: 0 0 8px 0;
    font-size: 14px;
    font-weight: 600;
    color: #333;
  }

  .preview-link {
    display: inline-block;
    padding: 6px 12px;
    background: #28a745;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
    transition: background-color 0.2s;
  }

  .preview-link:hover {
    background: #218838;
    color: white;
  }

  .feature-separator {
    height: 1px;
    background: #eee;
    margin: 16px 0;
  }

  /* Satellite download styles */
  .satellite-download-section {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #f0f0f0;
  }

  .satellite-download-btn {
    width: 100%;
    padding: 6px 12px;
    background: linear-gradient(135deg, #007bff, #0056b3);
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    transition: all 0.2s ease;
  }

  .satellite-download-btn:hover:not(:disabled) {
    background: linear-gradient(135deg, #0056b3, #004085);
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
  }

  .satellite-download-btn:active:not(:disabled) {
    transform: translateY(0);
  }

  .satellite-download-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }

  .satellite-download-btn.downloading {
    background: linear-gradient(135deg, #6c757d, #495057);
  }

  .spinner {
    width: 12px;
    height: 12px;
    border: 2px solid transparent;
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .satellite-status {
    margin-top: 6px;
    padding: 6px 8px;
    border-radius: 3px;
    font-size: 10px;
    font-weight: 500;
    word-wrap: break-word;
    overflow-wrap: break-word;
    line-height: 1.3;
    white-space: pre-line; /* Preserve line breaks from \n */
    max-height: 120px;
    overflow-y: auto;
  }

  .satellite-status.success {
    background: rgba(40, 167, 69, 0.1);
    color: #28a745;
    border: 1px solid rgba(40, 167, 69, 0.2);
  }

  .satellite-status.error {
    background: rgba(220, 53, 69, 0.1);
    color: #dc3545;
    border: 1px solid rgba(220, 53, 69, 0.2);
    max-height: 40px;
    overflow-y: auto;
  }
</style>
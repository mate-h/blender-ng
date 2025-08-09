<script lang="ts">
  import { getScaleOptions } from './gridUtils';
  import { gridCenter, gridScale, gridSize } from './stores';
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

  // Format coordinates for display
  function formatCoordinate(value: number, decimals: number = 6): string {
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
</script>

<div class="grid-tab">
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
</div>

<style>
  .grid-tab {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  
  .control-group {
    display: flex;
    align-items: center;
    gap: 10px;
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
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  
  .info-text {
    font-size: 12px;
    color: #666;
    font-weight: 500;
  }
</style>

<script lang="ts">
  import { layerVisibility } from '../stores';

  // Advanced roadways layer controls - read from store to avoid feedback loops
  const showRoadways = $derived($layerVisibility['roadways'] ?? true);
  let showBicycleRoutes = $state(true);
  let showHighwayLabels = $state(false);
  let roadwayOpacity = $state(0.8);

  function toggleRoadways() {
    layerVisibility.update(visibility => ({
      ...visibility,
      'roadways': !showRoadways
    }));
  }
</script>

<div class="roadways-controls">
  <div class="control-section">
    <h5>Advanced Roadways</h5>
    
    <div class="control-item">
      <label class="control-checkbox">
        <input type="checkbox" checked={showRoadways} onchange={toggleRoadways} />
        <span class="control-name">Show Roadways</span>
        <span class="control-indicator" style="background-color: #333;"></span>
      </label>
    </div>

    <div class="control-item" class:disabled={!showRoadways}>
      <label class="control-checkbox">
        <input type="checkbox" bind:checked={showBicycleRoutes} disabled={!showRoadways} />
        <span class="control-name">Bicycle Routes</span>
        <span class="control-indicator dashed" style="background-color: #0F7D4B;"></span>
      </label>
    </div>

    <div class="control-item" class:disabled={!showRoadways}>
      <label class="control-checkbox">
        <input type="checkbox" bind:checked={showHighwayLabels} disabled={!showRoadways} />
        <span class="control-name">Highway Labels</span>
        <span class="control-icon">🏷️</span>
      </label>
    </div>

    <div class="control-item opacity-control" class:disabled={!showRoadways}>
      <label class="opacity-label">
        <span>Opacity: {Math.round(roadwayOpacity * 100)}%</span>
        <input 
          type="range" 
          min="0.1" 
          max="1" 
          step="0.1" 
          bind:value={roadwayOpacity}
          disabled={!showRoadways}
          class="opacity-slider"
        />
      </label>
    </div>
  </div>

  <div class="road-types-section">
    <details>
      <summary>Road Type Colors</summary>
      <div class="road-type-list">
        <div class="road-type-item">
          <div class="color-indicator" style="background: #E892A2;"></div>
          <span>Motorway</span>
        </div>
        <div class="road-type-item">
          <div class="color-indicator" style="background: #F9B29C;"></div>
          <span>Trunk</span>
        </div>
        <div class="road-type-item">
          <div class="color-indicator" style="background: #FCD6A4;"></div>
          <span>Primary</span>
        </div>
        <div class="road-type-item">
          <div class="color-indicator" style="background: #F7FABF;"></div>
          <span>Secondary</span>
        </div>
        <div class="road-type-item">
          <div class="color-indicator" style="background: #C8E6C9;"></div>
          <span>Tertiary</span>
        </div>
        <div class="road-type-item">
          <div class="color-indicator" style="background: #BBDEFB;"></div>
          <span>Residential</span>
        </div>
        <div class="road-type-item">
          <div class="color-indicator" style="background: #E1BEE7;"></div>
          <span>Service</span>
        </div>
        <div class="road-type-item">
          <div class="color-indicator dashed" style="background: #0F7D4B;"></div>
          <span>Bicycle</span>
        </div>
      </div>
    </details>
  </div>
</div>

<style>
  .roadways-controls {
    display: flex;
    flex-direction: column;
    gap: 12px;
    font-size: 12px;
  }

  .control-section {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .control-section h5 {
    font-weight: 600;
    font-size: 13px;
    color: #333;
    margin: 0 0 4px 0;
    border-bottom: 1px solid #eee;
    padding-bottom: 2px;
  }

  .control-item {
    display: flex;
    align-items: center;
    transition: opacity 0.2s ease;
  }

  .control-item.disabled {
    opacity: 0.5;
  }

  .control-checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    color: #333;
    width: 100%;
  }

  .control-checkbox input[type="checkbox"] {
    width: 14px;
    height: 14px;
    cursor: pointer;
    accent-color: #007bff;
  }

  .control-checkbox input[type="checkbox"]:disabled {
    cursor: not-allowed;
  }

  .control-name {
    flex: 1;
    font-weight: 500;
  }

  .control-indicator {
    width: 16px;
    height: 3px;
    border-radius: 2px;
    flex-shrink: 0;
  }

  .control-indicator.dashed {
    background-image: linear-gradient(to right, currentColor 50%, transparent 50%);
    background-size: 6px 100%;
    background-repeat: repeat-x;
    background-color: transparent !important;
  }

  .control-icon {
    font-size: 14px;
    opacity: 0.8;
  }

  .opacity-control {
    margin-top: 4px;
  }

  .opacity-label {
    display: flex;
    flex-direction: column;
    gap: 4px;
    width: 100%;
    font-size: 11px;
    color: #666;
  }

  .opacity-slider {
    width: 100%;
    height: 4px;
    background: #ddd;
    border-radius: 2px;
    outline: none;
    cursor: pointer;
  }

  .opacity-slider:disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }

  .road-types-section {
    border-top: 1px solid #eee;
    padding-top: 8px;
  }

  .road-types-section details {
    font-size: 11px;
  }

  .road-types-section summary {
    cursor: pointer;
    font-weight: 500;
    color: #666;
    margin-bottom: 6px;
  }

  .road-types-section summary:hover {
    color: #333;
  }

  .road-type-list {
    display: flex;
    flex-direction: column;
    gap: 3px;
    margin-left: 8px;
  }

  .road-type-item {
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .color-indicator {
    width: 12px;
    height: 3px;
    border-radius: 1px;
    flex-shrink: 0;
  }

  .color-indicator.dashed {
    background-image: linear-gradient(to right, currentColor 50%, transparent 50%);
    background-size: 4px 100%;
    background-repeat: repeat-x;
    background-color: transparent !important;
  }

  .road-type-item span {
    font-size: 10px;
    color: #555;
  }
</style>

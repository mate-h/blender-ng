<script lang="ts">
  import { availableLayers, layerVisibility, projectLabelsVisible } from './stores';
  import RoadwaysControls from './roadways/RoadwaysControls.svelte';

  // Layer management
  function toggleLayerVisibility(layerId: string) {
    layerVisibility.update(visibility => ({
      ...visibility,
      [layerId]: !visibility[layerId]
    }));
  }
</script>

<div class="layers-tab">
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

  <!-- Advanced Roadways Controls -->
  <div class="roadways-section">
    <RoadwaysControls />
  </div>
</div>

<style>
  .layers-tab {
    display: flex;
    flex-direction: column;
  }

  .layers-section {
    display: flex;
    flex-direction: column;
    gap: 6px;
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

  .roadways-section {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #ddd;
  }
</style>

<script lang="ts">
  import { elevationQueryMode, elevationMarkers, terrainMode, selectedTrees } from './stores';

  // Elevation marker management
  function clearElevationMarkers() {
    elevationMarkers.set([]);
  }

  // Tree selection management
  function clearSelectedTrees() {
    selectedTrees.set([]);
  }
</script>

<div class="tools-tab">
  <div class="elevation-section">
    <div class="elevation-title">Elevation Tools:</div>
    <div class="elevation-controls">
      <label class="tool-checkbox">
        <input 
          type="checkbox" 
          bind:checked={$elevationQueryMode}
        />
        <span class="tool-name">Click for Elevation</span>
        <span class="tool-icon">📏</span>
      </label>
      
      <label class="tool-checkbox">
        <input 
          type="checkbox" 
          bind:checked={$terrainMode}
        />
        <span class="tool-name">3D Terrain View</span>
        <span class="tool-icon">🏔️</span>
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
  
  <div class="trees-section">
    <div class="trees-title">Selected Trees:</div>
    {#if $selectedTrees.length > 0}
      <div class="selected-trees-list">
        {#each $selectedTrees as tree}
          <div class="tree-item">
            <div class="tree-info">
              <span class="tree-species">{tree.properties.common_name || 'Unknown'}</span>
              <span class="tree-details">
                {tree.properties.genus_name} {tree.properties.species_name}
              </span>
              <span class="tree-location">{tree.properties.std_street}</span>
            </div>
          </div>
        {/each}
        <button 
          class="clear-trees-btn"
          on:click={clearSelectedTrees}
        >
          Clear Selected Trees ({$selectedTrees.length})
        </button>
      </div>
    {:else}
      <div class="no-trees">Click on trees to select them</div>
    {/if}
  </div>
</div>

<style>
  .tools-tab {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .elevation-section, .trees-section {
    display: flex;
    flex-direction: column;
  }

  .elevation-title, .trees-title {
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

  .tool-checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    font-size: 12px;
    color: #333;
    width: 100%;
  }

  .tool-checkbox input[type="checkbox"] {
    width: 14px;
    height: 14px;
    cursor: pointer;
    accent-color: #007bff;
  }

  .tool-name {
    flex: 1;
    font-weight: 500;
  }

  .tool-icon {
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
    margin-top: 4px;
  }

  .clear-markers-btn:hover {
    background: linear-gradient(135deg, #c82333, #a71e2a);
    transform: translateY(-1px);
  }

  .clear-markers-btn:active {
    transform: translateY(0);
  }

  .selected-trees-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .tree-item {
    padding: 8px;
    background: rgba(34, 139, 34, 0.1);
    border: 1px solid rgba(34, 139, 34, 0.2);
    border-radius: 4px;
  }

  .tree-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }

  .tree-species {
    font-weight: 600;
    font-size: 12px;
    color: #228B22;
  }

  .tree-details {
    font-size: 11px;
    color: #666;
    font-style: italic;
  }

  .tree-location {
    font-size: 11px;
    color: #333;
  }

  .clear-trees-btn {
    padding: 6px 12px;
    background: linear-gradient(135deg, #228B22, #006400);
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    margin-top: 8px;
  }

  .clear-trees-btn:hover {
    background: linear-gradient(135deg, #006400, #004d00);
    transform: translateY(-1px);
  }

  .clear-trees-btn:active {
    transform: translateY(0);
  }

  .no-trees {
    font-size: 12px;
    color: #666;
    font-style: italic;
    text-align: center;
    padding: 12px 0;
  }
</style>

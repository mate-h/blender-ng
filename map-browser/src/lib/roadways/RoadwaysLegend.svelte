<script lang="ts">
  let showLegend = false;

  const roadTypes = [
    { name: 'Motorway', color: '#E892A2', width: 6 },
    { name: 'Motorway Link', color: '#E892A2', width: 4 },
    { name: 'Trunk', color: '#F9B29C', width: 5 },
    { name: 'Primary', color: '#FCD6A4', width: 4 },
    { name: 'Secondary', color: '#F7FABF', width: 3 },
    { name: 'Tertiary', color: '#C8E6C9', width: 2.5 },
    { name: 'Residential', color: '#BBDEFB', width: 2 },
    { name: 'Service', color: '#E1BEE7', width: 1.5 },
    { name: 'Bicycle Route', color: '#0F7D4B', width: 3, dashed: true },
  ];
</script>

<div class="roadways-legend">
  <button 
    class="legend-toggle" 
    on:click={() => showLegend = !showLegend}
    title="Toggle roadways legend"
  >
    🛣️ Legend
  </button>
  
  {#if showLegend}
    <div class="legend-panel">
      <h4>Road Types</h4>
      <div class="legend-items">
        {#each roadTypes as road}
          <div class="legend-item">
            <div 
              class="legend-line" 
              class:dashed={road.dashed}
              style="background-color: {road.color}; height: {Math.max(road.width * 0.5, 2)}px;"
            ></div>
            <span class="legend-label">{road.name}</span>
          </div>
        {/each}
      </div>
      
      <div class="legend-info">
        <p><strong>Interactive Features:</strong></p>
        <ul>
          <li>Hover over roads to highlight</li>
          <li>Click roads for details</li>
          <li>Zoom to see more detail</li>
          <li>Dashed lines = bicycle routes</li>
        </ul>
      </div>
    </div>
  {/if}
</div>

<style>
  .roadways-legend {
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 1000;
  }

  .legend-toggle {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #ccc;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
  }

  .legend-toggle:hover {
    background: white;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }

  .legend-panel {
    position: absolute;
    top: 40px;
    right: 0;
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    min-width: 200px;
    max-width: 280px;
    backdrop-filter: blur(5px);
  }

  .legend-panel h4 {
    margin: 0 0 8px 0;
    font-size: 14px;
    font-weight: 600;
    color: #333;
    border-bottom: 1px solid #eee;
    padding-bottom: 4px;
  }

  .legend-items {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 12px;
  }

  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .legend-line {
    width: 30px;
    border-radius: 2px;
    flex-shrink: 0;
  }

  .legend-line.dashed {
    background-image: linear-gradient(to right, currentColor 50%, transparent 50%);
    background-size: 8px 100%;
    background-repeat: repeat-x;
    background-color: transparent !important;
  }

  .legend-label {
    font-size: 11px;
    color: #444;
    font-weight: 500;
  }

  .legend-info {
    border-top: 1px solid #eee;
    padding-top: 8px;
    font-size: 10px;
    color: #666;
  }

  .legend-info p {
    margin: 0 0 4px 0;
    font-weight: 600;
  }

  .legend-info ul {
    margin: 0;
    padding-left: 12px;
    list-style-type: disc;
  }

  .legend-info li {
    margin-bottom: 2px;
  }
</style>

<script lang="ts">
  import TabContainer from './TabContainer.svelte';
  import GridTab from './GridTab.svelte';
  import LayersTab from './LayersTab.svelte';
  import ToolsTab from './ToolsTab.svelte';
  import DownloadTab from './DownloadTab.svelte';
  
  // Mapbox token from the app (we'll need to pass this from the parent)
  export let mapboxToken: string;

  const tabs = [
    { id: 'grid', label: 'Grid', icon: '📐' },
    { id: 'layers', label: 'Layers', icon: '🗺️' },
    { id: 'tools', label: 'Tools', icon: '🔧' },
    { id: 'download', label: 'Download', icon: '⬇️' }
  ];
</script>

<div class="grid-controls">
  <TabContainer {tabs}>
    <svelte:fragment slot="grid">
      <GridTab />
    </svelte:fragment>
    
    <svelte:fragment slot="layers">
      <LayersTab />
    </svelte:fragment>
    
    <svelte:fragment slot="tools">
      <ToolsTab />
    </svelte:fragment>
    
    <svelte:fragment slot="download">
      <DownloadTab {mapboxToken} />
    </svelte:fragment>
  </TabContainer>
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
</style>
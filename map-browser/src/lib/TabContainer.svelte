<script lang="ts">
  import { writable } from 'svelte/store';
  
  export let tabs: Array<{id: string, label: string, icon?: string}>;
  export let activeTab = tabs[0]?.id || '';
  
  const activeTabStore = writable(activeTab);
  
  function setActiveTab(tabId: string) {
    activeTabStore.set(tabId);
    activeTab = tabId;
  }
  
  $: activeTab = $activeTabStore;
</script>

<div class="tab-container">
  <div class="tab-header">
    {#each tabs as tab}
      <button 
        class="tab-button" 
        class:active={activeTab === tab.id}
        on:click={() => setActiveTab(tab.id)}
      >
        {#if tab.icon}
          <span class="tab-icon">{tab.icon}</span>
        {/if}
        <span class="tab-label">{tab.label}</span>
      </button>
    {/each}
  </div>
  
  <div class="tab-content">
    {#if activeTab === 'grid'}
      <slot name="grid" />
    {:else if activeTab === 'layers'}
      <slot name="layers" />
    {:else if activeTab === 'tools'}
      <slot name="tools" />
    {:else if activeTab === 'download'}
      <slot name="download" />
    {/if}
  </div>
</div>

<style>
  .tab-container {
    width: 100%;
  }
  
  .tab-header {
    display: flex;
    border-bottom: 1px solid #ddd;
    margin-bottom: 12px;
  }
  
  .tab-button {
    flex: 1;
    padding: 8px 4px;
    border: none;
    background: transparent;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2px;
    font-size: 11px;
    color: #666;
    transition: all 0.2s ease;
    border-bottom: 2px solid transparent;
  }
  
  .tab-button:hover {
    background: rgba(0, 123, 255, 0.05);
    color: #007bff;
  }
  
  .tab-button.active {
    color: #007bff;
    border-bottom-color: #007bff;
    background: rgba(0, 123, 255, 0.05);
  }
  
  .tab-icon {
    font-size: 16px;
    opacity: 0.8;
  }
  
  .tab-label {
    font-weight: 500;
    white-space: nowrap;
  }
  
  .tab-content {
    min-height: 200px;
  }
</style>

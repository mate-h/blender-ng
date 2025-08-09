<script lang="ts">
  export let selectedRoad: GeoJSON.Feature | null = null;
  export let isVisible: boolean = false;

  function closePanel() {
    isVisible = false;
    selectedRoad = null;
  }

  function formatPropertyName(key: string): string {
    // Convert property keys to human-readable names
    const propertyNames: Record<string, string> = {
      'highway': 'Highway Type',
      'route': 'Route Type',
      'name': 'Road Name',
      'network': 'Network',
      'type': 'Type',
      'ref': 'Reference',
      'surface': 'Surface',
      'lanes': 'Number of Lanes',
      'maxspeed': 'Speed Limit',
      'oneway': 'One Way',
      'access': 'Access',
      'bicycle': 'Bicycle Access',
      'foot': 'Foot Access',
      'motor_vehicle': 'Motor Vehicle Access',
      'service': 'Service Type',
      'width': 'Width',
      'bridge': 'Bridge',
      'tunnel': 'Tunnel',
      'layer': 'Layer',
      'level': 'Level',
      'timestamp': 'Last Modified',
      'version': 'Version',
      'changeset': 'Changeset',
      'user': 'Modified By',
      'uid': 'User ID',
      'id': 'Feature ID'
    };
    
    return propertyNames[key] || key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' ');
  }

  function formatPropertyValue(key: string, value: unknown): string {
    if (value === null || value === undefined) return 'N/A';
    
    // Special formatting for certain properties
    switch (key) {
      case 'oneway':
        return value === 'yes' ? 'Yes' : value === 'no' ? 'No' : value;
      case 'bridge':
      case 'tunnel':
        return value === 'yes' ? 'Yes' : 'No';
      case 'timestamp':
        return new Date(value).toLocaleString();
      case 'maxspeed':
        return `${value} km/h`;
      case 'width':
        return `${value}m`;
      case 'lanes':
        return `${value} lane${value !== '1' ? 's' : ''}`;
      default:
        return String(value);
    }
  }

  function getPropertyCategory(key: string): string {
    const categories: Record<string, string> = {
      // Basic info
      'name': 'basic',
      'highway': 'basic',
      'route': 'basic',
      'type': 'basic',
      'network': 'basic',
      'ref': 'basic',
      
      // Physical properties
      'surface': 'physical',
      'lanes': 'physical',
      'width': 'physical',
      'bridge': 'physical',
      'tunnel': 'physical',
      'layer': 'physical',
      'level': 'physical',
      
      // Access and restrictions
      'access': 'access',
      'bicycle': 'access',
      'foot': 'access',
      'motor_vehicle': 'access',
      'oneway': 'access',
      'maxspeed': 'access',
      'service': 'access',
      
      // Metadata
      'timestamp': 'metadata',
      'version': 'metadata',
      'changeset': 'metadata',
      'user': 'metadata',
      'uid': 'metadata',
      'id': 'metadata'
    };
    
    return categories[key] || 'other';
  }

  $: roadProperties = selectedRoad?.properties ? 
    Object.entries(selectedRoad.properties)
      .filter(([key, value]) => value !== null && value !== undefined && value !== '')
      .reduce((acc, [key, value]) => {
        const category = getPropertyCategory(key);
        if (!acc[category]) acc[category] = [];
        acc[category].push([key, value]);
        return acc;
      }, {} as Record<string, [string, unknown][]>)
    : {};

  const categoryTitles: Record<string, string> = {
    'basic': 'Basic Information',
    'physical': 'Physical Properties',
    'access': 'Access & Restrictions',
    'metadata': 'Metadata',
    'other': 'Other Properties'
  };

  const categoryOrder = ['basic', 'physical', 'access', 'other', 'metadata'];
</script>

{#if isVisible && selectedRoad}
  <div class="roadways-info-panel">
    <div class="panel-header">
      <h3>Road Information</h3>
      <button class="close-btn" on:click={closePanel} title="Close">
        ✕
      </button>
    </div>
    
    <div class="panel-content">
      <div class="road-title">
        <h4>
          {selectedRoad.properties?.name || selectedRoad.properties?.ref || 'Unnamed Road'}
        </h4>
        {#if selectedRoad.properties?.highway}
          <span class="road-type-badge" class:highway={selectedRoad.properties.highway}>
            {selectedRoad.properties.highway}
          </span>
        {/if}
        {#if selectedRoad.properties?.route}
          <span class="road-type-badge route">
            {selectedRoad.properties.route} route
          </span>
        {/if}
      </div>

      <div class="properties-container">
        {#each categoryOrder as category}
          {#if roadProperties[category] && roadProperties[category].length > 0}
            <div class="property-category">
              <h5 class="category-title">{categoryTitles[category]}</h5>
              <div class="properties-grid">
                {#each roadProperties[category] as [key, value]}
                  <div class="property-row">
                    <span class="property-key">{formatPropertyName(key)}:</span>
                    <span class="property-value">{formatPropertyValue(key, value)}</span>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
        {/each}
      </div>

      {#if selectedRoad.geometry}
        <div class="geometry-info">
          <h5>Geometry</h5>
          <div class="property-row">
            <span class="property-key">Type:</span>
            <span class="property-value">{selectedRoad.geometry.type}</span>
          </div>
          {#if selectedRoad.geometry.coordinates}
            <div class="property-row">
              <span class="property-key">Coordinates:</span>
              <span class="property-value">
                {selectedRoad.geometry.type === 'MultiLineString' ? 
                  `${selectedRoad.geometry.coordinates.length} line segments` :
                  `${selectedRoad.geometry.coordinates.length} points`}
              </span>
            </div>
          {/if}
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .roadways-info-panel {
    position: fixed;
    top: 10px;
    right: 10px;
    width: 350px;
    max-height: calc(100vh - 20px);
    background: rgba(255, 255, 255, 0.98);
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(5px);
    z-index: 1000;
    display: flex;
    flex-direction: column;
  }

  .panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 16px;
    border-bottom: 1px solid #eee;
    background: rgba(248, 249, 250, 0.9);
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
    font-size: 18px;
    cursor: pointer;
    color: #666;
    padding: 4px;
    border-radius: 4px;
    transition: all 0.2s ease;
  }

  .close-btn:hover {
    background: rgba(0, 0, 0, 0.1);
    color: #333;
  }

  .panel-content {
    padding: 16px;
    overflow-y: auto;
    flex: 1;
  }

  .road-title {
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #eee;
  }

  .road-title h4 {
    margin: 0 0 8px 0;
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }

  .road-type-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    margin-right: 6px;
    margin-bottom: 4px;
  }

  .road-type-badge.highway {
    background: #E892A2;
    color: white;
  }

  .road-type-badge.route {
    background: #0F7D4B;
    color: white;
  }

  .properties-container {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .property-category {
    background: rgba(248, 249, 250, 0.5);
    border-radius: 6px;
    padding: 12px;
  }

  .category-title {
    margin: 0 0 8px 0;
    font-size: 13px;
    font-weight: 600;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .properties-grid {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .property-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 12px;
    font-size: 13px;
  }

  .property-key {
    font-weight: 500;
    color: #555;
    flex-shrink: 0;
    min-width: 100px;
  }

  .property-value {
    color: #333;
    text-align: right;
    word-break: break-word;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  }

  .geometry-info {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid #eee;
  }

  .geometry-info h5 {
    margin: 0 0 8px 0;
    font-size: 13px;
    font-weight: 600;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  /* Scrollbar styling */
  .panel-content::-webkit-scrollbar {
    width: 6px;
  }

  .panel-content::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }

  .panel-content::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
  }

  .panel-content::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
  }
</style>

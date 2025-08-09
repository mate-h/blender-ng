<script lang="ts">
  import MapboxMap from './lib/MapboxMap.svelte'
  import RoadwaysLegend from './lib/roadways/RoadwaysLegend.svelte'
  import { defaultCenter } from './lib/stores'
  
  const MAPBOX_TOKEN = "pk.eyJ1IjoibWF0ZWgiLCJhIjoiY2pmOTEzbHo2MzU3cTJ3b201NDNkOXQxZiJ9.UYLkoWDRs877jt_-k4LH4g"
</script>

<main>
  <!-- 49.3634, -123.2720 -->
  <MapboxMap 
    accessToken={MAPBOX_TOKEN}
    style="mapbox://styles/mapbox/satellite-streets-v12"
    center={[defaultCenter.lng, defaultCenter.lat]}
    zoom={12}
  />
  
  <RoadwaysLegend />
</main>

<style>
  main {
    width: 100vw;
    height: 100vh;
    position: relative;
    overflow: hidden;
  }
</style>

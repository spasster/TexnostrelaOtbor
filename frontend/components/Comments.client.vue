<template>
  <div>
    <div id="map" ref="map" style="height: 500px;"></div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import L from 'leaflet';
import 'leaflet-routing-machine';

export default {
  setup() {
    const map = ref(null);
    
    onMounted(() => {
      const mapInstance = L.map(map.value).setView([55.751244, 37.618423], 13); // Координаты центра карты

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
      }).addTo(mapInstance);

      const routingControl = L.Routing.control({
        waypoints: [
          L.latLng(55.751244, 37.618423), // Первая точка
          L.latLng(55.758239, 37.617659), // Вторая точка
          L.latLng(55.764081, 37.609218), // Третья точка
        ],
        routeWhileDragging: true,
      }).addTo(mapInstance);
    });

    return {
      map,
    };
  },
};
</script>

<style>
#map {
  height: 500px;
}
</style>

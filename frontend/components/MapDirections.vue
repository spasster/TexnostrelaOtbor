<template>
  <div>
   
    <div ref="mapContainer" class="container">
      <button 
      class="route-type-button"
      @click="toggleRouteType"
    >
      {{ routeType === 'pedestrian' ? 'Пеший маршрут' : 'Автомобильный маршрут' }}
    </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

const props = defineProps({
  apiKey: {
    type: String,
    required: true
  },
  directionsApiKey: {
    type: String,
    required: true
  },
  points: {
    type: Array,
    default: () => [],
    validator: value => value.every(p => Array.isArray(p) && p.length === 2)
  }
})

const mapContainer = ref(null)
let map = null
let directions = null
const markers = ref([])
const selectedPoints = ref([])
const routeType = ref('pedestrian') // 'pedestrian' или 'car'

// Watch for changes
watch([() => props.points, routeType], ([newPoints]) => {
  if (newPoints.length >= 2) {
    buildRoute(newPoints)
  }
})

onMounted(async () => {
  if (typeof mapgl === 'undefined') {
    console.error('2GIS mapgl not loaded')
    return
  }

  map = new mapgl.Map(mapContainer.value, {
    center: [37.668598, 55.76259],
    zoom: 13,
    key: props.apiKey
  })

  directions = new mapgl.Directions(map, {
    directionsApiKey: props.directionsApiKey
  })

  if (props.points.length >= 2) {
    buildRoute(props.points)
  } else {
    map.on('click', handleMapClick)
  }
})

onBeforeUnmount(() => {
  if (map) map.destroy()
  clearMarkers()
})

const buildRoute = (points) => {
  directions.clear()
  clearMarkers()

  // Create markers
  points.forEach(point => {
    markers.value.push(
      new mapgl.Marker(map, {
        coordinates: point,
        icon: 'https://docs.2gis.com/img/dotMarker.svg',
      })
    )
  })

  // Build route
  if (routeType.value === 'pedestrian') {
    directions.pedestrianRoute({ points })
  } else {
    directions.carRoute({ points })
  }
}

const toggleRouteType = () => {
  routeType.value = routeType.value === 'pedestrian' ? 'car' : 'pedestrian'
  if (props.points.length >= 2) {
    buildRoute(props.points)
  }
}

const handleMapClick = (e) => {
  const coords = e.lngLat
  selectedPoints.value.push(coords)

  markers.value.push(
    new mapgl.Marker(map, {
      coordinates: coords,
      icon: 'https://docs.2gis.com/img/dotMarker.svg',
    })
  )

  if (selectedPoints.value.length === 2) {
    buildRoute(selectedPoints.value)
  }
}

const clearMarkers = () => {
  markers.value.forEach(marker => marker.destroy())
  markers.value = []
}
</script>

<style scoped>
.container {
  margin: 0;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

.route-type-button {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 8px 16px;
  background: #00a81f;
  border-radius: 4px;
  border: none;
  color: white;
  cursor: pointer;
  z-index: 1;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.route-type-button:hover {
  background: #00921a;
}
</style>
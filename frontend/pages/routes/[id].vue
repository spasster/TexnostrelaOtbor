<template>
    <div class="page-container">
      <h1 v-if="routeData">{{ routeData.name }}</h1>
      <p v-if="routeData">{{ routeData.description }}</p>
      <div v-if="isLoading">Загрузка маршрута...</div>
      <div v-else-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <template v-else>
        <MapDirections
          :api-key="apiKey"
          :directions-api-key="apiKey"
          :points="routePoints"
        />
        <Points v-if="routeData?.points" :points="routeData.points"/>
      </template>
    </div>
  </template>
  
  <script setup lang="ts">
  interface RoutePoint {
    id: number
    name: string
    latitude: number
    longitude: number
    photo: string | null
    order: number
  }
  
  interface RouteData {
    id: number
    name: string
    points: RoutePoint[]
  }
  
  const route = useRoute()
  const { $apiFetch } = useNuxtApp()
  const apiKey = '8aff4786-dd40-4af6-bd21-9ec79e5dd737'
  
  const routeData = ref<RouteData | null>(null)
  const isLoading = ref(true)
  const errorMessage = ref('')
  
  const routePoints = computed(() => {
    return routeData.value.points.map(p => [p.latitude, p.longitude]) || []
  })
  
  const fetchRoute = async () => {
    try {
      const routeId = route.params.id
      if (!routeId) throw new Error('ID маршрута не указан')
      
      const response = await $apiFetch<RouteData>(`api/routes/get_route/${routeId}/`)
      routeData.value = response
      
    } catch (error: any) {
      errorMessage.value = 'Ошибка загрузки: ' + (error.data?.detail || error.message)
      console.error('Ошибка:', error)
    } finally {
      isLoading.value = false
    }
  }
  
  onMounted(fetchRoute)
  </script>
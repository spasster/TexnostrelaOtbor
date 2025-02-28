<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8 text-gray-800">Все маршруты</h1>
    
    <div v-if="pending" class="text-center py-12">
      <ProgressSpinner style="width: 50px; height: 50px" />
    </div>

    <div v-else-if="error" class="text-red-500 p-4 bg-red-100 rounded-lg">
      Ошибка загрузки маршрутов: {{ error.message }}
    </div>

    <div v-else>
      <div v-if="routes.length === 0" class="text-gray-500 text-center py-12">
        Маршруты не найдены
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <RouteCard
          v-for="route in routes"
          :key="route.id"
          image='/route-placeholder.jpg'
          :title="route.name"
          :description="route.description"
          :rating="route.rating"
          :tags="route.tags"
          @share-clicked="handleShare({id: route.id, title: route.title, description: route.description})"

          @details-clicked="navigateToRoute(route.id)"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>

const { data: routes, pending, error } = useFetch('/api/routes/get_routes/', {
  method: 'GET',
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

const navigateToRoute = (routeId: number) => {
  navigateTo(`/routes/${routeId}`)
}

const handleShare = (routeData: { 
  id: number;
  title?: string;
  description?: string;
}) => {
  const routeUrl = `${window.location.origin}/routes/${routeData.id}`;
  
  if (navigator.share) {
    navigator.share({
      title: routeData.title || 'Маршрут',
      text: routeData.description || 'Интересный маршрут',
      url: routeUrl
    });
  } else {
    navigator.clipboard.writeText(routeUrl);
    alert('Ссылка скопирована в буфер обмена!');
  }
};
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
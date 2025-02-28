<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8 text-gray-800">Мои приватные маршруты</h1>

    <div v-if="!filteredRoutes.length" class="text-gray-500 text-center py-12">
      У вас нет приватных маршрутов
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <RouteCard
        v-for="route in filteredRoutes"
        :key="route.id"
        :id="route.id"
        :image="route.photos?.[0] || '/route-placeholder.jpg'"
        :title="route.name"
        :description="route.description"
        :rating="route.rating"
        :tags="[route.type]"
        @details-clicked="navigateToRoute(route.id)"
      />
    </div>
  </div>
</template>

<script lang="ts" setup>
definePageMeta({ middleware: 'auth' });

const authStore = useAuthStore();
const router = useRouter();

const filteredRoutes = computed(() => {
  return authStore.user?.routes
    ?.filter(route => route.type === 'private')
    ?.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)) || [];
});

const navigateToRoute = (id: number) => {
  router.push(`/routes/${id}`);
};
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
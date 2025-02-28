<template>
  <Card class="w-96 overflow-hidden shadow-lg rounded-xl">
    <template #header>
      <div class="relative">
        <img :src="image" alt="route image" class="w-full h-48 object-cover rounded-t-xl" />
      </div>
    </template>

    <template #content>
      <div class="flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">{{ title }}</h3>
        <div class="flex items-center gap-1 text-gray-600">
          <i class="pi pi-star text-yellow-400"></i>
          <span>{{ rating }}</span>
        </div>
      </div>

      <p class="text-sm text-gray-500 mt-2">{{ description }}</p>

      <div class="flex flex-wrap gap-2 mt-3">
        <Tag v-for="tag in tags" :key="tag" class="bg-gray-200 text-gray-800">
          {{ tag }}
        </Tag>
      </div>
    </template>

    <template #footer>
      <div class="flex justify-between mt-2">
        <Button 
          icon="pi pi-share-alt" 
          label="Поделиться" 
          class="p-button-outlined" 
          @click="handleShareClick" 
        />
        <Button 
          label="Подробнее" 
          class="p-button-primary" 
          @click="$emit('details-clicked')" 
        />
      </div>
    </template>
  </Card>
</template>

<script lang="ts" setup>
defineProps({
  id: {
    type: Number,
    required: true
  },
  image: String,
  title: String,
  description: String,
  rating: Number,
  tags: Array as () => string[],
})

const emit = defineEmits(['details-clicked', 'share-clicked']);

const handleShareClick = () => {
  emit('share-clicked')
}
</script>
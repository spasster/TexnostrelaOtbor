<template>
  <div class="card">
    <Stepper value="1">
      <StepItem 
        v-for="(point, index) in points" 
        :key="point.id" 
        :value="String(index + 1)"
      >
        <Step>{{ point.name || `Точка ${index + 1}` }}</Step>
        <StepPanel v-slot="{ activateCallback }">
          <div class="flex flex-col gap-4 p-4">
            <div v-if="point.photo" class="h-48 overflow-hidden rounded-lg">
              <img 
                :src="point.photo" 
                :alt="point.name" 
                class="object-cover w-full h-full"
              />
            </div>
            
            <div class="space-y-2">
              <p class="text-gray-600 dark:text-gray-300">
                {{ point.description || 'Нет описания' }}
              </p>
              <div class="text-sm text-gray-500">
                Координаты: {{ point.latitude.toFixed(6) }}, {{ point.longitude.toFixed(6) }}
              </div>
            </div>
          </div>

          <div class="flex gap-2 py-4">
            <Button 
              v-if="index > 0" 
              label="Назад" 
              severity="secondary" 
              @click="activateCallback(String(index))"
            />
            
            <Button 
              v-if="index < points.length - 1" 
              label="Следующая точка" 
              @click="activateCallback(String(index + 2))"
            />
            
            <Button 
              v-if="index === points.length - 1" 
              label="Построить маршрут" 
              icon="pi pi-map" 
              @click="redirectToYandexMaps"
            />
          </div>
        </StepPanel>
      </StepItem>
    </Stepper>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';

const props = defineProps({
  points: {
    type: Array as () => Array<{
      id: number;
      name: string;
      description: string;
      latitude: number;
      longitude: number;
      photo: string | null;
      order: number;
    }>,
    required: true
  }
});

const redirectToYandexMaps = () => {
  const coords = props.points
    .map(p => `${p.longitude},${p.latitude}`)
    .join('~');
  
  const url = `https://yandex.ru/maps/?mode=routes&rtext=${encodeURIComponent(coords)}&rtt=pd`;
  window.open(url, '_blank');
};
</script>

<style>
.p-stepper .p-stepper-header {
  border-bottom: 0;
}

.p-stepper .p-stepper-nav {
  justify-content: center;
}

.p-step-item .p-step-title {
  font-size: 0.875rem;
}
</style>
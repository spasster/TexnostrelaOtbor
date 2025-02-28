<template>
  <div class="p-6 max-w-4xl mx-auto">
    <!-- Профиль -->
    <div class="flex items-center gap-6">
      <div class="relative group">
        <img
          :src="avatar || defaultAvatar"
          alt="Аватар"
          class="w-24 h-24 rounded-full border-4 border-gray-700"
        />
        <label
          for="avatar-upload"
          class="absolute inset-0 flex items-center justify-center bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer rounded-full"
        >
          <i class="pi pi-camera text-white text-xl"></i>
        </label>
        <input id="avatar-upload" type="file" class="hidden" @change="updateAvatar" />
      </div>
      <div>
        <h2 class="text-2xl font-semibold text-white">{{ user.name }}</h2>
        <p class="text-gray-400">{{ user.email }}</p>
        <p class="text-gray-400 text-sm">На сайте с: {{ registrationDate }}</p>
      </div>
      <Button label="Редактировать" icon="pi pi-pencil" class="ml-auto" @click="showEditDialog = true" />
      <Button label="Выйти" severity="danger" variant="outlined" icon="pi pi-sign-out" @click="authStore.logout(); navigateTo('/')" />
    </div>

    <!-- Статистика -->
    <div class="mt-8 grid grid-cols-4 gap-4 text-center">
      <div class="p-4 bg-gray-800 rounded-lg">
        <h3 class="text-lg font-semibold text-white">{{ completedRoutes.length }}</h3>
        <p class="text-gray-400 text-sm">Пройдено</p>
      </div>
      <div class="p-4 bg-gray-800 rounded-lg">
        <h3 class="text-lg font-semibold text-white">{{ createdRoutes.length }}</h3>
        <p class="text-gray-400 text-sm">Создано</p>
      </div>
      <div class="p-4 bg-gray-800 rounded-lg">
        <h3 class="text-lg font-semibold text-white">{{ commentsCount }}</h3>
        <p class="text-gray-400 text-sm">Комментариев</p>
      </div>
      <div class="p-4 bg-gray-800 rounded-lg">
        <h3 class="text-lg font-semibold text-white">{{ totalTravelTime }} ч</h3>
        <p class="text-gray-400 text-sm">В пути</p>
      </div>
    </div>

    <!-- Табы -->
    <div class="mt-8 card">
      <Tabs value="completed">
        <TabList>
          <Tab value="completed">Пройденные</Tab>
          <Tab value="created">Созданные</Tab>
          <Tab value="comments">Комментарии ({{ userComments.length }})</Tab>
        </TabList>
        <TabPanels>
          <!-- Пройденные маршруты -->
          <TabPanel value="completed">
            <div class="grid grid-cols-2 gap-4">
              <Card v-for="route in completedRoutes" :key="route.id">
                <template #content>
                  <div class="relative">
                    <img src="/route-placeholder.jpg" class="w-full h-32 object-cover rounded-lg" />
                    <span class="absolute bottom-2 right-2 bg-black/50 px-2 py-1 rounded text-sm">
                      ★ {{ route.rating }}
                    </span>
                  </div>
                  <h3 class="text-lg font-semibold mt-2">{{ route.name }}</h3>
                  <p class="text-gray-400 text-sm">{{ route.description }}</p>
                  <div class="mt-2 flex justify-between text-xs text-gray-400">
                    <span>Пройден: {{ formatDate(route.completedDate) }}</span>
                    <span>{{ route.distance }} км</span>
                  </div>
                </template>
              </Card>
            </div>
          </TabPanel>

          <!-- Созданные маршруты -->
          <TabPanel value="created">
            <div v-if="authStore.user?.routes?.length" class="grid grid-cols-2 gap-4">
              <Card v-for="route in authStore.user.routes" :key="route.id">
                <template #content>
                  <img 
                    v-if="route.photos?.length" 
                    :src="route.photos[0]" 
                    class="w-full h-32 object-cover rounded-lg"
                  />
                  <img 
                    v-else 
                    src="/route-placeholder.jpg" 
                    class="w-full h-32 object-cover rounded-lg"
                  />
                  <h3 class="text-lg font-semibold mt-2">{{ route.name }}</h3>
                  <p class="text-gray-400 text-sm">{{ route.description || 'Нет описания' }}</p>
                  <div class="mt-2 flex gap-2">
                    <Button icon="pi pi-pencil" class="p-button-sm" @click="editRoute(route)" />
                    <Button icon="pi pi-trash" class="p-button-sm p-button-danger" @click="deleteRoute(route)" />
                  </div>
                </template>
              </Card>
            </div>
            <div v-else class="text-center py-6">
              <p class="text-gray-400">У вас пока нет созданных маршрутов</p>
            </div>
          </TabPanel>

          <!-- Комментарии -->
          <TabPanel value="comments">
            <div class="space-y-4">
              <div v-for="comment in userComments" :key="comment.id" class="p-4 bg-gray-800 rounded-lg">
                <div class="flex items-center gap-2 text-sm text-gray-400">
                  <span>Маршрут: {{ comment.route.name }}</span>
                  <span>•</span>
                  <span>{{ formatDate(comment.date) }}</span>
                </div>
                <p class="mt-2 text-white">{{ comment.text }}</p>
                <div v-if="comment.replies.length" class="mt-4 ml-4 pl-4 border-l-2 border-gray-600">
                  <div v-for="reply in comment.replies" :key="reply.id" class="py-2">
                    <div class="flex items-center gap-2 text-sm">
                      <span class="font-semibold text-blue-400">{{ reply.author }}</span>
                      <span class="text-gray-400">{{ formatDate(reply.date) }}</span>
                    </div>
                    <p class="mt-1 text-gray-300">{{ reply.text }}</p>
                  </div>
                </div>
              </div>
            </div>
          </TabPanel>

         
        </TabPanels>
      </Tabs>
    </div>

    <!-- Создать маршрут -->
    <div class="mt-8">
      <Button label="Создать маршрут" icon="pi pi-plus" class="w-full" @click="createRoute" />
    </div>

    <!-- Диалог редактирования профиля -->
    <Dialog v-model:visible="showEditDialog" header="Редактирование профиля" :modal="true">
      <div class="flex flex-col gap-4">
        <label>
          <span class="text-gray-300">Старый пароль</span>
          <InputText v-model="oldPassword" toggleMask class="w-full" />
        </label>
        <label>
          <span class="text-gray-300">Новый пароль</span>
          <Password v-model="password" toggleMask class="w-full" />
        </label>
        <small v-if="errorMessage" class="text-red-400">{{ errorMessage }}</small>
      </div>
      <template #footer>
        <Button label="Сохранить" :loading="isLoading" icon="pi pi-check" @click="saveProfile" />
      </template>
    </Dialog>
    <Dialog v-model:visible="showCreateDialog" header="Создание маршрута" :modal="true" :style="{ width: '50rem' }">
      <div class="flex flex-col gap-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-gray-300 mb-2">Название маршрута*</label>
            <InputText v-model="newRoute.name" class="w-full" />
          </div>
          <div>
            <label class="block text-gray-300 mb-2">Тип маршрута</label>
            <Dropdown 
              v-model="newRoute.type" 
              :options="['public', 'private']" 
              placeholder="Выберите тип" 
              class="w-full" 
            />
          </div>
        </div>

        <div>
          <label class="block text-gray-300 mb-2">Описание</label>
          <Textarea v-model="newRoute.description" rows="3" class="w-full" />
        </div>

        <div>
          <div class="flex justify-between items-center mb-2">
            <span class="text-gray-300">Точки маршрута*</span>
            <Button 
              label="Добавить точку" 
              icon="pi pi-plus" 
              class="p-button-sm" 
              @click="addPoint" 
              :disabled="newRoute.points.length >= 10"
            />
          </div>
          
          <div class="space-y-4">
            <div 
              v-for="(point, index) in newRoute.points" 
              :key="index" 
              class="p-4 bg-gray-800 rounded-lg"
            >
              <div class="flex justify-between mb-2">
                <span class="text-gray-400">Точка #{{ index + 1 }}</span>
                <Button 
                  icon="pi pi-trash" 
                  class="p-button-sm p-button-danger" 
                  @click="removePoint(index)" 
                />
              </div>

              <div class="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <label class="block text-gray-300 mb-2">Название*</label>
                  <InputText v-model="point.name" class="w-full" />
                </div>
                <div>
                  <label class="block text-gray-300 mb-2">Порядок*</label>
                  <InputNumber 
                    v-model="point.order" 
                    class="w-full" 
                    :min="1" 
                    :max="newRoute.points.length"
                  />
                </div>
              </div>

              <div class="mb-4">
                <label class="block text-gray-300 mb-2">Описание точки</label>
                <Textarea v-model="point.description" rows="2" class="w-full" />
              </div>

              <div class="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <label class="block text-gray-300 mb-2">Широта*</label>
                  <InputNumber 
                    v-model="point.latitude" 
                     :minFractionDigits="6"
                    class="w-full" 
                    :min="-90" 
                    :max="90" 
                    :step="0.000001"
                  />
                </div>
                <div>
                  <label class="block text-gray-300 mb-2">Долгота*</label>
                  <InputNumber 
                    v-model="point.longitude" 
                    class="w-full" 
                    :minFractionDigits="6"
                    :min="-180" 
                    :max="180" 
                    :step="0.000001"
                  />
                </div>
              </div>

              <div class="mb-4">
                <label class="block text-gray-300 mb-2">Фото точки</label>
                <input 
                  type="file" 
                  accept="image/*" 
                  @change="(e) => handlePointPhoto(e, index)" 
                  class="hidden" 
                  :id="`point-photo-${index}`"
                >
                <label 
                  :for="`point-photo-${index}`" 
                  class="cursor-pointer flex items-center gap-2 text-primary"
                >
                  <i class="pi pi-upload"></i>
                  <span>{{ point.photo ? 'Изменить фото' : 'Загрузить фото' }}</span>
                </label>
                <img 
                  v-if="point.photo" 
                  :src="point.photo" 
                  class="mt-2 h-32 object-cover rounded-lg"
                >
              </div>
            </div>
          </div>
        </div>

        <small class="text-red-400">{{ createError }}</small>
      </div>

      <template #footer>
        <Button 
          label="Сохранить маршрут" 
          icon="pi pi-check" 
          :loading="isCreating" 
          @click="saveRoute" 
        />
      </template>
    </Dialog>
  </div>
</template>

<script lang="ts" setup>
definePageMeta({ middleware: 'auth' });

import { ref } from "vue";
import { format } from 'date-fns';
import { useAuthStore } from '~/stores/auth';
const { $apiFetch } = useNuxtApp()


const authStore = useAuthStore()
const user = computed(() => authStore.user);

const registrationDate = ref(format(new Date(2025, 1, 28), 'dd.MM.yyyy'));
const avatar = computed(() => authStore.user.avatar);
const defaultAvatar = "avatar.jpg";
const password = ref("");
const oldPassword = ref("");
const showEditDialog = ref(false);
const isLoading = ref(false);
const errorMessage = ref("");

async function saveProfile() {
  if (!password.value) {
    errorMessage.value = "Пароль не может быть пустым";
    return;
  }

  try {
    isLoading.value = true;
    errorMessage.value = "";

    await $apiFetch('api/auth/change_password/', {
      method: 'PATCH',
      body: { new_password: password.value, old_password: oldPassword.value}
    });

    // Сброс полей после успешного сохранения
    password.value = "";
    showEditDialog.value = false;
    useToast().add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Пароль успешно изменен',
      life: 3000
    });
  } catch (error: any) {
    errorMessage.value = error.data?.detail || 'Ошибка при изменении пароля';
  } finally {
    isLoading.value = false;
  }
}

// Маршруты
const completedRoutes = ref([
  { 
    id: 1, 
    name: "По горам", 
    description: "Красивый маршрут", 
    image: "https://via.placeholder.com/200",
    rating: 4.8,
    completedDate: new Date(2024, 2, 15),
    distance: 12.5
  },
]);

const createdRoutes = computed(() => authStore.user?.routes || []);

const favoriteRoutes = ref([
  { 
    id: 3, 
    name: "Морской берег", 
    description: "Маршрут вдоль моря", 
    image: "https://via.placeholder.com/200",
    addedDate: new Date(2024, 2, 10)
  },
]);

// Комментарии и ответы
const userComments = ref([
  {
    id: 1,
    text: 'Отличный маршрут! Рекомендую всем любителям природы.',
    date: new Date(2024, 2, 16),
    route: { id: 1, name: 'По горам' },
    replies: [
      {
        id: 11,
        text: 'Спасибо за отзыв! Рады, что вам понравилось!',
        author: 'Админ',
        date: new Date(2024, 2, 17)
      }
    ]
  }
]);

const userReplies = ref([
  {
    id: 2,
    commentId: 1,
    text: 'Ваш комментарий был отмечен как полезный',
    author: 'Модератор',
    date: new Date(2024, 2, 18),
    route: { id: 1, name: 'По горам' }
  }
]);

const totalTravelTime = ref(42);
const commentsCount = computed(() => userComments.value.length + userReplies.value.length);

function formatDate(date: Date) {
  return format(date, 'dd.MM.yyyy');
}

function getRouteImage(route: any) {
  if (route.photos?.length) {
    return route.photos[0];
  }
  return "/route-placeholder.jpg";
}

async function updateAvatar(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (!file) return;

  // Проверка размера файла
  if (file.size > 2 * 1024 * 1024) {
    useToast().add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Максимальный размер файла 2MB',
      life: 3000
    });
    return;
  }

  try {
    const formData = new FormData();
    formData.append('avatar', file);

    // Отправка файла
    const response = await $apiFetch('api/auth/change_avatar/', {
      method: 'POST',
      body: formData
    });

    // Обновление аватара в хранилище и локально
    authStore.user.avatar = URL.createObjectURL(file); // или response.data.avatar_url в зависимости от структуры ответа
    avatar.value = URL.createObjectURL(file);
    useToast().add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Аватар обновлён',
      life: 3000
    });

  } catch (error: any) {
    console.error('Ошибка загрузки аватара:', error);
    useToast().add({
      severity: 'error',
      summary: 'Ошибка',
      detail: error.data?.message || 'Не удалось обновить аватар',
      life: 3000
    });
  }
}

function editRoute(route: any) {
  console.log('Редактировать маршрут', route);
}

function deleteRoute(route: any) {
  console.log('Удалить маршрут', route);
}

function showOriginalComment(reply: any) {
  const comment = userComments.value.find(c => c.id === reply.commentId);
  if (comment) {
    // Логика показа комментария
  }
}

const showCreateDialog = ref(false);
const isCreating = ref(false);
const createError = ref('');

const newRoute = ref({
  name: '',
  type: 'public',
  description: '',
  points: [] as Array<{
    name: string;
    description: string;
    latitude: number | null;
    longitude: number | null;
    order: number;
    photo: string;
  }>,
  published: false
});

function addPoint() {
  newRoute.value.points.push({
    name: '',
    description: '',
    latitude: null,
    longitude: null,
    order: newRoute.value.points.length + 1,
    photo: ''
  });
}

function removePoint(index: number) {
  newRoute.value.points.splice(index, 1);
}

async function handlePointPhoto(event: Event, pointIndex: number) {
  const file = (event.target as HTMLInputElement).files?.[0];
  if (!file) return;

  if (file.size > 2 * 1024 * 1024) {
    useToast().add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Максимальный размер файла 2MB',
      life: 3000
    });
    return;
  }

  try {
    const reader = new FileReader();
    reader.onload = (e) => {
      if (e.target?.result) {
        newRoute.value.points[pointIndex].photo = e.target.result as string;
      }
    };
    reader.readAsDataURL(file);
  } catch (error) {
    console.error('Ошибка чтения файла:', error);
    useToast().add({
      severity: 'error',
      summary: 'Ошибка',
      detail: 'Не удалось загрузить фото',
      life: 3000
    });
  }
}

async function saveRoute() {
  try {
    isCreating.value = true;
    createError.value = '';

    // Валидация
    if (!newRoute.value.name.trim()) {
      createError.value = 'Название маршрута обязательно';
      return;
    }

    if (newRoute.value.points.length < 2) {
      createError.value = 'Добавьте минимум 2 точки';
      return;
    }

    for (const [index, point] of newRoute.value.points.entries()) {
      if (!point.name.trim()) {
        createError.value = `Название точки #${index + 1} обязательно`;
        return;
      }
      if (point.latitude === null || point.longitude === null) {
        createError.value = `Заполните координаты для точки #${index + 1}`;
        return;
      }
    }

    // Подготовка данных
    const routeData = {
      ...newRoute.value,
      points: newRoute.value.points.map(point => {
        const { photo, ...rest } = point;
        return {
          ...rest,
          ...(photo ? { photo } : {})
        };
      })
    };

    // Отправка данных
    const response = await $apiFetch('api/routes/create_route/', {
      method: 'POST',
      body: routeData,
      headers: {
        'Content-Type': 'application/json' // правильный заголовок для JSON
      }
    });

    // Обновление данных
    authStore.user.routes = [...authStore.user.routes, response];
    
    useToast().add({
      severity: 'success',
      summary: 'Успех',
      detail: 'Маршрут успешно создан!',
      life: 3000
    });

    showCreateDialog.value = false;
    resetForm();

  } catch (err) {
    // console.error('Ошибка создания маршрута:', err);
    // createError.value = err.data?.detail || 'Ошибка при создании маршрута';
  } finally {
    isCreating.value = false;
  }
}

function resetForm() {
  newRoute.value = {
    name: '',
    type: 'public',
    description: '',
    points: [],
    published: false
  };
}

function createRoute() {
  showCreateDialog.value = true;
  resetForm();
}
</script>

<style>
.pi-camera {
  transition: transform 0.2s;
}
.group:hover .pi-camera {
  transform: scale(1.2);
}
</style>
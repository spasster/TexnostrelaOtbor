<template>
  <div class="flex h-screen items-center justify-center bg-gray-900">
    <div class="w-96 p-6 bg-gray-800 rounded-lg shadow-lg relative">
      <NuxtLink to="/" class="absolute top-4 left-4 text-gray-400 hover:text-white">
        <i class="pi pi-home text-xl"></i>
      </NuxtLink>
      <h2 class="text-white text-2xl font-bold text-center">Регистрация</h2>
      <form class="mt-6 space-y-4" @submit.prevent="handleRegister">
        <div class="relative">
          <InputText v-model="credentials.email" class="w-full p-3 rounded" placeholder="Email" />
          <i class="pi pi-envelope absolute top-1/2 right-3 text-gray-500 transform -translate-y-1/2"></i>
        </div>
        <div class="relative">
          <InputText :type="showPassword ? 'text' : 'password'" v-model="credentials.password" class="w-full p-3 rounded" placeholder="Пароль" />
          <i 
            class="pi absolute top-1/2 right-3 text-gray-500 transform -translate-y-1/2 cursor-pointer"
            :class="showPassword ? 'pi-eye-slash' : 'pi-eye'" 
            @click="showPassword = !showPassword"
          ></i>
        </div>
        <div v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</div>
        <Button :loading="loading" label="Зарегестрироваться" type="submit" class="w-full mt-2" />
      </form>
      <p class="text-gray-400 text-center mt-4">
        Есть аккаунта? <NuxtLink to="/login" class="text-blue-400 hover:underline">Вход</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: false
})
import { useAuthStore } from '~/stores/auth';

const authStore = useAuthStore();;
const showPassword = ref(false);
const errorMessage = ref('');
const loading = ref(false);
const credentials = ref({
  email: '',
  password: '',
});

async function handleRegister() {
  errorMessage.value = '';

  loading.value = true;
  try {
    await authStore.register(credentials.value);
    navigateTo('/profile');
  } catch (error) {
    errorMessage.value = 'Неверные данные!';
  } finally {
    loading.value = false;
  }
}
</script>

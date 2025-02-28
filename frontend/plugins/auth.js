import { useAuthStore } from '~/stores/auth';

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore();
  authStore.initAuth();

  if (authStore.refreshToken) {
    await authStore.refreshAccessToken();
    await authStore.getUserInfo();
  }
});

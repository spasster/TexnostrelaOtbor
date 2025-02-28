import { useAuthStore } from '~/stores/auth';

export default defineNuxtPlugin((nuxtApp) => {
  const authStore = useAuthStore();

  nuxtApp.hook('app:created', () => {
    const originalFetch = $fetch.create({
      onRequest({ options }) {
        if (authStore.accessToken) {
          options.headers = {
            ...options.headers,
            Authorization: `Bearer ${authStore.accessToken}`,
          };
          options.baseURL = "http://127.0.0.1:8000"
        }
      },

      onResponseError({ response }) {
        if (response.status === 401) {
          authStore.logout();
          navigateTo('/login');
        }
      },
    });

    nuxtApp.provide('apiFetch', originalFetch);
  });
});

import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    accessToken: null,
    refreshToken: null,
  }),

  actions: {
    initAuth() {
      const accessCookie = useCookie('access_token');
      const refreshCookie = useCookie('refresh_token');

      this.accessToken = accessCookie.value || null;
      this.refreshToken = refreshCookie.value || null;
    },

    async login(credentials) {
      try {
        const response = await $fetch('/api/auth/login/', {
          baseURL: "http://127.0.0.1:8000",
          method: 'POST',
          body: credentials,
        });

        const accessCookie = useCookie('access_token');
        const refreshCookie = useCookie('refresh_token');

        accessCookie.value = response.access;
        refreshCookie.value = response.refresh;

        this.accessToken = response.access;
        this.refreshToken = response.refresh;

        await this.getUserInfo();
      } catch (error) {
        console.error('Ошибка авторизации:', error);
        throw error;
      }
    },

    async register(credentials) {
      try {
        await $fetch('/api/auth/register/', {
          baseURL: "http://127.0.0.1:8000",
          method: 'POST',
          body: credentials,
        });

        await this.login(credentials);
      } catch (error) {
        console.error('Ошибка регистрации:', error);
        throw error;
      }
    },

    async getUserInfo() {
      if (!this.accessToken) return;

      try {
        this.user = await $fetch('/api/auth/user_info/', {
          baseURL: "http://127.0.0.1:8000",
          headers: { Authorization: `Bearer ${this.accessToken}` },
        });
        this.user.avatar = 'http://127.0.0.1:8000' + this.user.avatar
        
      } catch (error) {
        console.error('Ошибка получения данных пользователя:', error);
        this.logout();
      }
    },

    async refreshAccessToken() {
      if (!this.refreshToken) return;

      try {
        const response = await $fetch('/api/auth/refresh/', {
          baseURL: "http://127.0.0.1:8000",
          method: 'POST',
          body: { refresh: this.refreshToken },
        });

        const accessCookie = useCookie('access_token');
        accessCookie.value = response.access;
        this.accessToken = response.access;
      } catch (error) {
        console.error('Ошибка обновления токена:', error);
        this.logout();
      }
    },

    logout() {
      const accessCookie = useCookie('access_token');
      const refreshCookie = useCookie('refresh_token');

      accessCookie.value = null;
      refreshCookie.value = null;

      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;
    },
  },
});

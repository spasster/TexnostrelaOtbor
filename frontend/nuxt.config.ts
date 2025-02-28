// https://nuxt.com/docs/api/configuration/nuxt-config

import Aura from '@primeuix/themes/aura';

export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: false },
  ssr: false,
  modules: [
    '@nuxtjs/tailwindcss',
    '@primevue/nuxt-module',
    '@pinia/nuxt',
    '@formkit/auto-animate/nuxt',
    'nuxt-mapbox'
  ],
  app: {
    head: {
      script: [
        { src: 'https://mapgl.2gis.com/api/js/v1', async: true, defer: true },
        { src: 'https://unpkg.com/@2gis/mapgl-directions@^2/dist/directions.js', async: true, defer: true },
      ],
    },
  },
  primevue: {
    options: {
        theme: {
            preset: Aura
        }
    }
  },
  auth: {
    baseURL: process.env.AUTH_ORIGIN || 'http://127.0.0.1:8000',
    provider: {
      type: 'authjs',
      endpoints: {
        signIn: { url: '/api/auth/login/', method: 'post' },
        signOut: { url: '/api/auth/logout/', method: 'post' },
        getSession: { url: '/api/auth/verify/', method: 'post' }
      },
      token: {
        signInResponseTokenPointer: '/access',
        maxAgeInSeconds: 60 * 15, // 15 минут
      },
      refreshToken: {
        signInResponseRefreshTokenPointer: '/refresh',
        maxAgeInSeconds: 60 * 60 * 24 * 7 // 7 дней
      }
    },
    session: {
      enableRefreshPeriodically: true,
      enableRefreshOnWindowFocus: true
    },
    globalAppMiddleware: true
  },
  css: [
    'primeicons/primeicons.css',
    '~/assets/css/main.css',
    '~/assets/css/tailwind.css',
    'leaflet/dist/leaflet.css',
    'leaflet-routing-machine/dist/leaflet-routing-machine.css'
  ]
})
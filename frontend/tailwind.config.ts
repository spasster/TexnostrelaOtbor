import type { Config } from 'tailwindcss'

export default <Partial<Config>>{
  content: [
    './pages/*.vue',
    './components/*.vue',
    './layouts/*.vue'
  ],
  theme: {
    extend: {
      colors: {
      }
    }
  }
}

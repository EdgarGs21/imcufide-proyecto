// vite.config.js
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        ligaFutbol: resolve(__dirname, 'liga-futbol.html'),
        // CORRECCIÓN AQUÍ:
        categoriaJuvenilA: resolve(__dirname, 'liga-juvenil-a.html'),
      },
    },
  },
})
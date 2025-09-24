// vite.config.js
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        ligaFutbol: resolve(__dirname, 'liga-futbol.html'),
        categoriaJuvenilA: resolve(__dirname, 'categoria-juvenil-a.html'),
        // --- AÑADE AQUÍ CUALQUIER OTRA PÁGINA HTML QUE CREES ---
      },
    },
  },
})
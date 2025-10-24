// vite.config.js
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        ligaFutbol: resolve(__dirname, 'liga-futbol.html'),
        categoriaJuvenilA: resolve(__dirname, 'liga-juvenil-a.html'), // Esta ya estaba
        // --- AÑADE ESTAS DOS LÍNEAS ---
        ligaJuvenilB: resolve(__dirname, 'liga-juvenil-b.html'),
        ligaInfantil: resolve(__dirname, 'liga-infantil.html'),
        // ---------------------------------
      },
    },
  },
})
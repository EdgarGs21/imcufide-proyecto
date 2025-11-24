// vite.config.js
import { resolve } from 'path'
import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        ligaFutbol: resolve(__dirname, 'liga-futbol.html'),
        categoriaPreparatoria: resolve(__dirname, 'liga-preparatoria.html'),
        ligaSecundaria: resolve(__dirname, 'liga-secundaria.html'),
        ligaPrimaria: resolve(__dirname, 'liga-primaria.html'),
        proximamente: resolve(__dirname, 'proximamente.html'),
        quienesSomos: resolve(__dirname, 'quienes-somos.html'),

        // ---------------------------------
      },
    },
  },
})
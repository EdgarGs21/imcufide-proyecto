<template>
  <div class="container">
    <!-- Mensaje de carga -->
    <div v-if="loading" class="d-flex justify-content-center my-5">
      <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;" role="status">
        <span class="visually-hidden">Cargando...</span>
      </div>
    </div>

    <!-- Mensaje de error -->
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <!-- Fila de botones de deportes -->
    <div v-if="deportes.length > 0" class="row justify-content-center g-3">
      <div v-for="deporte in deportes" :key="deporte.id" class="col-6 col-md-4 col-lg-2">
        <button class="btn btn-light p-4 w-100 h-100 shadow-sm">
          <i :class="getIcono(deporte.nombre)" style="font-size: 2.5rem;"></i>
          <span class="d-block mt-2">{{ deporte.nombre }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const deportes = ref([])
const loading = ref(true)
const error = ref(null)

const API_URL = 'https://imcufide-api.onrender.com'

// Función para asignar un ícono según el nombre del deporte
const getIcono = (nombre) => {
  const nombreNormalizado = nombre.toLowerCase();
  if (nombreNormalizado.includes('fútbol')) return 'bi bi- ফুটবল';
  if (nombreNormalizado.includes('básquetbol')) return 'bi bi-basketball';
  if (nombreNormalizado.includes('tenis')) return 'bi bi-circle-fill'; // No hay ícono de tenis en BS
  // Añade más casos aquí
  return 'bi bi-trophy'; // Un ícono por defecto
}

onMounted(async () => {
  try {
    const response = await axios.get(`${API_URL}/deportes/`)
    deportes.value = response.data
  } catch (err) {
    error.value = 'Error al cargar los deportes.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>
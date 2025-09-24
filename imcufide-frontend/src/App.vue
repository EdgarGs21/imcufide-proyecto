<template>
  <!-- Navbar superior (la dejaremos simple por ahora) -->
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm">
    <div class="container">
      <a class="navbar-brand" href="#">IMCUFIDE Tenango</a>
      <div class="navbar-nav">
        <a class="nav-link active" href="#">Inicio</a>
        <a class="nav-link" href="#">¿Quiénes somos?</a>
      </div>
    </div>
  </nav>

  <!-- Contenido principal -->
  <main class="container text-center mt-5">
    <!-- Logo (usaremos un placeholder por ahora) -->
    <img src="https://via.placeholder.com/150" alt="Logo IMCUFIDE" class="mb-4">

    <h1 class="display-5">Ligas de Desarrollo Tennango</h1>
    <p class="lead text-muted mb-5">
      Elige tu deporte y conoce los próximos partidos.
    </p>

    <!-- Aquí se cargará nuestra lista de deportes -->
    <DeportesList />
  </main>

</template>

<script setup>
import DeportesList from './components/DeportesList.vue'
</script>

<style>
  /* Podemos añadir estilos globales aquí si es necesario */
  body {
    background-color: #f8f9fa; /* Un gris muy claro */
  }
</style>
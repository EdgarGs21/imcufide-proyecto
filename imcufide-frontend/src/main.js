// src/main.js

// Importamos los datos de nuestro archivo de banners (para index.html)
import { bannersData } from './banners.js';

// Espera a que todo el contenido de la página se cargue
document.addEventListener('DOMContentLoaded', () => {

    // --- LÓGICA DEL HEADER (Se ejecuta en todas las páginas) ---
    const header = document.querySelector('.main-header');
    if (header) {
        const handleScroll = () => {
            if (window.scrollY > 50) {
                header.classList.add('header-scrolled');
            } else {
                header.classList.remove('header-scrolled');
            }
        };
        window.addEventListener('scroll', handleScroll);
    }

    // --- LÓGICA PARA EL CARRUSEL DEL BANNER (Solo para index.html) ---
    const bannerContainer = document.getElementById('banner-container');
    if (bannerContainer && bannersData) {
        let currentBannerIndex = 0;
        
        function showBanner(index) {
            const banner = bannersData[index];
            bannerContainer.innerHTML = `
                <div class="banner-slide" style="background-image: url('${banner.imagen}');">
                    <div class="banner-content fade-in">
                        <h1 class="banner-title">${banner.titulo}</h1>
                        <p class="banner-subtitle">${banner.subtitulo}</p>
                        <a href="${banner.enlace}" class="btn-banner">Ver más</a>
                    </div>
                </div>
            `;
        }
        function nextBanner() {
            currentBannerIndex = (currentBannerIndex + 1) % bannersData.length;
            showBanner(currentBannerIndex);
        }
        showBanner(currentBannerIndex);
        setInterval(nextBanner, 5000);
    }

    // --- LÓGICA PARA LAS PESTAÑAS (Tabs) ---
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabPanes = document.querySelectorAll('.tab-pane');
    if (tabLinks.length > 0) {
        tabLinks.forEach(link => {
            link.addEventListener('click', () => {
                const tabId = link.getAttribute('data-tab');

                tabLinks.forEach(item => item.classList.remove('active'));
                tabPanes.forEach(pane => pane.classList.remove('active'));

                const activePane = document.getElementById(tabId);
                link.classList.add('active');
                activePane.classList.add('active');
            });
        });
    }

    // --- LÓGICA PARA CARGAR EL CALENDARIO DE PARTIDOS ---
    const calendarioTabla = document.querySelector('.match-calendar');
    if (calendarioTabla) {
        const cuerpoTabla = calendarioTabla.querySelector('tbody');
        const urlApiPartidos = 'https://imcufide-proyecto.onrender.com/partidos/publico/';

        fetch(urlApiPartidos)
            .then(response => {
                if (!response.ok) throw new Error('Error en la respuesta de la API');
                return response.json();
            })
            .then(partidos => {
                cuerpoTabla.innerHTML = ''; // Limpiamos la tabla de ejemplo

                if (partidos.length === 0) {
                    cuerpoTabla.innerHTML = '<tr><td colspan="5">No hay partidos programados por el momento.</td></tr>';
                    return;
                }

                partidos.forEach(partido => {
                    const fila = document.createElement('tr');
                    const fechaFormateada = new Date(partido.fecha + 'T00:00:00').toLocaleDateString('es-MX', {
                        day: '2-digit', month: 'long', year: 'numeric'
                    });
                    
                    fila.innerHTML = `
                        <td>${fechaFormateada}</td>
                        <td>${partido.equipo_local_nombre}</td>
                        <td>${partido.equipo_visitante_nombre}</td>
                        <td>${partido.sede_nombre}</td>
                        <td>${partido.marcador_local !== null ? partido.marcador_local : '-'} - ${partido.marcador_visitante !== null ? partido.marcador_visitante : '-'}</td>
                    `;
                    cuerpoTabla.appendChild(fila);
                });
            })
            .catch(error => {
                console.error('Hubo un problema al obtener los partidos:', error);
                cuerpoTabla.innerHTML = '<tr><td colspan="5">No se pudo cargar el calendario. Por favor, intente más tarde.</td></tr>';
            });
    }

});
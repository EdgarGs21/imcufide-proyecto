// src/main.js

// Importamos los datos de nuestro archivo de banners (para index.html)
import { bannersData } from './banners.js';

// Espera a que todo el contenido de la página se cargue
document.addEventListener('DOMContentLoaded', () => {
    
    // --- LÓGICA DEL HEADER (CON OCULTAMIENTO AUTOMÁTICO) ---
    const header = document.querySelector('.main-header');
    if (header) {
        let lastScrollY = window.scrollY; // Guardamos la posición inicial

        const handleScroll = () => {
            const currentScrollY = window.scrollY;

            // Le damos un pequeño margen (más de 5px) para evitar activaciones accidentales
            if (currentScrollY > lastScrollY && currentScrollY > 50) {
                // Si bajamos, escondemos el header
                header.classList.add('header-hidden');
            } else {
                // Si subimos, lo mostramos
                header.classList.remove('header-hidden');
            }
            // Actualizamos la última posición del scroll
            lastScrollY = currentScrollY;
        };

        window.addEventListener('scroll', handleScroll);
    }

// --- LÓGICA PARA EL NUEVO CARRUSEL (CON LOOP INFINITO) ---
const carouselContainer = document.querySelector('.carousel-container');
if (carouselContainer && bannersData && bannersData.length > 0) {
    const track = carouselContainer.querySelector('.carousel-track');
    const nav = carouselContainer.querySelector('.carousel-nav');
    
    // 1. Poblar el carrusel con las imágenes y los puntos
    bannersData.forEach((banner, index) => {
        const slide = document.createElement('div');
        slide.classList.add('carousel-slide');
        slide.innerHTML = `<img src="${banner.imagen}" alt="${banner.titulo}">`;
        track.appendChild(slide);

        const dot = document.createElement('button');
        dot.classList.add('carousel-indicator');
        if (index === 0) dot.classList.add('active');
        dot.dataset.index = index;
        nav.appendChild(dot);
    });

    // 2. Crear los clones para el loop infinito
    const firstClone = track.firstElementChild.cloneNode(true);
    const lastClone = track.lastElementChild.cloneNode(true);
    track.appendChild(firstClone);
    track.insertBefore(lastClone, track.firstElementChild);

    const slides = Array.from(track.children);
    const dots = Array.from(nav.children);
    const slideWidth = slides[0].getBoundingClientRect().width;
    let currentSlideIndex = 1; // Empezamos en la primera imagen REAL, no en el clon

    // 3. Posición inicial del carrusel
    track.style.transform = `translateX(-${slideWidth * currentSlideIndex}px)`;

    const updateDots = (targetIndex) => {
        dots.forEach(dot => dot.classList.remove('active'));
        // Ajustamos el índice para los clones
        if (targetIndex === 0) {
            dots[dots.length - 1].classList.add('active');
        } else if (targetIndex === slides.length - 1) {
            dots[0].classList.add('active');
        } else {
            dots[targetIndex - 1].classList.add('active');
        }
    };

    const moveToSlide = () => {
        track.style.transition = 'transform 0.5s ease-in-out';
        track.style.transform = `translateX(-${slideWidth * currentSlideIndex}px)`;
        updateDots(currentSlideIndex);
    };

    // 4. Lógica para el movimiento automático
    const goToNextSlide = () => {
        if (currentSlideIndex >= slides.length - 1) return; // Previene múltiples saltos
        currentSlideIndex++;
        moveToSlide();
    };

    // 5. El "Salto Mágico"
    track.addEventListener('transitionend', () => {
        if (currentSlideIndex === slides.length - 1) { // Si estamos en el clon del final
            track.style.transition = 'none'; // Desactivamos la animación
            currentSlideIndex = 1; // Saltamos a la primera imagen real
            track.style.transform = `translateX(-${slideWidth * currentSlideIndex}px)`;
        }
    });

    // Lógica de los puntos
    nav.addEventListener('click', e => {
        const targetDot = e.target.closest('button');
        if (!targetDot) return;
        currentSlideIndex = parseInt(targetDot.dataset.index) + 1; // +1 por el clon inicial
        moveToSlide();
    });

    // Iniciar el intervalo automático
    setInterval(goToNextSlide, 4500);
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
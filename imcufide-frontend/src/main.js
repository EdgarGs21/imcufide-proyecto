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
    if (tabLinks.length > 0) { // <-- Asegúrate de que todo este bloque exista
        tabLinks.forEach(link => {
            link.addEventListener('click', () => {
                const tabId = link.getAttribute('data-tab');

                // Oculta todos los contenidos y quita la clase activa de los enlaces
                tabLinks.forEach(item => item.classList.remove('active'));
                tabPanes.forEach(pane => pane.classList.remove('active'));

                // Muestra el contenido y activa el enlace correspondiente
                const activePane = document.getElementById(tabId);
                link.classList.add('active');
                if (activePane) { // Añade una verificación si el panel existe
                   activePane.classList.add('active');
                }
            });
        });
    }

    // --- LÓGICA PARA CARGAR EL CALENDARIO DE PARTIDOS ---
  const gameListContainer = document.querySelector('.game-list-container');
const calendarGridElement = document.querySelector('.calendar-grid');

if (gameListContainer && calendarGridElement) {
    const gameList = gameListContainer.querySelector('.game-list');
    const monthYearTitle = document.getElementById('calendar-month-year');
    const daysGrid = calendarGridElement.querySelector('.days-grid');
    const prevMonthButton = calendarGridElement.querySelector('.prev-month');
    const nextMonthButton = calendarGridElement.querySelector('.next-month');
    const gameListTitle = gameListContainer.querySelector('h4'); // Buscamos el título "Próximos Partidos"

    const urlApiPartidos = 'https://imcufide-proyecto.onrender.com/partidos/publico/';
    let allPartidos = [];
    let currentDate = new Date();

    // --- FUNCIONES PARA EL CALENDARIO VISUAL ---
    function renderCalendar(date, selectedDate = null) { // selectedDate es la fecha clickeada
        daysGrid.innerHTML = '';
        const year = date.getFullYear();
        const month = date.getMonth();
        monthYearTitle.textContent = date.toLocaleDateString('es-MX', { month: 'long', year: 'numeric' });
        const firstDayOfMonth = new Date(year, month, 1).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const today = new Date(); today.setHours(0,0,0,0);

        // Días mes anterior
        for (let i = 0; i < firstDayOfMonth; i++) { /* ... código para días anteriores ... */
             const dayCell = document.createElement('div');
             dayCell.classList.add('day-cell', 'past');
             daysGrid.appendChild(dayCell);
         }

        // Días mes actual
        for (let day = 1; day <= daysInMonth; day++) {
            const dayCell = document.createElement('div');
            dayCell.classList.add('day-cell');
            dayCell.textContent = day;
            dayCell.dataset.date = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`; // Guardamos la fecha ISO

            const currentDayDate = new Date(year, month, day); currentDayDate.setHours(0,0,0,0);

            if (currentDayDate.getTime() === today.getTime()) dayCell.classList.add('today');

            // Marcar día seleccionado
            if (selectedDate && currentDayDate.getTime() === selectedDate.getTime()) {
                dayCell.classList.add('selected-day');
            }

            const hasGame = allPartidos.some(partido => partido.fecha === dayCell.dataset.date);
            if (hasGame) dayCell.classList.add('has-game');

            daysGrid.appendChild(dayCell);
        }
    }

    // --- FUNCIÓN PARA MOSTRAR PARTIDOS EN LA LISTA ---
    function renderGameList(partidosToShow, title = "Próximos Partidos") {
         gameListTitle.textContent = title; // Actualizar título de la lista
         gameList.innerHTML = '';

         if (!partidosToShow || partidosToShow.length === 0) {
             gameList.innerHTML = `<div class="game-item-placeholder">No hay partidos ${title === "Próximos Partidos" ? 'programados' : 'para esta fecha'}.</div>`;
             return;
         }

         partidosToShow.forEach(partido => {
             // ... (código para crear y añadir .game-item como lo teníamos) ...
             const gameItem = document.createElement('div');
             gameItem.classList.add('game-item');
             const dateTimeString = `${partido.fecha}T${partido.hora}`;
             const gameDate = new Date(dateTimeString);
             const fechaFormateada = !isNaN(gameDate) ? gameDate.toLocaleDateString('es-MX', { month: 'long', day: 'numeric', year: 'numeric' }) : 'Fecha inválida';
             const horaFormateada = !isNaN(gameDate) ? gameDate.toLocaleTimeString('es-MX', { hour: 'numeric', minute: '2-digit', hour12: true }) : 'Hora inválida';
             gameItem.innerHTML = `
                 <div class="game-info">
                     <strong>${partido.equipo_local_nombre} vs ${partido.equipo_visitante_nombre}</strong>
                     <p>${partido.sede_nombre}</p>
                 </div>
                 <div class="game-time">
                     <p>${fechaFormateada}</p>
                     <span>${horaFormateada}</span>
                 </div>
             `;
             gameList.appendChild(gameItem);
         });
    }

    // --- CARGA INICIAL DE DATOS ---
    fetch(urlApiPartidos)
        .then(response => { /* ... código fetch ... */
             if (!response.ok) throw new Error('Error en la respuesta de la API: ' + response.statusText);
             return response.json();
         })
        .then(partidos => {
            allPartidos = partidos;
            renderCalendar(currentDate); // Render calendario inicial

            // Filtrar y mostrar próximos partidos al cargar
            const hoy = new Date(); hoy.setHours(0, 0, 0, 0);
            const proximosPartidos = allPartidos
                .filter(partido => new Date(partido.fecha + 'T00:00:00') >= hoy)
                .sort((a, b) => new Date(a.fecha + 'T' + a.hora) - new Date(b.fecha + 'T' + b.hora));
            renderGameList(proximosPartidos, "Próximos Partidos");
        })
        .catch(error => { /* ... código catch ... */
             console.error('Hubo un problema al obtener los partidos:', error);
             gameList.innerHTML = '<div class="game-item-placeholder">No se pudo cargar el calendario.</div>';
             monthYearTitle.textContent = 'Error al cargar';
             daysGrid.innerHTML = '<div style="grid-column: 1 / -1; color: red;">No se pudo conectar.</div>';
         });

    // --- EVENT LISTENERS PARA NAVEGACIÓN Y CLICS EN DÍAS ---
    prevMonthButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });
    nextMonthButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    daysGrid.addEventListener('click', (event) => {
        const clickedDay = event.target.closest('.day-cell:not(.past)'); // Solo días del mes actual
        if (!clickedDay || !clickedDay.dataset.date) return; // Si no es un día válido, salir

        const selectedDateISO = clickedDay.dataset.date;
        const selectedDateObj = new Date(selectedDateISO + 'T00:00:00');

        // Filtrar partidos para la fecha seleccionada
        const partidosDelDia = allPartidos.filter(partido => partido.fecha === selectedDateISO);

        // Actualizar la lista de partidos
        const title = `Partidos del ${selectedDateObj.toLocaleDateString('es-MX', {day: 'numeric', month: 'long'})}`;
        renderGameList(partidosDelDia, title);

        // Volver a renderizar el calendario resaltando el día seleccionado
        renderCalendar(currentDate, selectedDateObj);
    });
}
});
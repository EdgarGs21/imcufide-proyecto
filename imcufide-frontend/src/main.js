// src/main.js

import { bannersData } from './banners.js';

document.addEventListener('DOMContentLoaded', () => {
    
    // --- LÓGICA DEL HEADER (CON OCULTAMIENTO AUTOMÁTICO) ---
    const header = document.querySelector('.main-header');
    if (header) {
        let lastScrollY = window.scrollY; 
        const handleScroll = () => {
            const currentScrollY = window.scrollY;
            if (currentScrollY > lastScrollY && currentScrollY > 50) {
                header.classList.add('header-hidden');
            } else {
                header.classList.remove('header-hidden');
            }
            lastScrollY = currentScrollY;
        };
        window.addEventListener('scroll', handleScroll);
    }

    // --- LÓGICA PARA EL CARRUSEL DE BANNERS (index.html) ---
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer && bannersData && bannersData.length > 0) {
        const track = carouselContainer.querySelector('.carousel-track');
        const nav = carouselContainer.querySelector('.carousel-nav');
        let slides = [];
        let dots = [];
        let currentSlideIndex = 1;

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

        const firstClone = track.firstElementChild.cloneNode(true);
        const lastClone = track.lastElementChild.cloneNode(true);
        track.appendChild(firstClone);
        track.insertBefore(lastClone, track.firstElementChild);

        slides = Array.from(track.children);
        dots = Array.from(nav.children);
        const slideWidth = slides.length > 0 ? slides[0].getBoundingClientRect().width : 0;
        
        track.style.transform = `translateX(-${slideWidth * currentSlideIndex}px)`;

        const updateDots = (targetIndex) => {
            dots.forEach(dot => dot.classList.remove('active'));
            let activeDotIndex = targetIndex - 1;
            if (targetIndex === 0) activeDotIndex = dots.length - 1;
            if (targetIndex === slides.length - 1) activeDotIndex = 0;
            if (dots[activeDotIndex]) dots[activeDotIndex].classList.add('active'); // Safety check
        };

        const moveToSlide = () => {
            if (!track) return;
            track.style.transition = 'transform 0.5s ease-in-out';
            track.style.transform = `translateX(-${slideWidth * currentSlideIndex}px)`;
            updateDots(currentSlideIndex);
        };

        const goToNextSlide = () => {
            if (currentSlideIndex >= slides.length - 1) return; 
            currentSlideIndex++;
            moveToSlide();
        };

        track.addEventListener('transitionend', () => {
             if (!track) return;
            if (currentSlideIndex === slides.length - 1) {
                track.style.transition = 'none';
                currentSlideIndex = 1;
                track.style.transform = `translateX(-${slideWidth * currentSlideIndex}px)`;
            }
             if (currentSlideIndex === 0) {
                 track.style.transition = 'none';
                 currentSlideIndex = slides.length - 2;
                 track.style.transform = `translateX(-${slideWidth * currentSlideIndex}px)`;
             }
        });

        nav.addEventListener('click', e => {
            const targetDot = e.target.closest('button');
            if (!targetDot) return;
            currentSlideIndex = parseInt(targetDot.dataset.index) + 1;
            moveToSlide();
        });

        setInterval(goToNextSlide, 4500);
    }

    // --- LÓGICA PARA LAS PESTAÑAS (Tabs) ---
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabPanes = document.querySelectorAll('.tab-pane');
    if (tabLinks.length > 0 && tabPanes.length > 0) {
        tabLinks.forEach(link => {
            link.addEventListener('click', () => {
                const tabId = link.getAttribute('data-tab');

                tabLinks.forEach(item => item.classList.remove('active'));
                tabPanes.forEach(pane => pane.classList.remove('active'));

                const activePane = document.getElementById(tabId);
                link.classList.add('active');
                if (activePane) {
                    activePane.classList.add('active');

                    // Lógica para cargar Equipos al hacer clic
                    if (tabId === 'tab-3' && !activePane.dataset.loaded) { 
                        cargarEquiposYPlantillas(activePane);
                        activePane.dataset.loaded = 'true'; 
                    }
                }
            });
        });
        // Asegurar que el contenido de la pestaña activa inicial sea visible
        const initiallyActiveLink = document.querySelector('.tab-link.active');
        if(initiallyActiveLink){
            const initialTabId = initiallyActiveLink.getAttribute('data-tab');
            const initialActivePane = document.getElementById(initialTabId);
            if(initialActivePane) initialActivePane.classList.add('active');
        }
    }

    // --- FUNCIÓN PARA CARGAR EQUIPOS Y PLANTILLAS ---
    function cargarEquiposYPlantillas(targetPane) {
        const teamsContainer = targetPane.querySelector('.teams-container');
        if (!teamsContainer) return;

        teamsContainer.innerHTML = '<p>Cargando equipos...</p>'; 

        // --- DETECCIÓN AUTOMÁTICA DEL ID DE CATEGORÍA ---
        let categoriaId = null;
        const pageName = window.location.pathname.split('/').pop(); 

        if (pageName === 'liga-juvenil-a.html') {
            categoriaId = 3; // ¡VERIFICA ESTE ID EN SUPABASE!
        } else if (pageName === 'liga-juvenil-b.html') {
            categoriaId = 2; // ¡VERIFICA ESTE ID EN SUPABASE!
        } else if (pageName === 'liga-infantil.html') {
            categoriaId = 1; // ¡VERIFICA ESTE ID EN SUPABASE!
        }

        if (!categoriaId) { 
            console.error("No se pudo determinar el ID de la categoría para esta página:", pageName);
            teamsContainer.innerHTML = '<p>Error al cargar la categoría.</p>';
            return;
        }
        // --- FIN DE LA DETECCIÓN ---

        const urlApiEquipos = `https://imcufide-proyecto.onrender.com/equipos/categoria/${categoriaId}/plantillas/`;

        fetch(urlApiEquipos)
            .then(response => {
                if (!response.ok) throw new Error('Error en API de equipos: ' + response.statusText);
                return response.json();
            })
            .then(equipos => {
                teamsContainer.innerHTML = ''; 

                if (!equipos || equipos.length === 0) {
                    teamsContainer.innerHTML = '<p>No hay equipos registrados en esta categoría.</p>';
                    return;
                }

                equipos.forEach(equipo => {
                    const teamCard = document.createElement('article');
                    teamCard.classList.add('team-card');

                    let jugadoresHtml = '';
                    if (equipo.jugadores && equipo.jugadores.length > 0) {
                        equipo.jugadores.forEach(jugador => {
                            jugadoresHtml += `
                                <tr>
                                    <td>${jugador.dorsal !== null ? jugador.dorsal : '-'}</td>
                                    <td>${jugador.nombre}</td>
                                    <td>${jugador.posicion || '-'}</td>
                                </tr>
                            `;
                        });
                    } else {
                        jugadoresHtml = '<tr><td colspan="3">No hay jugadores registrados.</td></tr>';
                    }

                    teamCard.innerHTML = `
                        <header class="team-card-header">
                            <img src="${equipo.escudo || './src/assets/icons/equipo-placeholder.png'}" alt="Escudo de ${equipo.nombre}" class="team-shield">
                            <h2>${equipo.nombre}</h2>
                        </header>
                        <table class="roster-table">
                            <thead>
                                <tr>
                                    <th>Dorsal</th>
                                    <th>Nombre</th>
                                    <th>Posición</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${jugadoresHtml}
                            </tbody>
                        </table>
                    `;
                    teamsContainer.appendChild(teamCard);
                });
            })
            .catch(error => {
                console.error('Error al obtener equipos:', error);
                teamsContainer.innerHTML = '<p>No se pudo cargar la información de los equipos.</p>';
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
        const gameListTitle = gameListContainer.querySelector('h4'); 

        const urlApiPartidos = 'https://imcufide-proyecto.onrender.com/partidos/publico/';
        let allPartidos = [];
        let currentDate = new Date();

        function renderCalendar(date, selectedDate = null) {
            daysGrid.innerHTML = '';
            const year = date.getFullYear();
            const month = date.getMonth();
            monthYearTitle.textContent = date.toLocaleDateString('es-MX', { month: 'long', year: 'numeric' });
            const firstDayOfMonth = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            const today = new Date(); today.setHours(0,0,0,0);

            for (let i = 0; i < firstDayOfMonth; i++) {
                 const dayCell = document.createElement('div');
                 dayCell.classList.add('day-cell', 'past');
                 daysGrid.appendChild(dayCell);
            }

            for (let day = 1; day <= daysInMonth; day++) {
                const dayCell = document.createElement('div');
                dayCell.classList.add('day-cell');
                dayCell.textContent = day;
                dayCell.dataset.date = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`; 

                const currentDayDate = new Date(year, month, day); currentDayDate.setHours(0,0,0,0);

                if (currentDayDate.getTime() === today.getTime()) dayCell.classList.add('today');

                if (selectedDate && currentDayDate.getTime() === selectedDate.getTime()) {
                    dayCell.classList.add('selected-day');
                }

                const hasGame = allPartidos.some(partido => partido.fecha === dayCell.dataset.date);
                if (hasGame) dayCell.classList.add('has-game');

                daysGrid.appendChild(dayCell);
            }
        }

        function renderGameList(partidosToShow, title = "Próximos Partidos") {
             if (!gameListTitle || !gameList) return; 
             gameListTitle.textContent = title; 
             gameList.innerHTML = '';

             if (!partidosToShow || partidosToShow.length === 0) {
                 gameList.innerHTML = `<div class="game-item-placeholder">No hay partidos ${title === "Próximos Partidos" ? 'programados' : 'para esta fecha'}.</div>`;
                 return;
             }

             partidosToShow.forEach(partido => {
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

        fetch(urlApiPartidos)
            .then(response => { 
                 if (!response.ok) throw new Error('Error en la respuesta de la API: ' + response.statusText);
                 return response.json();
             })
            .then(partidos => {
                allPartidos = partidos;
                renderCalendar(currentDate); 

                const hoy = new Date(); hoy.setHours(0, 0, 0, 0);
                const proximosPartidos = allPartidos
                    .filter(partido => new Date(partido.fecha + 'T00:00:00') >= hoy)
                    .sort((a, b) => new Date(a.fecha + 'T' + a.hora) - new Date(b.fecha + 'T' + b.hora));
                renderGameList(proximosPartidos, "Próximos Partidos");
            })
            .catch(error => { 
                 console.error('Hubo un problema al obtener los partidos:', error);
                 if (gameList) gameList.innerHTML = '<div class="game-item-placeholder">No se pudo cargar el calendario.</div>';
                 if (monthYearTitle) monthYearTitle.textContent = 'Error al cargar';
                 if (daysGrid) daysGrid.innerHTML = '<div style="grid-column: 1 / -1; color: red;">No se pudo conectar.</div>';
             });

        if(prevMonthButton) prevMonthButton.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() - 1);
            renderCalendar(currentDate);
        });
        if(nextMonthButton) nextMonthButton.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() + 1);
            renderCalendar(currentDate);
        });
        if(daysGrid) daysGrid.addEventListener('click', (event) => {
            const clickedDay = event.target.closest('.day-cell:not(.past)'); 
            if (!clickedDay || !clickedDay.dataset.date) return; 

            const selectedDateISO = clickedDay.dataset.date;
            const selectedDateObj = new Date(selectedDateISO + 'T00:00:00');
            const partidosDelDia = allPartidos.filter(partido => partido.fecha === selectedDateISO);
            const title = `Partidos del ${selectedDateObj.toLocaleDateString('es-MX', {day: 'numeric', month: 'long'})}`;
            
            renderGameList(partidosDelDia, title);
            renderCalendar(currentDate, selectedDateObj);
        });
    }

});
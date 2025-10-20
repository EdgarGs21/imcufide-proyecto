// src/banners.js

// 1. Importamos cada imagen al principio del archivo.
//    Esto le permite a Vite encontrarlas y procesarlas correctamente.
import bannerImg1 from './assets/banner_1.jpg';
import bannerImg2 from './assets/banner_2.jpg';
import bannerImg3 from './assets/banner_3.jpg';

// 2. Ahora, en lugar de texto, usamos las variables que acabamos de crear.
export const bannersData = [
    {
        imagen: bannerImg1, // <-- Cambio clave
        titulo: 'Inscripciones Abiertas para la Liga Municipal de Fútbol',
        subtitulo: 'Categorías infantiles y juveniles. ¡No te quedes fuera!',
        enlace: '#'
    },
    {
        imagen: bannerImg2, // <-- Cambio clave
        titulo: 'Gran Torneo de Voleibol de Verano 2025',
        subtitulo: 'Participa con tu equipo y compite por la copa municipal.',
        enlace: '#'
    },
    {
        imagen: bannerImg3, // <-- Cambio clave
        titulo: 'Clases de Activación Física para Adultos Mayores',
        subtitulo: 'Mantente activo y saludable. Consulta los horarios.',
        enlace: '#'
    }
];
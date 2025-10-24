# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time

# --- Schemas para Deporte ---
class DeporteBase(BaseModel):
    nombre: str
    icono: Optional[str] = None

class DeporteCreate(DeporteBase):
    pass

class Deporte(DeporteBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas para Categoria ---
class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    deporte_id: int

class Categoria(CategoriaBase):
    id: int
    deporte: Deporte # Asumiendo que quieres ver el detalle del deporte
    class Config:
        from_attributes = True

# --- Schemas para Documento ---
class DocumentoBase(BaseModel):
    nombre: str
    url_archivo: str

class DocumentoCreate(DocumentoBase):
    jugador_id: int

class Documento(DocumentoBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas para Jugador ---
class JugadorBase(BaseModel):
    nombre: str
    foto: Optional[str] = None
    edad: Optional[int] = None
    posicion: Optional[str] = None
    dorsal: Optional[int] = None
    municipio: Optional[str] = None

class JugadorCreate(JugadorBase):
    equipo_id: int

class Jugador(JugadorBase):
    id: int
    documentos: List[Documento] = []
    class Config:
        from_attributes = True

# --- INICIO DEL CÓDIGO AÑADIDO (Schema simplificado para plantillas) ---
class JugadorSimple(BaseModel):
    id: int
    nombre: str
    posicion: Optional[str] = None
    dorsal: Optional[int] = None

    class Config:
        from_attributes = True
# --- FIN DEL CÓDIGO AÑADIDO ---

# --- Schemas para Equipo ---
class EquipoBase(BaseModel):
    nombre: str
    escudo: Optional[str] = None
    nombre_entrenador: Optional[str] = None

class EquipoCreate(EquipoBase):
    categoria_id: int

class Equipo(EquipoBase):
    id: int
    categoria: Categoria # Asumiendo que quieres ver el detalle de la categoría
    jugadores: List[Jugador] = []
    class Config:
        from_attributes = True

# --- INICIO DEL CÓDIGO AÑADIDO (Schema para equipo con plantilla simple) ---
class EquipoConPlantilla(EquipoBase):
    id: int
    escudo: Optional[str] = None # Aseguramos que el escudo esté aquí
    jugadores: List[JugadorSimple] = [] # Usamos la lista de jugadores simplificada

    class Config:
        from_attributes = True
# --- FIN DEL CÓDIGO AÑADIDO ---


# --- Schemas para Sede ---
class SedeBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None

class SedeCreate(SedeBase):
    pass

class Sede(SedeBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas para EventoPartido ---
class EventoPartidoBase(BaseModel):
    tipo_evento: str
    minuto: int

class EventoPartidoCreate(EventoPartidoBase):
    partido_id: int
    jugador_id: int
    equipo_id: int

class EventoPartido(EventoPartidoBase):
    id: int
    class Config:
        from_attributes = True

# --- Schemas para Partido ---
class PartidoBase(BaseModel):
    fecha: date
    hora: time
    jornada: int
    marcador_local: Optional[int] = None # Corregido para aceptar None
    marcador_visitante: Optional[int] = None # Corregido para aceptar None

class PartidoCreate(PartidoBase):
    equipo_local_id: int
    equipo_visitante_id: int
    sede_id: int

class Partido(PartidoBase):
    id: int
    sede: Sede
    equipo_local: Equipo
    equipo_visitante: Equipo
    eventos: List[EventoPartido] = []
    class Config:
        from_attributes = True

class PartidoConNombres(BaseModel):
    id: int
    fecha: date
    hora: time
    jornada: int
    marcador_local: Optional[int] = None
    marcador_visitante: Optional[int] = None
    equipo_local_nombre: str
    equipo_visitante_nombre: str
    sede_nombre: str

    class Config:
        from_attributes = True

# --- Schemas para Usuario ---
class UsuarioBase(BaseModel):
    email: str

class UsuarioCreate(UsuarioBase):
    password: str
    rol: str = "editor"

class Usuario(UsuarioBase):
    id: int
    rol: str
    class Config:
        from_attributes = True

# --- Reconstrucción de Modelos ---
# ¡IMPORTANTE! Asegúrate de que estas llamadas estén DESPUÉS de definir todos los schemas que dependen unos de otros.
Jugador.model_rebuild()
Equipo.model_rebuild()
Partido.model_rebuild()
EquipoConPlantilla.model_rebuild() # Añadimos la reconstrucción del nuevo schema
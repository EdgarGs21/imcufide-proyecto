# models.py
from sqlalchemy import (Column, Integer, String, Date, 
                        Time, ForeignKey)
from sqlalchemy.orm import relationship
from database import Base

# --- Modelos de Administración ---
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rol = Column(String, default="editor", nullable=False)

# --- Modelos del Núcleo de la Liga ---
class Deporte(Base):
    __tablename__ = "deportes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    icono = Column(String, nullable=True)

    categorias = relationship("Categoria", back_populates="deporte")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    deporte_id = Column(Integer, ForeignKey("deportes.id"))

    deporte = relationship("Deporte", back_populates="categorias")
    equipos = relationship("Equipo", back_populates="categoria")

class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    escudo = Column(String, nullable=True)
    nombre_entrenador = Column(String, nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    categoria = relationship("Categoria", back_populates="equipos")
    jugadores = relationship("Jugador", back_populates="equipo")

class Jugador(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    foto = Column(String, nullable=True)
    edad = Column(Integer)
    posicion = Column(String)
    dorsal = Column(Integer)
    municipio = Column(String)
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    documentos = relationship("Documento", back_populates="jugador", cascade="all, delete-orphan")

    equipo = relationship("Equipo", back_populates="jugadores")
    eventos = relationship("EventoPartido", back_populates="jugador")

class Sede(Base):
    __tablename__ = "sedes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    direccion = Column(String, nullable=True)

    partidos = relationship("Partido", back_populates="sede")

class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date)
    hora = Column(Time)
    jornada = Column(Integer)
    marcador_local = Column(Integer, default=0)
    marcador_visitante = Column(Integer, default=0)
    
    equipo_local_id = Column(Integer, ForeignKey("equipos.id"))
    equipo_visitante_id = Column(Integer, ForeignKey("equipos.id"))
    sede_id = Column(Integer, ForeignKey("sedes.id"))

    sede = relationship("Sede", back_populates="partidos")
    eventos = relationship("EventoPartido", back_populates="partido")

    equipo_local = relationship("Equipo", foreign_keys=[equipo_local_id])
    equipo_visitante = relationship("Equipo", foreign_keys=[equipo_visitante_id])
    
class EventoPartido(Base):
    __tablename__ = "eventos_partido"
    
    id = Column(Integer, primary_key=True, index=True)
    tipo_evento = Column(String)
    minuto = Column(Integer)

    partido_id = Column(Integer, ForeignKey("partidos.id"))
    jugador_id = Column(Integer, ForeignKey("jugadores.id"))
    equipo_id = Column(Integer, ForeignKey("equipos.id"))

    partido = relationship("Partido", back_populates="eventos")
    jugador = relationship("Jugador", back_populates="eventos")

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    url_archivo = Column(String, nullable=False)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"))

    jugador = relationship("Jugador", back_populates="documentos")
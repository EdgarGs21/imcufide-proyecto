# crud.py
from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import select
import models, schemas, security

# --- CRUD para Deporte ---
def get_deporte_by_name(db: Session, nombre: str):
    return db.query(models.Deporte).filter(models.Deporte.nombre == nombre).first()

def get_deportes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Deporte).offset(skip).limit(limit).all()

def create_deporte(db: Session, deporte: schemas.DeporteCreate):
    db_deporte = models.Deporte(nombre=deporte.nombre, icono=deporte.icono)
    db.add(db_deporte)
    db.commit()
    db.refresh(db_deporte)
    return db_deporte

def get_deporte(db: Session, deporte_id: int):
    return db.query(models.Deporte).filter(models.Deporte.id == deporte_id).first()

def update_deporte(db: Session, deporte_id: int, deporte: schemas.DeporteCreate):
    db_deporte = db.query(models.Deporte).filter(models.Deporte.id == deporte_id).first()
    if db_deporte:
        db_deporte.nombre = deporte.nombre
        db_deporte.icono = deporte.icono
        db.commit()
        db.refresh(db_deporte)
    return db_deporte

def delete_deporte(db: Session, deporte_id: int):
    db_deporte = db.query(models.Deporte).filter(models.Deporte.id == deporte_id).first()
    if db_deporte:
        db.delete(db_deporte)
        db.commit()
    return db_deporte

# --- CRUD para Categoria ---
def get_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(nombre=categoria.nombre, deporte_id=categoria.deporte_id)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def get_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def update_categoria(db: Session, categoria_id: int, categoria: schemas.CategoriaCreate):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria:
        db_categoria.nombre = categoria.nombre
        db_categoria.deporte_id = categoria.deporte_id
        db.commit()
        db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
    return db_categoria

# --- CRUD para Equipo ---
def get_equipos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Equipo).offset(skip).limit(limit).all()

def create_equipo(db: Session, equipo: schemas.EquipoCreate):
    db_equipo = models.Equipo(**equipo.model_dump())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

def get_equipo(db: Session, equipo_id: int):
    return db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()

def update_equipo(db: Session, equipo_id: int, equipo: schemas.EquipoCreate):
    db_equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if db_equipo:
        db_equipo.nombre = equipo.nombre
        db_equipo.escudo = equipo.escudo
        db_equipo.nombre_entrenador = equipo.nombre_entrenador
        db_equipo.categoria_id = equipo.categoria_id
        db.commit()
        db.refresh(db_equipo)
    return db_equipo

def delete_equipo(db: Session, equipo_id: int):
    db_equipo = db.query(models.Equipo).filter(models.Equipo.id == equipo_id).first()
    if db_equipo:
        db.delete(db_equipo)
        db.commit()
    return db_equipo

# --- INICIO FUNCIÓN AÑADIDA PARA EQUIPOS POR CATEGORÍA ---
def obtener_equipos_por_categoria(db: Session, categoria_id: int):
    """Obtiene todos los equipos de una categoría específica, incluyendo sus jugadores."""
    return (db.query(models.Equipo)
            .options(joinedload(models.Equipo.jugadores)) # Carga ansiosa de jugadores
            .filter(models.Equipo.categoria_id == categoria_id)
            .order_by(models.Equipo.nombre.asc())
            .all())
# --- FIN FUNCIÓN AÑADIDA ---


# --- CRUD para Jugador ---
def get_jugadores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Jugador).offset(skip).limit(limit).all()

def create_jugador(db: Session, jugador: schemas.JugadorCreate):
    db_jugador = models.Jugador(**jugador.model_dump())
    db.add(db_jugador)
    db.commit()
    db.refresh(db_jugador)
    return db_jugador

def get_jugador(db: Session, jugador_id: int):
    return db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()

def update_jugador(db: Session, jugador_id: int, jugador: schemas.JugadorCreate):
    db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if db_jugador:
        jugador_data = jugador.model_dump()
        for key, value in jugador_data.items():
            setattr(db_jugador, key, value)
        db.commit()
        db.refresh(db_jugador)
    return db_jugador

def delete_jugador(db: Session, jugador_id: int):
    db_jugador = db.query(models.Jugador).filter(models.Jugador.id == jugador_id).first()
    if db_jugador:
        db.delete(db_jugador)
        db.commit()
    return db_jugador

# --- CRUD para Sede ---
def get_sede(db: Session, sede_id: int):
    return db.query(models.Sede).filter(models.Sede.id == sede_id).first()

def get_sedes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sede).offset(skip).limit(limit).all()

def create_sede(db: Session, sede: schemas.SedeCreate):
    db_sede = models.Sede(**sede.model_dump())
    db.add(db_sede)
    db.commit()
    db.refresh(db_sede)
    return db_sede

def update_sede(db: Session, sede_id: int, sede: schemas.SedeCreate):
    db_sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if db_sede:
        sede_data = sede.model_dump()
        for key, value in sede_data.items():
            setattr(db_sede, key, value)
        db.commit()
        db.refresh(db_sede)
    return db_sede

def delete_sede(db: Session, sede_id: int):
    db_sede = db.query(models.Sede).filter(models.Sede.id == sede_id).first()
    if db_sede:
        db.delete(db_sede)
        db.commit()
    return db_sede

# --- CRUD para Partido ---
def get_partido(db: Session, partido_id: int):
    return (db.query(models.Partido)
            .options(joinedload(models.Partido.sede),
                     joinedload(models.Partido.equipo_local),
                     joinedload(models.Partido.equipo_visitante),
                     joinedload(models.Partido.eventos))
            .filter(models.Partido.id == partido_id)
            .first())

def get_partidos(db: Session, skip: int = 0, limit: int = 100):
    return (db.query(models.Partido)
            .options(joinedload(models.Partido.sede),
                     joinedload(models.Partido.equipo_local),
                     joinedload(models.Partido.equipo_visitante))
            .offset(skip).limit(limit).all())

def create_partido(db: Session, partido: schemas.PartidoCreate):
    db_partido = models.Partido(**partido.model_dump())
    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    return db_partido

def update_partido(db: Session, partido_id: int, partido: schemas.PartidoCreate):
    db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if db_partido:
        partido_data = partido.model_dump()
        for key, value in partido_data.items():
            setattr(db_partido, key, value)
        db.commit()
        db.refresh(db_partido)
    return db_partido

def delete_partido(db: Session, partido_id: int):
    db_partido = db.query(models.Partido).filter(models.Partido.id == partido_id).first()
    if db_partido:
        db.delete(db_partido)
        db.commit()
    return db_partido

def obtener_partidos_con_nombres(db: Session):
    EquipoLocal = aliased(models.Equipo, name='equipo_local')
    EquipoVisitante = aliased(models.Equipo, name='equipo_visitante')
    query = (
        select(
            models.Partido.id,
            models.Partido.fecha,
            models.Partido.hora,
            models.Partido.jornada,
            models.Partido.marcador_local,
            models.Partido.marcador_visitante,
            EquipoLocal.nombre.label('equipo_local_nombre'),
            EquipoVisitante.nombre.label('equipo_visitante_nombre'),
            models.Sede.nombre.label('sede_nombre')
        )
        .join(EquipoLocal, models.Partido.equipo_local_id == EquipoLocal.id)
        .join(EquipoVisitante, models.Partido.equipo_visitante_id == EquipoVisitante.id)
        .join(models.Sede, models.Partido.sede_id == models.Sede.id)
        .order_by(models.Partido.fecha.desc(), models.Partido.hora.asc())
    )
    resultados = db.execute(query).mappings().all()
    return resultados

# --- CRUD para EventoPartido ---
def create_evento_partido(db: Session, evento: schemas.EventoPartidoCreate):
    db_evento = models.EventoPartido(**evento.model_dump())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def get_evento(db: Session, evento_id: int):
    return db.query(models.EventoPartido).filter(models.EventoPartido.id == evento_id).first()

def update_evento_partido(db: Session, evento_id: int, evento: schemas.EventoPartidoCreate):
    db_evento = db.query(models.EventoPartido).filter(models.EventoPartido.id == evento_id).first()
    if db_evento:
        evento_data = evento.model_dump()
        for key, value in evento_data.items():
            setattr(db_evento, key, value)
        db.commit()
        db.refresh(db_evento)
    return db_evento

def delete_evento_partido(db: Session, evento_id: int):
    db_evento = db.query(models.EventoPartido).filter(models.EventoPartido.id == evento_id).first()
    if db_evento:
        db.delete(db_evento)
        db.commit()
    return db_evento

# --- CRUD para Usuario ---
def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()

def create_user(db: Session, user: schemas.UsuarioCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.Usuario(email=user.email, hashed_password=hashed_password, rol=user.rol)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- CRUD para Documento ---
def create_documento(db: Session, documento: schemas.DocumentoCreate):
    db_documento = models.Documento(**documento.model_dump())
    db.add(db_documento)
    db.commit()
    db.refresh(db_documento)
    return db_documento
# routers/partidos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud 
import schemas
import models
from security import get_current_user
from database import get_db

router = APIRouter(
    prefix="/partidos",
    tags=["Partidos y Eventos"]
)

# Endpoint PÚBLICO para el calendario. Va PRIMERO para evitar conflictos.
@router.get("/publico/", response_model=List[schemas.PartidoConNombres])
def leer_partidos_publicos(db: Session = Depends(get_db)):
    partidos = crud.obtener_partidos_con_nombres(db=db)
    return partidos

@router.post("/", response_model=schemas.Partido, status_code=201)
def crear_nuevo_partido(partido: schemas.PartidoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    return crud.create_partido(db=db, partido=partido)

@router.get("/", response_model=List[schemas.Partido])
def leer_partidos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    partidos = crud.get_partidos(db, skip=skip, limit=limit)
    return partidos

@router.get("/{partido_id}", response_model=schemas.Partido)
def leer_partido_por_id(partido_id: int, db: Session = Depends(get_db)):
    db_partido = crud.get_partido(db, partido_id=partido_id)
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido

# --- Endpoints para Eventos de un Partido ---
@router.post("/{partido_id}/eventos/", response_model=schemas.EventoPartido, status_code=201)
def crear_evento_para_partido(partido_id: int, evento: schemas.EventoPartidoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    # Verificamos que el partido_id del path coincida con el del body
    if partido_id != evento.partido_id:
        raise HTTPException(status_code=400, detail="El ID del partido no coincide")
    return crud.create_evento_partido(db=db, evento=evento)

@router.put("/{partido_id}", response_model=schemas.Partido)
def actualizar_partido(partido_id: int, partido: schemas.PartidoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_partido = crud.update_partido(db, partido_id=partido_id, partido=partido)
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido

@router.delete("/{partido_id}", response_model=schemas.Partido)
def borrar_partido(partido_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_partido = crud.delete_partido(db, partido_id=partido_id)
    if db_partido is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return db_partido
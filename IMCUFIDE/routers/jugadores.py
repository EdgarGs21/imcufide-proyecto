# routers/jugadores.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from security import get_current_user
from database import get_db

router = APIRouter(
    prefix="/jugadores",
    tags=["Jugadores"]
)

@router.post("/", response_model=schemas.Jugador, status_code=201)
def crear_nuevo_jugador(jugador: schemas.JugadorCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    return crud.create_jugador(db=db, jugador=jugador)

@router.get("/", response_model=List[schemas.Jugador])
def leer_jugadores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jugadores = crud.get_jugadores(db, skip=skip, limit=limit)
    return jugadores

@router.get("/{jugador_id}", response_model=schemas.Jugador)
def leer_jugador_por_id(jugador_id: int, db: Session = Depends(get_db)):
    db_jugador = crud.get_jugador(db, jugador_id=jugador_id)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador

@router.put("/{jugador_id}", response_model=schemas.Jugador)
def actualizar_jugador(jugador_id: int, jugador: schemas.JugadorCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_jugador = crud.update_jugador(db, jugador_id=jugador_id, jugador=jugador)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador

@router.delete("/{jugador_id}", response_model=schemas.Jugador)
def borrar_jugador(jugador_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_jugador = crud.delete_jugador(db, jugador_id=jugador_id)
    if db_jugador is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return db_jugador
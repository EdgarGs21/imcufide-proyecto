# routers/deportes.py
from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from security import get_current_user
from database import get_db

router = APIRouter(
    prefix="/deportes",
    tags=["Deportes"]
)

@router.post("/", response_model=schemas.Deporte, status_code=201)
def crear_nuevo_deporte(deporte: schemas.DeporteCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
      # --- Verificación de Rol ---
    if current_user.rol != "super-admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para crear deportes")
    
    db_deporte = crud.get_deporte_by_name(db, nombre=deporte.nombre)
    if db_deporte:
        raise HTTPException(status_code=400, detail="El deporte con este nombre ya existe")
    return crud.create_deporte(db=db, deporte=deporte)

@router.get("/", response_model=List[schemas.Deporte])
def leer_deportes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    deportes = crud.get_deportes(db, skip=skip, limit=limit)
    return deportes

@router.get("/{deporte_id}", response_model=schemas.Deporte)
def leer_deporte_por_id(deporte_id: int, db: Session = Depends(get_db)):
    db_deporte = crud.get_deporte(db, deporte_id=deporte_id)
    if db_deporte is None:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")
    return db_deporte

@router.put("/{deporte_id}", response_model=schemas.Deporte)
def actualizar_deporte(deporte_id: int, deporte: schemas.DeporteCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
      # --- Verificación de Rol ---
    if current_user.rol != "super-admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar deportes")

    db_deporte = crud.update_deporte(db, deporte_id=deporte_id, deporte=deporte)
    if db_deporte is None:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")
    return db_deporte

@router.delete("/{deporte_id}", response_model=schemas.Deporte)
def borrar_deporte(deporte_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
     # --- Verificación de Rol ---
    if current_user.rol != "super-admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar deportes")

    db_deporte = crud.delete_deporte(db, deporte_id=deporte_id)
    if db_deporte is None:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")
    return db_deporte
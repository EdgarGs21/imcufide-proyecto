# routers/equipos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from security import get_current_user
from database import get_db

router = APIRouter(
    prefix="/equipos",
    tags=["Equipos"]
)

@router.post("/", response_model=schemas.Equipo, status_code=201)
def crear_nuevo_equipo(equipo: schemas.EquipoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
     # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
    
    return crud.create_equipo(db=db, equipo=equipo)

@router.get("/", response_model=List[schemas.Equipo])
def leer_equipos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    equipos = crud.get_equipos(db, skip=skip, limit=limit)
    return equipos

@router.get("/{equipo_id}", response_model=schemas.Equipo)
def leer_equipo_por_id(equipo_id: int, db: Session = Depends(get_db)):
    db_equipo = crud.get_equipo(db, equipo_id=equipo_id)
    if db_equipo is None:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return db_equipo

@router.put("/{equipo_id}", response_model=schemas.Equipo)
def actualizar_equipo(equipo_id: int, equipo: schemas.EquipoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
      # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_equipo = crud.update_equipo(db, equipo_id=equipo_id, equipo=equipo)
    if db_equipo is None:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return db_equipo

@router.delete("/{equipo_id}", response_model=schemas.Equipo)
def borrar_equipo(equipo_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_equipo = crud.delete_equipo(db, equipo_id=equipo_id)
    if db_equipo is None:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return db_equipo
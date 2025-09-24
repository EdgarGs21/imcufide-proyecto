# routers/sedes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from security import get_current_user
from database import get_db

router = APIRouter(
    prefix="/sedes",
    tags=["Sedes"]
)

@router.post("/", response_model=schemas.Sede, status_code=201)
def crear_nueva_sede(sede: schemas.SedeCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    return crud.create_sede(db=db, sede=sede)

@router.get("/", response_model=List[schemas.Sede])
def leer_sedes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sedes = crud.get_sedes(db, skip=skip, limit=limit)
    return sedes

@router.get("/{sede_id}", response_model=schemas.Sede)
def leer_sede_por_id(sede_id: int, db: Session = Depends(get_db)):
    db_sede = crud.get_sede(db, sede_id=sede_id)
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return db_sede

@router.put("/{sede_id}", response_model=schemas.Sede)
def actualizar_sede(sede_id: int, sede: schemas.SedeCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_sede = crud.update_sede(db, sede_id=sede_id, sede=sede)
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return db_sede

@router.delete("/{sede_id}", response_model=schemas.Sede)
def borrar_sede(sede_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_sede = crud.delete_sede(db, sede_id=sede_id)
    if db_sede is None:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return db_sede
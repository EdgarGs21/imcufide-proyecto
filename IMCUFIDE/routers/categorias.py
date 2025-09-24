# routers/categorias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, schemas, models
from security import get_current_user
from database import get_db

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)

@router.post("/", response_model=schemas.Categoria, status_code=201)
def crear_nueva_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
     # --- Verificación de Rol ---
    if current_user.rol != "super-admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para crear categorías")
   
    return crud.create_categoria(db=db, categoria=categoria)

@router.get("/", response_model=List[schemas.Categoria])
def leer_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categorias = crud.get_categorias(db, skip=skip, limit=limit)
    return categorias

@router.get("/{categoria_id}", response_model=schemas.Categoria)
def leer_categoria_por_id(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@router.put("/{categoria_id}", response_model=schemas.Categoria)
def actualizar_categoria(categoria_id: int, categoria: schemas.CategoriaCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol != "super-admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar categorías")
    
    db_categoria = crud.update_categoria(db, categoria_id=categoria_id, categoria=categoria)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@router.delete("/{categoria_id}", response_model=schemas.Categoria)
def borrar_categoria(categoria_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
     # --- Verificación de Rol ---
    if current_user.rol != "super-admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar categorías")
   
    db_categoria = crud.delete_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria
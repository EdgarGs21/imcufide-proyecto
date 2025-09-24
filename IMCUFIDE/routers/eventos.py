# routers/eventos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, schemas, models
from security import get_current_user
from database import get_db

router = APIRouter(
    prefix="/eventos",
    tags=["Eventos Individuales"]
)

@router.put("/{evento_id}", response_model=schemas.EventoPartido)
def actualizar_evento(evento_id: int, evento: schemas.EventoPartidoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_evento = crud.update_evento_partido(db, evento_id=evento_id, evento=evento)
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_evento

@router.delete("/{evento_id}", response_model=schemas.EventoPartido)
def borrar_evento(evento_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    # --- Verificación de Rol ---
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")
   
    db_evento = crud.delete_evento_partido(db, evento_id=evento_id)
    if db_evento is None:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return db_evento
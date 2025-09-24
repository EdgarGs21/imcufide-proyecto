# routers/documentos.py
import os
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import crud, schemas, models
from database import get_db
from security import get_current_user

# Configuración de Cloudinary (lee las credenciales del entorno)
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

router = APIRouter(
    prefix="/documentos",
    tags=["Documentos"]
)

@router.post("/upload/jugador/{jugador_id}", response_model=schemas.Documento)
def upload_documento_para_jugador(
    jugador_id: int,
    nombre_documento: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user)
):
    # Verificación de Rol
    if current_user.rol not in ["super-admin", "editor"]:
        raise HTTPException(status_code=403, detail="Permiso insuficiente")

    try:
        # Subir el archivo a Cloudinary
        # Usamos resource_type="raw" para archivos que no son imágenes/videos, como PDFs
        upload_result = cloudinary.uploader.upload(file.file, resource_type="raw", public_id=f"documentos/{file.filename}")
        
        # Obtener la URL segura que nos devuelve Cloudinary
        file_url = upload_result.get("secure_url")
        if not file_url:
            raise HTTPException(status_code=500, detail="No se pudo subir el archivo a Cloudinary")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")
    finally:
        file.file.close()

    # Crear el registro en nuestra base de datos con la URL de Cloudinary
    documento_a_crear = schemas.DocumentoCreate(
        nombre=nombre_documento,
        url_archivo=file_url,
        jugador_id=jugador_id
    )
    
    return crud.create_documento(db=db, documento=documento_a_crear)
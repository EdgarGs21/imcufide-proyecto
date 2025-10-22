# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import deportes, categorias, equipos, jugadores, sedes, partidos, eventos, auth, documentos

# Esto crea todas las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API del Proyecto IMCUFIDE",
    description="API para la gestión de las Ligas de Desarrollo de Tenango.",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "https://imcufide-proyecto.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers en la aplicación principal
app.include_router(deportes.router)
app.include_router(categorias.router)
app.include_router(equipos.router)
app.include_router(jugadores.router)
app.include_router(sedes.router)
app.include_router(partidos.router)
app.include_router(eventos.router)
app.include_router(auth.router)
app.include_router(documentos.router)

@app.get("/")
def read_root():
    return {"proyecto": "API de IMCUFIDE"}
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models import models
from app.schemas import schemas
from app.crud import crud
from app.db.session import engine, SessionLocal

# Crea las tablas en Supabase (si no existieran)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AquaGuard API",
    description="API para el monitoreo de inundaciones mediante IoT",
    version="1.0.0"
)

# Dependencia para abrir y cerrar la conexión a la base de datos por cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"status": "online", "message": "Bienvenido a la API de AquaGuard"}


# ENDPOINTS PARA SENSORES

@app.post("/api/sensors/", response_model=schemas.Sensor)
def create_sensor(sensor: schemas.SensorCreate, db: Session = Depends(get_db)):
    """Registra un nuevo sensor físico en el sistema."""
    return crud.create_sensor(db=db, sensor=sensor)

@app.get("/api/sensors/", response_model=List[schemas.Sensor])
def read_sensors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtiene la lista de sensores para mostrarlos en el mapa de Flutter."""
    return crud.get_sensors(db, skip=skip, limit=limit)


# ENDPOINTS PARA LECTURAS 

@app.post("/api/readings/", response_model=schemas.Reading)
def create_reading(reading: schemas.ReadingCreate, db: Session = Depends(get_db)):
    """Recibe el nivel de agua desde el microcontrolador y evalúa alertas."""
    return crud.create_reading(db=db, reading=reading)
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models import models
from app.schemas import schemas
from app.crud import crud
from app.db.session import engine, SessionLocal

from fastapi import FastAPI, Depends, HTTPException

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



@app.get("/api/sensors/{sensor_id}/readings", response_model=List[schemas.Reading])
def read_sensor_readings(sensor_id: str, limit: int = 50, db: Session = Depends(get_db)):
    """Obtiene el historial reciente de un sensor para graficar en el frontend."""
    return crud.get_readings_by_sensor(db, sensor_id=sensor_id, limit=limit)

# ==========================================
# ENDPOINTS PARA ALERTAS
# ==========================================
@app.get("/api/alerts/active", response_model=List[schemas.Alert])
def read_active_alerts(db: Session = Depends(get_db)):
    """Lista todas las alertas activas (no resueltas) en el sistema."""
    return crud.get_active_alerts(db)

@app.patch("/api/alerts/{alert_id}/resolve", response_model=schemas.Alert)
def resolve_alert(alert_id: str, db: Session = Depends(get_db)):
    """Marca una alerta como resuelta (Flujo de control de emergencias)."""
    alert = crud.resolve_alert(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    return alert
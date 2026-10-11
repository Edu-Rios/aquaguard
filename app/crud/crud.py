from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models import models
from app.schemas import schemas

# FUNCIONES DE SENSORES

def get_sensor(db: Session, sensor_id: str):
    # Busca un sensor específico por su ID
    return db.query(models.Sensor).filter(models.Sensor.id == sensor_id).first()

def get_sensors(db: Session, skip: int = 0, limit: int = 100):
    # Devuelve una lista de sensores 
    return db.query(models.Sensor).offset(skip).limit(limit).all()

def create_sensor(db: Session, sensor: schemas.SensorCreate):
    # Convierte el esquema validado de Pydantic en un modelo de SQLAlchemy
    db_sensor = models.Sensor(
        name=sensor.name,
        latitude=sensor.latitude,
        longitude=sensor.longitude,
        warning_level_cm=sensor.warning_level_cm,
        critical_level_cm=sensor.critical_level_cm,
        status=sensor.status
    )
    db.add(db_sensor)     # Prepara el dato
    db.commit()           # Lo guarda definitivamente en Supabase
    db.refresh(db_sensor) # Actualiza el objeto con el ID y fecha generados por la BD
    return db_sensor


# FUNCIONES DE LECTURAS 


def create_reading(db: Session, reading: schemas.ReadingCreate):
    # 1. Preparamos la lectura para guardarla
    db_reading = models.Reading(
        sensor_id=reading.sensor_id,
        water_level_cm=reading.water_level_cm,
        battery_level=reading.battery_level
    )
    db.add(db_reading)
    
    # Buscamos al sensor que mandó esta lectura
    sensor = db.query(models.Sensor).filter(models.Sensor.id == reading.sensor_id).first()
    
    if sensor:
        # 2. Actualizamos que el sensor está "vivo" (última comunicación)
        sensor.last_communication = datetime.now(timezone.utc)
        
        # 3. Evaluamos si hay inundación
        alert_type = None
        if reading.water_level_cm >= sensor.critical_level_cm:
            alert_type = 'critical'
        elif reading.water_level_cm >= sensor.warning_level_cm:
            alert_type = 'warning'
            
        if alert_type:
            # Hacemos un 'flush' para que la BD le asigne un ID temporal a la lectura
            # sin hacer el commit final todavía. Necesitamos ese ID para la alerta.
            db.flush() 
            
            # Generamos la alerta automáticamente
            db_alert = models.Alert(
                sensor_id=sensor.id,
                reading_id=db_reading.id,
                alert_type=alert_type
            )
            db.add(db_alert)

    # 4. Guardamos todo junto (La lectura, la actualización del sensor y la posible alerta)
    db.commit()
    db.refresh(db_reading)
    
    return db_reading
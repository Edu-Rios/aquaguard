from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# ESQUEMAS PARA SENSORES

class SensorBase(BaseModel):
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    warning_level_cm: float
    critical_level_cm: float
    status: Optional[str] = 'active'

class SensorCreate(SensorBase):
    pass # Hereda todo de SensorBase. Es lo que pedimos al crear uno nuevo.

class Sensor(SensorBase):
    id: UUID
    last_communication: Optional[datetime] = None
    created_at: datetime

    # Esto le dice a Pydantic que lea los datos de SQLAlchemy sin quejarse
    model_config = ConfigDict(from_attributes=True)



# ESQUEMAS PARA LECTURAS 

class ReadingBase(BaseModel):
    water_level_cm: float
    battery_level: Optional[int] = None

class ReadingCreate(ReadingBase):
    sensor_id: UUID

class Reading(ReadingBase):
    id: int
    sensor_id: UUID
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ESQUEMAS PARA ALERTAS

class AlertBase(BaseModel):
    alert_type: str # 'warning' o 'critical'
    is_resolved: Optional[bool] = False

class AlertCreate(AlertBase):
    sensor_id: UUID
    reading_id: int

class Alert(AlertBase):
    id: UUID
    sensor_id: UUID
    reading_id: int
    resolved_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, DateTime, BigInteger
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    push_token = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Sensor(Base):
    __tablename__ = "sensors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    warning_level_cm = Column(Float, nullable=False)
    critical_level_cm = Column(Float, nullable=False)
    status = Column(String(20), default='active')
    last_communication = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones para acceder fácilmente a los datos vinculados
    readings = relationship("Reading", back_populates="sensor", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="sensor", cascade="all, delete-orphan")

class Reading(Base):
    __tablename__ = "readings"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False)
    water_level_cm = Column(Float, nullable=False)
    battery_level = Column(Integer)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    sensor = relationship("Sensor", back_populates="readings")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False)
    reading_id = Column(BigInteger, ForeignKey("readings.id", ondelete="CASCADE"), nullable=False)
    alert_type = Column(String(20), nullable=False)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sensor = relationship("Sensor", back_populates="alerts")
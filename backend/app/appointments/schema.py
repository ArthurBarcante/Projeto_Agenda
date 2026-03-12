from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from app.appointments.model import AppointmentStatus


class AppointmentSchema(BaseModel):
    """Appointment schema."""

    model_config = ConfigDict(from_attributes=True)
    
    id: UUID | None = None
    creator_id: UUID
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    company_id: UUID


class AppointmentCreateSchema(AppointmentSchema):
    """Appointment create schema."""

    pass


class AppointmentUpdateSchema(BaseModel):
    """Appointment update schema."""

    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    status: AppointmentStatus | None = None


__all__ = ["AppointmentCreateSchema", "AppointmentSchema", "AppointmentUpdateSchema"]
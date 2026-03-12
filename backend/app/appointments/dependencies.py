from sqlalchemy.orm import Session

from app.appointments.repository import AppointmentRepository
from app.appointments.service import AppointmentService


def get_appointment_repository(db: Session) -> AppointmentRepository:
    return AppointmentRepository(db)


def get_appointment_service(db: Session) -> AppointmentService:
    return AppointmentService(db)


__all__ = ["get_appointment_repository", "get_appointment_service"]
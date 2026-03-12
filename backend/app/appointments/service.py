from sqlalchemy.orm import Session

from app.appointments.repository import AppointmentRepository


class AppointmentService:
    """Appointment service."""

    def __init__(self, db: Session) -> None:
        """Initialize appointment service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.repository = AppointmentRepository(db)


__all__ = ["AppointmentService"]
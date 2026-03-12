from sqlalchemy.orm import Session

from app.appointments.model import Appointment


class AppointmentRepository:
    """Appointment repository."""

    model = Appointment

    def __init__(self, db: Session) -> None:
        """Initialize appointment repository.
        
        Args:
            db: Database session
        """
        self.db = db


__all__ = ["AppointmentRepository"]
from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base
from app.models.mixins import TenantMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.user import User
  from app.models.appointment import Appointment

class AppointmentParticipant(TenantMixin, Base):
    __tablename__ = "appointment_participants"
    
    __table_args__ = (
      UniqueConstraint(
        "appointment_id",
        "user_id",
        name="uq_appointment_user"
      ),
      Index(
        "ix_appointment_participants_user_appointment",
        "user_id",
        "appointment_id",
      ),
    )
    
    appointment_id: Mapped[str] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("appointments.id", ondelete="CASCADE"),
      primary_key=True
    )
    
    user_id: Mapped[str] = mapped_column(
      UUID(as_uuid=True),
      ForeignKey("users.id", ondelete="CASCADE"),
      primary_key=True
    )
    
    # Relationships
    appointment: Mapped["Appointment"] = relationship(
      back_populates="participants"
    )
    
    user: Mapped["User"] = relationship()
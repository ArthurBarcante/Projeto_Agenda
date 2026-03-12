"""Appointment model."""

from datetime import datetime
from enum import Enum
from uuid import UUID
from sqlalchemy import String, Text, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import TenantModel


class AppointmentStatus(str, Enum):
    """Appointment status enumeration."""

    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Appointment(TenantModel):
    """Appointment model."""

    __tablename__ = "appointments"

    creator_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        SQLEnum(AppointmentStatus, name="appointment_status"),
        nullable=False,
        default=AppointmentStatus.SCHEDULED,
    )


__all__ = ["Appointment", "AppointmentStatus"]
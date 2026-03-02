import datetime
import enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config.uuid7 import generate_uuid7
from app.models.base import Base
from app.models.mixins import TenantMixin


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.appointment_participant import AppointmentParticipant


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    completed = "completed"


class Appointment(TenantMixin, Base):
    __tablename__ = "appointments"
    __table_args__ = (
        Index(
            "ix_appointments_company_starts_ends_status",
            "company_id",
            "starts_at",
            "ends_at",
            "status",
        ),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )

    creator_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    starts_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    ends_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus, name="appointment_status"),
        default=AppointmentStatus.scheduled,
        nullable=False,
    )

    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[datetime.datetime]

    # Relationships
    creator: Mapped["User"] = relationship(
        foreign_keys=[creator_id]
    )

    participants: Mapped[list["AppointmentParticipant"]] = relationship(
        back_populates="appointment",
        cascade="all, delete-orphan",
    )

    def can_be_updated(self) -> bool:
        return self.status == AppointmentStatus.scheduled

    def can_be_cancelled(self) -> bool:
        return self.status == AppointmentStatus.scheduled

    def is_past_due(self) -> bool:
        ends_at = self.ends_at
        if ends_at.tzinfo is None:
            return ends_at < datetime.datetime.utcnow()
        return ends_at < datetime.datetime.now(datetime.timezone.utc)

    def cancel(self, user: "User") -> None:
        if self.creator_id != user.id:
            raise PermissionError("Only the creator can cancel")

        if not self.can_be_cancelled():
            raise ValueError("Appointment cannot be cancelled")

        self.status = AppointmentStatus.cancelled


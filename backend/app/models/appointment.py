import datetime
import enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tenant_model import TenantModel


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.appointment_participant import AppointmentParticipant


class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    completed = "completed"


class Appointment(TenantModel):
    __tablename__ = "appointments"
    __table_args__ = (
        Index(
            "ix_appointments_company_start_end_status",
            "company_id",
            "start_time",
            "end_time",
            "status",
        ),
    )

    creator_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(AppointmentStatus, name="appointment_status"),
        default=AppointmentStatus.scheduled,
        nullable=False,
    )

    creator: Mapped["User"] = relationship(foreign_keys=[creator_id])
    participants: Mapped[list["AppointmentParticipant"]] = relationship(
        back_populates="appointment",
        cascade="all, delete-orphan",
    )

    def can_be_updated(self) -> bool:
        return self.status == AppointmentStatus.scheduled

    def can_be_cancelled(self) -> bool:
        return self.status == AppointmentStatus.scheduled

    def is_expired(self) -> bool:
        if self.end_time.tzinfo is None:
            return self.end_time < datetime.datetime.utcnow()
        return self.end_time < datetime.datetime.now(datetime.timezone.utc)

    def cancel(self, current_user: "User") -> None:
        if self.creator_id != current_user.id:
            raise PermissionError("Only the creator can cancel")
        if not self.can_be_cancelled():
            raise ValueError("Appointment cannot be cancelled")
        self.status = AppointmentStatus.cancelled

    @property
    def starts_at(self) -> datetime.datetime:
        return self.start_time

    @starts_at.setter
    def starts_at(self, value: datetime.datetime) -> None:
        self.start_time = value

    @property
    def ends_at(self) -> datetime.datetime:
        return self.end_time

    @ends_at.setter
    def ends_at(self, value: datetime.datetime) -> None:
        self.end_time = value

    @property
    def criador(self):
        return self.creator

    @property
    def participantes(self):
        return self.participants

    def pode_ser_atualizado(self) -> bool:
        return self.can_be_updated()

    def pode_ser_cancelado(self) -> bool:
        return self.can_be_cancelled()

    def esta_vencido(self) -> bool:
        return self.is_expired()

    def cancelar(self, usuario: "User") -> None:
        self.cancel(usuario)

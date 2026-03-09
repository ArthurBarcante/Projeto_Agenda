from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.models.tenant_model import TenantModel


if TYPE_CHECKING:
	from app.modules.schedule.models.appointment import Appointment
	from app.modules.users.models.user import User


class AppointmentParticipant(TenantModel):
	__tablename__ = "appointment_participants"

	id = None
	created_at = None
	updated_at = None

	__table_args__ = (
		UniqueConstraint("appointment_id", "user_id", name="uq_appointment_participant_user"),
		Index("ix_appointment_participants_user_appointment", "user_id", "appointment_id"),
	)

	appointment_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("appointments.id", ondelete="CASCADE"),
		primary_key=True,
	)
	user_id: Mapped[UUID] = mapped_column(
		UUID(as_uuid=True),
		ForeignKey("users.id", ondelete="CASCADE"),
		primary_key=True,
	)

	appointment: Mapped["Appointment"] = relationship(back_populates="participants")
	user: Mapped["User"] = relationship()

from datetime import datetime
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.tenant.tenant_context import get_tenant
from app.modules.schedule.models.appointment import Appointment as AppointmentAlias
from app.modules.schedule.models.appointment import AppointmentStatus as AppointmentStatusAlias
from app.modules.schedule.models.appointment_participant import AppointmentParticipant as AppointmentParticipantAlias
from app.core.db.repositories import BaseRepository


class AppointmentRepositoryAlias(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def create_appointment(
        self,
        appointment: AppointmentAlias,
        participants: list[AppointmentParticipantAlias],
        auto_commit: bool = True,
    ) -> AppointmentAlias:
        self.add(appointment)
        self.flush()
        if participants:
            self.add_all(participants)
        if auto_commit:
            self.commit()
            self.refresh(appointment)
        return appointment

    def find_by_id(self, appointment_id: UUID) -> AppointmentAlias | None:
        tenant_id = get_tenant()
        if tenant_id is None:
            raise RuntimeError("Tenant context is required")

        return (
            self.query(AppointmentAlias)
            .filter(
                AppointmentAlias.id == appointment_id,
                AppointmentAlias.company_id == tenant_id,
            )
            .first()
        )

    def has_time_conflict(
        self,
        user_ids: list[UUID],
        start_time: datetime,
        end_time: datetime,
        ignore_appointment_id: UUID | None = None,
    ) -> bool:
        if not user_ids:
            return False

        tenant_id = get_tenant()
        if tenant_id is None:
            raise RuntimeError("Tenant context is required")

        consulta = (
            self.query(AppointmentAlias.id)
            .outerjoin(
                AppointmentParticipantAlias,
                AppointmentParticipantAlias.appointment_id == AppointmentAlias.id,
            )
            .filter(AppointmentAlias.status == AppointmentStatusAlias.scheduled)
            .filter(AppointmentAlias.start_time < end_time)
            .filter(AppointmentAlias.end_time > start_time)
            .filter(AppointmentAlias.company_id == tenant_id)
            .filter(
                or_(
                    AppointmentAlias.creator_id.in_(user_ids),
                    AppointmentParticipantAlias.user_id.in_(user_ids),
                )
            )
        )

        if ignore_appointment_id is not None:
            consulta = consulta.filter(AppointmentAlias.id != ignore_appointment_id)

        consulta = consulta.with_for_update()

        return consulta.first() is not None

    def update_appointment(self, appointment: AppointmentAlias) -> AppointmentAlias:
        self.commit()
        self.refresh(appointment)
        return appointment

    def cancel_appointment(self, appointment: AppointmentAlias) -> AppointmentAlias:
        self.commit()
        self.refresh(appointment)
        return appointment

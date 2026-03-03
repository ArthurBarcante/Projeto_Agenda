from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.appointment import AppointmentStatus
from app.models.appointment_participant import AppointmentParticipant
from app.models.user import User
from app.schemas.appointment import AppointmentCreate
from app.schemas.appointment import AppointmentUpdate


class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def _check_time_conflict(
        self,
        users_ids: list[UUID],
        starts_at: datetime,
        ends_at: datetime,
        ignore_appointment_id: UUID | None = None,
    ) -> None:
        unique_user_ids = list(dict.fromkeys(users_ids))
        if not unique_user_ids:
            return

        query = (
            self.db.query(Appointment.id)
            .outerjoin(
                AppointmentParticipant,
                AppointmentParticipant.appointment_id == Appointment.id,
            )
            .filter(Appointment.status == AppointmentStatus.scheduled)
            .filter(Appointment.starts_at < ends_at)
            .filter(Appointment.ends_at > starts_at)
            .filter(
                or_(
                    Appointment.creator_id.in_(unique_user_ids),
                    AppointmentParticipant.user_id.in_(unique_user_ids),
                )
            )
        )

        if ignore_appointment_id is not None:
            query = query.filter(Appointment.id != ignore_appointment_id)

        if query.first() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time conflict for one or more users",
            )

    def create_appointment(
        self,
        data: AppointmentCreate,
        current_user: User,
    ) -> Appointment:
        participant_ids = [
            participant_id
            for participant_id in dict.fromkeys(data.participant_ids)
            if participant_id != current_user.id
        ]

        users_to_validate = [current_user.id, *participant_ids]
        self._check_time_conflict(
            users_ids=users_to_validate,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
        )

        appointment = Appointment(
            company_id=current_user.company_id,
            creator_id=current_user.id,
            title=data.title,
            description=data.description,
            starts_at=data.starts_at,
            ends_at=data.ends_at,
            status=AppointmentStatus.scheduled,
        )
        self.db.add(appointment)
        self.db.flush()

        for participant_id in participant_ids:
            self.db.add(
                AppointmentParticipant(
                    company_id=current_user.company_id,
                    appointment_id=appointment.id,
                    user_id=participant_id,
                )
            )

        self.db.commit()
        self.db.refresh(appointment)
        return appointment
        
    def get_or_404(self, appointment_id: UUID) -> Appointment:
        appointment = (
            self.db.query(Appointment)
            .filter(Appointment.id == appointment_id)
            .first()
        )

        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found"
            )

        return appointment

    def _ensure_creator_permission(
        self,
        appointment: Appointment,
        current_user: User
    ) -> None:
        if appointment.creator_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the creator can modify this appointment"
            )

    def update_appointment(
        self,
        appointment_id: UUID,
        data: AppointmentUpdate,
        current_user: User
    ) -> Appointment:

        appointment = self.get_or_404(appointment_id)

        self._ensure_creator_permission(appointment, current_user)

        if not appointment.can_be_updated():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only scheduled appointments can be updated"
            )

        payload = data.model_dump(exclude_unset=True)
        if "starts_at" in payload or "ends_at" in payload:
            starts_at = payload.get("starts_at", appointment.starts_at)
            ends_at = payload.get("ends_at", appointment.ends_at)

            participant_ids = [
                participant.user_id
                for participant in appointment.participants
            ]
            users_to_validate = [appointment.creator_id, *participant_ids]
            self._check_time_conflict(
                users_ids=users_to_validate,
                starts_at=starts_at,
                ends_at=ends_at,
                ignore_appointment_id=appointment.id,
            )

        for field, value in payload.items():
            setattr(appointment, field, value)
        
        self.db.commit()
        self.db.refresh(appointment)

        return appointment

    def cancel_appointment(
        self,
        appointment_id: UUID,
        current_user: User
    ) -> Appointment:

        appointment = self.get_or_404(appointment_id)

        try:
            appointment.cancel(current_user)
        except PermissionError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the creator can cancel"
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment cannot be cancelled"
            )

        self.db.commit()
        self.db.refresh(appointment)

        return appointment
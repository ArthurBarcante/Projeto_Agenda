from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.errors.api_error import APIError
from app.core.errors.error_codes import ErrorCode
from app.core.tenant.tenant_context import clear_tenant, set_tenant
from app.modules.schedule.models.appointment import Appointment
from app.modules.schedule.models.appointment import AppointmentStatus
from app.modules.schedule.models.appointment_participant import AppointmentParticipant
from app.modules.schedule.repositories.appointment_repository import AppointmentRepositoryAlias
from app.modules.schedule.schemas.appointment import AppointmentCreate, AppointmentUpdate
from app.modules.users.models.user import User
from app.modules.audit.services.audit_service import AuditService
from app.modules.outbox.services.outbox_service import OutboxService


class AppointmentService:
    _DETAIL_MAP = {
        "Time conflict for one or more users": "Time conflict for one or more users",
        "An appointment already exists at this time": "Time conflict for one or more users",
        "Appointment not found": "Appointment not found",
        "AppointmentAlias not found": "Appointment not found",
        "Only appointments agendados podem ser atualizados": "Only scheduled appointments can be updated",
        "Only o creator pode cancel": "Only the creator can cancel",
        "Only o creator pode modificar este appointment": "Only the creator can cancel",
        "AppointmentAlias cannot be cancelled": "Appointment cannot be cancelled",
    }

    def __init__(self, db: Session):
        self.db = db
        self.repository = AppointmentRepositoryAlias(db)
        self.audit_service = AuditService(db)
        self.outbox_service = OutboxService(db)

    def _snapshot_appointment(self, appointment: Appointment) -> dict[str, object]:
        participants = getattr(appointment, "participants", []) or []
        status = getattr(appointment, "status", None)
        status_value = getattr(status, "value", status)
        return {
            "id": str(appointment.id),
            "tenant_id": str(appointment.company_id),
            "creator_id": str(appointment.creator_id),
            "title": appointment.title,
            "description": appointment.description,
            "start_time": appointment.start_time.isoformat(),
            "end_time": appointment.end_time.isoformat(),
            "status": status_value,
            "participant_ids": [
                str(getattr(participant, "user_id", participant))
                for participant in participants
            ],
        }

    def _check_time_conflict(
        self,
        user_ids: list[UUID],
        start_time: datetime,
        end_time: datetime,
        ignore_appointment_id: UUID | None = None,
    ) -> None:
        unique_user_ids = list(dict.fromkeys(user_ids))
        if not unique_user_ids:
            return

        if self.repository.has_time_conflict(
            user_ids=unique_user_ids,
            start_time=start_time,
            end_time=end_time,
            ignore_appointment_id=ignore_appointment_id,
        ):
            raise APIError(
                codigo=ErrorCode.SCHEDULE_CONFLICT,
                mensagem="An appointment already exists at this time",
                status_code=status.HTTP_409_CONFLICT,
            )

    def get_or_404(self, appointment_id: UUID) -> Appointment:
        appointment = self.repository.find_by_id(appointment_id)
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found",
            )
        return appointment

    def _translate_exception(self, exc: HTTPException | APIError) -> HTTPException:
        if isinstance(exc, APIError):
            detail = self._DETAIL_MAP.get(exc.mensagem, exc.mensagem)
            status_code = 400 if exc.codigo == "SCHEDULE_CONFLICT" else exc.status_code
            return HTTPException(status_code=status_code, detail=detail)

        detail = self._DETAIL_MAP.get(exc.detail, exc.detail)
        return HTTPException(status_code=exc.status_code, detail=detail)

    def create_appointment(
        self,
        dados: AppointmentCreate | None = None,
        current_user: User | None = None,
        data: AppointmentCreate | None = None,
    ):
        payload_data = dados or data
        if payload_data is None or current_user is None:
            raise ValueError("Both appointment payload and current_user are required")

        set_tenant(current_user.company_id)
        try:
            payload = payload_data.model_dump()
            participant_ids = [
                participant_id
                for participant_id in dict.fromkeys(payload.get("participant_ids", payload.get("participantes_ids", [])))
                if participant_id != current_user.id
            ]
            self._check_time_conflict(
                user_ids=[current_user.id, *participant_ids],
                start_time=payload.get("start_time"),
                end_time=payload.get("end_time"),
            )

            appointment = Appointment(
                company_id=current_user.company_id,
                creator_id=current_user.id,
                title=payload.get("title"),
                description=payload.get("description"),
                start_time=payload.get("start_time"),
                end_time=payload.get("end_time"),
                status=AppointmentStatus.scheduled,
            )

            participants = [
                AppointmentParticipant(
                    company_id=current_user.company_id,
                    appointment_id=appointment.id,
                    user_id=participant_id,
                )
                for participant_id in participant_ids
            ]

            created_appointment = self.repository.create_appointment(
                appointment=appointment,
                participants=participants,
                auto_commit=False,
            )

            self.audit_service.registrar_evento(
                tenant_id=current_user.company_id,
                user_id=current_user.id,
                acao="criacao",
                entity="appointment",
                entidade_id=created_appointment.id,
                dados_antes=None,
                dados_depois=self._snapshot_appointment(created_appointment),
            )

            self.outbox_service.registrar_evento(
                company_id=current_user.company_id,
                event_type="APPOINTMENT_CREATED",
                payload={
                    "appointment_id": str(created_appointment.id),
                    "user_id": str(current_user.id),
                    "start_time": created_appointment.start_time.isoformat(),
                    "end_time": created_appointment.end_time.isoformat(),
                },
            )

            self.db.commit()
            self.db.refresh(created_appointment)
            return created_appointment
        except (HTTPException, APIError) as exc:
            raise self._translate_exception(exc) from exc
        except Exception:
            self.db.rollback()
            raise
        finally:
            clear_tenant()

    def update_appointment(
        self,
        appointment_id: UUID,
        dados: AppointmentUpdate | None = None,
        current_user: User | None = None,
        data: AppointmentUpdate | None = None,
    ):
        payload_data = dados or data
        if payload_data is None or current_user is None:
            raise ValueError("Both appointment payload and current_user are required")

        set_tenant(current_user.company_id)
        try:
            appointment = self.get_or_404(appointment_id)
            if getattr(appointment, "creator_id", None) != current_user.id:
                raise HTTPException(status_code=403, detail="Only the creator can cancel")

            can_be_updated = getattr(appointment, "can_be_updated", None)
            if not callable(can_be_updated) or not can_be_updated():
                raise HTTPException(status_code=400, detail="Only scheduled appointments can be updated")

            payload = payload_data.model_dump(exclude_unset=True)
            before_data = self._snapshot_appointment(appointment)
            if "start_time" in payload or "end_time" in payload:
                start_time = payload.get("start_time", appointment.start_time)
                end_time = payload.get("end_time", appointment.end_time)
                participant_ids = [
                    participant.user_id
                    for participant in getattr(appointment, "participants", [])
                ]
                self._check_time_conflict(
                    user_ids=[appointment.creator_id, *participant_ids],
                    start_time=start_time,
                    end_time=end_time,
                    ignore_appointment_id=appointment_id,
                )

            for field, value in payload.items():
                setattr(appointment, field, value)

            self.audit_service.registrar_evento(
                tenant_id=current_user.company_id,
                user_id=current_user.id,
                acao="edicao",
                entity="appointment",
                entidade_id=appointment.id,
                dados_antes=before_data,
                dados_depois=self._snapshot_appointment(appointment),
            )

            return self.repository.update_appointment(appointment)
        except (HTTPException, APIError) as exc:
            raise self._translate_exception(exc) from exc
        finally:
            clear_tenant()

    def cancel_appointment(self, appointment_id: UUID, current_user: User):
        set_tenant(current_user.company_id)
        try:
            appointment = self.get_or_404(appointment_id)
            before_data = self._snapshot_appointment(appointment)

            try:
                appointment.cancel(current_user)
            except PermissionError as exc:
                raise HTTPException(status_code=403, detail="Only the creator can cancel") from exc
            except ValueError as exc:
                raise HTTPException(status_code=400, detail="Appointment cannot be cancelled") from exc

            self.audit_service.registrar_evento(
                tenant_id=current_user.company_id,
                user_id=current_user.id,
                acao="cancellation",
                entity="appointment",
                entidade_id=appointment.id,
                dados_antes=before_data,
                dados_depois=self._snapshot_appointment(appointment),
            )

            return self.repository.cancel_appointment(appointment)
        except (HTTPException, APIError) as exc:
            raise self._translate_exception(exc) from exc
        finally:
            clear_tenant()

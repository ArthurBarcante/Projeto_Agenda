from fastapi import HTTPException

from app.core.errors.api_error import APIError
from app.core.tenant.tenant_context import clear_tenant, set_tenant
from app.modules.agenda.services.compromisso_service import CompromissoService


class AppointmentService(CompromissoService):
    _DETAIL_MAP = {
        "Conflito de horário para um ou mais usuários": "Time conflict for one or more users",
        "Já existe um compromisso nesse horário": "Time conflict for one or more users",
        "Compromisso não encontrado": "Appointment not found",
        "Apenas compromissos agendados podem ser atualizados": "Only scheduled appointments can be updated",
        "Apenas o criador pode cancelar": "Only the creator can cancel",
        "Compromisso não pode ser cancelado": "Appointment cannot be cancelled",
    }

    def _translate_exception(self, exc: HTTPException | APIError) -> HTTPException:
        if isinstance(exc, APIError):
            detail = self._DETAIL_MAP.get(exc.mensagem, exc.mensagem)
            status_code = 400 if exc.codigo == "CONFLITO_AGENDA" else exc.status_code
            return HTTPException(status_code=status_code, detail=detail)

        detail = self._DETAIL_MAP.get(exc.detail, exc.detail)
        return HTTPException(status_code=exc.status_code, detail=detail)

    @staticmethod
    def _is_updatable(appointment) -> bool:
        if hasattr(appointment, "pode_ser_atualizado"):
            return appointment.pode_ser_atualizado()
        if hasattr(appointment, "can_be_updated"):
            return appointment.can_be_updated()
        return False

    @staticmethod
    def _cancel_appointment(appointment, current_user) -> None:
        if hasattr(appointment, "cancelar"):
            appointment.cancelar(current_user)
            return
        if hasattr(appointment, "cancel"):
            appointment.cancel(current_user)
            return
        raise AttributeError("Appointment has no cancel method")

    def create_appointment(self, data, current_user):
        set_tenant(current_user.company_id)
        try:
            try:
                return self.criar_compromisso(dados=data, usuario_atual=current_user)
            except (HTTPException, APIError) as exc:
                raise self._translate_exception(exc) from exc
        finally:
            clear_tenant()

    def update_appointment(self, appointment_id, data, current_user):
        set_tenant(current_user.company_id)
        try:
            appointment = self.repository.buscar_por_id(appointment_id)
            if appointment is None:
                raise HTTPException(status_code=404, detail="Appointment not found")
            if getattr(appointment, "creator_id", None) != current_user.id:
                raise HTTPException(status_code=403, detail="Only the creator can cancel")

            if not self._is_updatable(appointment):
                raise HTTPException(status_code=400, detail="Only scheduled appointments can be updated")

            payload = data.model_dump(exclude_unset=True)
            starts_input = payload.get("starts_at", payload.get("start_time", payload.get("inicio_em")))
            ends_input = payload.get("ends_at", payload.get("end_time", payload.get("fim_em")))
            if starts_input is not None or ends_input is not None:
                starts_at = starts_input or appointment.starts_at
                ends_at = ends_input or appointment.ends_at
                participant_ids = [
                    participant.user_id
                    for participant in getattr(appointment, "participants", [])
                ]
                user_ids = [appointment.creator_id, *participant_ids]
                try:
                    self._verificar_conflito_horario(
                        usuarios_ids=user_ids,
                        inicio_em=starts_at,
                        fim_em=ends_at,
                        ignorar_compromisso_id=appointment_id,
                    )
                except (HTTPException, APIError) as exc:
                    raise self._translate_exception(exc) from exc

            field_map = {
                "titulo": "title",
                "descricao": "description",
                "title": "title",
                "description": "description",
                "starts_at": "starts_at",
                "ends_at": "ends_at",
                "start_time": "starts_at",
                "end_time": "ends_at",
                "inicio_em": "starts_at",
                "fim_em": "ends_at",
            }
            for field, value in payload.items():
                setattr(appointment, field_map.get(field, field), value)

            self.db.commit()
            self.db.refresh(appointment)

            try:
                return appointment
            except HTTPException as exc:
                raise self._translate_http_exception(exc) from exc
        finally:
            clear_tenant()

    def cancel_appointment(self, appointment_id, current_user):
        set_tenant(current_user.company_id)
        try:
            try:
                appointment = self.obter_ou_404(appointment_id)
            except HTTPException as exc:
                raise self._translate_exception(exc) from exc
            try:
                self._cancel_appointment(appointment, current_user)
            except PermissionError as exc:
                raise HTTPException(status_code=403, detail="Only the creator can cancel") from exc
            except ValueError as exc:
                raise HTTPException(status_code=400, detail="Appointment cannot be cancelled") from exc

            self.db.commit()
            self.db.refresh(appointment)

            try:
                return appointment
            except HTTPException as exc:
                raise self._translate_exception(exc) from exc
        finally:
            clear_tenant()

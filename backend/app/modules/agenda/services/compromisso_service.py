from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.errors.api_error import APIError
from app.core.errors.error_codes import ErrorCode
from app.core.tenant.tenant_context import clear_tenant, set_tenant
from app.models.appointment import Appointment as Compromisso
from app.models.appointment import AppointmentStatus as StatusCompromisso
from app.models.appointment_participant import AppointmentParticipant as ParticipanteCompromisso
from app.models.user import User as Usuario
from app.modules.agenda.repositories.compromisso_repository import CompromissoRepository
from app.modules.auditoria.services.audit_service import AuditService
from app.modules.outbox.services.outbox_service import OutboxService
from app.modules.agenda.schemas.compromisso import CompromissoAtualizacao
from app.modules.agenda.schemas.compromisso import CompromissoAtualizacao as AtualizacaoCompromissoLegado
from app.modules.agenda.schemas.compromisso import CompromissoCriacao
from app.modules.agenda.schemas.compromisso import CompromissoCriacao as CriacaoCompromissoLegado


class CompromissoService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = CompromissoRepository(db)
        self.audit_service = AuditService(db)
        self.outbox_service = OutboxService(db)

    def _snapshot_compromisso(self, compromisso: Compromisso) -> dict[str, object]:
        return {
            "id": str(compromisso.id),
            "tenant_id": str(compromisso.company_id),
            "creator_id": str(compromisso.creator_id),
            "title": compromisso.title,
            "description": compromisso.description,
            "start_time": compromisso.start_time.isoformat(),
            "end_time": compromisso.end_time.isoformat(),
            "status": compromisso.status.value,
            "participant_ids": [
                str(participante.user_id)
                for participante in compromisso.participantes
            ],
        }

    def _verificar_conflito_horario(
        self,
        usuarios_ids: list[UUID],
        inicio_em: datetime,
        fim_em: datetime,
        ignorar_compromisso_id: UUID | None = None,
    ) -> None:
        usuarios_unicos_ids = list(dict.fromkeys(usuarios_ids))
        if not usuarios_unicos_ids:
            return

        if self.repository.existe_conflito_horario(
            usuarios_ids=usuarios_unicos_ids,
            inicio_em=inicio_em,
            fim_em=fim_em,
            ignorar_compromisso_id=ignorar_compromisso_id,
        ):
            raise APIError(
                codigo=ErrorCode.CONFLITO_AGENDA,
                mensagem="Já existe um compromisso nesse horário",
                status_code=status.HTTP_409_CONFLICT,
            )

    def criar_compromisso(
        self,
        dados: CompromissoCriacao | CriacaoCompromissoLegado,
        usuario_atual: Usuario,
    ) -> Compromisso:
        set_tenant(usuario_atual.company_id)
        try:
            payload = dados.model_dump()

            raw_participants = payload.get("participant_ids", payload.get("participantes_ids", []))
            participantes_ids = [
                participante_id
                for participante_id in dict.fromkeys(raw_participants)
                if participante_id != usuario_atual.id
            ]

            start_time = payload.get("start_time", payload.get("inicio_em"))
            end_time = payload.get("end_time", payload.get("fim_em"))
            title = payload.get("title", payload.get("titulo"))
            description = payload.get("description", payload.get("descricao"))

            usuarios_para_validar = [usuario_atual.id, *participantes_ids]
            try:
                self._verificar_conflito_horario(
                    usuarios_ids=usuarios_para_validar,
                    inicio_em=start_time,
                    fim_em=end_time,
                )

                compromisso = Compromisso(
                    company_id=usuario_atual.company_id,
                    creator_id=usuario_atual.id,
                    title=title,
                    description=description,
                    start_time=start_time,
                    end_time=end_time,
                    status=StatusCompromisso.scheduled,
                )
                participantes: list[ParticipanteCompromisso] = []
                for participante_id in participantes_ids:
                    participantes.append(
                        ParticipanteCompromisso(
                            company_id=usuario_atual.company_id,
                            appointment_id=compromisso.id,
                            user_id=participante_id,
                        )
                    )

                compromisso_criado = self.repository.criar_compromisso(
                    compromisso=compromisso,
                    participantes=participantes,
                    auto_commit=False,
                )

                self.audit_service.registrar_evento(
                    tenant_id=usuario_atual.company_id,
                    usuario_id=usuario_atual.id,
                    acao="criacao",
                    entidade="compromisso",
                    entidade_id=compromisso_criado.id,
                    dados_antes=None,
                    dados_depois=self._snapshot_compromisso(compromisso_criado),
                )

                self.outbox_service.registrar_evento(
                    empresa_id=usuario_atual.company_id,
                    tipo_evento="APPOINTMENT_CREATED",
                    payload={
                        "appointment_id": str(compromisso_criado.id),
                        "user_id": str(usuario_atual.id),
                        "start_time": compromisso_criado.start_time.isoformat(),
                        "end_time": compromisso_criado.end_time.isoformat(),
                    },
                )

                self.db.commit()
            except Exception:
                self.db.rollback()
                raise

            self.db.refresh(compromisso_criado)
            return compromisso_criado
        finally:
            clear_tenant()

    def obter_ou_404(self, compromisso_id: UUID) -> Compromisso:
        compromisso = self.repository.buscar_por_id(compromisso_id)

        if not compromisso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Compromisso não encontrado",
            )

        return compromisso

    def _garantir_permissao_criador(
        self,
        compromisso: Compromisso,
        usuario_atual: Usuario,
    ) -> None:
        if compromisso.creator_id != usuario_atual.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas o criador pode modificar este compromisso",
            )

    def atualizar_compromisso(
        self,
        compromisso_id: UUID,
        dados: CompromissoAtualizacao | AtualizacaoCompromissoLegado,
        usuario_atual: Usuario,
    ) -> Compromisso:
        set_tenant(usuario_atual.company_id)
        try:
            compromisso = self.obter_ou_404(compromisso_id)

            self._garantir_permissao_criador(compromisso, usuario_atual)

            if not compromisso.pode_ser_atualizado():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Apenas compromissos agendados podem ser atualizados",
                )

            payload = dados.model_dump(exclude_unset=True)
            dados_antes = self._snapshot_compromisso(compromisso)
            if "start_time" in payload or "end_time" in payload or "inicio_em" in payload or "fim_em" in payload:
                inicio_em = payload.get("start_time", payload.get("inicio_em", compromisso.start_time))
                fim_em = payload.get("end_time", payload.get("fim_em", compromisso.end_time))

                participantes_ids = [
                    participante.user_id
                    for participante in compromisso.participantes
                ]
                usuarios_para_validar = [compromisso.creator_id, *participantes_ids]
                self._verificar_conflito_horario(
                    usuarios_ids=usuarios_para_validar,
                    inicio_em=inicio_em,
                    fim_em=fim_em,
                    ignorar_compromisso_id=compromisso.id,
                )

            mapa_campos = {
                "titulo": "title",
                "descricao": "description",
                "inicio_em": "start_time",
                "fim_em": "end_time",
                "start_time": "start_time",
                "end_time": "end_time",
            }

            for campo, valor in payload.items():
                setattr(compromisso, mapa_campos.get(campo, campo), valor)

            self.audit_service.registrar_evento(
                tenant_id=usuario_atual.company_id,
                usuario_id=usuario_atual.id,
                acao="edicao",
                entidade="compromisso",
                entidade_id=compromisso.id,
                dados_antes=dados_antes,
                dados_depois=self._snapshot_compromisso(compromisso),
            )

            return self.repository.atualizar_compromisso(compromisso)
        finally:
            clear_tenant()

    def cancelar_compromisso(
        self,
        compromisso_id: UUID,
        usuario_atual: Usuario,
    ) -> Compromisso:
        set_tenant(usuario_atual.company_id)
        try:
            compromisso = self.obter_ou_404(compromisso_id)
            dados_antes = self._snapshot_compromisso(compromisso)

            try:
                compromisso.cancelar(usuario_atual)
            except PermissionError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Apenas o criador pode cancelar",
                )
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Compromisso não pode ser cancelado",
                )

            self.audit_service.registrar_evento(
                tenant_id=usuario_atual.company_id,
                usuario_id=usuario_atual.id,
                acao="cancelamento",
                entidade="compromisso",
                entidade_id=compromisso.id,
                dados_antes=dados_antes,
                dados_depois=self._snapshot_compromisso(compromisso),
            )

            return self.repository.cancelar_compromisso(compromisso)
        finally:
            clear_tenant()

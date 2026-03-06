from datetime import datetime
from uuid import UUID

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.tenant.tenant_context import get_tenant
from app.models.appointment import Appointment as Compromisso
from app.models.appointment import AppointmentStatus as StatusCompromisso
from app.models.appointment_participant import AppointmentParticipant as ParticipanteCompromisso
from app.repositorios.base_repository import BaseRepository


class CompromissoRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def criar_compromisso(
        self,
        compromisso: Compromisso,
        participantes: list[ParticipanteCompromisso],
        auto_commit: bool = True,
    ) -> Compromisso:
        self.add(compromisso)
        self.flush()
        if participantes:
            self.add_all(participantes)
        if auto_commit:
            self.commit()
            self.refresh(compromisso)
        return compromisso

    def buscar_por_id(self, compromisso_id: UUID) -> Compromisso | None:
        tenant_id = get_tenant()
        if tenant_id is None:
            raise RuntimeError("Contexto de tenant é obrigatório")

        return (
            self.query(Compromisso)
            .filter(
                Compromisso.id == compromisso_id,
                Compromisso.company_id == tenant_id,
            )
            .first()
        )

    def existe_conflito_horario(
        self,
        usuarios_ids: list[UUID],
        inicio_em: datetime,
        fim_em: datetime,
        ignorar_compromisso_id: UUID | None = None,
    ) -> bool:
        if not usuarios_ids:
            return False

        tenant_id = get_tenant()
        if tenant_id is None:
            raise RuntimeError("Contexto de tenant é obrigatório")

        consulta = (
            self.query(Compromisso.id)
            .outerjoin(
                ParticipanteCompromisso,
                ParticipanteCompromisso.appointment_id == Compromisso.id,
            )
            .filter(Compromisso.status == StatusCompromisso.scheduled)
            .filter(Compromisso.start_time < fim_em)
            .filter(Compromisso.end_time > inicio_em)
            .filter(Compromisso.company_id == tenant_id)
            .filter(
                or_(
                    Compromisso.creator_id.in_(usuarios_ids),
                    ParticipanteCompromisso.user_id.in_(usuarios_ids),
                )
            )
        )

        if ignorar_compromisso_id is not None:
            consulta = consulta.filter(Compromisso.id != ignorar_compromisso_id)

        consulta = consulta.with_for_update()

        return consulta.first() is not None

    def atualizar_compromisso(self, compromisso: Compromisso) -> Compromisso:
        self.commit()
        self.refresh(compromisso)
        return compromisso

    def cancelar_compromisso(self, compromisso: Compromisso) -> Compromisso:
        self.commit()
        self.refresh(compromisso)
        return compromisso

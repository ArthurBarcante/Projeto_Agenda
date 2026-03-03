from datetime import datetime
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.compromisso import Compromisso
from app.models.compromisso import StatusCompromisso
from app.models.participante_compromisso import ParticipanteCompromisso
from app.models.usuario import Usuario
from app.schemas.compromisso import CompromissoAtualizacao as AtualizacaoCompromissoLegado
from app.schemas.compromisso import CompromissoCriacao as CriacaoCompromissoLegado
from app.schemas.compromisso import CompromissoAtualizacao, CompromissoCriacao


class CompromissoService:
    def __init__(self, db: Session):
        self.db = db

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

        consulta = (
            self.db.query(Compromisso.id)
            .outerjoin(
                ParticipanteCompromisso,
                ParticipanteCompromisso.appointment_id == Compromisso.id,
            )
            .filter(Compromisso.status == StatusCompromisso.agendado)
            .filter(Compromisso.starts_at < fim_em)
            .filter(Compromisso.ends_at > inicio_em)
            .filter(
                or_(
                    Compromisso.creator_id.in_(usuarios_unicos_ids),
                    ParticipanteCompromisso.user_id.in_(usuarios_unicos_ids),
                )
            )
        )

        if ignorar_compromisso_id is not None:
            consulta = consulta.filter(Compromisso.id != ignorar_compromisso_id)

        if consulta.first() is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Conflito de horário para um ou mais usuários",
            )

    def criar_compromisso(
        self,
        dados: CompromissoCriacao | CriacaoCompromissoLegado,
        usuario_atual: Usuario,
    ) -> Compromisso:
        payload = dados.model_dump()

        participantes_ids = [
            participante_id
            for participante_id in dict.fromkeys(payload["participantes_ids"])
            if participante_id != usuario_atual.id
        ]

        usuarios_para_validar = [usuario_atual.id, *participantes_ids]
        self._verificar_conflito_horario(
            usuarios_ids=usuarios_para_validar,
            inicio_em=payload["inicio_em"],
            fim_em=payload["fim_em"],
        )

        compromisso = Compromisso(
            company_id=usuario_atual.company_id,
            creator_id=usuario_atual.id,
            title=payload["titulo"],
            description=payload["descricao"],
            starts_at=payload["inicio_em"],
            ends_at=payload["fim_em"],
            status=StatusCompromisso.agendado,
        )
        self.db.add(compromisso)
        self.db.flush()

        for participante_id in participantes_ids:
            self.db.add(
                ParticipanteCompromisso(
                    company_id=usuario_atual.company_id,
                    appointment_id=compromisso.id,
                    user_id=participante_id,
                )
            )

        self.db.commit()
        self.db.refresh(compromisso)
        return compromisso

    def obter_ou_404(self, compromisso_id: UUID) -> Compromisso:
        compromisso = (
            self.db.query(Compromisso)
            .filter(Compromisso.id == compromisso_id)
            .first()
        )

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
        compromisso = self.obter_ou_404(compromisso_id)

        self._garantir_permissao_criador(compromisso, usuario_atual)

        if not compromisso.pode_ser_atualizado():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Apenas compromissos agendados podem ser atualizados",
            )

        payload = dados.model_dump(exclude_unset=True)
        if "inicio_em" in payload or "fim_em" in payload:
            inicio_em = payload.get("inicio_em", compromisso.starts_at)
            fim_em = payload.get("fim_em", compromisso.ends_at)

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
            "inicio_em": "starts_at",
            "fim_em": "ends_at",
        }

        for campo, valor in payload.items():
            setattr(compromisso, mapa_campos.get(campo, campo), valor)

        self.db.commit()
        self.db.refresh(compromisso)

        return compromisso

    def cancelar_compromisso(
        self,
        compromisso_id: UUID,
        usuario_atual: Usuario,
    ) -> Compromisso:
        compromisso = self.obter_ou_404(compromisso_id)

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

        self.db.commit()
        self.db.refresh(compromisso)

        return compromisso


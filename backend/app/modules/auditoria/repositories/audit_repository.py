from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repositorios.base_repository import BaseRepository


class AuditRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def registrar_evento(
        self,
        tenant_id: UUID,
        usuario_id: UUID | None,
        acao: str,
        entidade: str,
        entidade_id: UUID,
        dados_antes: dict[str, Any] | None,
        dados_depois: dict[str, Any] | None,
    ) -> AuditLog:
        evento = AuditLog(
            tenant_id=tenant_id,
            user_id=usuario_id,
            action=acao,
            entity=entidade,
            entity_id=entidade_id,
            before_data=dados_antes,
            after_data=dados_depois,
        )
        self.add(evento)
        self.flush()
        return evento
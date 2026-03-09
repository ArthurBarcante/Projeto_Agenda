from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.notifications.models.audit_log import AuditLog
from app.core.db.repositories import BaseRepository


class AuditRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def registrar_evento(
        self,
        tenant_id: UUID,
        user_id: UUID | None,
        acao: str,
        entity: str,
        entidade_id: UUID,
        dados_antes: dict[str, Any] | None,
        dados_depois: dict[str, Any] | None,
    ) -> AuditLog:
        evento = AuditLog(
            tenant_id=tenant_id,
            user_id=user_id,
            action=acao,
            entity=entity,
            entity_id=entidade_id,
            before_data=dados_antes,
            after_data=dados_depois,
        )
        self.add(evento)
        self.flush()
        return evento
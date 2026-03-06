from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.modules.auditoria.repositories.audit_repository import AuditRepository


class AuditService:
    def __init__(self, db: Session) -> None:
        self.repository = AuditRepository(db)

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
        return self.repository.registrar_evento(
            tenant_id=tenant_id,
            usuario_id=usuario_id,
            acao=acao,
            entidade=entidade,
            entidade_id=entidade_id,
            dados_antes=dados_antes,
            dados_depois=dados_depois,
        )
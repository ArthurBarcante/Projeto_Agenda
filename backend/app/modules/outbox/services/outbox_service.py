from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.outbox.models.outbox_event import OutboxEvent
from app.modules.outbox.repositories.outbox_repository import OutboxRepository


class OutboxService:
    def __init__(self, db: Session):
        self.repository = OutboxRepository(db)

    def registrar_evento(
        self,
        empresa_id: UUID,
        tipo_evento: str,
        payload: dict[str, object],
    ) -> OutboxEvent:
        return self.repository.criar_evento(
            empresa_id=empresa_id,
            tipo_evento=tipo_evento,
            payload=payload,
        )

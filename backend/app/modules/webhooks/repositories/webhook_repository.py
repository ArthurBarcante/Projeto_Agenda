from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.webhooks.models.webhook_subscription import WebhookSubscription
from app.repositorios.base_repository import BaseRepository


class WebhookRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def buscar_por_evento(
        self,
        event_type: str,
        empresa_id: UUID,
    ) -> list[WebhookSubscription]:
        return (
            self.query(WebhookSubscription)
            .filter(WebhookSubscription.event_type == event_type)
            .filter(WebhookSubscription.company_id == empresa_id)
            .filter(WebhookSubscription.is_active.is_(True))
            .all()
        )

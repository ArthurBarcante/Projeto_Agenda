from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.notifications.models.webhook_subscription import WebhookSubscription
from app.core.db.repositories import BaseRepository


class WebhookRepository(BaseRepository):
    def __init__(self, db: Session) -> None:
        super().__init__(db)

    def buscar_por_evento(
        self,
        event_type: str,
        company_id: UUID,
    ) -> list[WebhookSubscription]:
        return (
            self.query(WebhookSubscription)
            .filter(WebhookSubscription.event_type == event_type)
            .filter(WebhookSubscription.company_id == company_id)
            .filter(WebhookSubscription.is_active.is_(True))
            .all()
        )

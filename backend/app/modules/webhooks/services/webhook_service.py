import hashlib
import hmac
import json
import logging
from uuid import UUID

import requests
from sqlalchemy.orm import Session

from app.modules.webhooks.repositories.webhook_repository import WebhookRepository


logger = logging.getLogger(__name__)


class WebhookService:
    def __init__(self, db: Session, repository: WebhookRepository | None = None):
        self.db = db
        self.repository = repository or WebhookRepository(db)

    def _gerar_assinatura(self, payload: dict[str, object], secret: str) -> str:
        corpo_json = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        digest = hmac.new(
            secret.encode("utf-8"),
            corpo_json.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return digest

    def enviar_webhooks(
        self,
        event_type: str,
        payload: dict[str, object],
        empresa_id: UUID,
    ) -> None:
        subscriptions = self.repository.buscar_por_evento(
            event_type=event_type,
            empresa_id=empresa_id,
        )

        for subscription in subscriptions:
            assinatura = self._gerar_assinatura(payload, subscription.secret)
            headers = {
                "Content-Type": "application/json",
                "X-AIGENDA-SIGNATURE": assinatura,
            }

            try:
                requests.post(
                    subscription.url,
                    json=payload,
                    headers=headers,
                    timeout=5,
                )
            except requests.RequestException:
                logger.exception(
                    "Falha ao enviar webhook",
                    extra={
                        "url": subscription.url,
                        "empresa_id": str(empresa_id),
                        "event_type": event_type,
                    },
                )

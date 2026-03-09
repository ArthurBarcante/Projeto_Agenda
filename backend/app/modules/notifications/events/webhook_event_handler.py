import logging
from typing import Any
from uuid import UUID

from app.core.db.session_scope import SessionLocal
from app.modules.notifications.services.webhook_service import WebhookService


logger = logging.getLogger(__name__)


def _get_event_field(event: Any, nome_campo: str) -> Any:
    if hasattr(event, nome_campo):
        return getattr(event, nome_campo)
    if isinstance(event, dict):
        return event.get(nome_campo)
    return None


def _processar_evento(event: Any) -> None:
    event_type = _get_event_field(event, "event_type")
    payload = _get_event_field(event, "payload")
    company_id_raw = _get_event_field(event, "company_id")

    if not event_type or not isinstance(payload, dict) or company_id_raw is None:
        logger.error("Evento invalid para webhook", extra={"evento": str(event)})
        return

    company_id = UUID(str(company_id_raw))

    db = SessionLocal()
    try:
        service = WebhookService(db)
        service.enviar_webhooks(
            event_type=str(event_type),
            payload=payload,
            company_id=company_id,
        )
    finally:
        db.close()


def handle_appointment_created(event: Any) -> None:
    _processar_evento(event)


def handle_appointment_cancelled(event: Any) -> None:
    _processar_evento(event)

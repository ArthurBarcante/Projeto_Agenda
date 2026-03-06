import logging
from typing import Any
from uuid import UUID

from app.db.sessao import SessaoLocal
from app.modules.webhooks.services.webhook_service import WebhookService


logger = logging.getLogger(__name__)


def _obter_campo_evento(event: Any, nome_campo: str) -> Any:
    if hasattr(event, nome_campo):
        return getattr(event, nome_campo)
    if isinstance(event, dict):
        return event.get(nome_campo)
    return None


def _processar_evento(event: Any) -> None:
    tipo_evento = _obter_campo_evento(event, "tipo_evento")
    payload = _obter_campo_evento(event, "payload")
    empresa_id_raw = _obter_campo_evento(event, "company_id")

    if not tipo_evento or not isinstance(payload, dict) or empresa_id_raw is None:
        logger.error("Evento inválido para webhook", extra={"evento": str(event)})
        return

    empresa_id = UUID(str(empresa_id_raw))

    db = SessaoLocal()
    try:
        service = WebhookService(db)
        service.enviar_webhooks(
            event_type=str(tipo_evento),
            payload=payload,
            empresa_id=empresa_id,
        )
    finally:
        db.close()


def handle_compromisso_criado(event: Any) -> None:
    _processar_evento(event)


def handle_compromisso_cancelado(event: Any) -> None:
    _processar_evento(event)

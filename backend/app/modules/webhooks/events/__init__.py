from app.core.events.event_handler_registry import event_handler_registry
from app.core.events.event_types import EventType
from app.modules.webhooks.events.webhook_event_handler import (
    handle_compromisso_cancelado,
    handle_compromisso_criado,
)


def registrar_handlers_webhooks() -> None:
    event_handler_registry.registrar_handler(
        EventType.COMPROMISSO_CRIADO,
        handle_compromisso_criado,
    )
    event_handler_registry.registrar_handler(
        EventType.COMPROMISSO_CANCELADO,
        handle_compromisso_cancelado,
    )

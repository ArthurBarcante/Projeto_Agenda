from app.core.events.event_handler_registry import event_handler_registry
from app.core.events.event_types import EventType
from app.modules.notifications.events.webhook_event_handler import (
    handle_appointment_cancelled,
    handle_appointment_created,
)


def register_webhook_handlers() -> None:
    event_handler_registry.register_handler(
        EventType.APPOINTMENT_CREATED,
        handle_appointment_created,
    )
    event_handler_registry.register_handler(
        EventType.APPOINTMENT_CANCELLED,
        handle_appointment_cancelled,
    )

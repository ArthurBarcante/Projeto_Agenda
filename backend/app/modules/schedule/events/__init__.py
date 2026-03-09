from app.core.events.event_handler_registry import event_handler_registry
from app.core.events.event_types import EventType
from app.modules.schedule.events.handlers.appointment_cancelled_handler import (
    handle_appointment_cancelled,
)
from app.modules.schedule.events.handlers.appointment_created_handler import (
    handle_appointment_created,
)


def register_schedule_handlers() -> None:
    event_handler_registry.register_handler(
        EventType.APPOINTMENT_CREATED,
        handle_appointment_created,
    )
    event_handler_registry.register_handler(
        EventType.APPOINTMENT_CANCELLED,
        handle_appointment_cancelled,
    )

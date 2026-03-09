import logging
from typing import Any

from app.core.events.event_handler_registry import EventHandlerRegistry, event_handler_registry
from app.core.events.event_types import EventType


logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self, registry: EventHandlerRegistry):
        self._registry = registry

    def dispatch(self, event: Any) -> None:
        event_type = self._obter_tipo_evento(event)
        handlers = self._registry.buscar_handlers(event_type)

        for handler in handlers:
            handler(event)

    @staticmethod
    def _obter_tipo_evento(event: Any) -> EventType:
        if hasattr(event, "event_type"):
            return EventType(getattr(event, "event_type"))

        if isinstance(event, dict) and "event_type" in event:
            return EventType(event["event_type"])

        logger.error("Evento sem campo 'event_type'")
        raise ValueError("Evento sem campo 'event_type'")


event_bus = EventBus(event_handler_registry)

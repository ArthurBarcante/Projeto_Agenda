import logging
from typing import Any

from app.core.events.event_handler_registry import EventHandlerRegistry, event_handler_registry
from app.core.events.event_types import EventType


logger = logging.getLogger(__name__)


class EventBus:
    def __init__(self, registry: EventHandlerRegistry):
        self._registry = registry

    def dispatch(self, event: Any) -> None:
        tipo_evento = self._obter_tipo_evento(event)
        handlers = self._registry.buscar_handlers(tipo_evento)

        for handler in handlers:
            handler(event)

    @staticmethod
    def _obter_tipo_evento(event: Any) -> EventType:
        if hasattr(event, "tipo_evento"):
            return EventType(getattr(event, "tipo_evento"))

        if isinstance(event, dict) and "tipo_evento" in event:
            return EventType(event["tipo_evento"])

        logger.error("Evento sem campo 'tipo_evento'")
        raise ValueError("Evento sem campo 'tipo_evento'")


event_bus = EventBus(event_handler_registry)

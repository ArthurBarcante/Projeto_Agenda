from collections import defaultdict
from typing import Any, Callable

from app.core.events.event_types import EventType


EventHandler = Callable[[Any], None]


class EventHandlerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[EventType, list[EventHandler]] = defaultdict(list)

    def register_handler(self, event_type: EventType | str, handler: EventHandler) -> None:
        tipo = EventType(event_type)
        handlers = self._handlers[tipo]
        if handler not in handlers:
            handlers.append(handler)

    def buscar_handlers(self, event_type: EventType | str) -> list[EventHandler]:
        tipo = EventType(event_type)
        return list(self._handlers.get(tipo, []))


event_handler_registry = EventHandlerRegistry()

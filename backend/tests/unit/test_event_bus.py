from types import SimpleNamespace

from app.core.events.event_bus import EventBus
from app.core.events.event_handler_registry import EventHandlerRegistry
from app.core.events.event_types import EventType


def test_evento_dispara_execucao_do_handler_registrado():
    processed_events: list[str] = []

    def handler(evento):
        processed_events.append(evento.event_type)

    registry = EventHandlerRegistry()
    registry.register_handler(EventType.APPOINTMENT_CREATED, handler)
    bus = EventBus(registry)

    evento = SimpleNamespace(event_type=EventType.APPOINTMENT_CREATED.value)

    bus.dispatch(evento)

    assert processed_events == [EventType.APPOINTMENT_CREATED.value]

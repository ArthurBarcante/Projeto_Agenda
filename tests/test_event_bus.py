from types import SimpleNamespace

from app.core.events.event_bus import EventBus
from app.core.events.event_handler_registry import EventHandlerRegistry
from app.core.events.event_types import EventType


def test_evento_dispara_execucao_do_handler_registrado():
    eventos_processados: list[str] = []

    def handler(evento):
        eventos_processados.append(evento.tipo_evento)

    registry = EventHandlerRegistry()
    registry.registrar_handler(EventType.COMPROMISSO_CRIADO, handler)
    bus = EventBus(registry)

    evento = SimpleNamespace(tipo_evento=EventType.COMPROMISSO_CRIADO.value)

    bus.dispatch(evento)

    assert eventos_processados == [EventType.COMPROMISSO_CRIADO.value]

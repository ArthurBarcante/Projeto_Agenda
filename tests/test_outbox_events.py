from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

from app.modules.outbox.models.outbox_event import StatusOutboxEvento
from app.modules.outbox.repositories.outbox_repository import OutboxRepository
from app.modules.outbox.services.outbox_service import OutboxService


class FakeQuery:
    def __init__(self, resultados):
        self.resultados = resultados
        self.limite = None

    def filter(self, *_args):
        return self

    def order_by(self, *_args):
        return self

    def limit(self, limite):
        self.limite = limite
        return self

    def all(self):
        return self.resultados


class FakeSession:
    def __init__(self, resultados_consulta=None):
        self.adicionados = []
        self.flush_count = 0
        self.query_resultados = resultados_consulta or []
        self.last_query = None

    def add(self, instance):
        self.adicionados.append(instance)

    def flush(self):
        self.flush_count += 1

    def query(self, _model):
        self.last_query = FakeQuery(self.query_resultados)
        return self.last_query


def test_registro_de_evento():
    db = FakeSession()
    service = OutboxService(db)
    empresa_id = uuid4()

    evento = service.registrar_evento(
        empresa_id=empresa_id,
        tipo_evento="COMPROMISSO_CRIADO",
        payload={"compromisso_id": str(uuid4())},
    )

    assert len(db.adicionados) == 1
    assert evento.company_id == empresa_id
    assert evento.tipo_evento == "COMPROMISSO_CRIADO"
    assert evento.status == StatusOutboxEvento.PENDING.value
    assert evento.tentativas == 0
    assert db.flush_count == 1


def test_consulta_eventos_pendentes():
    evento = SimpleNamespace(id=uuid4())
    db = FakeSession(resultados_consulta=[evento])
    repository = OutboxRepository(db)

    resultado = repository.buscar_eventos_pendentes(limite=10)

    assert resultado == [evento]
    assert db.last_query is not None
    assert db.last_query.limite == 10


def test_mudanca_de_status():
    db = FakeSession()
    repository = OutboxRepository(db)

    evento = SimpleNamespace(
        status=StatusOutboxEvento.PENDING.value,
        tentativas=0,
        processar_em=datetime.now(timezone.utc),
    )

    repository.marcar_como_processando(evento)
    assert evento.status == StatusOutboxEvento.PROCESSING.value

    repository.marcar_como_concluido(evento)
    assert evento.status == StatusOutboxEvento.DONE.value

    repository.incrementar_tentativa(evento, max_tentativas=5, retry_delay_segundos=30)
    assert evento.status == StatusOutboxEvento.PENDING.value
    assert evento.tentativas == 1
    assert db.flush_count == 3

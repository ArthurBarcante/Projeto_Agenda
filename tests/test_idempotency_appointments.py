import os
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient


os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from app.api import dependencias
from app.models.compromisso import StatusCompromisso
from app.modules.agenda.api import compromissos as compromissos_api
from app.modules.agenda.services.compromisso_service import CompromissoService
from app.modules.permissoes.services.permission_service import PermissionService
from app.principal import app


class _CompromissoFalso:
    def __init__(self, empresa_id, criador_id):
        agora = datetime.now(timezone.utc).replace(microsecond=0)
        self.id = uuid4()
        self.company_id = empresa_id
        self.creator_id = criador_id
        self.title = "Reunião de planejamento"
        self.description = "Definir tarefas da sprint"
        self.starts_at = agora + timedelta(hours=1)
        self.ends_at = agora + timedelta(hours=2)
        self.status = StatusCompromisso.agendado
        self.created_at = agora
        self.updated_at = agora


class _IdempotencyServiceFalso:
    _armazenamento: dict[tuple[str, str], dict] = {}

    def __init__(self, db):
        self.db = db

    async def verificar_idempotencia(self, request, empresa_id):
        from fastapi.responses import JSONResponse

        chave = request.headers.get("Idempotency-Key")
        if not chave:
            return None

        registro = self._armazenamento.get((str(empresa_id), chave))
        if registro is None:
            return None

        return JSONResponse(
            content=registro["response_body"],
            status_code=registro["status_code"],
        )

    async def registrar_resposta(self, request, empresa_id, response_body, status_code):
        chave = request.headers.get("Idempotency-Key")
        if not chave:
            return

        self._armazenamento[(str(empresa_id), chave)] = {
            "response_body": response_body,
            "status_code": status_code,
        }


def test_post_compromisso_repetido_com_mesma_idempotency_key_retorna_mesma_resposta(monkeypatch):
    empresa_id = uuid4()
    usuario_id = uuid4()
    usuario_atual = SimpleNamespace(id=usuario_id, company_id=empresa_id)

    def override_obter_db():
        yield SimpleNamespace()

    def override_obter_usuario_atual():
        return usuario_atual

    app.dependency_overrides[dependencias.obter_db] = override_obter_db
    app.dependency_overrides[dependencias.obter_usuario_atual] = override_obter_usuario_atual

    contador_criacao = {"total": 0}

    def fake_criar_compromisso(self, dados, usuario_atual):
        contador_criacao["total"] += 1
        return _CompromissoFalso(
            empresa_id=usuario_atual.company_id,
            criador_id=usuario_atual.id,
        )

    monkeypatch.setattr(CompromissoService, "criar_compromisso", fake_criar_compromisso)
    monkeypatch.setattr(compromissos_api, "IdempotencyService", _IdempotencyServiceFalso)
    monkeypatch.setattr(PermissionService, "usuario_tem_permissao", lambda *args, **kwargs: True)
    _IdempotencyServiceFalso._armazenamento.clear()

    client = TestClient(app)
    payload = {
        "titulo": "Reunião de planejamento",
        "descricao": "Definir tarefas da sprint",
        "inicio_em": "2026-03-06T10:00:00Z",
        "fim_em": "2026-03-06T11:00:00Z",
        "participantes_ids": [],
    }
    headers = {"Idempotency-Key": "idem-key-123"}

    try:
        resposta_1 = client.post("/compromissos", json=payload, headers=headers)
        resposta_2 = client.post("/compromissos", json=payload, headers=headers)
    finally:
        app.dependency_overrides.clear()

    assert resposta_1.status_code == 201
    assert resposta_2.status_code == 201
    assert resposta_2.json() == resposta_1.json()
    assert contador_criacao["total"] == 1

import os
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient


os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from app.api import dependencias
from app.models.compromisso import StatusCompromisso
from app.modules.agenda.services.compromisso_service import CompromissoService
from app.modules.permissoes.services.permission_service import PermissionService
from app.principal import app


class _CompromissoFalso:
    def __init__(self, empresa_id, criador_id):
        agora = datetime.now(timezone.utc).replace(microsecond=0)
        self.id = uuid4()
        self.company_id = empresa_id
        self.creator_id = criador_id
        self.title = "Reunião"
        self.description = "Planejamento"
        self.starts_at = agora + timedelta(hours=1)
        self.ends_at = agora + timedelta(hours=2)
        self.status = StatusCompromisso.agendado
        self.created_at = agora
        self.updated_at = agora


def _override_obter_db():
    yield SimpleNamespace()


def _build_payload():
    return {
        "titulo": "Reunião",
        "descricao": "Planejamento",
        "inicio_em": "2026-03-06T10:00:00Z",
        "fim_em": "2026-03-06T11:00:00Z",
        "participantes_ids": [],
    }


def test_usuario_com_permissao_tem_acesso(monkeypatch):
    empresa_id = uuid4()
    usuario_id = uuid4()
    usuario_atual = SimpleNamespace(id=usuario_id, company_id=empresa_id)

    def override_obter_usuario_atual():
        return usuario_atual

    def fake_criar_compromisso(self, dados, usuario_atual):
        return _CompromissoFalso(
            empresa_id=usuario_atual.company_id,
            criador_id=usuario_atual.id,
        )

    monkeypatch.setattr(PermissionService, "usuario_tem_permissao", lambda *args, **kwargs: True)
    monkeypatch.setattr(CompromissoService, "criar_compromisso", fake_criar_compromisso)

    app.dependency_overrides[dependencias.obter_db] = _override_obter_db
    app.dependency_overrides[dependencias.obter_usuario_atual] = override_obter_usuario_atual

    client = TestClient(app)
    try:
        response = client.post("/compromissos", json=_build_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201


def test_usuario_sem_permissao_recebe_403(monkeypatch):
    empresa_id = uuid4()
    usuario_id = uuid4()
    usuario_atual = SimpleNamespace(id=usuario_id, company_id=empresa_id)

    def override_obter_usuario_atual():
        return usuario_atual

    monkeypatch.setattr(PermissionService, "usuario_tem_permissao", lambda *args, **kwargs: False)

    app.dependency_overrides[dependencias.obter_db] = _override_obter_db
    app.dependency_overrides[dependencias.obter_usuario_atual] = override_obter_usuario_atual

    client = TestClient(app)
    try:
        response = client.post("/compromissos", json=_build_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403

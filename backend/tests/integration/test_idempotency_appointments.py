import os
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient


os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from app.dependencies import fastapi as dependencies
from app.modules.schedule.models.appointment import AppointmentStatusAlias
from app.api.routers import schedule as appointments_api
from app.modules.schedule.services.appointment_service import AppointmentService
from app.modules.permissions.services.permission_service import PermissionService
from main import app


class _FakeAppointment:
    def __init__(self, company_id, creator_id):
        agora = datetime.now(timezone.utc).replace(microsecond=0)
        self.id = uuid4()
        self.company_id = company_id
        self.creator_id = creator_id
        self.title = "Planning meeting"
        self.description = "Definir tarefas da sprint"
        self.start_time = agora + timedelta(hours=1)
        self.end_time = agora + timedelta(hours=2)
        self.status = AppointmentStatusAlias.scheduled
        self.created_at = agora
        self.updated_at = agora


class _IdempotencyServiceFalso:
    _armazenamento: dict[tuple[str, str], dict] = {}

    def __init__(self, db):
        self.db = db

    async def verificar_idempotencia(self, request, company_id):
        from fastapi.responses import JSONResponse

        key = request.headers.get("Idempotency-Key")
        if not key:
            return None

        registro = self._armazenamento.get((str(company_id), key))
        if registro is None:
            return None

        return JSONResponse(
            content=registro["response_body"],
            status_code=registro["status_code"],
        )

    async def registrar_resposta(self, request, company_id, response_body, status_code):
        key = request.headers.get("Idempotency-Key")
        if not key:
            return

        self._armazenamento[(str(company_id), key)] = {
            "response_body": response_body,
            "status_code": status_code,
        }


def test_repeated_post_appointment_with_same_idempotency_key_returns_same_response(monkeypatch):
    company_id = uuid4()
    user_id = uuid4()
    current_user = SimpleNamespace(id=user_id, company_id=company_id)

    def override_obter_db():
        yield SimpleNamespace()

    def override_get_current_user():
        return current_user

    app.dependency_overrides[dependencies.get_db] = override_obter_db
    app.dependency_overrides[dependencies.get_current_user] = override_get_current_user

    contador_criacao = {"total": 0}

    def fake_create_appointment(self, dados, current_user):
        contador_criacao["total"] += 1
        return _FakeAppointment(
            company_id=current_user.company_id,
            creator_id=current_user.id,
        )

    monkeypatch.setattr(AppointmentService, "create_appointment", fake_create_appointment)
    monkeypatch.setattr(appointments_api, "IdempotencyService", _IdempotencyServiceFalso)
    monkeypatch.setattr(PermissionService, "user_has_permission", lambda *args, **kwargs: True)
    _IdempotencyServiceFalso._armazenamento.clear()

    client = TestClient(app)
    payload = {
        "title": "Planning meeting",
        "description": "Definir tarefas da sprint",
        "start_time": "2026-03-06T10:00:00Z",
        "end_time": "2026-03-06T11:00:00Z",
        "participantes_ids": [],
    }
    headers = {"Idempotency-Key": "idem-key-123"}

    try:
        resposta_1 = client.post("/appointments", json=payload, headers=headers)
        resposta_2 = client.post("/appointments", json=payload, headers=headers)
    finally:
        app.dependency_overrides.clear()

    assert resposta_1.status_code == 201
    assert resposta_2.status_code == 201
    assert resposta_2.json() == resposta_1.json()
    assert contador_criacao["total"] == 1

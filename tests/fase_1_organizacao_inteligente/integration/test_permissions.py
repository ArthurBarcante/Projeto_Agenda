import os
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

from fastapi.testclient import TestClient


os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from app.dependencies import fastapi as dependencies
from app.modules.schedule.models.appointment import AppointmentStatusAlias
from app.modules.schedule.services.appointment_service import AppointmentService
from app.modules.permissions.services.permission_service import PermissionService
from app.main import app


class _FakeAppointment:
    def __init__(self, company_id, creator_id):
        agora = datetime.now(timezone.utc).replace(microsecond=0)
        self.id = uuid4()
        self.company_id = company_id
        self.creator_id = creator_id
        self.title = "Meeting"
        self.description = "Planejamento"
        self.start_time = agora + timedelta(hours=1)
        self.end_time = agora + timedelta(hours=2)
        self.status = AppointmentStatusAlias.scheduled
        self.created_at = agora
        self.updated_at = agora


def _override_obter_db():
    yield SimpleNamespace()


def _build_payload():
    return {
        "title": "Meeting",
        "description": "Planejamento",
        "start_time": "2026-03-06T10:00:00Z",
        "end_time": "2026-03-06T11:00:00Z",
        "participantes_ids": [],
    }


def test_user_with_permission_has_access(monkeypatch):
    company_id = uuid4()
    user_id = uuid4()
    current_user = SimpleNamespace(id=user_id, company_id=company_id)

    def override_get_current_user():
        return current_user

    def fake_create_appointment(self, dados, current_user):
        return _FakeAppointment(
            company_id=current_user.company_id,
            creator_id=current_user.id,
        )

    monkeypatch.setattr(PermissionService, "user_has_permission", lambda *args, **kwargs: True)
    monkeypatch.setattr(AppointmentService, "create_appointment", fake_create_appointment)

    app.dependency_overrides[dependencies.get_db] = _override_obter_db
    app.dependency_overrides[dependencies.get_current_user] = override_get_current_user

    client = TestClient(app)
    try:
        response = client.post("/appointments", json=_build_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201


def test_user_without_permission_receives_403(monkeypatch):
    company_id = uuid4()
    user_id = uuid4()
    current_user = SimpleNamespace(id=user_id, company_id=company_id)

    def override_get_current_user():
        return current_user

    monkeypatch.setattr(PermissionService, "user_has_permission", lambda *args, **kwargs: False)

    app.dependency_overrides[dependencies.get_db] = _override_obter_db
    app.dependency_overrides[dependencies.get_current_user] = override_get_current_user

    client = TestClient(app)
    try:
        response = client.post("/appointments", json=_build_payload())
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403

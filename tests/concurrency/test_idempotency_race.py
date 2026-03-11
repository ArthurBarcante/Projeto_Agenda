import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.dependencies import fastapi as dependencies
from app.main import app
from app.modules.idempotency.repositories.idempotency_repository import IdempotencyRepository
from app.modules.permissions.services.permission_service import PermissionService
from app.modules.schedule.services.appointment_service import AppointmentService


def _create_test_tables(db: Session) -> None:
    db.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS appointments (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                creator_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
    )
    db.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS idempotency_keys (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                key TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                method TEXT NOT NULL,
                request_hash TEXT NOT NULL,
                response_body TEXT,
                status_code INTEGER,
                state TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT,
                UNIQUE(company_id, key)
            )
            """
        )
    )
    db.commit()


def _normalize_response_timestamps(body: dict) -> dict:
    normalized = dict(body)
    for field in ("start_time", "end_time", "created_at", "updated_at"):
        value = normalized.get(field)
        if isinstance(value, str):
            normalized[field] = datetime.fromisoformat(value.replace("Z", "+00:00")).isoformat()
    return normalized


@pytest.mark.asyncio
async def test_idempotency_prevents_duplicate_creation_under_concurrency(client, monkeypatch, tmp_path):
    database_file = tmp_path / "idempotency_race.db"
    engine = create_engine(
        f"sqlite+pysqlite:///{database_file}",
        connect_args={"check_same_thread": False},
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    setup_db = SessionLocal()
    try:
        _create_test_tables(setup_db)
    finally:
        setup_db.close()

    company_id = uuid4()
    user_id = uuid4()
    fixed_appointment_id = uuid4()
    now = datetime.now(timezone.utc).replace(microsecond=0)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_get_current_user():
        return SimpleNamespace(id=user_id, company_id=company_id)

    def fake_create_appointment(self, dados, current_user):
        self.db.execute(
            text(
                """
                INSERT INTO appointments (
                    id,
                    company_id,
                    creator_id,
                    title,
                    description,
                    start_time,
                    end_time,
                    status,
                    created_at,
                    updated_at
                ) VALUES (
                    :id,
                    :company_id,
                    :creator_id,
                    :title,
                    :description,
                    :start_time,
                    :end_time,
                    :status,
                    :created_at,
                    :updated_at
                )
                """
            ),
            {
                "id": str(fixed_appointment_id),
                "company_id": str(current_user.company_id),
                "creator_id": str(current_user.id),
                "title": dados.title,
                "description": dados.description,
                "start_time": dados.start_time.isoformat(),
                "end_time": dados.end_time.isoformat(),
                "status": "scheduled",
                "created_at": now.isoformat(),
                "updated_at": now.isoformat(),
            },
        )
        self.db.commit()

        return SimpleNamespace(
            id=fixed_appointment_id,
            company_id=current_user.company_id,
            creator_id=current_user.id,
            title=dados.title,
            description=dados.description,
            start_time=dados.start_time,
            end_time=dados.end_time,
            status="scheduled",
            created_at=now,
            updated_at=now,
        )

    app.dependency_overrides[dependencies.get_db] = override_get_db
    app.dependency_overrides[dependencies.get_current_user] = override_get_current_user

    original_buscar_por_chave = IdempotencyRepository.buscar_por_chave

    def buscar_por_chave_com_refresh(self, company_id, key):
        self.db.expire_all()
        return original_buscar_por_chave(self, company_id, key)

    monkeypatch.setattr(IdempotencyRepository, "buscar_por_chave", buscar_por_chave_com_refresh)
    monkeypatch.setattr(PermissionService, "user_has_permission", lambda *args, **kwargs: True)
    monkeypatch.setattr(AppointmentService, "create_appointment", fake_create_appointment)

    payload = {
        "title": "Concurrency check",
        "description": "Race condition validation",
        "start_time": "2026-03-12T10:00:00Z",
        "end_time": "2026-03-12T11:00:00Z",
        "participantes_ids": [],
    }
    headers = {"Idempotency-Key": "race-key-001"}

    test_client = client()

    async def do_post():
        return await asyncio.to_thread(
            test_client.post,
            "/appointments",
            json=payload,
            headers=headers,
        )

    try:
        responses = await asyncio.gather(*[do_post() for _ in range(10)])
    finally:
        app.dependency_overrides.clear()

    response_bodies = [response.json() for response in responses]
    normalized_bodies = [_normalize_response_timestamps(body) for body in response_bodies]

    assert all(response.status_code == 201 for response in responses)
    assert all(body == normalized_bodies[0] for body in normalized_bodies)

    verification_db = SessionLocal()
    try:
        appointment_count = verification_db.execute(
            text("SELECT COUNT(*) FROM appointments")
        ).scalar_one()
    finally:
        verification_db.close()

    assert appointment_count == 1

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.modules.schedule.models.appointment_participant import AppointmentParticipant  # noqa: F401
from app.modules.users.models.company import Company  # noqa: F401
from app.modules.users.models.user import User  # noqa: F401
from app.modules.schedule.services.appointment_service import AppointmentService
from app.modules.schedule.schemas.appointment import AppointmentCreate, AppointmentUpdate


def _build_chain_query(first_result):
    query = MagicMock()
    query.outerjoin.return_value = query
    query.filter.return_value = query
    query.with_for_update.return_value = query
    query.first.return_value = first_result
    return query


def _build_get_query(appointment):
    query = MagicMock()
    query.filter.return_value.first.return_value = appointment
    return query


def _build_appointment(*, creator_id, company_id):
    now = datetime.now(timezone.utc)
    appointment = SimpleNamespace(
        id=uuid4(),
        creator_id=creator_id,
        company_id=company_id,
        title="Existing",
        description="desc",
        start_time=now + timedelta(hours=1),
        end_time=now + timedelta(hours=2),
        participants=[SimpleNamespace(user_id=uuid4())],
    )
    appointment.can_be_updated = lambda: True
    return appointment


def test_create_returns_400_when_creator_has_conflict():
    creator_id = uuid4()
    company_id = uuid4()
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)

    db = MagicMock()
    db.query.return_value = _build_chain_query(first_result=SimpleNamespace(id=uuid4()))
    service = AppointmentService(db)

    data = AppointmentCreate(
        title="New",
        description=None,
        start_time=datetime.now(timezone.utc) + timedelta(hours=1),
        end_time=datetime.now(timezone.utc) + timedelta(hours=2),
        participant_ids=[],
    )

    with pytest.raises(HTTPException) as exc:
        service.create_appointment(data=data, current_user=current_user)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Time conflict for one or more users"


def test_create_returns_400_when_participant_has_conflict():
    creator_id = uuid4()
    participant_id = uuid4()
    company_id = uuid4()
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)

    db = MagicMock()
    db.query.return_value = _build_chain_query(first_result=SimpleNamespace(id=uuid4()))
    service = AppointmentService(db)

    data = AppointmentCreate(
        title="New",
        description=None,
        start_time=datetime.now(timezone.utc) + timedelta(hours=1),
        end_time=datetime.now(timezone.utc) + timedelta(hours=2),
        participant_ids=[participant_id],
    )

    with pytest.raises(HTTPException) as exc:
        service.create_appointment(data=data, current_user=current_user)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Time conflict for one or more users"


def test_update_returns_400_when_new_time_overlaps_existing():
    creator_id = uuid4()
    company_id = uuid4()
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)
    appointment = _build_appointment(creator_id=creator_id, company_id=company_id)

    db = MagicMock()
    db.query.side_effect = [
        _build_get_query(appointment),
        _build_chain_query(first_result=SimpleNamespace(id=uuid4())),
    ]
    service = AppointmentService(db)

    with pytest.raises(HTTPException) as exc:
        service.update_appointment(
            appointment_id=appointment.id,
            data=AppointmentUpdate(start_time=appointment.start_time + timedelta(minutes=15)),
            current_user=current_user,
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Time conflict for one or more users"


def test_create_succeeds_when_time_does_not_overlap():
    creator_id = uuid4()
    company_id = uuid4()
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)

    db = MagicMock()
    db.query.return_value = _build_chain_query(first_result=None)
    service = AppointmentService(db)

    data = AppointmentCreate(
        title="No conflict",
        description="ok",
        start_time=datetime.now(timezone.utc) + timedelta(hours=3),
        end_time=datetime.now(timezone.utc) + timedelta(hours=4),
        participant_ids=[],
    )

    created = service.create_appointment(data=data, current_user=current_user)

    assert created.title == "No conflict"
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(created)

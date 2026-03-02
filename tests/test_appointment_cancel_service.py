from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.core.tenant import clear_current_company_id, set_current_company_id
from app.models.appointment import AppointmentStatus
from app.modules.schedule.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentUpdate


def _build_appointment(*, creator_id, company_id, status: AppointmentStatus):
    now = datetime.now(timezone.utc)
    appointment = SimpleNamespace(
        id=uuid4(),
        creator_id=creator_id,
        company_id=company_id,
        title="Daily sync",
        description="Team alignment",
        starts_at=now + timedelta(hours=1),
        ends_at=now + timedelta(hours=2),
        status=status,
    )
    appointment.can_be_updated = lambda: appointment.status == AppointmentStatus.scheduled
    appointment.can_be_cancelled = lambda: appointment.status == AppointmentStatus.scheduled

    def cancel(user):
        if appointment.creator_id != user.id:
            raise PermissionError("Only the creator can cancel")

        if not appointment.can_be_cancelled():
            raise ValueError("Appointment cannot be cancelled")

        appointment.status = AppointmentStatus.cancelled

    appointment.cancel = cancel
    return appointment


def _build_service_with_query_result(result):
    db = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = result
    return AppointmentService(db), db


def test_creator_can_cancel_appointment():
    creator_id = uuid4()
    company_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        company_id=company_id,
        status=AppointmentStatus.scheduled,
    )
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)

    service, db = _build_service_with_query_result(appointment)
    result = service.cancel_appointment(appointment.id, current_user)

    assert result.status == AppointmentStatus.cancelled
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(appointment)


def test_participant_cannot_cancel_appointment():
    creator_id = uuid4()
    company_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        company_id=company_id,
        status=AppointmentStatus.scheduled,
    )
    participant_user = SimpleNamespace(id=uuid4(), company_id=company_id)

    service, db = _build_service_with_query_result(appointment)

    with pytest.raises(HTTPException) as exc:
        service.cancel_appointment(appointment.id, participant_user)

    assert exc.value.status_code == 403
    db.commit.assert_not_called()


def test_cannot_cancel_appointment_already_cancelled():
    creator_id = uuid4()
    company_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        company_id=company_id,
        status=AppointmentStatus.cancelled,
    )
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)

    service, db = _build_service_with_query_result(appointment)

    with pytest.raises(HTTPException) as exc:
        service.cancel_appointment(appointment.id, current_user)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Appointment cannot be cancelled"
    db.commit.assert_not_called()


def test_cancel_appointment_returns_404_for_other_tenant():
    creator_id = uuid4()
    company_a = uuid4()
    company_b = uuid4()
    appointment_id = uuid4()
    current_user = SimpleNamespace(id=creator_id, company_id=company_a)

    set_current_company_id(company_b)
    try:
        service, db = _build_service_with_query_result(None)

        with pytest.raises(HTTPException) as exc:
            service.cancel_appointment(appointment_id, current_user)
    finally:
        clear_current_company_id()

    assert exc.value.status_code == 404
    assert exc.value.detail == "Appointment not found"
    db.commit.assert_not_called()


def test_update_appointment_returns_400_when_status_is_cancelled():
    creator_id = uuid4()
    company_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        company_id=company_id,
        status=AppointmentStatus.cancelled,
    )
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)

    service, db = _build_service_with_query_result(appointment)

    with pytest.raises(HTTPException) as exc:
        service.update_appointment(
            appointment_id=appointment.id,
            data=AppointmentUpdate(title="Updated title"),
            current_user=current_user,
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Only scheduled appointments can be updated"
    db.commit.assert_not_called()


def test_update_appointment_returns_400_when_status_is_completed():
    creator_id = uuid4()
    company_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        company_id=company_id,
        status=AppointmentStatus.completed,
    )
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)

    service, db = _build_service_with_query_result(appointment)

    with pytest.raises(HTTPException) as exc:
        service.update_appointment(
            appointment_id=appointment.id,
            data=AppointmentUpdate(description="Updated description"),
            current_user=current_user,
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Only scheduled appointments can be updated"
    db.commit.assert_not_called()


def test_cancel_appointment_returns_400_when_status_is_completed():
    creator_id = uuid4()
    company_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        company_id=company_id,
        status=AppointmentStatus.completed,
    )
    current_user = SimpleNamespace(id=creator_id, company_id=company_id)

    service, db = _build_service_with_query_result(appointment)

    with pytest.raises(HTTPException) as exc:
        service.cancel_appointment(appointment.id, current_user)

    assert exc.value.status_code == 400
    assert exc.value.detail == "Appointment cannot be cancelled"
    db.commit.assert_not_called()
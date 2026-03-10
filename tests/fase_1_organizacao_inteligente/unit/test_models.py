from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.modules.schedule.models.appointment import Appointment, AppointmentStatus


def _appointment(end_time: datetime, status: AppointmentStatus = AppointmentStatus.scheduled):
    return Appointment(
        company_id=uuid4(),
        creator_id=uuid4(),
        title="Planning",
        description="Sprint",
        start_time=end_time - timedelta(hours=1),
        end_time=end_time,
        status=status,
    )


def test_appointment_is_expired_with_timezone_aware_datetime():
    past = datetime.now(timezone.utc) - timedelta(minutes=1)
    appointment = _appointment(end_time=past)

    assert appointment.is_expired() is True


def test_appointment_cancel_changes_status_for_creator():
    appointment = _appointment(end_time=datetime.now(timezone.utc) + timedelta(hours=1))
    creator = SimpleNamespace(id=appointment.creator_id)

    appointment.cancel(creator)

    assert appointment.status == AppointmentStatus.cancelled


def test_appointment_cancel_raises_for_non_creator():
    appointment = _appointment(end_time=datetime.now(timezone.utc) + timedelta(hours=1))

    with pytest.raises(PermissionError):
        appointment.cancel(SimpleNamespace(id=uuid4()))

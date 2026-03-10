from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.modules.schedule.models.appointment import Appointment, AppointmentStatus
from app.modules.schedule.models.appointment_participant import AppointmentParticipant  # noqa: F401
from app.modules.users.models.company import Company  # noqa: F401
from app.modules.users.models.user import User  # noqa: F401


def _build_appointment(*, creator_id, status: AppointmentStatus) -> Appointment:
    now = datetime.now(timezone.utc)
    return Appointment(
        creator_id=creator_id,
        company_id=uuid4(),
        title="Daily sync",
        description="Team alignment",
        start_time=now + timedelta(hours=1),
        end_time=now + timedelta(hours=2),
        status=status,
    )


def test_cancel_changes_status_when_creator_and_scheduled():
    creator_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        status=AppointmentStatus.scheduled,
    )
    current_user = SimpleNamespace(id=creator_id)

    appointment.cancel(current_user)

    assert appointment.status == AppointmentStatus.cancelled


def test_cancel_raises_permission_error_for_non_creator():
    creator_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        status=AppointmentStatus.scheduled,
    )
    current_user = SimpleNamespace(id=uuid4())

    with pytest.raises(PermissionError, match="Only the creator can cancel"):
        appointment.cancel(current_user)


def test_cancel_raises_value_error_when_not_cancellable():
    creator_id = uuid4()
    appointment = _build_appointment(
        creator_id=creator_id,
        status=AppointmentStatus.completed,
    )
    current_user = SimpleNamespace(id=creator_id)

    with pytest.raises(ValueError, match="Appointment cannot be cancelled"):
        appointment.cancel(current_user)

    assert appointment.status == AppointmentStatus.completed
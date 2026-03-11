from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.dependencies.fastapi import get_current_user, require_permission
from app.core.db.session_scope import get_db
from app.modules.idempotency.decorators import idempotent
from app.modules.users.models.user import User
from app.modules.schedule.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.modules.schedule.services.appointment_service import AppointmentService


router = APIRouter(prefix="/appointments", tags=["appointments"])
legacy_router = APIRouter(prefix="/appointments", tags=["appointments"])


def get_appointment_service(db: Session = Depends(get_db)):
    return AppointmentService(db)


@router.post("", response_model=AppointmentResponse, status_code=201)
@legacy_router.post("", response_model=AppointmentResponse, status_code=201)
@idempotent()
async def create_appointment(
    request: Request,
    dados: AppointmentCreate,
    current_user: User = Depends(require_permission("agenda.criar")),
    db: Session = Depends(get_db),
    service: AppointmentService = Depends(get_appointment_service),
):
    appointment = service.create_appointment(
        dados=dados,
        current_user=current_user,
    )

    return appointment


@router.put("/{appointment_id}", response_model=AppointmentResponse)
@legacy_router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: UUID,
    dados: AppointmentUpdate,
    current_user: User = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.update_appointment(
        appointment_id=appointment_id,
        dados=dados,
        current_user=current_user,
    )


@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
@legacy_router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: UUID,
    current_user: User = Depends(get_current_user),
    service: AppointmentService = Depends(get_appointment_service),
):
    return service.cancel_appointment(
        appointment_id=appointment_id,
        current_user=current_user,
    )

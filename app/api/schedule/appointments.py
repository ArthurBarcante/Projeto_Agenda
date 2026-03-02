from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.modules.schedule.services.appointment_service import AppointmentService
from app.schemas.appointment import AppointmentCreate
from app.schemas.appointment import AppointmentResponse, AppointmentUpdate


router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.create_appointment(
        data=data,
        current_user=current_user,
    )


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: UUID,
    data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.update_appointment(
        appointment_id=appointment_id,
        data=data,
        current_user=current_user,
    )


@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
def cancel_appointment(
    appointment_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.cancel_appointment(
        appointment_id=appointment_id,
        current_user=current_user,
    )
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.dependencies.fastapi import get_current_user, require_permission
from app.core.db.session_scope import get_db
from app.modules.users.models.user import User
from app.modules.idempotency.services.idempotency_service import IdempotencyService
from app.modules.schedule.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from app.modules.schedule.services.appointment_service import AppointmentService


router = APIRouter(prefix="/appointments", tags=["appointments"])
legacy_router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post("", response_model=AppointmentResponse, status_code=201)
@legacy_router.post("", response_model=AppointmentResponse, status_code=201)
async def create_appointment(
    request: Request,
    dados: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("agenda.criar")),
):
    idempotency_service = IdempotencyService(db)
    resposta_armazenada = await idempotency_service.verificar_idempotencia(
        request=request,
        company_id=current_user.company_id,
    )
    if resposta_armazenada is not None:
        return resposta_armazenada

    service = AppointmentService(db)
    appointment = service.create_appointment(
        dados=dados,
        current_user=current_user,
    )

    resposta_serializada = AppointmentResponse.model_validate(appointment).model_dump(mode="json")
    await idempotency_service.registrar_resposta(
        request=request,
        company_id=current_user.company_id,
        response_body=resposta_serializada,
        status_code=status.HTTP_201_CREATED,
    )

    return resposta_serializada


@router.put("/{appointment_id}", response_model=AppointmentResponse)
@legacy_router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: UUID,
    dados: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = AppointmentService(db)
    return service.update_appointment(
        appointment_id=appointment_id,
        dados=dados,
        current_user=current_user,
    )


@router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
@legacy_router.patch("/{appointment_id}/cancel", response_model=AppointmentResponse)
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

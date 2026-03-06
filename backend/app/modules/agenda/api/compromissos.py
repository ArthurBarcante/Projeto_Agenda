from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.api.dependencias import obter_usuario_atual, require_permission
from app.db.sessao import obter_db
from app.models.user import User
from app.modules.idempotency.services.idempotency_service import IdempotencyService
from app.modules.agenda.schemas.compromisso import CompromissoAtualizacao
from app.modules.agenda.schemas.compromisso import CompromissoCriacao, CompromissoResposta
from app.modules.agenda.services.compromisso_service import CompromissoService


router = APIRouter(prefix="/appointments", tags=["appointments"])
legacy_router = APIRouter(prefix="/compromissos", tags=["compromissos"])


@router.post("", response_model=CompromissoResposta, status_code=201)
@legacy_router.post("", response_model=CompromissoResposta, status_code=201)
async def criar_compromisso(
    request: Request,
    dados: CompromissoCriacao,
    db: Session = Depends(obter_db),
    usuario_atual: User = Depends(require_permission("agenda.criar")),
):
    idempotency_service = IdempotencyService(db)
    resposta_armazenada = await idempotency_service.verificar_idempotencia(
        request=request,
        empresa_id=usuario_atual.company_id,
    )
    if resposta_armazenada is not None:
        return resposta_armazenada

    servico = CompromissoService(db)
    compromisso = servico.criar_compromisso(
        dados=dados,
        usuario_atual=usuario_atual,
    )

    resposta_serializada = CompromissoResposta.model_validate(compromisso).model_dump(mode="json")
    await idempotency_service.registrar_resposta(
        request=request,
        empresa_id=usuario_atual.company_id,
        response_body=resposta_serializada,
        status_code=status.HTTP_201_CREATED,
    )

    return resposta_serializada


@router.put("/{compromisso_id}", response_model=CompromissoResposta)
@legacy_router.put("/{compromisso_id}", response_model=CompromissoResposta)
def atualizar_compromisso(
    compromisso_id: UUID,
    dados: CompromissoAtualizacao,
    db: Session = Depends(obter_db),
    usuario_atual: User = Depends(obter_usuario_atual),
):
    servico = CompromissoService(db)
    return servico.atualizar_compromisso(
        compromisso_id=compromisso_id,
        dados=dados,
        usuario_atual=usuario_atual,
    )


@router.patch("/{compromisso_id}/cancel", response_model=CompromissoResposta)
@legacy_router.patch("/{compromisso_id}/cancelar", response_model=CompromissoResposta)
def cancelar_compromisso(
    compromisso_id: UUID,
    db: Session = Depends(obter_db),
    usuario_atual: User = Depends(obter_usuario_atual),
):
    servico = CompromissoService(db)
    return servico.cancelar_compromisso(
        compromisso_id=compromisso_id,
        usuario_atual=usuario_atual,
    )

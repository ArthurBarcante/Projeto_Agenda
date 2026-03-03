from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencias import obter_usuario_atual
from app.db.sessao import obter_db
from app.models.usuario import Usuario
from app.modules.compromissos.services.compromisso_service import CompromissoService
from app.schemas.compromisso import CompromissoAtualizacao
from app.schemas.compromisso import CompromissoCriacao, CompromissoResposta


router = APIRouter(prefix="/compromissos", tags=["compromissos"])


@router.post("", response_model=CompromissoResposta, status_code=201)
def criar_compromisso(
    dados: CompromissoCriacao,
    db: Session = Depends(obter_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    servico = CompromissoService(db)
    return servico.criar_compromisso(
        dados=dados,
        usuario_atual=usuario_atual,
    )


@router.put("/{compromisso_id}", response_model=CompromissoResposta)
def atualizar_compromisso(
    compromisso_id: UUID,
    dados: CompromissoAtualizacao,
    db: Session = Depends(obter_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    servico = CompromissoService(db)
    return servico.atualizar_compromisso(
        compromisso_id=compromisso_id,
        dados=dados,
        usuario_atual=usuario_atual,
    )


@router.patch("/{compromisso_id}/cancelar", response_model=CompromissoResposta)
def cancelar_compromisso(
    compromisso_id: UUID,
    db: Session = Depends(obter_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual),
):
    servico = CompromissoService(db)
    return servico.cancelar_compromisso(
        compromisso_id=compromisso_id,
        usuario_atual=usuario_atual,
    )
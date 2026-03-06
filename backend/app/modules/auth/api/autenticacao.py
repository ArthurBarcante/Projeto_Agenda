from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.autenticacao.seguranca import verificar_senha
from app.core.autenticacao.token_jwt import criar_token_acesso
from app.core.inquilino import definir_empresa_atual_id
from app.db.sessao import obter_db
from app.models.company import Company
from app.models.user import User


router = APIRouter(prefix="/auth", tags=["auth"])
legacy_router = APIRouter(prefix="/autenticacao", tags=["autenticacao"])


class RequisicaoLogin(BaseModel):
    identificador_empresa: str
    email: EmailStr
    senha: str


class RespostaToken(BaseModel):
    token_acesso: str
    tipo_token: str = "bearer"


@router.post("/login", response_model=RespostaToken)
@legacy_router.post("/entrar", response_model=RespostaToken)
def entrar(dados: RequisicaoLogin, db: Session = Depends(obter_db)):
    empresa = db.query(Company).filter(Company.slug == dados.identificador_empresa).first()

    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    definir_empresa_atual_id(empresa.id)

    usuario = db.query(User).filter(
        User.email == dados.email,
        User.company_id == empresa.id,
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    if not verificar_senha(dados.senha, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    token_acesso = criar_token_acesso(
        {
            "sub": str(usuario.id),
            "company_id": str(empresa.id),
            "company_slug": empresa.slug,
        }
    )

    return RespostaToken(token_acesso=token_acesso)

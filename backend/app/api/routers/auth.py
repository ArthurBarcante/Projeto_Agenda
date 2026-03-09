from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security.security import verificar_senha
from app.core.security.token_jwt import criar_token_acesso
from app.core.tenant_scope import set_current_company_id
from app.core.db.session_scope import get_db
from app.modules.users.models.company import Company
from app.modules.users.models.user import User


router = APIRouter(prefix="/auth", tags=["auth"])
legacy_router = APIRouter(prefix="/authentication", tags=["authentication"])


class LoginRequest(BaseModel):
    company_identifier: str
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    token_acesso: str
    tipo_token: str = "bearer"


@router.post("/login", response_model=TokenResponse)
@legacy_router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    company = db.query(Company).filter(Company.slug == dados.company_identifier).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials invalids",
        )

    set_current_company_id(company.id)

    user = db.query(User).filter(
        User.email == dados.email,
        User.company_id == company.id,
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials invalids",
        )

    if not verificar_senha(dados.senha, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials invalids",
        )

    token_acesso = criar_token_acesso(
        {
            "sub": str(user.id),
            "company_id": str(company.id),
            "company_slug": company.slug,
        }
    )

    return TokenResponse(token_acesso=token_acesso)

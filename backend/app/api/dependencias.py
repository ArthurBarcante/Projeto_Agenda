from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.autenticacao.token_jwt import decodificar_token
from app.core.errors.api_error import APIError
from app.core.errors.error_codes import ErrorCode
from app.core.inquilino import definir_empresa_atual_id
from app.db.sessao import obter_db
from app.models.user import User
from app.models.company import Company
from app.modules.permissoes.services.permission_service import PermissionService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(obter_db)
) -> User:

    try:
        payload = decodificar_token(token)
        user_id: str = payload.get("sub")
        company_id: str = payload.get("company_id")

        if user_id is None or company_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    definir_empresa_atual_id(company_id)

    usuario = db.query(User).filter(
        User.id == user_id,
        User.company_id == company_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    return usuario


def obter_empresa_atual(
    usuario_atual: User = Depends(obter_usuario_atual),
    db: Session = Depends(obter_db)
) -> Company:

    empresa = db.query(Company).filter(
        Company.id == usuario_atual.company_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empresa não encontrada"
        )

    return empresa


def require_permission(codigo_permissao: str):
    def guard(
        usuario_atual: User = Depends(obter_usuario_atual),
        db: Session = Depends(obter_db),
    ) -> User:
        permissao_service = PermissionService(db)
        if not permissao_service.usuario_tem_permissao(
            usuario_id=usuario_atual.id,
            codigo_permissao=codigo_permissao,
        ):
            raise APIError(
                codigo=ErrorCode.USUARIO_NAO_AUTORIZADO,
                mensagem="Usuário não possui permissão para esta ação",
                status_code=status.HTTP_403_FORBIDDEN,
            )
        return usuario_atual

    return guard
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError

from app.core.autenticacao.token_jwt import decodificar_token
from app.core.inquilino import definir_empresa_atual_id
from app.db.sessao import obter_db
from app.models.usuario import Usuario
from app.models.empresa import Empresa

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/autenticacao/entrar")


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(obter_db)
) -> Usuario:

    try:
        payload = decodificar_token(token)
        usuario_id: str = payload.get("sub")
        empresa_id: str = payload.get("company_id")

        if usuario_id is None or empresa_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    definir_empresa_atual_id(empresa_id)

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id,
        Usuario.company_id == empresa_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    return usuario


def obter_empresa_atual(
    usuario_atual: Usuario = Depends(obter_usuario_atual),
    db: Session = Depends(obter_db)
) -> Empresa:

    empresa = db.query(Empresa).filter(
        Empresa.id == usuario_atual.company_id
    ).first()

    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empresa não encontrada"
        )

    return empresa
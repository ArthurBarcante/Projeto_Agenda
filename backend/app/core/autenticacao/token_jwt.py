from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings


def criar_token_acesso(dados: dict) -> str:
    para_codificar = dados.copy()

    expira_em = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    para_codificar.update({"exp": expira_em})

    return jwt.encode(
        para_codificar,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decodificar_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

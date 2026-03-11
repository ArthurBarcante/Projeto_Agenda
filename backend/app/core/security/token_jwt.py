from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jose import JWTError, jwt
from app.core.config import settings


JWT_ISSUER = "agenda-api"
JWT_AUDIENCE = "agenda-client"


def criar_token_acesso(dados: dict) -> str:
    para_codificar = dados.copy()

    agora = datetime.now(timezone.utc)

    expira_em = agora + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    para_codificar.update(
        {
            # Standard claim that identifies who issued the token.
            "iss": JWT_ISSUER,
            # Standard claim that identifies the intended token consumer.
            "aud": JWT_AUDIENCE,
            # Standard claim with token issuance timestamp.
            "iat": agora,
            # Standard unique identifier for replay tracking/revocation lists.
            "jti": str(uuid4()),
            # Standard expiration timestamp for token validity.
            "exp": expira_em,
        }
    )

    return jwt.encode(
        para_codificar,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            issuer=JWT_ISSUER,
            audience=JWT_AUDIENCE,
            options={
                "require_exp": True,
                "require_iss": True,
                "require_aud": True,
                "require_iat": True,
                "require_jti": True,
            },
        )
    except JWTError:
        # Keep jose validation errors explicit for callers that map auth failures.
        raise

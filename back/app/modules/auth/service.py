from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.logging_config import get_logger
from app.core.security import create_access_token, verify_password
from app.modules.auth.schema import UserLogin
from app.modules.users.model import User

_logger = get_logger(__name__)


def authenticate_user(db: Session, payload: UserLogin) -> dict:
    db_user = db.query(User).filter(User.email == payload.email).first()

    if not db_user or not verify_password(payload.password, str(db_user.password)):
        _logger.warning("login_failed email=%s", payload.email)
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    _logger.info("login_success user_id=%d", db_user.id)
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

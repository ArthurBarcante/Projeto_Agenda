from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.modules.auth.schema import UserLogin
from app.modules.users.model import User


def authenticate_user(db: Session, payload: UserLogin) -> dict:
    db_user = db.query(User).filter(User.email == payload.email).first()

    if not db_user or not verify_password(payload.password, str(db_user.password)):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


def build_me_payload(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
    }

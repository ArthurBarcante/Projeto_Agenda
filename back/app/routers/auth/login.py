from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.deps import get_db
from app.models.user import User
from app.schemas.auth.login import UserLogin
from app.core.security import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):

    # Busca usuário pelo email
    db_user = db.query(User).filter(User.email == data.email).first()

    # Mensagem genérica: não revela se é email ou senha inválidos
    if not db_user or not verify_password(data.password, str(db_user.password)):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    access_token = create_access_token(data={"sub": str(db_user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
    }

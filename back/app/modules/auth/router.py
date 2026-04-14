from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database.deps import get_db
from app.modules.auth.schema import LoginResponse, UserLogin
from app.modules.auth.service import authenticate_user, build_me_payload
from app.modules.users.model import User
from app.modules.users.schema import UserCreate
from app.modules.users.service import build_register_response, register_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    return authenticate_user(db, data)


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    created_user = register_user(db, user)
    return build_register_response(created_user)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return build_me_payload(current_user)

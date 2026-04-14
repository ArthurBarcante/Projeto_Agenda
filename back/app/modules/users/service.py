from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.users.model import User
from app.modules.users.schema import UserCreate, UserUpdate


def register_user(db: Session, payload: UserCreate) -> User:
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    if db.query(User).filter(User.cpf == payload.cpf).first():
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    new_user = User(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password),
        phone=payload.phone,
        cpf=payload.cpf,
        birthdate=payload.birthdate,
        role=payload.role,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def build_register_response(user: User) -> dict:
    return {
        "message": "Usuário criado com sucesso",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }


def update_user_profile(db: Session, current_user: User, payload: UserUpdate) -> User:
    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        return current_user

    if "email" in update_data and update_data["email"] != current_user.email:
        existing_user = db.query(User).filter(User.email == update_data["email"]).first()
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

from fastapi import APIRouter, HTTPException
from app.schemas.auth.register import RegisterRequest
from app.models.fake_db import users_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: RegisterRequest):

    # 🔥 Verificar email duplicado
    for user in users_db:
        if user["email"] == data.email:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        if user["cpf"] == data.cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    # 🔥 Criar novo usuário
    new_user = {
        "id": len(users_db) + 1,
        "name": data.name,
        "email": data.email,
        "password": data.password,
        "birth_date": str(data.birth_date),
        "cpf": data.cpf,
        "phone": data.phone
    }

    users_db.append(new_user)

    return {
        "message": "Usuário criado com sucesso",
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"]
        }
    }

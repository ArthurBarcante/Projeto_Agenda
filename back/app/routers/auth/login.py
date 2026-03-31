from fastapi import APIRouter, HTTPException
from app.schemas.auth.login import LoginRequest
from app.models.fake_db import users_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(data: LoginRequest):
	for user in users_db:
		if user["email"] == data.email and user["password"] == data.password:
			return {
				"message": "Login realizado com sucesso",
				"user": {
					"id": user["id"],
					"name": user["name"],
					"email": user["email"]
				}
			}

	raise HTTPException(status_code=401, detail="Email ou senha inválidos")

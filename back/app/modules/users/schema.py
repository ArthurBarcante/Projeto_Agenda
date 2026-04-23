from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    phone: str
    cpf: str
    birthdate: date
    role: str

    @field_validator("confirm_password")
    def passwords_match(cls, value, info):
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("As senhas não coincidem")
        return value


class UserPublicResponse(BaseModel):
    """Dados não-sensíveis — seguro para qualquer contexto."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: str


class UserPrivateResponse(UserPublicResponse):
    """Dados completos — usar apenas em endpoints do próprio usuário autenticado."""

    phone: str
    cpf: str
    birthdate: date


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birthdate: date | None = None


class UserRegisterResponse(BaseModel):
    message: str
    user: dict
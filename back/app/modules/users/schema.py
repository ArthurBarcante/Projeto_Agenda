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


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    phone: str
    cpf: str
    birthdate: date
    role: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birthdate: date | None = None


class UserRegisterResponse(BaseModel):
    message: str
    user: dict
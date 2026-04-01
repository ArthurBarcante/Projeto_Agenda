from pydantic import BaseModel, EmailStr, field_validator
from datetime import date


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

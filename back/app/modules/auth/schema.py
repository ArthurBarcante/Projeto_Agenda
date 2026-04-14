from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Compatibility alias for previous imports.
LoginRequest = UserLogin


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

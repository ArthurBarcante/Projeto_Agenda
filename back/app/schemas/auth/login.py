from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Compatibility alias for previous imports.
LoginRequest = UserLogin

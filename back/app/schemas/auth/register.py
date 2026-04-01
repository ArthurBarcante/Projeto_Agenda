from datetime import date

from pydantic import BaseModel, EmailStr, field_validator


class RegisterRequest(BaseModel):
	name: str
	email: EmailStr
	password: str
	confirm_password: str
	phone: str
	cpf: str
	birthdate: date
	role: str

	def to_user_data(self):
		data = self.model_dump()
		data.pop("confirm_password", None)
		return data

	@field_validator("confirm_password")
	def passwords_match(cls, value, info):
		if "password" in info.data and value != info.data["password"]:
			raise ValueError("As senhas não coincidem")
		return value

from pydantic import BaseModel
from pydantic import EmailStr, field_validator
from datetime import date


class RegisterRequest(BaseModel):
	name: str
	email: EmailStr
	password: str
	confirm_password: str
	birth_date: date
	cpf: str
	phone: str

	def to_user_data(self):
		data = self.model_dump()
		data.pop("confirm_password", None)
		return data

	@field_validator("confirm_password")
	def passwords_match(cls, value, info):
		if "password" in info.data and value != info.data["password"]:
			raise ValueError("As senhas não coincidem")
		return value

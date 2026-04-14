from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class EventBase(BaseModel):
	title: str
	description: str | None = None
	start_at: datetime
	end_at: datetime | None = None
	location: str | None = None

	@model_validator(mode="after")
	def validate_dates(self):
		if self.end_at is not None and self.end_at < self.start_at:
			raise ValueError("end_at nao pode ser menor que start_at")
		return self


class EventCreate(EventBase):
	pass


class EventUpdate(BaseModel):
	title: str | None = None
	description: str | None = None
	start_at: datetime | None = None
	end_at: datetime | None = None
	location: str | None = None

	@model_validator(mode="after")
	def validate_dates(self):
		if (
			self.start_at is not None
			and self.end_at is not None
			and self.end_at < self.start_at
		):
			raise ValueError("end_at nao pode ser menor que start_at")
		return self


class EventResponse(EventBase):
	model_config = ConfigDict(from_attributes=True)

	id: int
	user_id: int

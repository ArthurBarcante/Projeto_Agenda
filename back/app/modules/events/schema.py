from datetime import datetime

from pydantic import BaseModel, ConfigDict, model_validator


def _check_date_order(start_at, end_at) -> None:
	"""Lança ValueError se end_at for anterior a start_at."""
	if start_at is not None and end_at is not None and end_at < start_at:
		raise ValueError("end_at nao pode ser menor que start_at")


class EventBase(BaseModel):
	title: str
	description: str | None = None
	start_at: datetime
	end_at: datetime | None = None
	location: str | None = None

	@model_validator(mode="after")
	def validate_dates(self):
		_check_date_order(self.start_at, self.end_at)
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
		_check_date_order(self.start_at, self.end_at)
		return self


class EventResponse(EventBase):
	model_config = ConfigDict(from_attributes=True)

	id: int
	user_id: int

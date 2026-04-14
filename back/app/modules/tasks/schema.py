from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
	title: str
	description: str | None = None
	completed: bool = False
	due_date: datetime | None = None


class TaskCreate(TaskBase):
	pass


class TaskUpdate(BaseModel):
	title: str | None = None
	description: str | None = None
	completed: bool | None = None
	due_date: datetime | None = None


class TaskResponse(TaskBase):
	model_config = ConfigDict(from_attributes=True)

	id: int
	user_id: int
	completed_at: datetime | None = None

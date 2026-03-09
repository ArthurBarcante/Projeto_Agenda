from datetime import datetime
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.modules.schedule.models.appointment import AppointmentStatus


class AppointmentUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default=None, validation_alias=AliasChoices("title", "title"))
    description: str | None = Field(default=None, validation_alias=AliasChoices("description", "description"))
    start_time: datetime | None = Field(default=None, validation_alias=AliasChoices("start_time", "start_time", "start_time"))
    end_time: datetime | None = Field(default=None, validation_alias=AliasChoices("end_time", "end_time", "end_time"))
    status: AppointmentStatus | None = None


class AppointmentCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(validation_alias=AliasChoices("title", "title"))
    description: str | None = Field(default=None, validation_alias=AliasChoices("description", "description"))
    start_time: datetime = Field(validation_alias=AliasChoices("start_time", "start_time", "start_time"))
    end_time: datetime = Field(validation_alias=AliasChoices("end_time", "end_time", "end_time"))
    participant_ids: list[UUID] = Field(
        default_factory=list,
        validation_alias=AliasChoices("participant_ids", "participantes_ids"),
    )


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    company_id: UUID = Field(validation_alias=AliasChoices("company_id", "company_id"))
    creator_id: UUID = Field(validation_alias=AliasChoices("creator_id", "creator_id"))
    title: str = Field(validation_alias=AliasChoices("title", "title"))
    description: str | None = Field(default=None, validation_alias=AliasChoices("description", "description"))
    start_time: datetime = Field(validation_alias=AliasChoices("start_time", "start_time", "start_time"))
    end_time: datetime = Field(validation_alias=AliasChoices("end_time", "end_time", "end_time"))
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime


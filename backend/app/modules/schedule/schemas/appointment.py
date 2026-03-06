from datetime import datetime
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.models.appointment import AppointmentStatus


class AppointmentUpdate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = Field(default=None, validation_alias=AliasChoices("title", "titulo"))
    description: str | None = Field(default=None, validation_alias=AliasChoices("description", "descricao"))
    start_time: datetime | None = Field(default=None, validation_alias=AliasChoices("start_time", "starts_at", "inicio_em"))
    end_time: datetime | None = Field(default=None, validation_alias=AliasChoices("end_time", "ends_at", "fim_em"))
    status: AppointmentStatus | None = None


class AppointmentCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(validation_alias=AliasChoices("title", "titulo"))
    description: str | None = Field(default=None, validation_alias=AliasChoices("description", "descricao"))
    start_time: datetime = Field(validation_alias=AliasChoices("start_time", "starts_at", "inicio_em"))
    end_time: datetime = Field(validation_alias=AliasChoices("end_time", "ends_at", "fim_em"))
    participant_ids: list[UUID] = Field(
        default_factory=list,
        validation_alias=AliasChoices("participant_ids", "participantes_ids"),
    )


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    company_id: UUID = Field(validation_alias=AliasChoices("company_id", "empresa_id"))
    creator_id: UUID = Field(validation_alias=AliasChoices("creator_id", "criador_id"))
    title: str = Field(validation_alias=AliasChoices("title", "titulo"))
    description: str | None = Field(default=None, validation_alias=AliasChoices("description", "descricao"))
    start_time: datetime = Field(validation_alias=AliasChoices("start_time", "starts_at", "inicio_em"))
    end_time: datetime = Field(validation_alias=AliasChoices("end_time", "ends_at", "fim_em"))
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime


class LegacyAppointmentUpdate(AppointmentUpdate):
    pass


class LegacyAppointmentCreate(AppointmentCreate):
    pass


class LegacyAppointmentResponse(AppointmentResponse):
    pass

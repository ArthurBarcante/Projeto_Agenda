from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.appointment import AppointmentStatus


class AppointmentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    status: AppointmentStatus | None = None


class AppointmentCreate(BaseModel):
    title: str
    description: str | None = None
    starts_at: datetime
    ends_at: datetime
    participant_ids: list[UUID] = Field(default_factory=list)


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company_id: UUID
    creator_id: UUID
    title: str
    description: str | None
    starts_at: datetime
    ends_at: datetime
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime
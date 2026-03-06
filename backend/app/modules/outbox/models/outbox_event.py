import enum
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Index, Integer, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.tenant_model import TenantModel


class StatusOutboxEvento(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"


class OutboxEvent(TenantModel):
    __tablename__ = "outbox_events"
    __table_args__ = (
        Index("ix_outbox_events_company_id", "company_id"),
        Index("ix_outbox_events_status", "status"),
        Index("ix_outbox_events_process_at", "process_at"),
    )

    updated_at = None

    event_type: Mapped[str] = mapped_column(Text, nullable=False)

    payload: Mapped[dict[str, Any]] = mapped_column(
        "payload",
        JSONB,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        "status",
        Text,
        default=StatusOutboxEvento.PENDING.value,
        nullable=False,
    )

    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    process_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def tipo_evento(self):
        return self.event_type

    @tipo_evento.setter
    def tipo_evento(self, value: str) -> None:
        self.event_type = value

    @property
    def tentativas(self):
        return self.attempts

    @tentativas.setter
    def tentativas(self, value: int) -> None:
        self.attempts = value

    @property
    def processar_em(self):
        return self.process_at

    @processar_em.setter
    def processar_em(self, value: datetime) -> None:
        self.process_at = value

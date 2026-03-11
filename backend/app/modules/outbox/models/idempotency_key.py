from datetime import datetime
from enum import Enum
from typing import Any

from sqlalchemy import DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db.models.tenant_model import TenantModel


class IdempotencyState(str, Enum):
    """Estado do registro de idempotência durante o processamento da requisição."""
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class IdempotencyKey(TenantModel):
    __tablename__ = "idempotency_keys"
    __table_args__ = (
        UniqueConstraint("company_id", "key", name="uq_idempotency_keys_company_key"),
    )

    key: Mapped[str] = mapped_column(String(255), nullable=False)

    endpoint: Mapped[str] = mapped_column(
        "endpoint",
        String(255),
        nullable=False,
    )

    method: Mapped[str] = mapped_column(String(16), nullable=False)

    request_hash: Mapped[str] = mapped_column(
        "request_hash",
        String(128),
        nullable=False,
    )

    response_body: Mapped[dict[str, Any] | None] = mapped_column(
        "response_body",
        JSONB,
        nullable=True,
    )

    status_code: Mapped[int | None] = mapped_column(
        "status_code",
        Integer,
        nullable=True,
    )

    state: Mapped[IdempotencyState] = mapped_column(
        ENUM(IdempotencyState, name="idempotency_state"),
        nullable=False,
        default=IdempotencyState.IN_PROGRESS,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
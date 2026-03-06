from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.tenant_model import TenantModel


class IdempotencyKey(TenantModel):
    __tablename__ = "idempotency_keys"
    __table_args__ = (
        UniqueConstraint("company_id", "key", name="uq_idempotency_keys_company_key"),
    )

    updated_at = None

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

    response_body: Mapped[dict[str, Any]] = mapped_column(
        "response_body",
        JSONB,
        nullable=False,
    )

    status_code: Mapped[int] = mapped_column(
        "status_code",
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
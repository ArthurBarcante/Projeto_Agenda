from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, Index, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.tenant_model import TenantModel


class AuditLog(TenantModel):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("ix_audit_logs_company_entity_created", "company_id", "entity", "created_at"),
    )

    updated_at = None

    user_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    action: Mapped[str] = mapped_column(String(120), nullable=False)

    entity: Mapped[str] = mapped_column(String(120), nullable=False)

    entity_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False)

    before_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    after_data: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
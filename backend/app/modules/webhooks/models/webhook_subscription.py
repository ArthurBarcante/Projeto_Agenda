from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config.uuid7 import generate_uuid7
from app.models.base import Base


class WebhookSubscription(Base):
    __tablename__ = "webhook_subscriptions"
    __table_args__ = (
        Index(
            "ix_webhook_subscriptions_company_event_active",
            "company_id",
            "event_type",
            "is_active",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )

    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )

    url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    secret: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def empresa_id(self):
        return self.company_id

    @empresa_id.setter
    def empresa_id(self, value: UUID) -> None:
        self.company_id = value

    @property
    def ativo(self):
        return self.is_active

    @ativo.setter
    def ativo(self, value: bool) -> None:
        self.is_active = value

    @property
    def criado_em(self):
        return self.created_at

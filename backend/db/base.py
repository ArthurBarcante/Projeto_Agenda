from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, synonym

from app.config import generate_uuid7


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )


class TenantModel(BaseModel):
    __abstract__ = True

    @declared_attr.directive
    def tenant_id(cls) -> Mapped[UUID]:
        return mapped_column(
            "company_id",
            UUID(as_uuid=True),
            ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )

    @declared_attr.directive
    def company_id(cls):
        return synonym("tenant_id")


__all__ = ["Base", "BaseModel", "TenantModel"]
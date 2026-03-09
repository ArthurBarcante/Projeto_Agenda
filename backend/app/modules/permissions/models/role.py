from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship, synonym

from app.core.config.uuid7 import generate_uuid7
from app.core.db.models.base import Base

if TYPE_CHECKING:
    from app.modules.permissions.models.role_permission import RolePermission
    from app.modules.permissions.models.user_role import UserRole


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = (
        Index("ix_roles_company_id", "company_id"),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )

    tenant_id: Mapped[UUID] = mapped_column(
        "company_id",
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )

    company_id = synonym("tenant_id")

    name: Mapped[str] = mapped_column(String(120), nullable=False)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    permissions: Mapped[list["RolePermission"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    users: Mapped[list["UserRole"]] = relationship(
        back_populates="role",
        cascade="all, delete-orphan",
    )

    @property
    def nome(self):
        return self.name

    @nome.setter
    def nome(self, value: str) -> None:
        self.name = value

    @property
    def description(self):
        return self.description

    @description.setter
    def description(self, value: str | None) -> None:
        self.description = value

    @property
    def created_at(self):
        return self.created_at

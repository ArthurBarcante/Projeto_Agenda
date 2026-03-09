from typing import TYPE_CHECKING

from sqlalchemy import Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config.uuid7 import generate_uuid7
from app.core.db.models.base import Base

if TYPE_CHECKING:
    from app.modules.permissions.models.role_permission import RolePermission


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = (
        Index("ix_permissions_code", "code"),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid7,
    )

    code: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    roles: Mapped[list["RolePermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete-orphan",
    )

    @property
    def codigo(self):
        return self.code

    @codigo.setter
    def codigo(self, value: str) -> None:
        self.code = value

    @property
    def description(self):
        return self.description

    @description.setter
    def description(self, value: str | None) -> None:
        self.description = value

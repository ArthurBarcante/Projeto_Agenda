"""User model."""

from uuid import UUID
from sqlalchemy import Boolean, String, UUID as SQLAUUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import TenantModel


class User(TenantModel):
    """User model."""

    __tablename__ = "users"

    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    hash_senha: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)


__all__ = ["User"]
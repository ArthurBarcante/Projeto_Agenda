from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.tenant_model import TenantModel


if TYPE_CHECKING:
	from app.models.company import Company


class User(TenantModel):
	__tablename__ = "users"

	__table_args__ = (
		UniqueConstraint("company_id", "email", name="uq_user_company_email"),
	)

	name: Mapped[str] = mapped_column(String(120), nullable=False)
	email: Mapped[str] = mapped_column(String(255), nullable=False)
	password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

	company: Mapped["Company"] = relationship(back_populates="users")

	@property
	def empresa(self):
		return self.company

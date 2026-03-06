from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, synonym

from app.models.base_model import BaseModel


class TenantModel(BaseModel):
    __abstract__ = True
    __tenant_scoped__ = True

    company_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
    )

    @declared_attr
    def tenant_id(cls):
        return synonym("company_id")

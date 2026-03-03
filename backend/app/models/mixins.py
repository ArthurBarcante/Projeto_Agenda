from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class InquilinoMixin:
    __tenant_scoped__ = True

    company_id: Mapped[UUID] = mapped_column(
        "empresa_id",
        UUID(as_uuid=True),
        ForeignKey("empresas.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
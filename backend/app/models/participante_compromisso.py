from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import Base
from app.models.mixins import InquilinoMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.compromisso import Compromisso


class ParticipanteCompromisso(InquilinoMixin, Base):
    __tablename__ = "participantes_compromissos"

    __table_args__ = (
        UniqueConstraint(
            "compromisso_id",
            "usuario_id",
            name="uq_participante_compromisso_usuario"
        ),
        Index(
            "ix_participantes_compromissos_usuario_compromisso",
            "usuario_id",
            "compromisso_id",
        ),
    )

    appointment_id: Mapped[str] = mapped_column(
        "compromisso_id",
        UUID(as_uuid=True),
        ForeignKey("compromissos.id", ondelete="CASCADE"),
        primary_key=True
    )

    user_id: Mapped[str] = mapped_column(
        "usuario_id",
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        primary_key=True
    )

    # Relationships
    compromisso: Mapped["Compromisso"] = relationship(
        back_populates="participantes"
    )

    usuario: Mapped["Usuario"] = relationship()
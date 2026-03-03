import datetime
import enum
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config.uuid7 import gerar_uuid7
from app.models.base import Base
from app.models.mixins import InquilinoMixin


if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.participante_compromisso import ParticipanteCompromisso


class StatusCompromisso(str, enum.Enum):
    agendado = "scheduled"
    cancelado = "cancelled"
    concluido = "completed"


class Compromisso(InquilinoMixin, Base):
    __tablename__ = "compromissos"
    __table_args__ = (
        Index(
            "ix_compromissos_empresa_inicio_fim_status",
            "empresa_id",
            "inicio_em",
            "fim_em",
            "estado",
        ),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=gerar_uuid7,
    )

    creator_id: Mapped[str] = mapped_column(
        "criador_id",
        UUID(as_uuid=True),
        ForeignKey("usuarios.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        "titulo",
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        "descricao",
        Text,
        nullable=True,
    )

    starts_at: Mapped[datetime.datetime] = mapped_column(
        "inicio_em",
        DateTime(timezone=True),
        nullable=False,
    )

    ends_at: Mapped[datetime.datetime] = mapped_column(
        "fim_em",
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[StatusCompromisso] = mapped_column(
        "estado",
        Enum(StatusCompromisso, name="appointment_status"),
        default=StatusCompromisso.agendado,
        nullable=False,
    )

    created_at: Mapped[datetime.datetime]
    updated_at: Mapped[datetime.datetime]

    # Relationships
    criador: Mapped["Usuario"] = relationship(
        foreign_keys=[creator_id]
    )

    participantes: Mapped[list["ParticipanteCompromisso"]] = relationship(
        back_populates="compromisso",
        cascade="all, delete-orphan",
    )

    def pode_ser_atualizado(self) -> bool:
        return self.status == StatusCompromisso.agendado

    def pode_ser_cancelado(self) -> bool:
        return self.status == StatusCompromisso.agendado

    def esta_vencido(self) -> bool:
        fim_em = self.ends_at
        if fim_em.tzinfo is None:
            return fim_em < datetime.datetime.utcnow()
        return fim_em < datetime.datetime.now(datetime.timezone.utc)

    def cancelar(self, usuario: "Usuario") -> None:
        if self.creator_id != usuario.id:
            raise PermissionError("Apenas o criador pode cancelar")

        if not self.pode_ser_cancelado():
            raise ValueError("Compromisso não pode ser cancelado")

        self.status = StatusCompromisso.cancelado


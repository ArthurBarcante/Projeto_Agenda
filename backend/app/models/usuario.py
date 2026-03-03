from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base
from app.core.config.uuid7 import gerar_uuid7
from typing import TYPE_CHECKING
import datetime

if TYPE_CHECKING:
  from app.models.empresa import Empresa
    

class Usuario(Base):
  __tablename__ = "usuarios"
  __tenant_scoped__ = True
  
  __table_args__ = (
    UniqueConstraint("empresa_id", "email", name="uq_usuario_empresa_email"),
  )
  
  id: Mapped[UUID] = mapped_column(
    UUID(as_uuid=True), 
    primary_key=True, 
    default=gerar_uuid7
    )
  
  company_id: Mapped[UUID] = mapped_column(
    "empresa_id",
    UUID(as_uuid=True), 
    ForeignKey("empresas.id", ondelete="CASCADE"),
    nullable=False
    )
  
  name: Mapped[str] = mapped_column(
    "nome",
    String(120), 
    nullable=False
    )  
  
  email: Mapped[str] = mapped_column(
    String(255),
    nullable=False
    )
  
  password_hash: Mapped[str] = mapped_column(
    "hash_senha",
    String(255),
    nullable=False
    )
  
  is_active: Mapped[bool] = mapped_column(
    "ativo",
    Boolean,
    default=True,
    nullable=False
    )
  
  created_at: Mapped[datetime.datetime]
  updated_at: Mapped[datetime.datetime]
  
  # Relationships ORM
  empresa: Mapped["Empresa"] = relationship(
    back_populates="users"
    )
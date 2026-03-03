from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum
import enum
from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
  from app.models.usuario import Usuario

class PlanoEmpresa(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    
class Empresa(BaseModel):
  __tablename__ = "empresas"
  
  name: Mapped[str] = mapped_column(
    "nome",
    String(150), 
    nullable=False
    )
  
  slug: Mapped[str] = mapped_column(
    "identificador",
    String(150),
    unique = True,
    nullable=False
    )
  
  plan: Mapped[PlanoEmpresa] = mapped_column(
    "plano",
    Enum(PlanoEmpresa, name = "company_plan_enum"),
    nullable=False
    )
  
  is_active: Mapped[bool] = mapped_column(
    "ativo",
    Boolean,
    default=True,
    nullable=False
    )
  
  # Relationships ORM
  users: Mapped[List["Usuario"]] = relationship(
    back_populates="empresa",
    cascade="all, delete-orphan"
    )
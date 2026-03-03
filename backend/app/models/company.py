from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum
import enum
from app.models.base import BaseModel
from sqlalchemy.orm import relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User

class CompanyPlan(str, enum.Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    
class Company(BaseModel):
  __tablename__ = "companies"
  
  name: Mapped[str] = mapped_column(
    String(150), 
    nullable=False
    )
  
  slug: Mapped[str] = mapped_column(
    String(150),
    unique = True,
    nullable=False
    )
  
  plan: Mapped[CompanyPlan] = mapped_column(
    Enum(CompanyPlan, name = "company_plan_enum"),
    nullable=False
    )
  
  is_active: Mapped[bool] = mapped_column(
    Boolean,
    default=True,
    nullable=False
    )
  
  # Relationships ORM
  users: Mapped[List["User"]] = relationship(
    back_populates="company",
    cascade="all, delete-orphan"
    )
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime
from typing import Optional
from app.core.config.uuid7 import generate_uuid7
from sqlalchemy.dialects.postgresql import UUID

class Base(DeclarativeBase):
  pass

class BaseModel(Base):
  __abstract__ = True
  
  id: Mapped[UUID] = mapped_column(
    UUID(as_uuid=True), 
    primary_key=True, 
    default=generate_uuid7
    )
  
  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), 
    default=lambda: datetime.now(timezone.utc),
    nullable=False
    )
  
  updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc),
    nullable=False
    )
  
  deleted_at: Mapped[Optional[datetime]] = mapped_column(
    DateTime(timezone=True),
    nullable=True
    )
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.base import Base


class Task(Base):
	__tablename__ = "tasks"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, nullable=False)
	description = Column(Text, nullable=True)
	completed = Column(Boolean, nullable=False, default=False)
	due_date = Column(DateTime, nullable=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

	user = relationship("User", back_populates="tasks")

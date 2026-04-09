from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.base import Base


class Event(Base):
	__tablename__ = "events"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, nullable=False)
	description = Column(Text, nullable=True)
	start_at = Column(DateTime, nullable=False)
	end_at = Column(DateTime, nullable=True)
	location = Column(String, nullable=True)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

	user = relationship("User", back_populates="events")

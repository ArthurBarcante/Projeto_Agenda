from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.utils import get_utc_now
from app.database.base import Base


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    badge_id = Column(Integer, ForeignKey("badges.id", ondelete="CASCADE"), nullable=False, index=True)
    earned_at = Column(DateTime, nullable=False, default=get_utc_now)

    __table_args__ = (UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),)

    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database.base import Base


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    completed_tasks = Column(Integer, nullable=False, default=0)
    total_tasks = Column(Integer, nullable=False, default=0)
    daily_goal = Column(Integer, nullable=False, default=3)
    streak_days = Column(Integer, nullable=False, default=0)
    best_streak = Column(Integer, nullable=False, default=0)
    daily_completed_tasks = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, nullable=False)
    # Registra exclusivamente a última vez que o usuário COMPLETOU uma tarefa.
    # Separado de updated_at para que decrementos não corrompam o cálculo de streak.
    last_completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="progress")
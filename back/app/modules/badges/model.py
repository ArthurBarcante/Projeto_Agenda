from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Regras simples de desbloqueio (podem evoluir para regras compostas depois).
    required_tasks = Column(Integer, nullable=False, default=0)
    required_streak = Column(Integer, nullable=False, default=0)

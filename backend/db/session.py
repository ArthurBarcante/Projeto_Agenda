"""Database session configuration."""

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine

SessionLocal = None


def init_session(engine: Engine) -> None:
    """Initialize session factory.
    
    Args:
        engine: SQLAlchemy Engine instance
    """
    global SessionLocal
    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


def get_session() -> Session:
    """Get database session.
    
    Returns:
        Database session
        
    Raises:
        RuntimeError: If session was not initialized
    """
    if SessionLocal is None:
        raise RuntimeError("Database session not initialized")
    return SessionLocal()


__all__ = ["get_session", "init_session", "SessionLocal"]

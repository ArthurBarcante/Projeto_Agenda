"""Database connection configuration."""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def create_db_engine(database_url: str) -> Engine:
    """Create SQLAlchemy engine.
    
    Args:
        database_url: Database connection URL
        
    Returns:
        SQLAlchemy Engine instance
    """
    return create_engine(
        database_url,
        pool_pre_ping=True,
        echo=False,
    )


__all__ = ["create_db_engine"]

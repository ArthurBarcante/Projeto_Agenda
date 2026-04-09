import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

# Update this fallback with your real PostgreSQL password for local development.
DEFAULT_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/aigenda"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)


def create_engine_from_url(database_url: str | None = None) -> Engine:
	url = database_url or DATABASE_URL
	connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
	return create_engine(url, connect_args=connect_args)


engine = create_engine_from_url(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

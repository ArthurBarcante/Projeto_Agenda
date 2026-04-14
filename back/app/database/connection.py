from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL


def create_engine_from_url(database_url: str | None = None) -> Engine:
	url = database_url or DATABASE_URL
	connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
	return create_engine(url, connect_args=connect_args)


engine = create_engine_from_url(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

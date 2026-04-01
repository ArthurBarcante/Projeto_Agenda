from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Update this password with your real PostgreSQL password.
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/aigenda"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"
DEFAULT_DATABASE_URL = "sqlite:///./render.db"
DEFAULT_SECRET_KEY = "dev-secret-key-change-me"

load_dotenv(ENV_FILE)

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
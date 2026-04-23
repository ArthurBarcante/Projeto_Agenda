from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"
DEFAULT_DATABASE_URL = "sqlite:///./render.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    database_url: str = DEFAULT_DATABASE_URL
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    allowed_origins: str = "http://localhost:5500,http://127.0.0.1:5500"

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError(
                "SECRET_KEY não definida. Configure a variável de ambiente antes de iniciar a aplicação."
            )
        return value


settings = Settings()


def parse_allowed_origins(raw_origins: str) -> list[str]:
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

# Mantem compatibilidade com imports existentes no projeto.
DATABASE_URL = settings.database_url
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
ALLOWED_ORIGINS = parse_allowed_origins(settings.allowed_origins)
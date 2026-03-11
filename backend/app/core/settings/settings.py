from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "Aigenda"

    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = int(
        os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "100")
    )

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    def validate_secret_key_security(self) -> None:
        normalized_environment = (self.ENVIRONMENT or "").strip().lower()
        normalized_secret_key = (self.SECRET_KEY or "").strip()

        # Fail fast in non-development environments to prevent deploying with a
        # predictable or missing signing key, which would compromise token security.
        if normalized_environment != "development" and (
            not normalized_secret_key or normalized_secret_key == "dev-secret-key"
        ):
            raise RuntimeError(
                "Insecure SECRET_KEY configuration detected. "
                "Set a strong SECRET_KEY for non-development environments."
            )

settings = Settings()
settings.validate_secret_key_security()
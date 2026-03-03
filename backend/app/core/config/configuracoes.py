from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    PROJECT_NAME: str = "Aigenda"
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
settings = Settings()
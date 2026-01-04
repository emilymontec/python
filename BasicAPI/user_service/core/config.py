from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "User Service"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DATABASE_URL: str = "sqlite:///../auth_service/auth.db"
    AUTH_ALGORITHM: str = "HS256"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()

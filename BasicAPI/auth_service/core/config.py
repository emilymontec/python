from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Auth Service"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    DATABASE_URL: str = "sqlite:///./auth.db"

    class Config:
        env_file = ".env"


settings = Settings()
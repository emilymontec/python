from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "Product Service"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DATABASE_URL: str = "sqlite:///./products.db"
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()

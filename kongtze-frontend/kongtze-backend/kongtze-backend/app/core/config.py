from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Settings
    PROJECT_NAME: str = "Kongtze"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/kongtze"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # AI Services
    GEMINI_API_KEY: str = ""
    GOOGLE_CLOUD_VISION_CREDENTIALS: str = ""
    
    # File Storage
    STORAGE_PATH: str = "/app/storage"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Configuration
    ULTRA_SAFE_API_KEY: str
    ULTRA_SAFE_BASE_URL: str = "https://api.ultrasafe.com/v1"
    API_PORT: int = 8000
    
    # Database Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    CHROMA_DB_PATH: str = "./chroma_db"
    
    # Task Configuration
    TASK_TIMEOUT: int = 300
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
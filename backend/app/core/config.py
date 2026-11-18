from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Universal Multi-Company Financial Valuation & DCF Engine"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "production-grade-dcf-engine-secret-key-2026-financials"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./universal_dcf.db")
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        case_sensitive = True

settings = Settings()

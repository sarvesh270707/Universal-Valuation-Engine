import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    VectraDesk / Universal Financial Valuation Engine Configuration.
    Enforces Pydantic v2 SettingsConfigDict with environment variable precedence.
    """
    PROJECT_NAME: str = "Universal Multi-Company Financial Valuation & DCF Engine"
    API_V1_STR: str = "/api/v1"
    
    # Security: Read SECRET_KEY from environment; generate safe fallback for dev only
    SECRET_KEY: str = os.getenv("SECRET_KEY", "vectradesk-ephemeral-dev-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./universal_dcf.db")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()

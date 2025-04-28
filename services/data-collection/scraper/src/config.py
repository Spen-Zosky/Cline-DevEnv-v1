"""
Configuration Settings

This module contains the configuration settings for the Data Scraper Service.
"""

import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8081, env="PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Database settings
    MONGODB_URI: str = Field(
        default="mongodb://admin:password@mongodb:27017/scraper?authSource=admin",
        env="MONGODB_URI"
    )
    MONGODB_DB: str = Field(default="scraper", env="MONGODB_DB")
    
    # MinIO settings
    MINIO_ENDPOINT: str = Field(default="minio:9000", env="MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: str = Field(default="minioadmin", env="MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = Field(default="minioadmin", env="MINIO_SECRET_KEY")
    MINIO_BUCKET: str = Field(default="scraper-data", env="MINIO_BUCKET")
    MINIO_SECURE: bool = Field(default=False, env="MINIO_SECURE")
    
    # Scraper settings
    MAX_CONCURRENT_SCRAPERS: int = Field(default=5, env="MAX_CONCURRENT_SCRAPERS")
    DEFAULT_TIMEOUT: int = Field(default=30, env="DEFAULT_TIMEOUT")  # seconds
    USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        env="USER_AGENT"
    )
    RETRY_COUNT: int = Field(default=3, env="RETRY_COUNT")
    RETRY_DELAY: int = Field(default=5, env="RETRY_DELAY")  # seconds
    
    # Logging settings
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    # API settings
    API_PREFIX: str = Field(default="/api", env="API_PREFIX")
    
    class Config:
        """Pydantic config"""
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

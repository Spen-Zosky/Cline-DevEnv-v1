"""
Configuration Settings

This module contains the configuration settings for the Data Preprocessor Service.
"""

import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings"""
    
    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8082, env="PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Database settings
    MONGODB_URI: str = Field(
        default="mongodb://admin:password@mongodb:27017/preprocessor?authSource=admin",
        env="MONGODB_URI"
    )
    MONGODB_DB: str = Field(default="preprocessor", env="MONGODB_DB")
    
    # PostgreSQL settings
    POSTGRES_URI: str = Field(
        default="postgresql://admin:password@postgres:5432/research_db",
        env="POSTGRES_URI"
    )
    
    # MinIO settings
    MINIO_ENDPOINT: str = Field(default="minio:9000", env="MINIO_ENDPOINT")
    MINIO_ACCESS_KEY: str = Field(default="minioadmin", env="MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY: str = Field(default="minioadmin", env="MINIO_SECRET_KEY")
    MINIO_SECURE: bool = Field(default=False, env="MINIO_SECURE")
    
    # MinIO buckets
    MINIO_RAW_BUCKET: str = Field(default="raw-data", env="MINIO_RAW_BUCKET")
    MINIO_PROCESSED_BUCKET: str = Field(default="processed-data", env="MINIO_PROCESSED_BUCKET")
    
    # Preprocessing settings
    MAX_CONCURRENT_JOBS: int = Field(default=5, env="MAX_CONCURRENT_JOBS")
    JOB_POLL_INTERVAL: int = Field(default=5, env="JOB_POLL_INTERVAL")  # seconds
    DEFAULT_CHUNK_SIZE: int = Field(default=1000, env="DEFAULT_CHUNK_SIZE")
    
    # Text preprocessing settings
    DEFAULT_LANGUAGE: str = Field(default="en", env="DEFAULT_LANGUAGE")
    ENABLE_LEMMATIZATION: bool = Field(default=True, env="ENABLE_LEMMATIZATION")
    ENABLE_STEMMING: bool = Field(default=False, env="ENABLE_STEMMING")
    REMOVE_STOPWORDS: bool = Field(default=True, env="REMOVE_STOPWORDS")
    REMOVE_PUNCTUATION: bool = Field(default=True, env="REMOVE_PUNCTUATION")
    LOWERCASE: bool = Field(default=True, env="LOWERCASE")
    
    # Image preprocessing settings
    DEFAULT_IMAGE_SIZE: str = Field(default="224x224", env="DEFAULT_IMAGE_SIZE")
    DEFAULT_IMAGE_FORMAT: str = Field(default="jpg", env="DEFAULT_IMAGE_FORMAT")
    
    # Data collection service endpoints
    CRAWLER_SERVICE_URL: str = Field(default="http://data-crawler:8080", env="CRAWLER_SERVICE_URL")
    SCRAPER_SERVICE_URL: str = Field(default="http://data-scraper:8081", env="SCRAPER_SERVICE_URL")
    
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

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Artifact Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    WORKERS: int = 4
    
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/reqarchitect"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_TIMEOUT: int = 5
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SESSION_TIMEOUT: int = 3600  # 1 hour
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None
    
    # Monitoring settings
    METRICS_ENABLED: bool = True
    HEALTH_CHECK_ENABLED: bool = True
    PROMETHEUS_ENABLED: bool = True
    
    # OpenTelemetry settings
    OTEL_ENABLED: bool = True
    OTEL_ENDPOINT: str = "http://localhost:4317"
    OTEL_SERVICE_NAME: str = "artifact-service"
    OTEL_SERVICE_VERSION: str = "1.0.0"
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_USER_PER_MINUTE: int = 100
    RATE_LIMIT_TENANT_PER_HOUR: int = 1000
    
    # Security settings
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Artifact-specific settings
    MAX_ARTIFACT_SIZE_MB: int = 1000000  # 1TB
    MAX_FILE_COUNT: int = 100000
    ALLOWED_ARTIFACT_TYPES: list = [
        "source", "build", "image", "config", "script", 
        "binary", "container", "package", "library", "framework"
    ]
    ALLOWED_FORMATS: list = [
        "docker", "yaml", "json", "xml", "jar", "war", "ear",
        "exe", "dll", "so", "dylib", "tar", "zip", "gz", "bz2",
        "rpm", "deb", "msi", "pkg", "apk", "ipa"
    ]
    
    # Integrity and security settings
    INTEGRITY_CHECK_ENABLED: bool = True
    SECURITY_SCAN_ENABLED: bool = True
    VULNERABILITY_SCAN_ENABLED: bool = True
    COMPLIANCE_CHECK_ENABLED: bool = True
    
    # Performance settings
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 300  # 5 minutes
    QUERY_TIMEOUT: int = 30  # seconds
    
    # Backup and retention
    BACKUP_ENABLED: bool = True
    BACKUP_RETENTION_DAYS: int = 90
    ARCHIVE_ENABLED: bool = True
    ARCHIVE_THRESHOLD_DAYS: int = 365
    
    # Event streaming
    EVENT_STREAM_ENABLED: bool = True
    EVENT_RETENTION_HOURS: int = 24
    
    # API documentation
    API_DOCS_ENABLED: bool = True
    API_DOCS_TITLE: str = "Artifact Service API"
    API_DOCS_DESCRIPTION: str = "API for managing ArchiMate 3.2 Artifact elements"
    API_DOCS_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "development":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    settings.CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8080"]
    settings.OTEL_ENABLED = False

elif settings.ENVIRONMENT == "testing":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    settings.DATABASE_URL = "postgresql://test:test@localhost:5432/test_db"
    settings.REDIS_DB = 1
    settings.OTEL_ENABLED = False
    settings.METRICS_ENABLED = False

elif settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    settings.CORS_ORIGINS = [
        "https://reqarchitect.com",
        "https://app.reqarchitect.com"
    ]
    settings.RATE_LIMIT_ENABLED = True
    settings.SECURITY_SCAN_ENABLED = True
    settings.COMPLIANCE_CHECK_ENABLED = True

# Validate critical settings
if not settings.JWT_SECRET_KEY or settings.JWT_SECRET_KEY == "your-secret-key-change-in-production":
    raise ValueError("JWT_SECRET_KEY must be set in production")

if settings.ENVIRONMENT == "production" and settings.DATABASE_URL.startswith("postgresql://user:password"):
    raise ValueError("DATABASE_URL must be properly configured in production")

# Log configuration
import logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(settings.LOG_FILE) if settings.LOG_FILE else logging.NullHandler()
    ]
) 
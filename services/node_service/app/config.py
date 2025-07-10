from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Node Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    WORKERS: int = 1
    
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/node_service"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SSL: bool = False
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
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
    OTEL_SERVICE_NAME: str = "node-service"
    OTEL_SERVICE_VERSION: str = "1.0.0"
    OTEL_ENDPOINT: str = "http://localhost:4317"
    OTEL_TRACES_SAMPLER: str = "always_on"
    OTEL_TRACES_SAMPLER_ARG: str = "1.0"
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 100
    RATE_LIMIT_REQUESTS_PER_HOUR: int = 1000
    
    # Security settings
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Node-specific settings
    NODE_DEFAULT_AVAILABILITY_TARGET: float = 99.9
    NODE_DEFAULT_SECURITY_LEVEL: str = "standard"
    NODE_DEFAULT_LIFECYCLE_STATE: str = "active"
    NODE_DEFAULT_ENVIRONMENT: str = "production"
    
    # Analysis settings
    ANALYSIS_ENABLED: bool = True
    CAPACITY_ANALYSIS_ENABLED: bool = True
    DEPLOYMENT_MAP_ENABLED: bool = True
    
    # Event emission settings
    EVENT_EMISSION_ENABLED: bool = True
    EVENT_CHANNEL_PREFIX: str = "node_events"
    
    # Validation settings
    VALIDATION_ENABLED: bool = True
    STRICT_VALIDATION: bool = False
    
    # Performance settings
    MAX_PAGE_SIZE: int = 1000
    DEFAULT_PAGE_SIZE: int = 100
    CACHE_TTL: int = 300  # 5 minutes
    
    # Backup and recovery
    BACKUP_ENABLED: bool = True
    BACKUP_RETENTION_DAYS: int = 30
    BACKUP_SCHEDULE: str = "0 2 * * *"  # Daily at 2 AM
    
    # Maintenance settings
    MAINTENANCE_MODE: bool = False
    MAINTENANCE_MESSAGE: str = "Service is under maintenance"
    
    # API documentation
    API_DOCS_ENABLED: bool = True
    API_DOCS_TITLE: str = "Node Service API"
    API_DOCS_DESCRIPTION: str = "Node Service for managing ArchiMate 3.2 Node elements"
    API_DOCS_VERSION: str = "1.0.0"
    
    # ArchiMate integration
    ARCHIMATE_VERSION: str = "3.2"
    ARCHIMATE_LAYER: str = "Technology"
    ARCHIMATE_ELEMENT: str = "Node"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "development":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    settings.OTEL_TRACES_SAMPLER_ARG = "1.0"
    settings.RATE_LIMIT_ENABLED = False

elif settings.ENVIRONMENT == "testing":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    settings.DATABASE_URL = "postgresql://test:test@localhost:5432/node_service_test"
    settings.REDIS_DB = 1
    settings.OTEL_ENABLED = False
    settings.METRICS_ENABLED = False

elif settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "INFO"
    settings.WORKERS = 4
    settings.DATABASE_POOL_SIZE = 20
    settings.DATABASE_MAX_OVERFLOW = 30
    settings.RATE_LIMIT_ENABLED = True

# Validate critical settings
def validate_settings():
    """Validate critical settings."""
    if not settings.JWT_SECRET_KEY or settings.JWT_SECRET_KEY == "your-secret-key-here":
        raise ValueError("JWT_SECRET_KEY must be set in production")
    
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL must be set")
    
    if settings.ENVIRONMENT == "production" and settings.DEBUG:
        raise ValueError("DEBUG must be False in production")

# Call validation
validate_settings() 
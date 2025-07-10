from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "Application Service API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/reqarchitect"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600
    
    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SSL: bool = False
    
    # JWT settings
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Security settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Rate limiting
    RATE_LIMIT_PER_HOUR: int = 1000
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_BURST: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Monitoring
    METRICS_ENABLED: bool = True
    HEALTH_CHECK_INTERVAL: int = 30
    
    # Service-specific settings
    SERVICE_PORT: int = 8080
    SERVICE_HOST: str = "0.0.0.0"
    
    # OpenTelemetry settings
    OTEL_ENABLED: bool = True
    OTEL_SERVICE_NAME: str = "application-service"
    OTEL_ENDPOINT: str = "http://localhost:4317"
    
    # Event bus settings
    EVENT_BUS_ENABLED: bool = True
    EVENT_BUS_REDIS_CHANNEL: str = "application_service_events"
    
    # Validation settings
    MAX_NAME_LENGTH: int = 255
    MAX_DESCRIPTION_LENGTH: int = 2000
    MAX_ENDPOINT_LENGTH: int = 500
    
    # Performance settings
    DEFAULT_LATENCY_TARGET_MS: int = 200
    DEFAULT_AVAILABILITY_TARGET_PCT: float = 99.9
    DEFAULT_THROUGHPUT_TARGET_RPS: int = 1000
    
    # Business settings
    DEFAULT_BUSINESS_VALUE: str = "medium"
    DEFAULT_BUSINESS_CRITICALITY: str = "medium"
    DEFAULT_SECURITY_LEVEL: str = "standard"
    DEFAULT_DATA_CLASSIFICATION: str = "internal"
    
    # Deployment settings
    DEFAULT_DEPLOYMENT_MODEL: str = "monolithic"
    DEFAULT_SCALING_STRATEGY: str = "horizontal"
    DEFAULT_DELIVERY_CHANNEL: str = "http"
    DEFAULT_AUTHENTICATION_METHOD: str = "none"
    
    # Documentation settings
    API_DOCS_ENABLED: bool = True
    API_DOCS_TITLE: str = "Application Service API"
    API_DOCS_DESCRIPTION: str = "API for managing ArchiMate 3.2 Application Service elements"
    API_DOCS_VERSION: str = "1.0.0"
    
    # Testing settings
    TESTING: bool = False
    TEST_DATABASE_URL: str = "postgresql://test:test@localhost:5432/test_db"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Environment-specific overrides
if os.getenv("ENVIRONMENT") == "production":
    settings.DEBUG = False
    settings.LOG_LEVEL = "WARNING"
    settings.METRICS_ENABLED = True
    settings.OTEL_ENABLED = True
elif os.getenv("ENVIRONMENT") == "development":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    settings.METRICS_ENABLED = True
    settings.OTEL_ENABLED = False
elif os.getenv("ENVIRONMENT") == "testing":
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    settings.METRICS_ENABLED = False
    settings.OTEL_ENABLED = False
    settings.TESTING = True 
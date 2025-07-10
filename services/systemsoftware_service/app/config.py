from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "System Software Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    WORKERS: int = 1
    
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/systemsoftware_db"
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
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security settings
    CORS_ORIGINS: list = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["*"]
    CORS_ALLOW_HEADERS: list = ["*"]
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 100
    RATE_LIMIT_REQUESTS_PER_HOUR: int = 1000
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: Optional[str] = None
    
    # Monitoring and observability
    METRICS_ENABLED: bool = True
    HEALTH_CHECK_ENABLED: bool = True
    TRACING_ENABLED: bool = True
    
    # OpenTelemetry settings
    OTEL_ENABLED: bool = True
    OTEL_SERVICE_NAME: str = "systemsoftware-service"
    OTEL_SERVICE_VERSION: str = "1.0.0"
    OTEL_ENDPOINT: Optional[str] = None
    OTEL_TRACES_EXPORTER: str = "otlp"
    OTEL_METRICS_EXPORTER: str = "otlp"
    OTEL_LOGS_EXPORTER: str = "otlp"
    
    # Prometheus settings
    PROMETHEUS_ENABLED: bool = True
    PROMETHEUS_PORT: int = 9090
    
    # Event bus settings
    EVENT_BUS_ENABLED: bool = True
    EVENT_BUS_REDIS_CHANNEL: str = "system_software_events"
    
    # Validation settings
    VALIDATION_ENABLED: bool = True
    VALIDATION_STRICT: bool = True
    
    # Cache settings
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 300  # 5 minutes
    CACHE_MAX_SIZE: int = 1000
    
    # Backup and recovery
    BACKUP_ENABLED: bool = True
    BACKUP_FREQUENCY: str = "daily"
    BACKUP_RETENTION_DAYS: int = 30
    
    # Compliance settings
    COMPLIANCE_ENABLED: bool = True
    COMPLIANCE_AUDIT_ENABLED: bool = True
    COMPLIANCE_REPORTING_ENABLED: bool = True
    
    # Performance settings
    PERFORMANCE_MONITORING_ENABLED: bool = True
    PERFORMANCE_THRESHOLDS_ENABLED: bool = True
    
    # Security compliance
    SECURITY_SCANNING_ENABLED: bool = True
    VULNERABILITY_CHECK_ENABLED: bool = True
    PATCH_MANAGEMENT_ENABLED: bool = True
    
    # API documentation
    API_DOCS_ENABLED: bool = True
    API_DOCS_TITLE: str = "System Software Service API"
    API_DOCS_DESCRIPTION: str = "API for managing ArchiMate 3.2 System Software elements"
    API_DOCS_VERSION: str = "1.0.0"
    
    # Database migration
    MIGRATION_ENABLED: bool = True
    MIGRATION_AUTO_UPGRADE: bool = False
    
    # Testing settings
    TESTING_ENABLED: bool = False
    TEST_DATABASE_URL: Optional[str] = None
    
    # Development settings
    DEVELOPMENT_MODE: bool = False
    HOT_RELOAD: bool = False
    
    # Production settings
    PRODUCTION_MODE: bool = True
    SSL_ENABLED: bool = False
    SSL_CERT_FILE: Optional[str] = None
    SSL_KEY_FILE: Optional[str] = None
    
    # Load balancing
    LOAD_BALANCER_ENABLED: bool = False
    LOAD_BALANCER_HEALTH_CHECK_PATH: str = "/health"
    
    # Circuit breaker
    CIRCUIT_BREAKER_ENABLED: bool = True
    CIRCUIT_BREAKER_FAILURE_THRESHOLD: int = 5
    CIRCUIT_BREAKER_RECOVERY_TIMEOUT: int = 60
    
    # Retry settings
    RETRY_ENABLED: bool = True
    RETRY_MAX_ATTEMPTS: int = 3
    RETRY_BACKOFF_FACTOR: float = 2.0
    
    # Timeout settings
    REQUEST_TIMEOUT: int = 30
    DATABASE_TIMEOUT: int = 10
    REDIS_TIMEOUT: int = 5
    
    # Memory settings
    MAX_MEMORY_USAGE: int = 512  # MB
    MEMORY_MONITORING_ENABLED: bool = True
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = ["json", "yaml", "yml", "txt"]
    
    # Notification settings
    NOTIFICATION_ENABLED: bool = True
    NOTIFICATION_EMAIL_ENABLED: bool = False
    NOTIFICATION_WEBHOOK_ENABLED: bool = True
    
    # ArchiMate specific settings
    ARCHIMATE_VERSION: str = "3.2"
    ARCHIMATE_LAYER: str = "Technology"
    ARCHIMATE_ELEMENT_TYPE: str = "System Software"
    
    # System Software specific settings
    SOFTWARE_TYPE_VALIDATION_ENABLED: bool = True
    VULNERABILITY_SCORE_VALIDATION_ENABLED: bool = True
    LICENSE_VALIDATION_ENABLED: bool = True
    COMPLIANCE_VALIDATION_ENABLED: bool = True
    
    # Integration settings
    EXTERNAL_API_ENABLED: bool = True
    EXTERNAL_API_TIMEOUT: int = 30
    EXTERNAL_API_RETRY_ATTEMPTS: int = 3
    
    # Data validation
    DATA_VALIDATION_ENABLED: bool = True
    DATA_SANITIZATION_ENABLED: bool = True
    
    # Audit settings
    AUDIT_LOGGING_ENABLED: bool = True
    AUDIT_EVENT_RETENTION_DAYS: int = 365
    
    # Performance optimization
    QUERY_OPTIMIZATION_ENABLED: bool = True
    CONNECTION_POOLING_ENABLED: bool = True
    CACHING_ENABLED: bool = True
    
    # Error handling
    ERROR_REPORTING_ENABLED: bool = True
    ERROR_NOTIFICATION_ENABLED: bool = True
    
    # Maintenance settings
    MAINTENANCE_MODE_ENABLED: bool = False
    MAINTENANCE_MESSAGE: str = "Service is under maintenance"
    
    # Feature flags
    FEATURE_FLAGS_ENABLED: bool = True
    ADVANCED_ANALYTICS_ENABLED: bool = True
    MACHINE_LEARNING_ENABLED: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Environment-specific overrides
if settings.ENVIRONMENT == "development":
    settings.DEBUG = True
    settings.DEVELOPMENT_MODE = True
    settings.HOT_RELOAD = True
    settings.LOG_LEVEL = "DEBUG"
    settings.VALIDATION_STRICT = False

elif settings.ENVIRONMENT == "testing":
    settings.TESTING_ENABLED = True
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    settings.DATABASE_URL = settings.TEST_DATABASE_URL or "postgresql://test:test@localhost:5432/test_systemsoftware_db"

elif settings.ENVIRONMENT == "production":
    settings.DEBUG = False
    settings.PRODUCTION_MODE = True
    settings.LOG_LEVEL = "WARNING"
    settings.VALIDATION_STRICT = True
    settings.SSL_ENABLED = True
    settings.CIRCUIT_BREAKER_ENABLED = True
    settings.RATE_LIMIT_ENABLED = True

# Validate critical settings
def validate_settings():
    """Validate critical settings."""
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL is required")
    
    if not settings.JWT_SECRET_KEY or settings.JWT_SECRET_KEY == "your-secret-key-change-in-production":
        if settings.ENVIRONMENT == "production":
            raise ValueError("JWT_SECRET_KEY must be set in production")
    
    if settings.RATE_LIMIT_REQUESTS_PER_MINUTE <= 0:
        raise ValueError("RATE_LIMIT_REQUESTS_PER_MINUTE must be positive")
    
    if settings.RATE_LIMIT_REQUESTS_PER_HOUR <= 0:
        raise ValueError("RATE_LIMIT_REQUESTS_PER_HOUR must be positive")

# Validate settings on import
validate_settings() 
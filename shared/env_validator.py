"""
Shared environment validation utility for ReqArchitect services.
Provides standardized environment variable validation and loading.
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common required environment variables for all services
COMMON_REQUIRED_KEYS = [
    "SERVICE_PORT",
    "JWT_SECRET",
    "DATABASE_URL"
]

# Service-specific required environment variables
SERVICE_REQUIRED_KEYS = {
    "gateway_service": [
        "GATEWAY_PORT",
        "AUTH_SERVICE_URL",
        "AI_MODELING_SERVICE_URL",
        "USAGE_SERVICE_URL",
        "BILLING_SERVICE_URL",
        "INVOICE_SERVICE_URL",
        "NOTIFICATION_SERVICE_URL"
    ],
    "auth_service": [
        "AUTH_PORT",
        "SECRET_KEY",
        "ACCESS_TOKEN_EXPIRE_MINUTES"
    ],
    "ai_modeling_service": [
        "AI_MODELING_PORT",
        "OPENAI_API_KEY",
        "MODEL_NAME"
    ],
    "usage_service": [
        "USAGE_PORT",
        "USAGE_DB_NAME"
    ],
    "billing_service": [
        "BILLING_PORT",
        "STRIPE_SECRET_KEY",
        "STRIPE_PUBLISHABLE_KEY"
    ],
    "invoice_service": [
        "INVOICE_PORT",
        "INVOICE_DB_NAME",
        "PDF_STORAGE_PATH"
    ],
    "notification_service": [
        "NOTIFICATION_PORT",
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USERNAME",
        "SMTP_PASSWORD"
    ],
    "monitoring_dashboard_service": [
        "MONITORING_PORT",
        "DASHBOARD_REFRESH_INTERVAL"
    ]
}

# Optional environment variables with defaults
OPTIONAL_KEYS_WITH_DEFAULTS = {
    "LOG_LEVEL": "INFO",
    "ENVIRONMENT": "development",
    "DEBUG": "false",
    "CORS_ORIGINS": "*",
    "RATE_LIMIT_PER_MINUTE": "100",
    "REQUEST_TIMEOUT": "30",
    "HEALTH_CHECK_INTERVAL": "30",
    "DATABASE_POOL_SIZE": "10",
    "DATABASE_MAX_OVERFLOW": "20",
    "REDIS_URL": "redis://localhost:6379/0",
    "REDIS_PASSWORD": "",
    "REDIS_DB": "0"
}

def load_environment(service_name: Optional[str] = None) -> None:
    """
    Load environment variables from .env file.
    
    Args:
        service_name: Name of the service for service-specific validation
    """
    # Load .env file if it exists
    load_dotenv()
    
    # Set service name from environment if not provided
    if not service_name:
        service_name = os.getenv("SERVICE_NAME", "unknown")
    
    logger.info(f"Loading environment for service: {service_name}")

def validate_environment(service_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate that all required environment variables are present.
    
    Args:
        service_name: Name of the service for service-specific validation
        
    Returns:
        Dict containing all environment variables with defaults applied
        
    Raises:
        ValueError: If required environment variables are missing
    """
    # Load environment
    load_environment(service_name)
    
    # Set service name from environment if not provided
    if not service_name:
        service_name = os.getenv("SERVICE_NAME", "unknown")
    
    # Collect all required keys for this service
    required_keys = COMMON_REQUIRED_KEYS.copy()
    if service_name in SERVICE_REQUIRED_KEYS:
        required_keys.extend(SERVICE_REQUIRED_KEYS[service_name])
    
    # Check for missing required keys
    missing_keys = []
    for key in required_keys:
        if not os.getenv(key):
            missing_keys.append(key)
    
    if missing_keys:
        error_msg = f"Missing required environment variables for {service_name}: {', '.join(missing_keys)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    # Build environment config with defaults
    config = {}
    
    # Add all required keys
    for key in required_keys:
        config[key] = os.getenv(key)
    
    # Add optional keys with defaults
    for key, default_value in OPTIONAL_KEYS_WITH_DEFAULTS.items():
        config[key] = os.getenv(key, default_value)
    
    # Add all other environment variables
    for key, value in os.environ.items():
        if key not in config:
            config[key] = value
    
    logger.info(f"Environment validation successful for {service_name}")
    return config

def get_service_config(service_name: str) -> Dict[str, Any]:
    """
    Get validated configuration for a specific service.
    
    Args:
        service_name: Name of the service
        
    Returns:
        Dict containing service configuration
    """
    return validate_environment(service_name)

def validate_database_url(database_url: str) -> bool:
    """
    Validate database URL format.
    
    Args:
        database_url: Database connection string
        
    Returns:
        True if valid, False otherwise
    """
    if not database_url:
        return False
    
    # Basic validation for common database URLs
    valid_prefixes = [
        "postgresql://",
        "postgres://",
        "mysql://",
        "sqlite://",
        "oracle://",
        "mssql://"
    ]
    
    return any(database_url.startswith(prefix) for prefix in valid_prefixes)

def validate_port(port_str: str) -> bool:
    """
    Validate port number.
    
    Args:
        port_str: Port as string
        
    Returns:
        True if valid, False otherwise
    """
    try:
        port = int(port_str)
        return 1 <= port <= 65535
    except (ValueError, TypeError):
        return False

def validate_boolean(value: str) -> bool:
    """
    Validate boolean string value.
    
    Args:
        value: Boolean string value
        
    Returns:
        True if valid boolean, False otherwise
    """
    return value.lower() in ("true", "false", "1", "0", "yes", "no")

def get_environment_summary(service_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get a summary of the current environment configuration.
    
    Args:
        service_name: Name of the service
        
    Returns:
        Dict containing environment summary
    """
    config = validate_environment(service_name)
    
    # Create summary (excluding sensitive data)
    summary = {
        "service_name": service_name or os.getenv("SERVICE_NAME", "unknown"),
        "environment": config.get("ENVIRONMENT", "unknown"),
        "debug": config.get("DEBUG", "false"),
        "log_level": config.get("LOG_LEVEL", "INFO"),
        "service_port": config.get("SERVICE_PORT", "unknown"),
        "database_configured": bool(config.get("DATABASE_URL")),
        "redis_configured": bool(config.get("REDIS_URL")),
        "total_variables": len(config)
    }
    
    return summary

def print_environment_summary(service_name: Optional[str] = None) -> None:
    """
    Print a formatted summary of the current environment configuration.
    
    Args:
        service_name: Name of the service
    """
    summary = get_environment_summary(service_name)
    
    print("=" * 50)
    print(f"Environment Summary for {summary['service_name']}")
    print("=" * 50)
    print(f"Environment: {summary['environment']}")
    print(f"Debug Mode: {summary['debug']}")
    print(f"Log Level: {summary['log_level']}")
    print(f"Service Port: {summary['service_port']}")
    print(f"Database Configured: {summary['database_configured']}")
    print(f"Redis Configured: {summary['redis_configured']}")
    print(f"Total Variables: {summary['total_variables']}")
    print("=" * 50)

# Convenience function for quick validation
def validate_env(service_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Quick validation function for use in service startup.
    
    Args:
        service_name: Name of the service
        
    Returns:
        Dict containing validated configuration
    """
    try:
        return validate_environment(service_name)
    except ValueError as e:
        logger.error(f"Environment validation failed: {e}")
        raise 
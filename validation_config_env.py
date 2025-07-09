#!/usr/bin/env python3
"""
Enhanced Validation Configuration with Environment Variable Support
Supports CI/CD environment overrides for test data and JWT tokens
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

def load_config_with_env_overrides(config_path: str = "validation_config.json") -> Dict[str, Any]:
    """Load configuration with environment variable overrides"""
    
    # Load base configuration
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    # Environment variable overrides
    env_overrides = {
        # JWT Settings
        'JWT_SECRET': ('jwt_settings', 'secret'),
        'JWT_ALGORITHM': ('jwt_settings', 'algorithm'),
        'JWT_EXPIRATION_HOURS': ('jwt_settings', 'expiration_hours'),
        
        # Test Data
        'TEST_TENANT_ID': ('test_data', 'tenant_id'),
        'TEST_USER_ID': ('test_data', 'user_id'),
        'TEST_EMAIL': ('test_data', 'email'),
        'TEST_PASSWORD': ('test_data', 'password'),
        'TEST_ROLE': ('test_data', 'role'),
        
        # Validation Settings
        'VALIDATION_RETRY_ATTEMPTS': ('validation_settings', 'retry_attempts'),
        'VALIDATION_RETRY_DELAY': ('validation_settings', 'retry_delay'),
        'VALIDATION_TIMEOUT': ('validation_settings', 'timeout'),
        'VALIDATION_CHECK_INTERVAL': ('validation_settings', 'check_interval_minutes'),
        'VALIDATION_HISTORY_RETENTION': ('validation_settings', 'history_retention_days'),
        
        # Environment-specific settings
        'VALIDATION_ENV': ('environment', 'name'),
        'CI_PIPELINE_ID': ('environment', 'pipeline_id'),
        'CI_COMMIT_SHA': ('environment', 'commit_sha'),
        'CI_BRANCH': ('environment', 'branch'),
    }
    
    # Apply environment variable overrides
    for env_var, (section, key) in env_overrides.items():
        env_value = os.getenv(env_var)
        if env_value is not None:
            # Ensure section exists
            if section not in config:
                config[section] = {}
            
            # Convert numeric values
            if key in ['retry_attempts', 'retry_delay', 'timeout', 'check_interval_minutes', 'history_retention_days', 'expiration_hours']:
                try:
                    env_value = int(env_value)
                except ValueError:
                    try:
                        env_value = float(env_value)
                    except ValueError:
                        pass  # Keep as string
            
            config[section][key] = env_value
    
    # Set default values if not provided
    if 'jwt_settings' not in config:
        config['jwt_settings'] = {
            'enabled': True,
            'secret': os.getenv('JWT_SECRET', 'supersecret'),
            'algorithm': 'HS256',
            'expiration_hours': 24
        }
    
    if 'test_data' not in config:
        config['test_data'] = {
            'tenant_id': os.getenv('TEST_TENANT_ID', 'test-tenant-123'),
            'user_id': os.getenv('TEST_USER_ID', 'test-user-456'),
            'email': os.getenv('TEST_EMAIL', 'test@example.com'),
            'password': os.getenv('TEST_PASSWORD', 'testpass123'),
            'role': os.getenv('TEST_ROLE', 'Admin')
        }
    
    if 'validation_settings' not in config:
        config['validation_settings'] = {
            'retry_attempts': 3,
            'retry_delay': 2,
            'timeout': 30,
            'check_interval_minutes': 15,
            'history_retention_days': 7
        }
    
    if 'environment' not in config:
        config['environment'] = {
            'name': os.getenv('VALIDATION_ENV', 'development'),
            'pipeline_id': os.getenv('CI_PIPELINE_ID', 'local'),
            'commit_sha': os.getenv('CI_COMMIT_SHA', 'unknown'),
            'branch': os.getenv('CI_BRANCH', 'unknown')
        }
    
    # Add CI/CD specific settings
    if os.getenv('CI') == 'true':
        config['ci_settings'] = {
            'enabled': True,
            'fail_on_critical_errors': True,
            'send_alerts': True,
            'artifact_retention_days': 30
        }
    else:
        config['ci_settings'] = {
            'enabled': False,
            'fail_on_critical_errors': False,
            'send_alerts': False,
            'artifact_retention_days': 7
        }
    
    return config

def save_env_config(config: Dict[str, Any], output_path: str = "validation_config_env.json"):
    """Save configuration with environment overrides"""
    with open(output_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Environment-aware configuration saved to {output_path}")

def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate environment-aware validation config")
    parser.add_argument("--input", default="validation_config.json", help="Input config file")
    parser.add_argument("--output", default="validation_config_env.json", help="Output config file")
    parser.add_argument("--print", action="store_true", help="Print config to stdout")
    
    args = parser.parse_args()
    
    # Load configuration with environment overrides
    config = load_config_with_env_overrides(args.input)
    
    # Save to output file
    save_env_config(config, args.output)
    
    # Print if requested
    if args.print:
        print(json.dumps(config, indent=2))

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Fix .env files with correct database URLs based on postgres-init configuration
"""

import os
from pathlib import Path

# Correct database configurations based on postgres-init files
SERVICES_CONFIG = {
    'auth_service': {
        'db_name': 'auth_db',
        'db_user': 'auth_user',
        'db_pass': 'auth_pass',
        'port': 8001,
        'extra_vars': {
            'ACCESS_TOKEN_EXPIRE_MINUTES': '60'
        }
    },
    'usage_service': {
        'db_name': 'usage_db',
        'db_user': 'usage_user',
        'db_pass': 'usage_pass',
        'port': 8000,
        'extra_vars': {}
    },
    'billing_service': {
        'db_name': 'billing_db',
        'db_user': 'billing_user',
        'db_pass': 'billing_pass',
        'port': 8010,
        'extra_vars': {
            'STRIPE_SECRET_KEY': 'your-stripe-secret-key',
            'STRIPE_PUBLISHABLE_KEY': 'your-stripe-publishable-key'
        }
    },
    'invoice_service': {
        'db_name': 'invoice_db',
        'db_user': 'invoice_user',
        'db_pass': 'invoice_pass',
        'port': 8011,
        'extra_vars': {
            'INVOICE_DB_NAME': 'invoice_service',
            'PDF_STORAGE_PATH': '/app/invoices'
        }
    },
    'notification_service': {
        'db_name': 'notification_db',
        'db_user': 'notification_user',
        'db_pass': 'notification_pass',
        'port': 8000,
        'extra_vars': {
            'SMTP_HOST': 'smtp.gmail.com',
            'SMTP_PORT': '587',
            'SMTP_USERNAME': 'your-email@gmail.com',
            'SMTP_PASSWORD': 'your-app-password'
        }
    },
    'audit_log_service': {
        'db_name': 'audit_db',
        'db_user': 'audit_user',
        'db_pass': 'audit_pass',
        'port': 8000,
        'extra_vars': {}
    },
    'ai_modeling_service': {
        'db_name': 'ai_modeling_db',
        'db_user': 'ai_user',
        'db_pass': 'ai_pass',
        'port': 8002,
        'extra_vars': {
            'OPENAI_API_KEY': 'your-openai-api-key-here',
            'MODEL_NAME': 'gpt-4'
        }
    }
}

def generate_env_content(service_name, config):
    """Generate .env file content for a service"""
    db_url = f"postgresql://{config['db_user']}:{config['db_pass']}@postgres_db:5432/{config['db_name']}"
    
    content = f"""# {service_name.replace('_', ' ').title()} Environment Configuration
DATABASE_URL={db_url}
JWT_SECRET=supersecret
SECRET_KEY=your-super-secret-key-change-this-in-production
SERVICE_PORT={config['port']}
ENVIRONMENT=development
LOG_LEVEL=INFO
"""
    
    # Add extra variables
    for key, value in config['extra_vars'].items():
        content += f"{key}={value}\n"
    
    return content

def main():
    """Generate .env files for all target services"""
    print("🔧 Generating .env files with correct database URLs...")
    
    for service_name, config in SERVICES_CONFIG.items():
        service_path = Path(f"services/{service_name}")
        env_file = service_path / ".env"
        
        # Create service directory if it doesn't exist
        service_path.mkdir(exist_ok=True)
        
        # Generate .env content
        env_content = generate_env_content(service_name, config)
        
        # Write .env file
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created {env_file}")
        print(f"   Database URL: {config['db_user']}@{config['db_name']}")
    
    print("\n🎉 All .env files generated successfully!")
    print("\nNext steps:")
    print("1. Run: docker-compose down")
    print("2. Run: docker-compose up -d")
    print("3. Run: python validate_db_connections.py")

if __name__ == "__main__":
    main() 
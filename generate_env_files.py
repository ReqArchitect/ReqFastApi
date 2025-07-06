#!/usr/bin/env python3
"""
Generate missing .env files for target services
"""

import os
from pathlib import Path

# Target services and their configurations
SERVICES_CONFIG = {
    'auth_service': {
        'port': 8001,
        'extra_vars': {
            'ACCESS_TOKEN_EXPIRE_MINUTES': '60'
        }
    },
    'usage_service': {
        'port': 8000,
        'extra_vars': {}
    },
    'billing_service': {
        'port': 8010,
        'extra_vars': {
            'STRIPE_SECRET_KEY': 'your-stripe-secret-key',
            'STRIPE_PUBLISHABLE_KEY': 'your-stripe-publishable-key'
        }
    },
    'invoice_service': {
        'port': 8011,
        'extra_vars': {
            'INVOICE_DB_NAME': 'invoice_service',
            'PDF_STORAGE_PATH': '/app/invoices'
        }
    },
    'notification_service': {
        'port': 8000,
        'extra_vars': {
            'SMTP_HOST': 'smtp.gmail.com',
            'SMTP_PORT': '587',
            'SMTP_USERNAME': 'your-email@gmail.com',
            'SMTP_PASSWORD': 'your-app-password'
        }
    },
    'audit_log_service': {
        'port': 8000,
        'extra_vars': {}
    },
    'ai_modeling_service': {
        'port': 8002,
        'extra_vars': {
            'OPENAI_API_KEY': 'your-openai-api-key-here',
            'MODEL_NAME': 'gpt-4'
        }
    }
}

def generate_env_content(service_name, config):
    """Generate .env file content for a service"""
    content = f"""# {service_name.replace('_', ' ').title()} Environment Configuration
DATABASE_URL=postgresql://reqadmin:reqpass@postgres_db:5432/{service_name}
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
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
    print("🔧 Generating .env files for target services...")
    
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
    
    print("\n🎉 All .env files generated successfully!")
    print("\nNext steps:")
    print("1. Run: docker-compose down")
    print("2. Run: docker-compose up -d")
    print("3. Run: python validate_db_connections.py")

if __name__ == "__main__":
    main() 
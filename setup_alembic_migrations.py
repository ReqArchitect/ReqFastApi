#!/usr/bin/env python3
"""
Script to scaffold Alembic migrations for all target services.
Run this script to set up database migrations for the operational phase.
"""

import os
import shutil
from pathlib import Path

# Target services for migration setup
TARGET_SERVICES = [
    'auth_service',
    'usage_service', 
    'billing_service',
    'invoice_service',
    'notification_service',
    'audit_log_service',
    'ai_modeling_service'
]

def create_alembic_structure(service_name):
    """Create Alembic directory structure for a service."""
    service_path = Path(f"services/{service_name}")
    alembic_path = service_path / "alembic"
    versions_path = alembic_path / "versions"
    
    # Create directories
    alembic_path.mkdir(exist_ok=True)
    versions_path.mkdir(exist_ok=True)
    
    print(f"✅ Created Alembic structure for {service_name}")

def create_alembic_ini(service_name):
    """Create alembic.ini file for a service."""
    ini_content = """[alembic]
script_location = alembic
sqlalchemy.url = env:DATABASE_URL
"""
    
    ini_path = Path(f"services/{service_name}/alembic.ini")
    ini_path.write_text(ini_content)
    print(f"✅ Created alembic.ini for {service_name}")

def create_env_py(service_name):
    """Create env.py file for a service."""
    env_content = '''from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))
from app.models import Base

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
'''
    
    env_path = Path(f"services/{service_name}/alembic/env.py")
    env_path.write_text(env_content)
    print(f"✅ Created env.py for {service_name}")

def create_script_mako(service_name):
    """Create script.py.mako template for a service."""
    mako_content = '''"""
Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    ${upgrades if upgrades else "pass"}

def downgrade():
    ${downgrades if downgrades else "pass"}
'''
    
    mako_path = Path(f"services/{service_name}/alembic/script.py.mako")
    mako_path.write_text(mako_content)
    print(f"✅ Created script.py.mako for {service_name}")

def create_readme(service_name):
    """Create README for Alembic setup."""
    readme_content = f'''# {service_name.replace('_', ' ').title()} Database Migrations

This directory contains database migrations for the {service_name}.

## Usage

1. Generate a new migration:
   ```bash
   cd services/{service_name}
   alembic revision --autogenerate -m "Description of changes"
   ```

2. Apply migrations:
   ```bash
   alembic upgrade head
   ```

3. Check current migration state:
   ```bash
   alembic current
   ```

4. Rollback to previous version:
   ```bash
   alembic downgrade -1
   ```

## Environment Setup

Ensure DATABASE_URL is set in your environment:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/{service_name}_db"
```
'''
    
    readme_path = Path(f"services/{service_name}/alembic/README")
    readme_path.write_text(readme_content)
    print(f"✅ Created README for {service_name}")

def main():
    """Main function to set up Alembic for all target services."""
    print("🚀 Setting up Alembic migrations for target services...")
    print("=" * 60)
    
    for service in TARGET_SERVICES:
        print(f"\n📦 Processing {service}...")
        
        # Check if service exists
        service_path = Path(f"services/{service}")
        if not service_path.exists():
            print(f"❌ Service {service} not found, skipping...")
            continue
            
        # Check if models.py exists
        models_path = service_path / "app" / "models.py"
        if not models_path.exists():
            print(f"❌ models.py not found in {service}, skipping...")
            continue
        
        # Create Alembic structure
        create_alembic_structure(service)
        create_alembic_ini(service)
        create_env_py(service)
        create_script_mako(service)
        create_readme(service)
        
        print(f"✅ Completed Alembic setup for {service}")
    
    print("\n" + "=" * 60)
    print("🎉 Alembic setup completed for all target services!")
    print("\nNext steps:")
    print("1. Set DATABASE_URL environment variable for each service")
    print("2. Run 'alembic revision --autogenerate -m \"Initial migration\"' in each service directory")
    print("3. Run 'alembic upgrade head' to apply migrations")
    print("4. Verify schema alignment with 'alembic current' and 'alembic heads'")

if __name__ == "__main__":
    main() 
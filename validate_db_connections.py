import os
import glob
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

SERVICES = [
    'auth_service',
    'usage_service',
    'billing_service',
    'invoice_service',
    'notification_service',
    'audit_log_service',
    'ai_modeling_service',
]

BASE_DIR = os.path.join(os.path.dirname(__file__), 'services')

results = []


for service in SERVICES:
    env_path = os.path.join(BASE_DIR, service, '.env')
    service_name = service.replace('_service', '')
    if not os.path.exists(env_path):
        results.append((service, '❌ .env file not found'))
        continue
    load_dotenv(env_path, override=True)
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        results.append((service, '❌ DATABASE_URL not set'))
        continue
    # Try both 'postgres' and 'localhost' as host
    tried = []
    for host in ['postgres', 'localhost']:
        test_url = db_url.replace('postgres://', 'postgresql://')  # normalize
        test_url = test_url.replace('@postgres:', f'@{host}:')
        try:
            engine = create_engine(test_url)
            with engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            results.append((service, f'✅ Connection successful (host: {host})'))
            break
        except Exception as e:
            tried.append(f'{host}: {e}')
    else:
        results.append((service, f'❌ Connection failed: ' + ' | '.join(tried)))

print('\nDatabase Connection Validation Results:')
for service, status in results:
    print(f'{service}: {status}')

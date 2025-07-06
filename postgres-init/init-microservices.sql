
-- Create users if not exists
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'audit_user') THEN
        CREATE USER audit_user WITH PASSWORD 'audit_pass';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'auth_user') THEN
        CREATE USER auth_user WITH PASSWORD 'auth_pass';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'billing_user') THEN
        CREATE USER billing_user WITH PASSWORD 'billing_pass';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'usage_user') THEN
        CREATE USER usage_user WITH PASSWORD 'usage_pass';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'invoice_user') THEN
        CREATE USER invoice_user WITH PASSWORD 'invoice_pass';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'notification_user') THEN
        CREATE USER notification_user WITH PASSWORD 'notification_pass';
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'ai_user') THEN
        CREATE USER ai_user WITH PASSWORD 'ai_pass';
    END IF;
END
$$;

-- Create databases (plain SQL, not in DO block)
CREATE DATABASE audit_db WITH OWNER = audit_user ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE = template0;
CREATE DATABASE auth_db WITH OWNER = auth_user ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE = template0;
CREATE DATABASE billing_db WITH OWNER = billing_user ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE = template0;
CREATE DATABASE usage_db WITH OWNER = usage_user ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE = template0;
CREATE DATABASE invoice_db WITH OWNER = invoice_user ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE = template0;
CREATE DATABASE notification_db WITH OWNER = notification_user ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE = template0;
CREATE DATABASE ai_modeling_db WITH OWNER = ai_user ENCODING = 'UTF8' LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8' TEMPLATE = template0;

GRANT ALL PRIVILEGES ON DATABASE audit_db TO audit_user;
GRANT ALL PRIVILEGES ON DATABASE auth_db TO auth_user;
GRANT ALL PRIVILEGES ON DATABASE billing_db TO billing_user;
GRANT ALL PRIVILEGES ON DATABASE usage_db TO usage_user;
GRANT ALL PRIVILEGES ON DATABASE invoice_db TO invoice_user;
GRANT ALL PRIVILEGES ON DATABASE notification_db TO notification_user;
GRANT ALL PRIVILEGES ON DATABASE ai_modeling_db TO ai_user;

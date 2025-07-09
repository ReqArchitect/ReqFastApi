#!/usr/bin/env python3
"""
Database seeding script for ReqArchitect microservices
"""

import psycopg2
import json
from datetime import datetime, timedelta
from passlib.hash import bcrypt

# Database configurations for each service
DB_CONFIGS = {
    "auth_service": {
        "host": "localhost",
        "port": 5432,
        "user": "auth_user",
        "password": "auth_pass",
        "database": "auth_db"
    },
    "billing_service": {
        "host": "localhost",
        "port": 5432,
        "user": "billing_user",
        "password": "billing_pass",
        "database": "billing_db"
    },
    "ai_modeling_service": {
        "host": "localhost",
        "port": 5432,
        "user": "ai_user",
        "password": "ai_pass",
        "database": "ai_modeling_db"
    }
}

# Test data
TEST_DATA = {
    "tenant_id": "test-tenant-123",
    "user_id": "test-user-456",
    "email": "test@example.com",
    "password": "testpass123",
    "role": "Admin"
}

def connect_to_db(service_name):
    """Connect to the database for a specific service"""
    try:
        conn = psycopg2.connect(**DB_CONFIGS[service_name])
        return conn
    except Exception as e:
        print(f"❌ Database connection failed for {service_name}: {e}")
        return None

def seed_auth_service():
    """Seed auth_service database with test user"""
    print("🔐 Seeding auth_service database...")
    
    conn = connect_to_db("auth_service")
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Hash the password
        hashed_password = bcrypt.hash(TEST_DATA["password"])
        
        # Check if user already exists
        cursor.execute(
            "SELECT user_id FROM \"user\" WHERE email = %s",
            (TEST_DATA["email"],)
        )
        
        if cursor.fetchone():
            print("✅ Test user already exists")
            return True
        
        # Insert test user
        cursor.execute("""
            INSERT INTO "user" (user_id, email, hashed_password, role, tenant_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            TEST_DATA["user_id"],
            TEST_DATA["email"],
            hashed_password,
            TEST_DATA["role"],
            TEST_DATA["tenant_id"]
        ))
        
        conn.commit()
        print("✅ Test user created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed auth_service: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def seed_billing_service():
    """Seed billing_service database with test data"""
    print("💰 Seeding billing_service database...")
    
    conn = connect_to_db("billing_service")
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create test subscription plan
        plan_limits = {
            "api_calls": 1000,
            "storage_gb": 10,
            "users": 5
        }
        
        cursor.execute("""
            INSERT INTO subscription_plan (plan_id, name, limits, price_per_month)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (plan_id) DO NOTHING
        """, (
            "basic-plan",
            "Basic Plan",
            json.dumps(plan_limits),
            29.99
        ))
        
        # Create test billing profile
        trial_expiry = datetime.utcnow() + timedelta(days=30)
        
        cursor.execute("""
            INSERT INTO tenant_billing_profile 
            (tenant_id, plan_id, billing_email, payment_method, trial_expiry, active)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (tenant_id) DO NOTHING
        """, (
            TEST_DATA["tenant_id"],
            "basic-plan",
            "billing@test-tenant.com",
            "card_123456789",
            trial_expiry,
            True
        ))
        
        conn.commit()
        print("✅ Test billing data created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed billing_service: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def seed_ai_modeling_service():
    """Seed ai_modeling_service database with test data"""
    print("🤖 Seeding ai_modeling_service database...")
    
    conn = connect_to_db("ai_modeling_service")
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create test modeling input
        cursor.execute("""
            INSERT INTO modeling_input 
            (tenant_id, user_id, input_type, input_text, created_at)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (
            TEST_DATA["tenant_id"],
            TEST_DATA["user_id"],
            "goal",
            "Optimize supply chain efficiency",
            datetime.utcnow()
        ))
        
        conn.commit()
        print("✅ Test AI modeling data created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to seed ai_modeling_service: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def main():
    """Main seeding function"""
    print("🚀 Starting database seeding...")
    print("=" * 50)
    
    # Seed auth service
    auth_success = seed_auth_service()
    
    # Seed billing service
    billing_success = seed_billing_service()
    
    # Seed AI modeling service
    ai_success = seed_ai_modeling_service()
    
    print("\n" + "=" * 50)
    print("SEEDING RESULTS")
    print("=" * 50)
    print(f"Auth Service: {'✅ Success' if auth_success else '❌ Failed'}")
    print(f"Billing Service: {'✅ Success' if billing_success else '❌ Failed'}")
    print(f"AI Modeling Service: {'✅ Success' if ai_success else '❌ Failed'}")
    
    if all([auth_success, billing_success, ai_success]):
        print("\n🎉 All services seeded successfully!")
        print("You can now run the validation tests.")
    else:
        print("\n⚠️ Some services failed to seed. Check the errors above.")

if __name__ == "__main__":
    main() 
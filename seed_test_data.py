#!/usr/bin/env python3
"""
Seed test data for ReqArchitect microservices validation
"""

import requests
import json
import uuid
from datetime import datetime, timedelta
from passlib.hash import bcrypt

# Test data configuration
TEST_DATA = {
    "tenant_id": "test-tenant-123",
    "user_id": "test-user-456",
    "email": "test@example.com",
    "password": "testpass123",
    "role": "Admin"
}

def seed_auth_service():
    """Seed test user in auth_service"""
    print("🔐 Seeding auth_service with test user...")
    
    # Hash the password
    hashed_password = bcrypt.hash(TEST_DATA["password"])
    
    # Create test user data
    user_data = {
        "user_id": TEST_DATA["user_id"],
        "email": TEST_DATA["email"],
        "hashed_password": hashed_password,
        "role": TEST_DATA["role"],
        "tenant_id": TEST_DATA["tenant_id"]
    }
    
    # Note: Since auth_service doesn't have a user creation endpoint,
    # we'll need to add one or use direct database insertion
    # For now, let's test the login with the existing user
    
    # Test login with the test credentials
    login_data = {
        "email": TEST_DATA["email"],
        "password": TEST_DATA["password"],
        "role": TEST_DATA["role"],
        "tenant_id": TEST_DATA["tenant_id"]
    }
    
    try:
        response = requests.post("http://localhost:8001/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            print("✅ Login successful with test credentials")
            return True
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False

def seed_billing_service():
    """Seed test billing profile in billing_service"""
    print("💰 Seeding billing_service with test profile...")
    
    # Create test subscription plan
    plan_data = {
        "plan_id": "basic-plan",
        "name": "Basic Plan",
        "limits": {
            "api_calls": 1000,
            "storage_gb": 10,
            "users": 5
        },
        "price_per_month": 29.99
    }
    
    # Create test billing profile
    profile_data = {
        "tenant_id": TEST_DATA["tenant_id"],
        "plan_id": "basic-plan",
        "billing_email": "billing@test-tenant.com",
        "payment_method": "card_123456789",
        "trial_expiry": (datetime.utcnow() + timedelta(days=30)).isoformat(),
        "active": True
    }
    
    # Note: Since billing_service doesn't have creation endpoints,
    # we'll test the existing endpoints and see what data is available
    
    try:
        # Test getting plans
        response = requests.get("http://localhost:8010/billing/plans", timeout=10)
        if response.status_code == 200:
            plans = response.json()
            print(f"✅ Found {len(plans)} existing plans")
        else:
            print(f"❌ Failed to get plans: {response.status_code}")
            
        # Test getting billing profile
        response = requests.get(f"http://localhost:8010/billing/tenant/{TEST_DATA['tenant_id']}", timeout=10)
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Found existing billing profile for tenant")
            return True
        else:
            print(f"❌ No billing profile found for tenant (expected): {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Billing service error: {str(e)}")
        return False

def test_ai_modeling_service():
    """Test AI modeling service endpoints"""
    print("🤖 Testing AI modeling service...")
    
    # Test data for AI modeling
    modeling_data = {
        "tenant_id": TEST_DATA["tenant_id"],
        "user_id": TEST_DATA["user_id"],
        "input_type": "goal",
        "input_text": "Optimize supply chain efficiency"
    }
    
    headers = {
        "X-Tenant-ID": TEST_DATA["tenant_id"],
        "X-User-ID": TEST_DATA["user_id"]
    }
    
    try:
        # Test generate endpoint
        response = requests.post(
            "http://localhost:8002/ai_modeling/generate", 
            json=modeling_data, 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ AI modeling generation successful: {result}")
        else:
            print(f"❌ AI modeling generation failed: {response.status_code} - {response.text}")
            
        # Test history endpoint
        response = requests.get(
            f"http://localhost:8002/ai_modeling/history/{TEST_DATA['user_id']}", 
            headers=headers, 
            timeout=10
        )
        
        if response.status_code == 200:
            history = response.json()
            print(f"✅ AI modeling history retrieved: {len(history)} items")
        else:
            print(f"❌ AI modeling history failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ AI modeling service error: {str(e)}")

def test_invoice_service():
    """Test invoice service endpoints"""
    print("🧾 Testing invoice service...")
    
    try:
        # Test list invoices
        response = requests.get(f"http://localhost:8011/invoices/{TEST_DATA['tenant_id']}", timeout=10)
        if response.status_code == 200:
            invoices = response.json()
            print(f"✅ Invoice list retrieved: {len(invoices)} invoices")
        else:
            print(f"❌ Invoice list failed: {response.status_code}")
            
        # Test generate invoice (should return 501)
        response = requests.post(f"http://localhost:8011/invoices/generate/{TEST_DATA['tenant_id']}", timeout=10)
        if response.status_code == 501:
            print("✅ Invoice generation correctly returns 501 (Not Implemented)")
        else:
            print(f"⚠️ Invoice generation returned {response.status_code} instead of 501")
            
    except Exception as e:
        print(f"❌ Invoice service error: {str(e)}")

def main():
    """Main function to seed and test data"""
    print("🚀 Starting test data seeding and validation...")
    print("=" * 60)
    
    # Seed auth service
    auth_success = seed_auth_service()
    
    # Seed billing service
    billing_success = seed_billing_service()
    
    # Test AI modeling service
    test_ai_modeling_service()
    
    # Test invoice service
    test_invoice_service()
    
    print("\n" + "=" * 60)
    print("SEEDING SUMMARY")
    print("=" * 60)
    print(f"Auth Service: {'✅ Success' if auth_success else '❌ Failed'}")
    print(f"Billing Service: {'✅ Success' if billing_success else '❌ Failed'}")
    print("\nNext steps:")
    print("1. If auth login failed, check if test user exists in database")
    print("2. If billing profile not found, create one via database")
    print("3. Check AI modeling service logs for 500 error details")
    print("4. Consider implementing invoice generation stub")

if __name__ == "__main__":
    main() 
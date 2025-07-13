#!/usr/bin/env python3
"""
Simple JWT Token Generator for Gateway Service Testing
"""

import jwt
import datetime

# JWT configuration (matching gateway service)
SECRET_KEY = "REPLACE_WITH_REAL_SECRET"
ALGORITHM = "HS256"

def create_test_jwt():
    """Create a test JWT token for gateway service testing"""
    
    # Token payload
    payload = {
        "user_id": "550e8400-e29b-41d4-a716-446655440002",
        "tenant_id": "550e8400-e29b-41d4-a716-446655440001", 
        "role": "Admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        "iat": datetime.datetime.utcnow(),
        "sub": "test-user"
    }
    
    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    print("🔑 Test JWT Token Generated:")
    print("=" * 50)
    print(f"Token: {token}")
    print("=" * 50)
    print()
    print("📋 Usage:")
    print(f'Invoke-WebRequest -Uri "http://localhost:8080/services" -Headers @{{"Authorization"="Bearer {token}"; "Content-Type"="application/json"}} -Method GET')
    print()
    print("🔍 Token Details:")
    print(f"User ID: {payload['user_id']}")
    print(f"Tenant ID: {payload['tenant_id']}")
    print(f"Role: {payload['role']}")
    print(f"Expires: {payload['exp']}")
    
    return token

if __name__ == "__main__":
    create_test_jwt() 
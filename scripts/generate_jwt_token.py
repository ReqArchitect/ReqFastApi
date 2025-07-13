#!/usr/bin/env python3
"""
JWT Token Generator for ReqArchitect Gateway Testing
Generates valid JWT tokens for testing authentication flows
"""

import jwt
import uuid
from datetime import datetime, timedelta
import json

# JWT Configuration (matching auth_service)
SECRET_KEY = "your-super-secret-key-change-this-in-production"  # Match auth_service actual secret
ALGORITHM = "HS256"

def generate_test_token():
    """Generate a valid JWT token for testing"""
    
    # Test user data
    tenant_id = str(uuid.uuid4())
    user_id = str(uuid.uuid4())
    
    # Token payload
    payload = {
        "tenant_id": tenant_id,
        "user_id": user_id,
        "role": "Admin",  # Admin role for full access
        "email": "test@reqarchitect.com",
        "exp": datetime.utcnow() + timedelta(hours=24),  # 24 hour expiry
        "iat": datetime.utcnow(),
        "sub": user_id
    }
    
    # Generate token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "token": token,
        "payload": payload,
        "tenant_id": tenant_id,
        "user_id": user_id
    }

def main():
    """Main function to generate and display token"""
    print("🔐 Generating JWT Token for Gateway Testing")
    print("=" * 50)
    
    result = generate_test_token()
    
    print(f"✅ Token Generated Successfully")
    print(f"📋 Tenant ID: {result['tenant_id']}")
    print(f"👤 User ID: {result['user_id']}")
    print(f"🔑 Role: {result['payload']['role']}")
    print(f"⏰ Expires: {result['payload']['exp']}")
    print()
    print("🔑 JWT Token:")
    print(result['token'])
    print()
    print("📝 PowerShell Variable:")
    print(f'$Token = "{result["token"]}"')
    print()
    print("🧪 Test Commands:")
    print(f'Invoke-RestMethod -Uri "http://localhost:8080/gateway/auth/user" -Headers @{{"Authorization"="Bearer $Token"}}')
    print(f'Invoke-RestMethod -Uri "http://localhost:8080/gateway/analytics/kpis" -Headers @{{"Authorization"="Bearer $Token"}}')
    print(f'Invoke-RestMethod -Uri "http://localhost:8080/gateway/health"')

if __name__ == "__main__":
    main() 
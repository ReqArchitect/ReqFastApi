#!/usr/bin/env python3
"""
Fix dependencies by adding PyJWT to all service requirements files
"""

import os
from pathlib import Path

# Target services
SERVICES = [
    'auth_service',
    'usage_service', 
    'billing_service',
    'invoice_service',
    'notification_service',
    'audit_log_service',
    'ai_modeling_service'
]

def add_pyjwt_to_requirements(service_name):
    """Add PyJWT to a service's requirements.txt file"""
    requirements_file = Path(f"services/{service_name}/requirements.txt")
    
    if not requirements_file.exists():
        print(f"❌ requirements.txt not found for {service_name}")
        return False
    
    with open(requirements_file, 'r') as f:
        content = f.read()
    
    # Check if PyJWT is already present
    if 'PyJWT' in content:
        print(f"✅ PyJWT already present in {service_name}")
        return True
    
    # Add PyJWT after uvicorn
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        if line.strip().startswith('uvicorn['):
            new_lines.append('PyJWT>=2.8,<3.0')
    
    # Write back to file
    with open(requirements_file, 'w') as f:
        f.write('\n'.join(new_lines))
    
    print(f"✅ Added PyJWT to {service_name}")
    return True

def main():
    """Add PyJWT to all service requirements files"""
    print("🔧 Adding PyJWT to all service requirements files...")
    
    for service in SERVICES:
        add_pyjwt_to_requirements(service)
    
    print("\n🎉 Dependencies fixed!")
    print("\nNext steps:")
    print("1. Rebuild containers: docker-compose build")
    print("2. Restart services: docker-compose up -d")
    print("3. Test health endpoints")

if __name__ == "__main__":
    main() 
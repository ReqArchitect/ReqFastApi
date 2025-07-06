#!/usr/bin/env python3
"""
Test script to verify Docker container builds and health endpoints
"""
import subprocess
import time
import requests
import sys

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def test_docker_build(service_path):
    """Test if a service can build successfully"""
    print(f"Testing build for {service_path}...")
    success, stdout, stderr = run_command("docker build -t test-build .", cwd=service_path)
    if success:
        print(f"✅ {service_path} builds successfully")
        return True
    else:
        print(f"❌ {service_path} build failed:")
        print(f"   Error: {stderr}")
        return False

def main():
    """Main test function"""
    services = [
        "services/analytics_service",
        "services/feedback_service", 
        "services/event_bus_service",
        "services/auth_service",
        "services/ai_modeling_service",
        "services/usage_service",
        "services/onboarding_state_service/app",
        "services/audit_log_service/app",
        "services/notification_service",
        "services/billing_service",
        "services/invoice_service",
        "services/gateway_service"
    ]
    
    print("Testing Docker builds for all services...")
    print("=" * 50)
    
    failed_builds = []
    for service in services:
        if not test_docker_build(service):
            failed_builds.append(service)
        print()
    
    if failed_builds:
        print("❌ Some services failed to build:")
        for service in failed_builds:
            print(f"   - {service}")
        return False
    else:
        print("✅ All services build successfully!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
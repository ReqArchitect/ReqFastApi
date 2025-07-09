#!/usr/bin/env python3
"""
ReqArchitect Microservices Validation Runner

This script starts the required services using docker-compose and then runs
the comprehensive validation tests.
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def run_command(cmd, cwd=None, capture_output=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=capture_output, 
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_docker():
    """Check if Docker is available"""
    print("🔍 Checking Docker availability...")
    success, stdout, stderr = run_command("docker --version")
    if success:
        print(f"✅ Docker found: {stdout.strip()}")
        return True
    else:
        print("❌ Docker not found or not accessible")
        return False

def check_docker_compose():
    """Check if docker-compose is available"""
    print("🔍 Checking Docker Compose availability...")
    success, stdout, stderr = run_command("docker-compose --version")
    if success:
        print(f"✅ Docker Compose found: {stdout.strip()}")
        return True
    else:
        print("❌ Docker Compose not found or not accessible")
        return False

def start_services():
    """Start the required services using docker-compose"""
    print("\n🚀 Starting ReqArchitect services...")
    
    # Check if services are already running
    success, stdout, stderr = run_command("docker-compose ps")
    if success and "Up" in stdout:
        print("✅ Services are already running")
        return True
    
    # Start services
    print("📦 Starting services with docker-compose up -d...")
    success, stdout, stderr = run_command("docker-compose up -d")
    
    if success:
        print("✅ Services started successfully")
        return True
    else:
        print(f"❌ Failed to start services: {stderr}")
        return False

def wait_for_services():
    """Wait for services to be ready"""
    print("\n⏳ Waiting for services to be ready...")
    
    services_to_check = [
        ("auth_service", "http://localhost:8001/health"),
        ("usage_service", "http://localhost:8000/health"),
        ("billing_service", "http://localhost:8010/health"),
        ("invoice_service", "http://localhost:8011/health"),
        ("notification_service", "http://localhost:8000/health"),
        ("audit_log_service", "http://localhost:8000/health"),
        ("ai_modeling_service", "http://localhost:8002/health")
    ]
    
    import requests
    
    max_wait_time = 120  # 2 minutes
    start_time = time.time()
    
    while time.time() - start_time < max_wait_time:
        all_ready = True
        
        for service_name, health_url in services_to_check:
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print(f"✅ {service_name} is ready")
                else:
                    print(f"⏳ {service_name} not ready yet (status: {response.status_code})")
                    all_ready = False
            except requests.exceptions.RequestException:
                print(f"⏳ {service_name} not ready yet (connection failed)")
                all_ready = False
        
        if all_ready:
            print("🎉 All services are ready!")
            return True
        
        print("Waiting 10 seconds before next check...")
        time.sleep(10)
    
    print("❌ Timeout waiting for services to be ready")
    return False

def run_validation_tests():
    """Run the validation tests"""
    print("\n🧪 Running validation tests...")
    
    success, stdout, stderr = run_command("python test_microservices.py")
    
    if success:
        print("✅ Validation tests completed successfully")
        return True
    else:
        print(f"❌ Validation tests failed: {stderr}")
        return False

def stop_services():
    """Stop the services"""
    print("\n🛑 Stopping services...")
    
    success, stdout, stderr = run_command("docker-compose down")
    
    if success:
        print("✅ Services stopped successfully")
    else:
        print(f"❌ Failed to stop services: {stderr}")

def main():
    """Main function"""
    print("=" * 60)
    print("ReqArchitect Microservices Validation")
    print("=" * 60)
    
    # Check prerequisites
    if not check_docker():
        print("❌ Docker is required but not available")
        sys.exit(1)
    
    if not check_docker_compose():
        print("❌ Docker Compose is required but not available")
        sys.exit(1)
    
    # Check if test script exists
    if not Path("test_microservices.py").exists():
        print("❌ test_microservices.py not found")
        sys.exit(1)
    
    try:
        # Start services
        if not start_services():
            print("❌ Failed to start services")
            sys.exit(1)
        
        # Wait for services to be ready
        if not wait_for_services():
            print("❌ Services failed to start properly")
            sys.exit(1)
        
        # Run validation tests
        if not run_validation_tests():
            print("❌ Validation tests failed")
            sys.exit(1)
        
        print("\n🎉 Validation completed successfully!")
        print("📄 Check microservices_validation_report.md for detailed results")
        
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Validation failed with error: {str(e)}")
        sys.exit(1)
    finally:
        # Ask user if they want to stop services
        response = input("\nDo you want to stop the services? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            stop_services()

if __name__ == "__main__":
    main() 
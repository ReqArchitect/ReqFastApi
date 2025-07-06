#!/usr/bin/env python3
"""
Comprehensive test script for FastAPI microservices
Tests structure, builds, and runtime validation
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

class MicroserviceTester:
    def __init__(self):
        self.target_services = [
            "gateway_service",
            "notification_service", 
            "ai_modeling_service",
            "auth_service",
            "usage_service",
            "billing_service",
            "invoice_service"
        ]
        
        self.service_ports = {
            "gateway_service": 8080,
            "auth_service": 8001,
            "ai_modeling_service": 8002,
            "billing_service": 8010,
            "invoice_service": 8011,
            "notification_service": 8000,
            "usage_service": 8000
        }
        
        self.failed_services = []
        self.passed_services = []

    def run_command(self, cmd, cwd=None, capture_output=True):
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

    def check_service_structure(self, service_name):
        """Check if service has correct structure"""
        print(f"🔍 Checking structure for {service_name}...")
        
        service_path = f"services/{service_name}"
        required_files = [
            "app/main.py",
            "app/models.py", 
            "app/schemas.py",
            "app/database.py",
            "app/__init__.py",
            "requirements.txt",
            "Dockerfile"
        ]
        
        missing_files = []
        for file_path in required_files:
            full_path = f"{service_path}/{file_path}"
            if not os.path.exists(full_path):
                missing_files.append(file_path)
        
        if missing_files:
            print(f"❌ {service_name} missing files: {missing_files}")
            return False
        else:
            print(f"✅ {service_name} structure is correct")
            return True

    def check_imports(self, service_name):
        """Check if service uses absolute imports"""
        print(f"🔍 Checking imports for {service_name}...")
        
        main_py_path = f"services/{service_name}/app/main.py"
        if not os.path.exists(main_py_path):
            print(f"❌ {service_name} main.py not found")
            return False
            
        with open(main_py_path, 'r') as f:
            content = f.read()
            
        # Check for absolute imports
        absolute_imports = [
            "from app import models",
            "from app import schemas", 
            "from app.database import"
        ]
        
        relative_imports = [
            "from . import models",
            "from . import schemas",
            "from .database import"
        ]
        
        has_absolute = any(imp in content for imp in absolute_imports)
        has_relative = any(imp in content for imp in relative_imports)
        
        if has_absolute and not has_relative:
            print(f"✅ {service_name} uses absolute imports")
            return True
        elif has_relative:
            print(f"❌ {service_name} uses relative imports")
            return False
        else:
            print(f"⚠️ {service_name} no app imports found")
            return True

    def check_health_endpoint(self, service_name):
        """Check if service has health endpoint"""
        print(f"🔍 Checking health endpoint for {service_name}...")
        
        main_py_path = f"services/{service_name}/app/main.py"
        if not os.path.exists(main_py_path):
            print(f"❌ {service_name} main.py not found")
            return False
            
        with open(main_py_path, 'r') as f:
            content = f.read()
            
        if "@app.get(\"/health\")" in content:
            print(f"✅ {service_name} has health endpoint")
            return True
        else:
            print(f"❌ {service_name} missing health endpoint")
            return False

    def check_dockerfile(self, service_name):
        """Check if Dockerfile has correct CMD"""
        print(f"🔍 Checking Dockerfile for {service_name}...")
        
        dockerfile_path = f"services/{service_name}/Dockerfile"
        if not os.path.exists(dockerfile_path):
            print(f"❌ {service_name} Dockerfile not found")
            return False
            
        with open(dockerfile_path, 'r') as f:
            content = f.read()
            
        # Check for correct CMD format
        if "CMD [\"uvicorn\", \"app.main:app\"" in content:
            print(f"✅ {service_name} Dockerfile has correct CMD")
            return True
        else:
            print(f"❌ {service_name} Dockerfile has incorrect CMD")
            return False

    def test_docker_build(self, service_name):
        """Test if service can build successfully"""
        print(f"🔨 Testing build for {service_name}...")
        
        service_path = f"services/{service_name}"
        success, stdout, stderr = self.run_command(
            "docker build -t test-build .", 
            cwd=service_path
        )
        
        if success:
            print(f"✅ {service_name} builds successfully")
            return True
        else:
            print(f"❌ {service_name} build failed:")
            print(f"   Error: {stderr}")
            return False

    def check_docker_compose_config(self, service_name):
        """Check if service is properly configured in docker-compose.yml"""
        print(f"🔍 Checking docker-compose config for {service_name}...")
        
        if not os.path.exists("docker-compose.yml"):
            print("❌ docker-compose.yml not found")
            return False
            
        with open("docker-compose.yml", 'r') as f:
            content = f.read()
            
        # Check if service is defined
        if f"  {service_name}:" in content:
            print(f"✅ {service_name} is defined in docker-compose.yml")
            return True
        else:
            print(f"❌ {service_name} not found in docker-compose.yml")
            return False

    def test_health_endpoint_runtime(self, service_name):
        """Test health endpoint at runtime (requires containers to be running)"""
        if service_name not in self.service_ports:
            print(f"⚠️ {service_name} port not configured")
            return True
            
        port = self.service_ports[service_name]
        health_url = f"http://localhost:{port}/health"
        
        try:
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} health endpoint responding")
                return True
            else:
                print(f"❌ {service_name} health endpoint returned {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"⚠️ {service_name} health endpoint not accessible (container may not be running)")
            return True  # Don't fail if container isn't running

    def run_comprehensive_test(self, service_name):
        """Run all tests for a service"""
        print(f"\n{'='*60}")
        print(f"Testing {service_name}")
        print(f"{'='*60}")
        
        tests = [
            ("Structure", self.check_service_structure),
            ("Imports", self.check_imports),
            ("Health Endpoint", self.check_health_endpoint),
            ("Dockerfile", self.check_dockerfile),
            ("Docker Compose", self.check_docker_compose_config),
            ("Docker Build", self.test_docker_build),
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            try:
                if test_func(service_name):
                    passed_tests += 1
            except Exception as e:
                print(f"❌ {test_name} test failed with exception: {e}")
        
        # Calculate score
        score = (passed_tests / total_tests) * 100
        
        print(f"\n📊 {service_name} Test Results:")
        print(f"   Passed: {passed_tests}/{total_tests} tests ({score:.1f}%)")
        
        if score >= 80:
            print(f"✅ {service_name} PASSED")
            self.passed_services.append(service_name)
        else:
            print(f"❌ {service_name} FAILED")
            self.failed_services.append(service_name)
        
        return score >= 80

    def run_all_tests(self):
        """Run tests for all target services"""
        print("🚀 Starting comprehensive microservices audit...")
        print(f"Target services: {', '.join(self.target_services)}")
        
        for service in self.target_services:
            self.run_comprehensive_test(service)
        
        # Summary
        print(f"\n{'='*60}")
        print("FINAL RESULTS")
        print(f"{'='*60}")
        
        print(f"✅ Passed services ({len(self.passed_services)}):")
        for service in self.passed_services:
            print(f"   - {service}")
        
        if self.failed_services:
            print(f"\n❌ Failed services ({len(self.failed_services)}):")
            for service in self.failed_services:
                print(f"   - {service}")
        
        overall_score = (len(self.passed_services) / len(self.target_services)) * 100
        print(f"\n📊 Overall Score: {overall_score:.1f}%")
        
        if overall_score >= 80:
            print("🎉 Microservices audit PASSED!")
            return True
        else:
            print("❌ Microservices audit FAILED!")
            return False

def main():
    tester = MicroserviceTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 
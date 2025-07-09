#!/usr/bin/env python3
"""
Comprehensive Microservices Validation Script
Tests all ReqArchitect platform services systematically
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Test data configuration
TEST_DATA = {
    "tenant_id": "test-tenant-123",
    "user_id": "test-user-456", 
    "email": "test@example.com",
    "password": "testpass123",
    "role": "Admin"
}

# Service configurations
SERVICES = {
    "gateway_service": {
        "port": 8080,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/api/v1/health", "GET")
        ]
    },
    "auth_service": {
        "port": 8001,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/auth/login", "POST"),
            ("/auth/roles", "GET")
        ]
    },
    "ai_modeling_service": {
        "port": 8002,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/ai_modeling/generate", "POST"),
            ("/ai_modeling/history/{user_id}", "GET")
        ]
    },
    "usage_service": {
        "port": 8005,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/usage/tenant/{tenant_id}", "GET"),
            ("/usage/user/{user_id}", "GET")
        ]
    },
    "notification_service": {
        "port": 8006,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/notification/send", "POST")
        ]
    },
    "audit_log_service": {
        "port": 8007,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/audit_log/query", "GET")
        ]
    },
    "billing_service": {
        "port": 8010,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/billing/tenant/{tenant_id}", "GET"),
            ("/billing/plans", "GET"),
            ("/billing/usage_report", "GET")
        ]
    },
    "invoice_service": {
        "port": 8011,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/invoices/{tenant_id}", "GET"),
            ("/invoices/generate/{tenant_id}", "POST")
        ]
    },
    "monitoring_dashboard_service": {
        "port": 8012,
        "endpoints": [
            ("/health", "GET"),
            ("/metrics", "GET"),
            ("/dashboard", "GET")
        ]
    }
}

class MicroservicesValidator:
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        
    def test_endpoint(self, service_name: str, endpoint: str, method: str, 
                     data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict:
        """Test a single endpoint and return results"""
        port = SERVICES[service_name]["port"]
        url = f"http://localhost:{port}{endpoint}"
        
        # Replace placeholders in endpoint
        if "{tenant_id}" in endpoint:
            endpoint = endpoint.replace("{tenant_id}", TEST_DATA["tenant_id"])
        if "{user_id}" in endpoint:
            endpoint = endpoint.replace("{user_id}", TEST_DATA["user_id"])
            url = f"http://localhost:{port}{endpoint}"
        
        start_time = time.time()
        
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=10)
            elif method == "PUT":
                response = requests.put(url, json=data, headers=headers, timeout=10)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                return {
                    "service": service_name,
                    "endpoint": endpoint,
                    "method": method,
                    "status_code": None,
                    "response_time": None,
                    "success": False,
                    "error": f"Unsupported method: {method}"
                }
            
            response_time = round((time.time() - start_time) * 1000, 2)  # ms
            
            # Determine if this is a success
            success = response.status_code in [200, 201, 202, 204]
            
            # Parse response body
            try:
                response_body = response.json() if response.content else None
            except:
                response_body = response.text if response.content else None
            
            return {
                "service": service_name,
                "endpoint": endpoint,
                "method": method,
                "status_code": response.status_code,
                "response_time": response_time,
                "success": success,
                "response_body": response_body,
                "error": None
            }
            
        except requests.exceptions.ConnectionError:
            return {
                "service": service_name,
                "endpoint": endpoint,
                "method": method,
                "status_code": None,
                "response_time": None,
                "success": False,
                "error": "Connection refused"
            }
        except requests.exceptions.Timeout:
            return {
                "service": service_name,
                "endpoint": endpoint,
                "method": method,
                "status_code": None,
                "response_time": None,
                "success": False,
                "error": "Request timeout"
            }
        except Exception as e:
            return {
                "service": service_name,
                "endpoint": endpoint,
                "method": method,
                "status_code": None,
                "response_time": None,
                "success": False,
                "error": str(e)
            }
    
    def test_auth_login(self) -> Dict:
        """Test auth login with test credentials"""
        login_data = {
            "email": TEST_DATA["email"],
            "password": TEST_DATA["password"],
            "tenant_id": TEST_DATA["tenant_id"]
        }
        
        return self.test_endpoint("auth_service", "/auth/login", "POST", data=login_data)
    
    def test_ai_modeling_generate(self) -> Dict:
        """Test AI modeling generation"""
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
        
        return self.test_endpoint("ai_modeling_service", "/ai_modeling/generate", "POST", 
                                data=modeling_data, headers=headers)
    
    def test_invoice_generate(self) -> Dict:
        """Test invoice generation"""
        return self.test_endpoint("invoice_service", f"/invoices/generate/{TEST_DATA['tenant_id']}", "POST")
    
    def test_notification_send(self) -> Dict:
        """Test notification sending"""
        notification_data = {
            "tenant_id": TEST_DATA["tenant_id"],
            "user_id": TEST_DATA["user_id"],
            "type": "email",
            "subject": "Test Notification",
            "message": "This is a test notification",
            "recipient": "test@example.com"
        }
        
        return self.test_endpoint("notification_service", "/notification/send", "POST", data=notification_data)
    
    def test_audit_log_query(self) -> Dict:
        """Test audit log query"""
        return self.test_endpoint("audit_log_service", f"/audit_log/query?tenant_id={TEST_DATA['tenant_id']}", "GET")
    
    def run_comprehensive_validation(self):
        """Run comprehensive validation of all services"""
        print("🚀 Starting comprehensive microservices validation...")
        print("=" * 80)
        
        # Test all basic endpoints (health, metrics)
        for service_name, config in SERVICES.items():
            print(f"\n🔍 Testing {service_name}...")
            
            for endpoint, method in config["endpoints"]:
                result = self.test_endpoint(service_name, endpoint, method)
                self.results.append(result)
                
                status_icon = "✅" if result["success"] else "❌"
                print(f"  {status_icon} {method} {endpoint}: {result['status_code']} ({result['response_time']}ms)")
                
                if result["error"]:
                    print(f"    Error: {result['error']}")
        
        # Test specific API functionality
        print(f"\n🔍 Testing API functionality with seeded data...")
        
        # Auth login
        auth_result = self.test_auth_login()
        self.results.append(auth_result)
        print(f"  {'✅' if auth_result['success'] else '❌'} POST /auth/login: {auth_result['status_code']}")
        
        # AI modeling
        ai_result = self.test_ai_modeling_generate()
        self.results.append(ai_result)
        print(f"  {'✅' if ai_result['success'] else '❌'} POST /ai_modeling/generate: {ai_result['status_code']}")
        
        # Invoice generation
        invoice_result = self.test_invoice_generate()
        self.results.append(invoice_result)
        print(f"  {'✅' if invoice_result['success'] else '❌'} POST /invoices/generate: {invoice_result['status_code']}")
        
        # Notification
        notification_result = self.test_notification_send()
        self.results.append(notification_result)
        print(f"  {'✅' if notification_result['success'] else '❌'} POST /notification/send: {notification_result['status_code']}")
        
        # Audit log
        audit_result = self.test_audit_log_query()
        self.results.append(audit_result)
        print(f"  {'✅' if audit_result['success'] else '❌'} GET /audit_log/query: {audit_result['status_code']}")
        
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "=" * 80)
        print("📊 VALIDATION SUMMARY")
        print("=" * 80)
        
        # Group results by service
        service_results = {}
        for result in self.results:
            service = result["service"]
            if service not in service_results:
                service_results[service] = []
            service_results[service].append(result)
        
        # Calculate statistics
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - successful_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(successful_tests/total_tests*100):.1f}%")
        
        # Service-by-service breakdown
        print("\n📋 DETAILED RESULTS")
        print("-" * 80)
        
        for service_name, results in service_results.items():
            service_success = sum(1 for r in results if r["success"])
            service_total = len(results)
            service_rate = (service_success/service_total*100) if service_total > 0 else 0
            
            print(f"\n🔧 {service_name.upper()}")
            print(f"   Success Rate: {service_rate:.1f}% ({service_success}/{service_total})")
            
            for result in results:
                status_icon = "✅" if result["success"] else "❌"
                endpoint_name = result["endpoint"].split("/")[-1] if result["endpoint"] else "unknown"
                print(f"   {status_icon} {result['method']} {result['endpoint']}: {result['status_code']} ({result['response_time']}ms)")
                
                if result["error"]:
                    print(f"      Error: {result['error']}")
        
        # Create summary table
        self.create_summary_table()
        
        # Save detailed results
        self.save_detailed_results()
    
    def create_summary_table(self):
        """Create a summary table in markdown format"""
        print("\n📋 SUMMARY TABLE")
        print("-" * 80)
        print("| Service | Endpoint | Status Code | Response Time | Working |")
        print("|---------|----------|-------------|---------------|---------|")
        
        for result in self.results:
            service = result["service"]
            endpoint = result["endpoint"]
            status_code = result["status_code"] or "N/A"
            response_time = f"{result['response_time']}ms" if result["response_time"] else "N/A"
            working = "✅" if result["success"] else "❌"
            
            print(f"| {service} | {endpoint} | {status_code} | {response_time} | {working} |")
    
    def save_detailed_results(self):
        """Save detailed results to JSON file"""
        report_data = {
            "timestamp": self.start_time.isoformat(),
            "test_data": TEST_DATA,
            "results": self.results,
            "summary": {
                "total_tests": len(self.results),
                "successful_tests": sum(1 for r in self.results if r["success"]),
                "failed_tests": sum(1 for r in self.results if not r["success"])
            }
        }
        
        with open("validation_results.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n💾 Detailed results saved to validation_results.json")

def main():
    """Main function"""
    validator = MicroservicesValidator()
    validator.run_comprehensive_validation()

if __name__ == "__main__":
    main() 
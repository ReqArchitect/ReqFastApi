#!/usr/bin/env python3
"""
ReqArchitect Microservices Validation Script

This script tests the functionality of all FastAPI microservices in the ReqArchitect platform.
It validates endpoints, authentication, response structures, and error handling.
"""

import requests
import json
import time
import sys
from typing import Dict, Any, List
from datetime import datetime, timedelta
import uuid

# Service configurations
SERVICES = {
    "auth_service": {
        "base_url": "http://localhost:8001",
        "port": 8001,
        "endpoints": ["/health", "/metrics", "/auth/login", "/auth/logout", "/auth/me", "/auth/refresh", "/auth/roles"]
    },
    "billing_service": {
        "base_url": "http://localhost:8010",
        "port": 8010,
        "endpoints": ["/health", "/metrics", "/billing/tenant/{tenant_id}", "/billing/usage_report", "/billing/trigger_alerts", "/billing/upgrade_plan", "/billing/plans"]
    },
    "invoice_service": {
        "base_url": "http://localhost:8011",
        "port": 8011,
        "endpoints": ["/health", "/metrics", "/invoices/generate/{tenant_id}", "/invoices/{tenant_id}", "/invoices/{invoice_id}/download", "/invoices/mark_paid/{invoice_id}", "/invoices/stripe/{invoice_id}"]
    },
    "ai_modeling_service": {
        "base_url": "http://localhost:8002",
        "port": 8002,
        "endpoints": ["/health", "/metrics", "/ai_modeling/generate", "/ai_modeling/history/{user_id}", "/ai_modeling/feedback"]
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

class MicroserviceTester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.test_results = {}
        
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def test_health_endpoint(self, service_name: str, base_url: str) -> Dict[str, Any]:
        """Test the health endpoint of a service"""
        self.log(f"Testing health endpoint for {service_name}")
        try:
            response = self.session.get(f"{base_url}/health", timeout=10)
            result = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                health_data = response.json()
                self.log(f"✅ {service_name} health check passed: {health_data.get('status', 'unknown')}")
            else:
                self.log(f"❌ {service_name} health check failed: {response.status_code}")
                
            return result
            
        except requests.exceptions.RequestException as e:
            self.log(f"❌ {service_name} health check error: {str(e)}", "ERROR")
            return {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
    
    def test_metrics_endpoint(self, service_name: str, base_url: str) -> Dict[str, Any]:
        """Test the metrics endpoint of a service"""
        self.log(f"Testing metrics endpoint for {service_name}")
        try:
            response = self.session.get(f"{base_url}/metrics", timeout=10)
            result = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ {service_name} metrics endpoint working")
            else:
                self.log(f"❌ {service_name} metrics endpoint failed: {response.status_code}")
                
            return result
            
        except requests.exceptions.RequestException as e:
            self.log(f"❌ {service_name} metrics error: {str(e)}", "ERROR")
            return {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
    
    def test_auth_service(self, base_url: str) -> Dict[str, Any]:
        """Test authentication service endpoints"""
        self.log("Testing Auth Service endpoints")
        results = {}
        
        # Test login
        login_data = {
            "email": TEST_DATA["email"],
            "password": TEST_DATA["password"],
            "role": TEST_DATA["role"],
            "tenant_id": TEST_DATA["tenant_id"]
        }
        
        try:
            response = self.session.post(f"{base_url}/auth/login", json=login_data, timeout=10)
            results["login"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                auth_data = response.json()
                self.auth_token = auth_data.get("token")
                self.log(f"✅ Login successful, token received")
            else:
                self.log(f"❌ Login failed: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            results["login"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Login error: {str(e)}", "ERROR")
        
        # Test /auth/me with token
        if self.auth_token:
            headers = {"Authorization": f"Bearer {self.auth_token}"}
            try:
                response = self.session.get(f"{base_url}/auth/me", headers=headers, timeout=10)
                results["me"] = {
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "response": response.json() if response.status_code == 200 else None,
                    "error": None
                }
                
                if response.status_code == 200:
                    self.log(f"✅ /auth/me successful")
                else:
                    self.log(f"❌ /auth/me failed: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                results["me"] = {
                    "status_code": None,
                    "success": False,
                    "response": None,
                    "error": str(e)
                }
                self.log(f"❌ /auth/me error: {str(e)}", "ERROR")
        
        # Test /auth/roles
        try:
            response = self.session.get(f"{base_url}/auth/roles", timeout=10)
            results["roles"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ /auth/roles successful")
            else:
                self.log(f"❌ /auth/roles failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["roles"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ /auth/roles error: {str(e)}", "ERROR")
        
        return results
    
    def test_usage_service(self, base_url: str) -> Dict[str, Any]:
        """Test usage service endpoints"""
        self.log("Testing Usage Service endpoints")
        results = {}
        
        # Headers for authentication
        headers = {
            "X-Tenant-ID": TEST_DATA["tenant_id"],
            "X-User-ID": TEST_DATA["user_id"],
            "X-Role": TEST_DATA["role"]
        }
        
        # Test get usage metrics
        try:
            response = self.session.get(
                f"{base_url}/usage/tenant/{TEST_DATA['tenant_id']}", 
                headers=headers, 
                timeout=10
            )
            results["usage_metrics"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Usage metrics retrieved successfully")
            else:
                self.log(f"❌ Usage metrics failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["usage_metrics"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Usage metrics error: {str(e)}", "ERROR")
        
        # Test system health
        try:
            response = self.session.get(f"{base_url}/usage/system_health", headers=headers, timeout=10)
            results["system_health"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ System health retrieved successfully")
            else:
                self.log(f"❌ System health failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["system_health"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ System health error: {str(e)}", "ERROR")
        
        return results
    
    def test_billing_service(self, base_url: str) -> Dict[str, Any]:
        """Test billing service endpoints"""
        self.log("Testing Billing Service endpoints")
        results = {}
        
        # Headers for authentication
        headers = {
            "X-Tenant-ID": TEST_DATA["tenant_id"],
            "X-User-ID": TEST_DATA["user_id"],
            "X-Role": TEST_DATA["role"]
        }
        
        # Test get billing profile
        try:
            response = self.session.get(
                f"{base_url}/billing/tenant/{TEST_DATA['tenant_id']}", 
                headers=headers, 
                timeout=10
            )
            results["billing_profile"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Billing profile retrieved successfully")
            else:
                self.log(f"❌ Billing profile failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["billing_profile"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Billing profile error: {str(e)}", "ERROR")
        
        # Test get plans
        try:
            response = self.session.get(f"{base_url}/billing/plans", timeout=10)
            results["plans"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Billing plans retrieved successfully")
            else:
                self.log(f"❌ Billing plans failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["plans"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Billing plans error: {str(e)}", "ERROR")
        
        # Test usage report
        usage_report_data = {
            "tenant_id": TEST_DATA["tenant_id"],
            "api_calls": 1500,
            "storage_gb": 25.5,
            "users_active": 12
        }
        
        try:
            response = self.session.post(f"{base_url}/billing/usage_report", json=usage_report_data, timeout=10)
            results["usage_report"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Usage report submitted successfully")
            else:
                self.log(f"❌ Usage report failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["usage_report"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Usage report error: {str(e)}", "ERROR")
        
        return results
    
    def test_invoice_service(self, base_url: str) -> Dict[str, Any]:
        """Test invoice service endpoints"""
        self.log("Testing Invoice Service endpoints")
        results = {}
        
        # Test list invoices
        try:
            response = self.session.get(f"{base_url}/invoices/{TEST_DATA['tenant_id']}", timeout=10)
            results["list_invoices"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Invoice list retrieved successfully")
            else:
                self.log(f"❌ Invoice list failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["list_invoices"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Invoice list error: {str(e)}", "ERROR")
        
        # Test generate invoice (this might return 501 as it's not implemented)
        try:
            response = self.session.post(f"{base_url}/invoices/generate/{TEST_DATA['tenant_id']}", timeout=10)
            results["generate_invoice"] = {
                "status_code": response.status_code,
                "success": response.status_code in [200, 201],
                "response": response.json() if response.status_code in [200, 201] else None,
                "error": None
            }
            
            if response.status_code in [200, 201]:
                self.log(f"✅ Invoice generation successful")
            elif response.status_code == 501:
                self.log(f"⚠️ Invoice generation not implemented (expected)")
            else:
                self.log(f"❌ Invoice generation failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["generate_invoice"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Invoice generation error: {str(e)}", "ERROR")
        
        return results
    
    def test_notification_service(self, base_url: str) -> Dict[str, Any]:
        """Test notification service endpoints"""
        self.log("Testing Notification Service endpoints")
        results = {}
        
        # Test send notification
        notification_data = {
            "notification_id": str(uuid.uuid4()),
            "user_id": TEST_DATA["user_id"],
            "tenant_id": TEST_DATA["tenant_id"],
            "channel": "email",
            "message": "Test notification message",
            "event_type": "test_event"
        }
        
        try:
            response = self.session.post(f"{base_url}/notifications/send", json=notification_data, timeout=10)
            results["send_notification"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Notification sent successfully")
            else:
                self.log(f"❌ Notification send failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["send_notification"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Notification send error: {str(e)}", "ERROR")
        
        # Test get user notifications
        try:
            response = self.session.get(f"{base_url}/notifications/user/{TEST_DATA['user_id']}", timeout=10)
            results["user_notifications"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ User notifications retrieved successfully")
            else:
                self.log(f"❌ User notifications failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["user_notifications"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ User notifications error: {str(e)}", "ERROR")
        
        # Test create template
        template_data = {
            "template_id": "test_template",
            "event_type": "test_event",
            "channel": "email",
            "content": "Hello {{user_name}}, this is a test notification."
        }
        
        try:
            response = self.session.post(f"{base_url}/notifications/template", json=template_data, timeout=10)
            results["create_template"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Notification template created successfully")
            else:
                self.log(f"❌ Notification template creation failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["create_template"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Notification template creation error: {str(e)}", "ERROR")
        
        return results
    
    def test_audit_log_service(self, base_url: str) -> Dict[str, Any]:
        """Test audit log service endpoints"""
        self.log("Testing Audit Log Service endpoints")
        results = {}
        
        # Test create audit log
        audit_data = {
            "service": "test_service",
            "event_type": "test_event",
            "payload": {
                "user_id": TEST_DATA["user_id"],
                "tenant_id": TEST_DATA["tenant_id"],
                "action": "test_action"
            }
        }
        
        try:
            response = self.session.post(f"{base_url}/audit/log", json=audit_data, timeout=10)
            results["create_audit_log"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Audit log created successfully")
            else:
                self.log(f"❌ Audit log creation failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["create_audit_log"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Audit log creation error: {str(e)}", "ERROR")
        
        # Test list audit logs
        try:
            response = self.session.get(f"{base_url}/audit/logs", timeout=10)
            results["list_audit_logs"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ Audit logs retrieved successfully")
            else:
                self.log(f"❌ Audit logs retrieval failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["list_audit_logs"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ Audit logs retrieval error: {str(e)}", "ERROR")
        
        return results
    
    def test_ai_modeling_service(self, base_url: str) -> Dict[str, Any]:
        """Test AI modeling service endpoints"""
        self.log("Testing AI Modeling Service endpoints")
        results = {}
        
        # Headers for authentication
        headers = {
            "X-Tenant-ID": TEST_DATA["tenant_id"],
            "X-User-ID": TEST_DATA["user_id"]
        }
        
        # Test generate modeling
        modeling_data = {
            "tenant_id": TEST_DATA["tenant_id"],
            "user_id": TEST_DATA["user_id"],
            "input_type": "goal",
            "input_text": "Optimize supply chain efficiency and reduce costs by 20%"
        }
        
        try:
            response = self.session.post(f"{base_url}/ai_modeling/generate", json=modeling_data, headers=headers, timeout=10)
            results["generate_modeling"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ AI modeling generation successful")
            else:
                self.log(f"❌ AI modeling generation failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["generate_modeling"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ AI modeling generation error: {str(e)}", "ERROR")
        
        # Test get history
        try:
            response = self.session.get(f"{base_url}/ai_modeling/history/{TEST_DATA['user_id']}", headers=headers, timeout=10)
            results["get_history"] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "response": response.json() if response.status_code == 200 else None,
                "error": None
            }
            
            if response.status_code == 200:
                self.log(f"✅ AI modeling history retrieved successfully")
            else:
                self.log(f"❌ AI modeling history failed: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            results["get_history"] = {
                "status_code": None,
                "success": False,
                "response": None,
                "error": str(e)
            }
            self.log(f"❌ AI modeling history error: {str(e)}", "ERROR")
        
        return results
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run tests for all services"""
        self.log("Starting comprehensive microservices validation")
        self.log("=" * 60)
        
        all_results = {}
        
        for service_name, config in SERVICES.items():
            self.log(f"\n🔍 Testing {service_name.upper()}")
            self.log("-" * 40)
            
            base_url = config["base_url"]
            service_results = {}
            
            # Test health endpoint
            service_results["health"] = self.test_health_endpoint(service_name, base_url)
            
            # Test metrics endpoint
            service_results["metrics"] = self.test_metrics_endpoint(service_name, base_url)
            
            # Test service-specific endpoints
            if service_name == "auth_service":
                service_results["endpoints"] = self.test_auth_service(base_url)
            elif service_name == "billing_service":
                service_results["endpoints"] = self.test_billing_service(base_url)
            elif service_name == "invoice_service":
                service_results["endpoints"] = self.test_invoice_service(base_url)
            elif service_name == "ai_modeling_service":
                service_results["endpoints"] = self.test_ai_modeling_service(base_url)
            
            all_results[service_name] = service_results
        
        return all_results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive test report"""
        report = []
        report.append("# ReqArchitect Microservices Validation Report")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        total_services = len(results)
        successful_services = 0
        
        for service_name, service_results in results.items():
            report.append(f"## {service_name.upper()}")
            report.append("")
            
            # Health check
            health = service_results.get("health", {})
            if health.get("success"):
                report.append("✅ **Health Check**: PASSED")
                successful_services += 1
            else:
                report.append(f"❌ **Health Check**: FAILED - {health.get('error', 'Unknown error')}")
            
            # Metrics
            metrics = service_results.get("metrics", {})
            if metrics.get("success"):
                report.append("✅ **Metrics Endpoint**: PASSED")
            else:
                report.append(f"❌ **Metrics Endpoint**: FAILED - {metrics.get('error', 'Unknown error')}")
            
            # Service-specific endpoints
            endpoints = service_results.get("endpoints", {})
            if endpoints:
                report.append("### Endpoint Tests:")
                for endpoint_name, endpoint_result in endpoints.items():
                    if endpoint_result.get("success"):
                        report.append(f"✅ **{endpoint_name}**: PASSED")
                    else:
                        status_code = endpoint_result.get("status_code")
                        error = endpoint_result.get("error")
                        report.append(f"❌ **{endpoint_name}**: FAILED - Status: {status_code}, Error: {error}")
            
            report.append("")
            report.append("---")
            report.append("")
        
        # Summary
        report.append("## Summary")
        report.append(f"- **Total Services**: {total_services}")
        report.append(f"- **Successful Health Checks**: {successful_services}")
        report.append(f"- **Success Rate**: {(successful_services/total_services)*100:.1f}%")
        
        return "\n".join(report)

def main():
    """Main function to run the microservices validation"""
    tester = MicroserviceTester()
    
    try:
        results = tester.run_all_tests()
        
        # Generate and save report
        report = tester.generate_report(results)
        
        with open("microservices_validation_report.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        tester.log("Validation complete! Report saved to microservices_validation_report.md")
        
        # Print summary to console
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        
        total_services = len(results)
        successful_services = sum(1 for r in results.values() if r.get("health", {}).get("success"))
        
        print(f"Total Services Tested: {total_services}")
        print(f"Successful Health Checks: {successful_services}")
        print(f"Success Rate: {(successful_services/total_services)*100:.1f}%")
        
        if successful_services == total_services:
            print("🎉 All services are healthy!")
        else:
            print("⚠️ Some services have issues. Check the detailed report.")
        
    except KeyboardInterrupt:
        tester.log("Validation interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        tester.log(f"Validation failed with error: {str(e)}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main() 
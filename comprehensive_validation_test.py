#!/usr/bin/env python3
"""
Comprehensive Validation Test for ReqArchitect Microservices
Tests all functional endpoints with realistic data and captures results
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class ServiceValidator:
    def __init__(self):
        self.results = []
        self.base_urls = {
            'auth_service': 'http://localhost:8001',
            'billing_service': 'http://localhost:8010', 
            'invoice_service': 'http://localhost:8011',
            'ai_modeling_service': 'http://localhost:8002',
            'usage_service': 'http://localhost:8005',
            'notification_service': 'http://localhost:8006',
            'audit_log_service': 'http://localhost:8007'
        }
        
    def test_endpoint(self, service: str, endpoint: str, method: str = 'GET', 
                     data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, 
                     expected_status: int = 200) -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        url = f"{self.base_urls[service]}{endpoint}"
        start_time = time.time()
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            duration = time.time() - start_time
            
            result = {
                'service': service,
                'endpoint': endpoint,
                'method': method,
                'url': url,
                'status_code': response.status_code,
                'response_time': round(duration, 3),
                'success': response.status_code == expected_status,
                'response_body': response.text[:500] if response.text else '',
                'headers': dict(response.headers),
                'error': None
            }
            
        except Exception as e:
            duration = time.time() - start_time
            result = {
                'service': service,
                'endpoint': endpoint,
                'method': method,
                'url': url,
                'status_code': None,
                'response_time': round(duration, 3),
                'success': False,
                'response_body': '',
                'headers': {},
                'error': str(e)
            }
            
        self.results.append(result)
        return result
    
    def test_auth_service(self):
        """Test auth service endpoints"""
        print("Testing Auth Service...")
        
        # Test health endpoint
        self.test_endpoint('auth_service', '/health')
        
        # Test roles endpoint
        self.test_endpoint('auth_service', '/auth/roles')
        
        # Test login with test credentials
        login_data = {
            "email": "test@example.com",
            "password": "testpass123", 
            "role": "Admin",
            "tenant_id": "test-tenant-123"
        }
        self.test_endpoint('auth_service', '/auth/login', 'POST', login_data)
        
        # Test logout
        self.test_endpoint('auth_service', '/auth/logout', 'POST')
        
        # Test me endpoint (requires auth)
        self.test_endpoint('auth_service', '/auth/me')
        
        # Test refresh endpoint
        self.test_endpoint('auth_service', '/auth/refresh', 'POST')
    
    def test_billing_service(self):
        """Test billing service endpoints"""
        print("Testing Billing Service...")
        
        # Test health endpoint
        self.test_endpoint('billing_service', '/health')
        
        # Test get plans
        self.test_endpoint('billing_service', '/billing/plans')
        
        # Test get tenant billing profile
        self.test_endpoint('billing_service', '/billing/tenant/test-tenant-123')
        
        # Test usage report
        usage_data = {
            "tenant_id": "test-tenant-123",
            "api_calls": 150,
            "storage_gb": 5.2,
            "active_users": 3
        }
        self.test_endpoint('billing_service', '/billing/usage_report', 'POST', usage_data)
        
        # Test trigger alerts
        alert_data = {
            "tenant_id": "test-tenant-123",
            "alert_type": "usage_threshold",
            "threshold": 80
        }
        self.test_endpoint('billing_service', '/billing/trigger_alerts', 'POST', alert_data)
        
        # Test upgrade plan
        upgrade_data = {
            "tenant_id": "test-tenant-123",
            "new_plan_id": "premium-plan",
            "effective_date": "2025-01-01"
        }
        self.test_endpoint('billing_service', '/billing/upgrade_plan', 'POST', upgrade_data)
    
    def test_invoice_service(self):
        """Test invoice service endpoints"""
        print("Testing Invoice Service...")
        
        # Test health endpoint
        self.test_endpoint('invoice_service', '/health')
        
        # Test get invoices for tenant
        self.test_endpoint('invoice_service', '/invoices/test-tenant-123')
        
        # Test generate invoice
        self.test_endpoint('invoice_service', '/invoices/generate/test-tenant-123', 'POST')
    
    def test_ai_modeling_service(self):
        """Test AI modeling service endpoints"""
        print("Testing AI Modeling Service...")
        
        # Test health endpoint
        self.test_endpoint('ai_modeling_service', '/health')
        
        # Test generate modeling
        modeling_data = {
            "tenant_id": "test-tenant-123",
            "user_id": "test-user-456", 
            "input_type": "goal",
            "input_text": "Optimize supply chain efficiency for manufacturing operations"
        }
        headers = {
            "X-Tenant-ID": "test-tenant-123",
            "X-User-ID": "test-user-456"
        }
        self.test_endpoint('ai_modeling_service', '/ai_modeling/generate', 'POST', modeling_data, headers)
        
        # Test get history
        self.test_endpoint('ai_modeling_service', '/ai_modeling/history/test-user-456')
        
        # Test submit feedback
        feedback_data = {
            "output_id": 1,
            "user_id": "test-user-456",
            "rating": 4,
            "comments": "Good analysis, but could be more detailed"
        }
        self.test_endpoint('ai_modeling_service', '/ai_modeling/feedback', 'POST', feedback_data)
    
    def test_usage_service(self):
        """Test usage service endpoints"""
        print("Testing Usage Service...")
        
        # Test health endpoint
        self.test_endpoint('usage_service', '/health')
        
        # Test get usage metrics
        self.test_endpoint('usage_service', '/usage/tenant/test-tenant-123')
        
        # Test get system health
        self.test_endpoint('usage_service', '/usage/system_health')
        
        # Test get audit events
        self.test_endpoint('usage_service', '/usage/activity/test-tenant-123')
    
    def test_notification_service(self):
        """Test notification service endpoints"""
        print("Testing Notification Service...")
        
        # Test health endpoint
        self.test_endpoint('notification_service', '/health')
        
        # Test send notification
        notification_data = {
            "notification_id": "test-notif-001",
            "user_id": "test-user-456",
            "tenant_id": "test-tenant-123",
            "channel": "email",
            "message": "Test notification message for validation",
            "event_type": "system_alert",
            "delivered": False
        }
        self.test_endpoint('notification_service', '/notifications/send', 'POST', notification_data)
        
        # Test get user notifications
        self.test_endpoint('notification_service', '/notifications/user/test-user-456')
        
        # Test create template
        template_data = {
            "template_id": "test-template-001",
            "event_type": "system_alert",
            "channel": "email",
            "content": "System alert: {message}"
        }
        self.test_endpoint('notification_service', '/notifications/template', 'POST', template_data)
        
        # Test get template by event
        self.test_endpoint('notification_service', '/notifications/template/system_alert')
    
    def test_audit_log_service(self):
        """Test audit log service endpoints"""
        print("Testing Audit Log Service...")
        
        # Test health endpoint
        self.test_endpoint('audit_log_service', '/health')
        
        # Test query audit logs
        self.test_endpoint('audit_log_service', '/audit_log/query?tenant_id=test-tenant-123')
        
        # Test query with filters
        self.test_endpoint('audit_log_service', '/audit_log/query?tenant_id=test-tenant-123&event_type=login')
    
    def run_all_tests(self):
        """Run all service tests"""
        print("Starting comprehensive validation test...")
        print("=" * 60)
        
        self.test_auth_service()
        self.test_billing_service()
        self.test_invoice_service()
        self.test_ai_modeling_service()
        self.test_usage_service()
        self.test_notification_service()
        self.test_audit_log_service()
        
        print("=" * 60)
        print("All tests completed!")
    
    def generate_summary_table(self) -> str:
        """Generate a summary table of all test results"""
        summary = []
        summary.append("ReqArchitect Microservices Validation Summary")
        summary.append("=" * 80)
        summary.append(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary.append("")
        
        # Group results by service
        service_results = {}
        for result in self.results:
            service = result['service']
            if service not in service_results:
                service_results[service] = []
            service_results[service].append(result)
        
        for service, results in service_results.items():
            summary.append(f"\n{service.upper().replace('_', ' ')}")
            summary.append("-" * 50)
            
            for result in results:
                status = "✅" if result['success'] else "❌"
                status_code = result['status_code'] or "ERROR"
                endpoint = result['endpoint']
                method = result['method']
                response_time = result['response_time']
                
                summary.append(f"{status} {method} {endpoint:<30} {status_code:>3} ({response_time}s)")
                
                if result['error']:
                    summary.append(f"    Error: {result['error']}")
                elif not result['success'] and result['response_body']:
                    summary.append(f"    Response: {result['response_body'][:100]}...")
        
        # Overall statistics
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r['success'])
        failed_tests = total_tests - successful_tests
        
        summary.append("\n" + "=" * 80)
        summary.append(f"TOTAL TESTS: {total_tests}")
        summary.append(f"SUCCESSFUL: {successful_tests}")
        summary.append(f"FAILED: {failed_tests}")
        summary.append(f"SUCCESS RATE: {(successful_tests/total_tests*100):.1f}%")
        
        return "\n".join(summary)
    
    def save_results(self, filename: str = "validation_results.json"):
        """Save detailed results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"Detailed results saved to {filename}")

def main():
    validator = ServiceValidator()
    validator.run_all_tests()
    
    # Generate and print summary
    summary = validator.generate_summary_table()
    print("\n" + summary)
    
    # Save detailed results
    validator.save_results()
    
    # Save summary to file
    with open("validation_summary.txt", "w") as f:
        f.write(summary)
    print("\nSummary saved to validation_summary.txt")

if __name__ == "__main__":
    main() 
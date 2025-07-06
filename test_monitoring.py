#!/usr/bin/env python3
"""
Test script for ReqArchitect monitoring and observability features.
Validates health endpoints, metrics endpoints, and monitoring dashboard.
"""

import requests
import json
import time
import sys
from typing import Dict, List, Optional

# Service configuration
SERVICES = {
    "gateway_service": {"port": 8080, "external": True},
    "auth_service": {"port": 8001, "external": True},
    "ai_modeling_service": {"port": 8002, "external": True},
    "usage_service": {"port": 8000, "external": False},
    "billing_service": {"port": 8010, "external": True},
    "invoice_service": {"port": 8011, "external": True},
    "notification_service": {"port": 8000, "external": False},
    "monitoring_dashboard_service": {"port": 8012, "external": True}
}

def test_health_endpoint(service_name: str, port: int, external: bool = True) -> Dict:
    """Test health endpoint for a service"""
    base_url = f"http://localhost:{port}" if external else f"http://{service_name}:{port}"
    health_url = f"{base_url}/health"
    
    try:
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "service": service_name,
                "status": "healthy",
                "response_time": response.elapsed.total_seconds() * 1000,
                "data": data
            }
        else:
            return {
                "service": service_name,
                "status": "unhealthy",
                "error": f"HTTP {response.status_code}",
                "response_time": response.elapsed.total_seconds() * 1000
            }
    except requests.exceptions.RequestException as e:
        return {
            "service": service_name,
            "status": "error",
            "error": str(e),
            "response_time": 0
        }

def test_metrics_endpoint(service_name: str, port: int, external: bool = True) -> Dict:
    """Test metrics endpoint for a service"""
    base_url = f"http://localhost:{port}" if external else f"http://{service_name}:{port}"
    metrics_url = f"{base_url}/metrics"
    
    try:
        response = requests.get(metrics_url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "service": service_name,
                "status": "success",
                "metrics_count": len(data),
                "data": data
            }
        else:
            return {
                "service": service_name,
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }
    except requests.exceptions.RequestException as e:
        return {
            "service": service_name,
            "status": "error",
            "error": str(e)
        }

def test_monitoring_dashboard() -> Dict:
    """Test monitoring dashboard endpoints"""
    base_url = "http://localhost:8012"
    
    results = {}
    
    # Test dashboard health
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        results["dashboard_health"] = {
            "status": "success" if response.status_code == 200 else "error",
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        results["dashboard_health"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test dashboard metrics
    try:
        response = requests.get(f"{base_url}/metrics", timeout=5)
        results["dashboard_metrics"] = {
            "status": "success" if response.status_code == 200 else "error",
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        results["dashboard_metrics"] = {
            "status": "error",
            "error": str(e)
        }
    
    # Test dashboard status API
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        results["dashboard_status"] = {
            "status": "success" if response.status_code == 200 else "error",
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 200 else None
        }
    except Exception as e:
        results["dashboard_status"] = {
            "status": "error",
            "error": str(e)
        }
    
    return results

def print_results(results: List[Dict], title: str):
    """Print test results in a formatted way"""
    print(f"\n{'='*60}")
    print(f"📊 {title}")
    print(f"{'='*60}")
    
    for result in results:
        service = result["service"]
        status = result["status"]
        
        if status == "healthy" or status == "success":
            print(f"✅ {service}: {status}")
            if "response_time" in result:
                print(f"   ⏱️  Response Time: {result['response_time']:.2f}ms")
            if "metrics_count" in result:
                print(f"   📈 Metrics Count: {result['metrics_count']}")
        else:
            print(f"❌ {service}: {status}")
            if "error" in result:
                print(f"   🔍 Error: {result['error']}")

def main():
    """Main test function"""
    print("🚀 ReqArchitect Monitoring & Observability Test Suite")
    print("=" * 60)
    
    # Test health endpoints
    print("\n🔍 Testing Health Endpoints...")
    health_results = []
    
    for service_name, config in SERVICES.items():
        if config["external"]:  # Only test externally accessible services
            result = test_health_endpoint(service_name, config["port"], config["external"])
            health_results.append(result)
            time.sleep(0.1)  # Small delay between requests
    
    print_results(health_results, "Health Endpoint Test Results")
    
    # Test metrics endpoints
    print("\n📈 Testing Metrics Endpoints...")
    metrics_results = []
    
    for service_name, config in SERVICES.items():
        if config["external"]:  # Only test externally accessible services
            result = test_metrics_endpoint(service_name, config["port"], config["external"])
            metrics_results.append(result)
            time.sleep(0.1)  # Small delay between requests
    
    print_results(metrics_results, "Metrics Endpoint Test Results")
    
    # Test monitoring dashboard
    print("\n🖥️  Testing Monitoring Dashboard...")
    dashboard_results = test_monitoring_dashboard()
    
    print(f"\n{'='*60}")
    print("📊 Monitoring Dashboard Test Results")
    print(f"{'='*60}")
    
    for endpoint, result in dashboard_results.items():
        if result["status"] == "success":
            print(f"✅ {endpoint}: {result['status']}")
            if "status_code" in result:
                print(f"   📡 Status Code: {result['status_code']}")
        else:
            print(f"❌ {endpoint}: {result['status']}")
            if "error" in result:
                print(f"   🔍 Error: {result['error']}")
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 Test Summary")
    print(f"{'='*60}")
    
    healthy_services = sum(1 for r in health_results if r["status"] == "healthy")
    total_services = len(health_results)
    
    successful_metrics = sum(1 for r in metrics_results if r["status"] == "success")
    total_metrics = len(metrics_results)
    
    dashboard_success = sum(1 for r in dashboard_results.values() if r["status"] == "success")
    total_dashboard = len(dashboard_results)
    
    print(f"🏥 Health Endpoints: {healthy_services}/{total_services} healthy")
    print(f"📊 Metrics Endpoints: {successful_metrics}/{total_metrics} successful")
    print(f"🖥️  Dashboard Endpoints: {dashboard_success}/{total_dashboard} successful")
    
    # Overall success rate
    total_tests = total_services + total_metrics + total_dashboard
    successful_tests = healthy_services + successful_metrics + dashboard_success
    success_rate = (successful_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n🎯 Overall Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 Excellent! Monitoring system is working well.")
    elif success_rate >= 70:
        print("⚠️  Good! Some issues detected, but system is functional.")
    else:
        print("🚨 Issues detected! Please check service configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
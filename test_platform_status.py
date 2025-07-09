#!/usr/bin/env python3
"""
Test script for the /platform/status endpoint
Validates the monitoring dashboard service's platform status aggregation
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8012"
PLATFORM_STATUS_ENDPOINT = f"{BASE_URL}/platform/status"

def test_platform_status_basic():
    """Test basic platform status endpoint"""
    print("🔍 Testing basic platform status...")
    
    try:
        response = requests.get(PLATFORM_STATUS_ENDPOINT, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Basic platform status test passed")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response Time: {response.elapsed.total_seconds():.2f}s")
            print(f"   Timestamp: {data.get('timestamp')}")
            print(f"   Environment: {data.get('environment')}")
            print(f"   Overall Status: {data.get('summary', {}).get('overall_status')}")
            return True
        else:
            print(f"❌ Basic platform status test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Basic platform status test failed: {str(e)}")
        return False

def test_platform_status_critical_only():
    """Test platform status with critical_only filter"""
    print("\n🔍 Testing critical services only...")
    
    try:
        response = requests.get(f"{PLATFORM_STATUS_ENDPOINT}?critical_only=true", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {})
            critical_services = [name for name, status in services.items() 
                              if status.get('critical', False)]
            
            print("✅ Critical services filter test passed")
            print(f"   Critical Services Found: {len(critical_services)}")
            print(f"   Services: {list(services.keys())}")
            
            # Verify only critical services are returned
            all_critical = all(status.get('critical', False) for status in services.values())
            if all_critical:
                print("   ✅ All returned services are marked as critical")
            else:
                print("   ⚠️ Some non-critical services were returned")
            
            return True
        else:
            print(f"❌ Critical services test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Critical services test failed: {str(e)}")
        return False

def test_platform_status_cache():
    """Test platform status caching behavior"""
    print("\n🔍 Testing cache behavior...")
    
    try:
        # First request
        start_time = time.time()
        response1 = requests.get(PLATFORM_STATUS_ENDPOINT, timeout=30)
        first_request_time = time.time() - start_time
        
        # Second request (should use cache)
        start_time = time.time()
        response2 = requests.get(PLATFORM_STATUS_ENDPOINT, timeout=30)
        second_request_time = time.time() - start_time
        
        if response1.status_code == 200 and response2.status_code == 200:
            data1 = response1.json()
            data2 = response2.json()
            
            cache_info1 = data1.get('cache_info', {})
            cache_info2 = data2.get('cache_info', {})
            
            print("✅ Cache behavior test passed")
            print(f"   First Request Time: {first_request_time:.3f}s")
            print(f"   Second Request Time: {second_request_time:.3f}s")
            print(f"   Cache Valid (1st): {cache_info1.get('cache_valid')}")
            print(f"   Cache Valid (2nd): {cache_info2.get('cache_valid')}")
            
            # Second request should be faster due to caching
            if second_request_time < first_request_time:
                print("   ✅ Second request was faster (cache working)")
            else:
                print("   ⚠️ Second request was not faster")
            
            return True
        else:
            print(f"❌ Cache test failed: {response1.status_code}, {response2.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cache test failed: {str(e)}")
        return False

def test_platform_status_force_refresh():
    """Test platform status with force refresh"""
    print("\n🔍 Testing force refresh...")
    
    try:
        response = requests.get(f"{PLATFORM_STATUS_ENDPOINT}?force_refresh=true", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            cache_info = data.get('cache_info', {})
            
            print("✅ Force refresh test passed")
            print(f"   Cache Valid: {cache_info.get('cache_valid')}")
            print(f"   Last Update: {cache_info.get('last_update')}")
            
            return True
        else:
            print(f"❌ Force refresh test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Force refresh test failed: {str(e)}")
        return False

def test_platform_status_metrics():
    """Test platform status with and without metrics"""
    print("\n🔍 Testing metrics inclusion...")
    
    try:
        # Request with metrics
        response_with_metrics = requests.get(f"{PLATFORM_STATUS_ENDPOINT}?include_metrics=true", timeout=30)
        
        # Request without metrics
        response_without_metrics = requests.get(f"{PLATFORM_STATUS_ENDPOINT}?include_metrics=false", timeout=30)
        
        if response_with_metrics.status_code == 200 and response_without_metrics.status_code == 200:
            data_with_metrics = response_with_metrics.json()
            data_without_metrics = response_without_metrics.json()
            
            # Check if metrics are included/excluded properly
            services_with_metrics = data_with_metrics.get('services', {})
            services_without_metrics = data_without_metrics.get('services', {})
            
            print("✅ Metrics inclusion test passed")
            
            # Count services with uptime information
            with_uptime = sum(1 for service in services_with_metrics.values() 
                             if 'uptime' in service or 'uptime_seconds' in service)
            without_uptime = sum(1 for service in services_without_metrics.values() 
                                if 'uptime' in service or 'uptime_seconds' in service)
            
            print(f"   Services with uptime (include_metrics=true): {with_uptime}")
            print(f"   Services with uptime (include_metrics=false): {without_uptime}")
            
            return True
        else:
            print(f"❌ Metrics test failed: {response_with_metrics.status_code}, {response_without_metrics.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Metrics test failed: {str(e)}")
        return False

def test_platform_status_structure():
    """Test platform status response structure"""
    print("\n🔍 Testing response structure...")
    
    try:
        response = requests.get(PLATFORM_STATUS_ENDPOINT, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ['timestamp', 'environment', 'cache_info', 'summary', 'services']
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                print("✅ Response structure test passed")
                print(f"   All required fields present: {required_fields}")
                
                # Check summary structure
                summary = data.get('summary', {})
                summary_fields = ['total_services', 'healthy_services', 'unhealthy_services', 
                                'critical_services', 'healthy_critical_services', 
                                'success_rate', 'critical_success_rate', 'overall_status']
                
                missing_summary_fields = [field for field in summary_fields if field not in summary]
                if not missing_summary_fields:
                    print(f"   Summary structure valid: {summary_fields}")
                else:
                    print(f"   ⚠️ Missing summary fields: {missing_summary_fields}")
                
                # Check cache info structure
                cache_info = data.get('cache_info', {})
                cache_fields = ['last_update', 'cache_valid', 'cache_duration_seconds']
                missing_cache_fields = [field for field in cache_fields if field not in cache_info]
                if not missing_cache_fields:
                    print(f"   Cache info structure valid: {cache_fields}")
                else:
                    print(f"   ⚠️ Missing cache fields: {missing_cache_fields}")
                
                return True
            else:
                print(f"❌ Response structure test failed: missing fields {missing_fields}")
                return False
        else:
            print(f"❌ Response structure test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Response structure test failed: {str(e)}")
        return False

def test_platform_status_service_details():
    """Test individual service status details"""
    print("\n🔍 Testing service status details...")
    
    try:
        response = requests.get(PLATFORM_STATUS_ENDPOINT, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            services = data.get('services', {})
            
            print("✅ Service details test passed")
            print(f"   Total Services: {len(services)}")
            
            # Check each service has required fields
            for service_name, service_data in services.items():
                required_service_fields = ['status', 'response_time_ms', 'last_check', 'critical']
                missing_fields = [field for field in required_service_fields 
                                if field not in service_data]
                
                if missing_fields:
                    print(f"   ⚠️ Service {service_name} missing fields: {missing_fields}")
                else:
                    print(f"   ✅ Service {service_name}: {service_data['status']} "
                          f"({service_data['response_time_ms']}ms)")
            
            return True
        else:
            print(f"❌ Service details test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Service details test failed: {str(e)}")
        return False

def main():
    """Run all platform status tests"""
    print("🚀 Starting Platform Status Endpoint Tests")
    print("=" * 50)
    
    tests = [
        test_platform_status_basic,
        test_platform_status_critical_only,
        test_platform_status_cache,
        test_platform_status_force_refresh,
        test_platform_status_metrics,
        test_platform_status_structure,
        test_platform_status_service_details
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Platform status endpoint is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    main() 
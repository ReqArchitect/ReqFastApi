#!/usr/bin/env python3
"""
Critical Services Health Check Script
Used in CI/CD pipeline to validate critical services and set outputs
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Critical services that must be healthy
CRITICAL_SERVICES = [
    "auth_service",
    "gateway_service",
    "ai_modeling_service"
]

# Minimum success rate for critical services
MIN_CRITICAL_SUCCESS_RATE = 80.0

# Maximum allowed 500 errors for critical services
MAX_500_ERRORS = 0

def load_latest_validation_results() -> Dict:
    """Load the latest validation results from JSON file"""
    output_dir = Path("validation_outputs")
    
    if not output_dir.exists():
        print("No validation outputs directory found")
        return {}
    
    # Find the latest validation results file
    json_files = list(output_dir.glob("validation_results_*.json"))
    if not json_files:
        print("No validation results files found")
        return {}
    
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    
    try:
        with open(latest_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading validation results: {e}")
        return {}

def analyze_critical_services(results: Dict) -> Tuple[bool, Dict]:
    """Analyze critical services health"""
    if not results or 'cycle_results' not in results:
        return False, {}
    
    cycle_results = results['cycle_results']
    service_health = results.get('service_health', {})
    
    critical_status = {}
    all_critical_healthy = True
    
    for service_name in CRITICAL_SERVICES:
        # Get service health metrics
        health = service_health.get(service_name, {})
        success_rate = health.get('api_success_ratio', 0.0)
        error_rate = health.get('error_rate', 100.0)
        
        # Count 500 errors for this service
        service_results = [r for r in cycle_results if r['service_name'] == service_name]
        error_500_count = sum(1 for r in service_results if r.get('status_code') == 500)
        
        # Check if service is healthy
        is_healthy = (
            success_rate >= MIN_CRITICAL_SUCCESS_RATE and
            error_500_count <= MAX_500_ERRORS
        )
        
        critical_status[service_name] = {
            'success_rate': success_rate,
            'error_rate': error_rate,
            'error_500_count': error_500_count,
            'is_healthy': is_healthy
        }
        
        if not is_healthy:
            all_critical_healthy = False
    
    return all_critical_healthy, critical_status

def calculate_overall_success_rate(results: Dict) -> float:
    """Calculate overall success rate"""
    if not results or 'cycle_results' not in results:
        return 0.0
    
    cycle_results = results['cycle_results']
    total_tests = len(cycle_results)
    successful_tests = sum(1 for r in cycle_results if r.get('success', False))
    
    return (successful_tests / total_tests * 100) if total_tests > 0 else 0.0

def generate_github_outputs(critical_healthy: bool, critical_status: Dict, overall_success_rate: float):
    """Generate GitHub Actions outputs"""
    # Set critical status
    critical_status_str = "PASSED" if critical_healthy else "FAILED"
    print(f"::set-output name=critical_status::{critical_status_str}")
    
    # Set overall success rate
    print(f"::set-output name=success_rate::{overall_success_rate:.1f}")
    
    # Set individual service statuses
    for service_name, status in critical_status.items():
        output_name = f"{service_name}_success_rate"
        print(f"::set-output name={output_name}::{status['success_rate']:.1f}")
        
        output_name = f"{service_name}_error_500_count"
        print(f"::set-output name={output_name}::{status['error_500_count']}")
        
        output_name = f"{service_name}_healthy"
        print(f"::set-output name={output_name}::{str(status['is_healthy']).lower()}")
    
    # Set environment variable for other steps
    os.environ['CRITICAL_SERVICES_HEALTHY'] = str(critical_healthy).lower()
    os.environ['OVERALL_SUCCESS_RATE'] = f"{overall_success_rate:.1f}"

def main():
    """Main function"""
    print("Checking critical services health...")
    
    # Load validation results
    results = load_latest_validation_results()
    
    if not results:
        print("No validation results found. Failing health check.")
        sys.exit(1)
    
    # Analyze critical services
    critical_healthy, critical_status = analyze_critical_services(results)
    overall_success_rate = calculate_overall_success_rate(results)
    
    # Print analysis
    print(f"\nCritical Services Analysis:")
    print(f"Overall Success Rate: {overall_success_rate:.1f}%")
    print(f"Critical Services Healthy: {critical_healthy}")
    
    for service_name, status in critical_status.items():
        health_icon = "✅" if status['is_healthy'] else "❌"
        print(f"  {health_icon} {service_name}:")
        print(f"    Success Rate: {status['success_rate']:.1f}%")
        print(f"    Error Rate: {status['error_rate']:.1f}%")
        print(f"    500 Errors: {status['error_500_count']}")
    
    # Generate GitHub outputs
    generate_github_outputs(critical_healthy, critical_status, overall_success_rate)
    
    # Exit with error if critical services are unhealthy
    if not critical_healthy:
        print("\n❌ Critical services are unhealthy. Build will fail.")
        sys.exit(1)
    else:
        print("\n✅ All critical services are healthy.")

if __name__ == "__main__":
    main() 
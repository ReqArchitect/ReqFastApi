#!/usr/bin/env python3
"""
Validation Summary Generator
Creates comprehensive validation reports with charts and timestamps
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

def load_latest_validation_results() -> Dict:
    """Load the latest validation results"""
    output_dir = Path("validation_outputs")
    
    if not output_dir.exists():
        return {}
    
    json_files = list(output_dir.glob("validation_results_*.json"))
    if not json_files:
        return {}
    
    latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
    
    try:
        with open(latest_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading validation results: {e}")
        return {}

def create_ascii_chart(data: List[Tuple[str, float]], title: str, width: int = 50) -> str:
    """Create ASCII bar chart"""
    if not data:
        return f"{title}\nNo data available"
    
    chart = f"{title}\n"
    chart += "=" * (len(title) + 10) + "\n"
    
    max_value = max(value for _, value in data) if data else 0
    
    for label, value in data:
        if max_value > 0:
            bar_length = int((value / max_value) * width)
        else:
            bar_length = 0
        
        bar = "█" * bar_length
        chart += f"{label:<20} {bar} {value:>6.1f}%\n"
    
    return chart

def generate_service_summary(results: Dict) -> str:
    """Generate service-level summary"""
    if not results or 'service_health' not in results:
        return "No service health data available"
    
    service_health = results['service_health']
    
    # Prepare data for chart
    service_data = []
    for service_name, health in service_health.items():
        success_rate = health.get('api_success_ratio', 0.0)
        service_data.append((service_name, success_rate))
    
    # Sort by success rate (descending)
    service_data.sort(key=lambda x: x[1], reverse=True)
    
    return create_ascii_chart(service_data, "Service Success Rates")

def generate_endpoint_summary(results: Dict) -> str:
    """Generate endpoint-level summary"""
    if not results or 'cycle_results' not in results:
        return "No endpoint data available"
    
    cycle_results = results['cycle_results']
    
    # Group by service and count endpoints
    service_endpoints = {}
    for result in cycle_results:
        service_name = result['service_name']
        endpoint = result['endpoint']
        success = result.get('success', False)
        
        if service_name not in service_endpoints:
            service_endpoints[service_name] = {'total': 0, 'successful': 0, 'endpoints': []}
        
        service_endpoints[service_name]['total'] += 1
        if success:
            service_endpoints[service_name]['successful'] += 1
        
        service_endpoints[service_name]['endpoints'].append({
            'endpoint': endpoint,
            'method': result['method'],
            'status_code': result.get('status_code'),
            'success': success,
            'response_time': result.get('response_time')
        })
    
    summary = "Endpoint Summary by Service\n"
    summary += "=" * 40 + "\n\n"
    
    for service_name, data in service_endpoints.items():
        success_rate = (data['successful'] / data['total'] * 100) if data['total'] > 0 else 0
        summary += f"{service_name.upper()}:\n"
        summary += f"  Success Rate: {success_rate:.1f}% ({data['successful']}/{data['total']})\n"
        
        # List failed endpoints
        failed_endpoints = [ep for ep in data['endpoints'] if not ep['success']]
        if failed_endpoints:
            summary += f"  Failed Endpoints:\n"
            for ep in failed_endpoints:
                status_code = ep.get('status_code', 'N/A')
                summary += f"    {ep['method']} {ep['endpoint']} -> {status_code}\n"
        
        summary += "\n"
    
    return summary

def generate_error_analysis(results: Dict) -> str:
    """Generate error analysis"""
    if not results or 'cycle_results' not in results:
        return "No error data available"
    
    cycle_results = results['cycle_results']
    
    # Count errors by status code
    error_counts = {}
    for result in cycle_results:
        if not result.get('success', False):
            status_code = result.get('status_code', 'Unknown')
            error_counts[status_code] = error_counts.get(status_code, 0) + 1
    
    if not error_counts:
        return "No errors detected"
    
    summary = "Error Analysis\n"
    summary += "=" * 20 + "\n"
    
    # Sort by count (descending)
    sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)
    
    for status_code, count in sorted_errors:
        percentage = (count / len(cycle_results)) * 100
        summary += f"  {status_code}: {count} ({percentage:.1f}%)\n"
    
    return summary

def generate_timestamp_summary(results: Dict) -> str:
    """Generate timestamp and metadata summary"""
    timestamp = results.get('timestamp', datetime.now().isoformat())
    
    summary = "Validation Metadata\n"
    summary += "=" * 20 + "\n"
    summary += f"Timestamp: {timestamp}\n"
    summary += f"Total Tests: {len(results.get('cycle_results', []))}\n"
    
    # Calculate overall metrics
    cycle_results = results.get('cycle_results', [])
    if cycle_results:
        successful_tests = sum(1 for r in cycle_results if r.get('success', False))
        total_tests = len(cycle_results)
        overall_success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        summary += f"Successful Tests: {successful_tests}\n"
        summary += f"Failed Tests: {total_tests - successful_tests}\n"
        summary += f"Overall Success Rate: {overall_success_rate:.1f}%\n"
    
    return summary

def main():
    """Main function"""
    print("Generating validation summary...")
    
    # Load validation results
    results = load_latest_validation_results()
    
    if not results:
        print("No validation results found")
        sys.exit(1)
    
    # Generate summary sections
    timestamp_summary = generate_timestamp_summary(results)
    service_summary = generate_service_summary(results)
    endpoint_summary = generate_endpoint_summary(results)
    error_analysis = generate_error_analysis(results)
    
    # Combine all sections
    full_summary = f"""
# ReqArchitect Validation Summary
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{timestamp_summary}

{service_summary}

{endpoint_summary}

{error_analysis}

---
*This summary was generated automatically by the CI/CD validation framework.*
"""
    
    # Write to file
    with open('validation_summary.md', 'w') as f:
        f.write(full_summary)
    
    print("Validation summary generated: validation_summary.md")
    
    # Also print to console for CI/CD logs
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    print(timestamp_summary)
    print(service_summary)
    print(error_analysis)

if __name__ == "__main__":
    main() 
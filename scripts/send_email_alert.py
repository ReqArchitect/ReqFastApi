#!/usr/bin/env python3
"""
Email Alert Script for Validation Framework
Sends email notifications when validation fails or regressions are detected
"""

import os
import sys
import json
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, List

def load_validation_results() -> Dict:
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

def check_for_regressions(results: Dict) -> List[Dict]:
    """Check for regressions (new failures)"""
    regressions = []
    
    if not results or 'cycle_results' not in results:
        return regressions
    
    cycle_results = results['cycle_results']
    
    # Check for 500 errors (critical regressions)
    for result in cycle_results:
        if result.get('status_code') == 500:
            regressions.append({
                'type': 'critical',
                'service': result['service_name'],
                'endpoint': result['endpoint'],
                'method': result['method'],
                'status_code': 500,
                'message': 'Server error (500) detected'
            })
    
    # Check for authentication failures
    for result in cycle_results:
        if result.get('status_code') == 401:
            regressions.append({
                'type': 'auth_failure',
                'service': result['service_name'],
                'endpoint': result['endpoint'],
                'method': result['method'],
                'status_code': 401,
                'message': 'Authentication failure'
            })
    
    return regressions

def check_critical_services_health(results: Dict) -> Dict:
    """Check health of critical services"""
    critical_services = ["auth_service", "gateway_service", "ai_modeling_service"]
    service_health = results.get('service_health', {})
    
    critical_status = {}
    for service_name in critical_services:
        health = service_health.get(service_name, {})
        success_rate = health.get('api_success_ratio', 0.0)
        error_rate = health.get('error_rate', 100.0)
        
        critical_status[service_name] = {
            'success_rate': success_rate,
            'error_rate': error_rate,
            'is_healthy': success_rate >= 80.0
        }
    
    return critical_status

def create_email_content(results: Dict, regressions: List[Dict], critical_status: Dict) -> str:
    """Create email content"""
    timestamp = results.get('timestamp', datetime.now().isoformat())
    
    # Calculate overall metrics
    cycle_results = results.get('cycle_results', [])
    total_tests = len(cycle_results)
    successful_tests = sum(1 for r in cycle_results if r.get('success', False))
    overall_success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
    
    # Determine alert level
    has_critical_regressions = any(r['type'] == 'critical' for r in regressions)
    has_critical_service_failures = any(not status['is_healthy'] for status in critical_status.values())
    
    if has_critical_regressions or has_critical_service_failures:
        subject_prefix = "🚨 CRITICAL"
        alert_level = "CRITICAL"
    elif regressions:
        subject_prefix = "⚠️ WARNING"
        alert_level = "WARNING"
    else:
        subject_prefix = "✅ HEALTHY"
        alert_level = "HEALTHY"
    
    # Build email content
    content = f"""
{subject_prefix} ReqArchitect Validation Alert

Validation Run: {timestamp}
Overall Success Rate: {overall_success_rate:.1f}% ({successful_tests}/{total_tests})

ALERT LEVEL: {alert_level}

"""

    # Critical services status
    content += "CRITICAL SERVICES STATUS:\n"
    content += "=" * 30 + "\n"
    for service_name, status in critical_status.items():
        health_icon = "✅" if status['is_healthy'] else "❌"
        content += f"{health_icon} {service_name}: {status['success_rate']:.1f}% success rate\n"
    
    content += "\n"
    
    # Regressions
    if regressions:
        content += "REGRESSIONS DETECTED:\n"
        content += "=" * 25 + "\n"
        for regression in regressions:
            content += f"• {regression['service']} - {regression['method']} {regression['endpoint']}\n"
            content += f"  Status: {regression['status_code']} - {regression['message']}\n"
        content += "\n"
    
    # Service breakdown
    service_health = results.get('service_health', {})
    content += "SERVICE BREAKDOWN:\n"
    content += "=" * 20 + "\n"
    for service_name, health in service_health.items():
        success_rate = health.get('api_success_ratio', 0.0)
        error_rate = health.get('error_rate', 100.0)
        content += f"• {service_name}: {success_rate:.1f}% success, {error_rate:.1f}% error rate\n"
    
    content += f"""

---
This alert was generated automatically by the ReqArchitect validation framework.
For more details, check the validation reports in the CI/CD pipeline.
"""
    
    return content

def send_email(content: str, subject: str):
    """Send email alert"""
    # Get email configuration from environment
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    from_email = os.getenv('FROM_EMAIL', smtp_username) or smtp_username
    to_emails = os.getenv('EMAIL_RECIPIENTS', '').split(',')
    
    if not smtp_username or not smtp_password or not to_emails or not from_email:
        print("Email configuration missing. Skipping email alert.")
        return
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(content, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email alert sent to {', '.join(to_emails)}")
        
    except Exception as e:
        print(f"Failed to send email alert: {e}")

def main():
    """Main function"""
    print("Checking for validation alerts...")
    
    # Load validation results
    results = load_validation_results()
    
    if not results:
        print("No validation results found")
        return
    
    # Check for regressions
    regressions = check_for_regressions(results)
    
    # Check critical services
    critical_status = check_critical_services_health(results)
    
    # Determine if we should send an alert
    has_critical_regressions = any(r['type'] == 'critical' for r in regressions)
    has_critical_service_failures = any(not status['is_healthy'] for status in critical_status.values())
    has_regressions = len(regressions) > 0
    
    # Only send alerts if there are issues
    if not (has_critical_regressions or has_critical_service_failures or has_regressions):
        print("No issues detected. No alert needed.")
        return
    
    # Create email content
    content = create_email_content(results, regressions, critical_status)
    
    # Determine subject
    if has_critical_regressions or has_critical_service_failures:
        subject = "🚨 CRITICAL: ReqArchitect Validation Failures"
    elif has_regressions:
        subject = "⚠️ WARNING: ReqArchitect Validation Issues"
    else:
        subject = "✅ ReqArchitect Validation Status"
    
    # Send email
    send_email(content, subject)

if __name__ == "__main__":
    main() 
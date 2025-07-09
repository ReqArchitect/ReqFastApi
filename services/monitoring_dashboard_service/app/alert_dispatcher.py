#!/usr/bin/env python3
"""
Internal Alert Dispatcher for Monitoring Dashboard Service
Monitors platform status and sends alerts for critical service issues
"""

import asyncio
import aiohttp
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class AlertPayload:
    """Alert payload structure"""
    service_name: str
    status: str
    error_summary: str
    timestamp: str
    critical: bool
    response_time_ms: float
    environment: str

class AlertDispatcher:
    """Internal alert dispatcher for monitoring dashboard"""
    
    def __init__(self, notification_service_url: str = "http://notification_service:8006"):
        self.notification_service_url = notification_service_url
        self.last_alert_time = {}  # Track last alert per service to avoid spam
        self.alert_cooldown = 300  # 5 minutes between alerts for same service
        
    async def check_platform_status(self) -> Dict[str, Any]:
        """Get current platform status from internal endpoint"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:8012/platform/status") as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"Failed to get platform status: HTTP {response.status}")
                        return {}
        except Exception as e:
            logger.error(f"Error getting platform status: {str(e)}")
            return {}
    
    def should_send_alert(self, service_name: str, status: str) -> bool:
        """Determine if we should send an alert for this service status"""
        # Only alert for degraded or unknown critical services
        if status not in ["degraded", "unknown"]:
            return False
            
        # Check cooldown period
        now = datetime.utcnow()
        last_alert = self.last_alert_time.get(service_name)
        
        if last_alert:
            time_since_last = (now - last_alert).total_seconds()
            if time_since_last < self.alert_cooldown:
                logger.info(f"Alert for {service_name} in cooldown period ({time_since_last:.0f}s remaining)")
                return False
        
        return True
    
    def create_alert_payload(self, service_name: str, service_data: Dict, environment: str) -> AlertPayload:
        """Create alert payload for notification service"""
        return AlertPayload(
            service_name=service_name,
            status=service_data.get("status", "unknown"),
            error_summary=service_data.get("error", "No specific error information"),
            timestamp=datetime.utcnow().isoformat(),
            critical=service_data.get("critical", False),
            response_time_ms=service_data.get("response_time_ms", 0),
            environment=environment
        )
    
    async def send_alert(self, alert: AlertPayload) -> bool:
        """Send alert to notification service"""
        try:
            # Prepare notification payload
            notification_payload = {
                "tenant_id": "system-monitoring",
                "user_id": "monitoring-system",
                "type": "email",
                "subject": f"🚨 Critical Service Alert: {alert.service_name}",
                "message": self._format_alert_message(alert),
                "recipient": "ops@reqarchitect.com",
                "priority": "high" if alert.critical else "medium",
                "metadata": {
                    "service_name": alert.service_name,
                    "status": alert.status,
                    "critical": alert.critical,
                    "environment": alert.environment,
                    "response_time_ms": alert.response_time_ms
                }
            }
            
            # Send to notification service
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.notification_service_url}/notification/send",
                    json=notification_payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        logger.info(f"Alert sent successfully for {alert.service_name}")
                        self.last_alert_time[alert.service_name] = datetime.utcnow()
                        return True
                    else:
                        logger.error(f"Failed to send alert: HTTP {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error sending alert for {alert.service_name}: {str(e)}")
            return False
    
    def _format_alert_message(self, alert: AlertPayload) -> str:
        """Format alert message for notification"""
        status_icon = "🔴" if alert.status == "unknown" else "🟡"
        critical_badge = "🚨 CRITICAL" if alert.critical else "⚠️ WARNING"
        
        message = f"""
{status_icon} {critical_badge} SERVICE ALERT

Service: {alert.service_name}
Status: {alert.status.upper()}
Environment: {alert.environment}
Response Time: {alert.response_time_ms}ms
Timestamp: {alert.timestamp}

Error Summary: {alert.error_summary}

This alert was automatically generated by the monitoring dashboard service.
Please investigate the service health immediately.
"""
        return message.strip()
    
    async def process_alerts(self) -> Dict[str, Any]:
        """Process platform status and send alerts for critical issues"""
        logger.info("Processing alerts from platform status...")
        
        # Get current platform status
        platform_status = await self.check_platform_status()
        if not platform_status:
            logger.error("Could not retrieve platform status for alert processing")
            return {"processed": False, "alerts_sent": 0}
        
        environment = platform_status.get("environment", "unknown")
        services = platform_status.get("services", {})
        
        alerts_sent = 0
        critical_issues = []
        
        # Check each service for critical issues
        for service_name, service_data in services.items():
            status = service_data.get("status", "unknown")
            critical = service_data.get("critical", False)
            
            # Only process critical services
            if not critical:
                continue
                
            # Check if we should send an alert
            if self.should_send_alert(service_name, status):
                alert = self.create_alert_payload(service_name, service_data, environment)
                
                # Send alert
                if await self.send_alert(alert):
                    alerts_sent += 1
                    critical_issues.append({
                        "service": service_name,
                        "status": status,
                        "timestamp": alert.timestamp
                    })
                    logger.warning(f"Alert sent for critical service {service_name}: {status}")
                else:
                    logger.error(f"Failed to send alert for {service_name}")
        
        # Log summary
        if critical_issues:
            logger.warning(f"Critical issues detected: {len(critical_issues)} services")
            for issue in critical_issues:
                logger.warning(f"  - {issue['service']}: {issue['status']}")
        else:
            logger.info("No critical issues detected")
        
        return {
            "processed": True,
            "alerts_sent": alerts_sent,
            "critical_issues": critical_issues,
            "total_services_checked": len(services),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def start_monitoring(self, interval_seconds: int = 60):
        """Start continuous monitoring with alert processing"""
        logger.info(f"Starting alert dispatcher with {interval_seconds}s interval")
        
        while True:
            try:
                await self.process_alerts()
                await asyncio.sleep(interval_seconds)
            except Exception as e:
                logger.error(f"Error in alert dispatcher loop: {str(e)}")
                await asyncio.sleep(interval_seconds)

# Global alert dispatcher instance
alert_dispatcher = AlertDispatcher() 
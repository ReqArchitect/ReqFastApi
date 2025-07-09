from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import aiohttp
import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv

# Import alert dispatcher
from .alert_dispatcher import alert_dispatcher

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Audit trail logging
audit_logs = []

app = FastAPI(title="Monitoring Dashboard", version="1.0.0")

# Service configuration with critical services marked
SERVICES = {
    "gateway_service": {"url": "http://gateway_service:8080", "port": 8080, "critical": True},
    "auth_service": {"url": "http://auth_service:8001", "port": 8001, "critical": True},
    "ai_modeling_service": {"url": "http://ai_modeling_service:8002", "port": 8002, "critical": True},
    "usage_service": {"url": "http://usage_service:8005", "port": 8005, "critical": False},
    "notification_service": {"url": "http://notification_service:8006", "port": 8006, "critical": False},
    "audit_log_service": {"url": "http://audit_log_service:8007", "port": 8007, "critical": False},
    "billing_service": {"url": "http://billing_service:8010", "port": 8010, "critical": False},
    "invoice_service": {"url": "http://invoice_service:8011", "port": 8011, "critical": False},
    "monitoring_dashboard_service": {"url": "http://monitoring_dashboard_service:8012", "port": 8012, "critical": False},
}

# In-memory storage for service status with caching
service_status = {}
service_metrics = {}
last_cache_update = None
CACHE_DURATION = 15  # seconds

# Templates setup
templates = Jinja2Templates(directory="app/templates")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/health")
def health_check():
    """Health check endpoint for the monitoring service"""
    return {
        "status": "healthy",
        "service": "monitoring_dashboard",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": get_uptime()
    }

@app.get("/metrics")
def get_metrics():
    """Prometheus-style metrics endpoint"""
    metrics = {
        "service_uptime_seconds": get_uptime(),
        "services_total": len(SERVICES),
        "services_healthy": sum(1 for status in service_status.values() if status.get("status") == "healthy"),
        "services_unhealthy": sum(1 for status in service_status.values() if status.get("status") != "healthy"),
        "last_check_timestamp": time.time()
    }
    
    # Add per-service metrics
    for service_name, status in service_status.items():
        metrics[f"service_{service_name}_status"] = 1 if status.get("status") == "healthy" else 0
        metrics[f"service_{service_name}_response_time_ms"] = status.get("response_time", 0)
    
    return metrics

async def check_service_health(service_name: str, service_config: Dict) -> Dict:
    """Check health of a single service"""
    start_time = time.time()
    status = {
        "service": service_name,
        "url": service_config["url"],
        "status": "unknown",
        "last_check": datetime.utcnow().isoformat(),
        "response_time": 0,
        "error": None,
        "critical": service_config.get("critical", False)
    }
    
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Check health endpoint
            async with session.get(f"{service_config['url']}/health") as response:
                response_time = round((time.time() - start_time) * 1000, 2)
                status["response_time"] = response_time
                
                if response.status == 200:
                    data = await response.json()
                    status["status"] = data.get("status", "healthy")
                    
                    # Log anomalies
                    if response_time > 1000:  # > 1 second
                        logger.warning(f"Slow response from {service_name}: {response_time}ms")
                    
                else:
                    status["status"] = "unhealthy"
                    status["error"] = f"HTTP {response.status}"
                    logger.error(f"Health check failed for {service_name}: HTTP {response.status}")
            
            # Check metrics endpoint if health is successful
            if status["status"] == "healthy":
                try:
                    async with session.get(f"{service_config['url']}/metrics") as metrics_response:
                        if metrics_response.status == 200:
                            metrics_data = await metrics_response.json()
                            status["metrics"] = metrics_data
                        else:
                            status["metrics_error"] = f"HTTP {metrics_response.status}"
                except Exception as e:
                    status["metrics_error"] = str(e)
                    
    except asyncio.TimeoutError:
        status["status"] = "timeout"
        status["error"] = "Request timeout"
        status["response_time"] = round((time.time() - start_time) * 1000, 2)
        logger.error(f"Timeout checking {service_name}")
    except Exception as e:
        status["status"] = "unhealthy"
        status["error"] = str(e)
        status["response_time"] = round((time.time() - start_time) * 1000, 2)
        logger.error(f"Error checking {service_name}: {str(e)}")
    
    return status

async def check_all_services():
    """Check health of all services concurrently"""
    global last_cache_update
    
    tasks = []
    for service_name, service_config in SERVICES.items():
        task = check_service_health(service_name, service_config)
        tasks.append(task)
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, (service_name, _) in enumerate(SERVICES.items()):
        if isinstance(results[i], Exception):
            service_status[service_name] = {
                "service": service_name,
                "status": "error",
                "error": str(results[i]),
                "last_check": datetime.utcnow().isoformat(),
                "response_time": 0,
                "critical": SERVICES[service_name].get("critical", False)
            }
        else:
            service_status[service_name] = results[i]
    
    last_cache_update = datetime.utcnow()

def is_cache_valid() -> bool:
    """Check if cached data is still valid"""
    if last_cache_update is None:
        return False
    return (datetime.utcnow() - last_cache_update).total_seconds() < CACHE_DURATION

@app.get("/platform/status")
async def get_platform_status(
    critical_only: bool = Query(False, description="Return only critical services"),
    include_metrics: bool = Query(True, description="Include detailed metrics"),
    force_refresh: bool = Query(False, description="Force refresh cache")
):
    """
    Get aggregated platform status from all microservices.
    
    Returns a structured JSON summary with health status, uptime, and metrics.
    Supports caching for 15 seconds to reduce service pressure.
    """
    
    # Check if we need to refresh cache
    if force_refresh or not is_cache_valid():
        logger.info("Refreshing platform status cache")
        await check_all_services()
    else:
        logger.info("Using cached platform status")
    
    # Calculate success rates and uptime
    total_services = len(service_status)
    healthy_services = sum(1 for status in service_status.values() if status.get("status") == "healthy")
    critical_services = sum(1 for status in service_status.values() if status.get("critical", False))
    healthy_critical = sum(1 for status in service_status.values() 
                          if status.get("status") == "healthy" and status.get("critical", False))
    
    success_rate = (healthy_services / total_services * 100) if total_services > 0 else 0
    critical_success_rate = (healthy_critical / critical_services * 100) if critical_services > 0 else 0
    
    # Build response
    response = {
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("VALIDATION_ENV", "development"),
        "cache_info": {
            "last_update": last_cache_update.isoformat() if last_cache_update else None,
            "cache_valid": is_cache_valid(),
            "cache_duration_seconds": CACHE_DURATION
        },
        "summary": {
            "total_services": total_services,
            "healthy_services": healthy_services,
            "unhealthy_services": total_services - healthy_services,
            "critical_services": critical_services,
            "healthy_critical_services": healthy_critical,
            "success_rate": round(success_rate, 2),
            "critical_success_rate": round(critical_success_rate, 2),
            "overall_status": "healthy" if success_rate >= 80 else "degraded" if success_rate >= 50 else "unhealthy"
        },
        "services": {}
    }
    
    # Filter services based on critical_only parameter
    filtered_services = service_status
    if critical_only:
        filtered_services = {name: status for name, status in service_status.items() 
                           if status.get("critical", False)}
        response["summary"]["filtered_services"] = len(filtered_services)
    
    # Build service status summary
    for service_name, status in filtered_services.items():
        service_summary = {
            "status": status.get("status", "unknown"),
            "response_time_ms": status.get("response_time", 0),
            "last_check": status.get("last_check"),
            "critical": status.get("critical", False)
        }
        
        # Add error information if present
        if status.get("error"):
            service_summary["error"] = status.get("error")
        
        # Add uptime if available in metrics
        if include_metrics and status.get("metrics"):
            metrics = status.get("metrics", {})
            if "uptime" in metrics:
                service_summary["uptime"] = metrics["uptime"]
            if "service_uptime_seconds" in metrics:
                service_summary["uptime_seconds"] = metrics["service_uptime_seconds"]
        
        # Add success rate if available
        if status.get("status") == "healthy":
            service_summary["success_rate"] = "100%"
        elif status.get("status") == "degraded":
            service_summary["success_rate"] = "50-80%"
        else:
            service_summary["success_rate"] = "0%"
        
        response["services"][service_name] = service_summary
    
    # Log anomalies
    slow_services = [name for name, status in filtered_services.items() 
                    if status.get("response_time", 0) > 1000]
    if slow_services:
        logger.warning(f"Slow services detected: {slow_services}")
    
    error_services = [name for name, status in filtered_services.items() 
                     if status.get("status") != "healthy"]
    if error_services:
        logger.error(f"Unhealthy services detected: {error_services}")
    
    return response

@app.get("/api/status")
async def get_service_status():
    """API endpoint to get current service status"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "services": service_status,
        "summary": {
            "total": len(SERVICES),
            "healthy": sum(1 for status in service_status.values() if status.get("status") == "healthy"),
            "unhealthy": sum(1 for status in service_status.values() if status.get("status") != "healthy")
        }
    }

@app.post("/api/check")
async def trigger_health_check(background_tasks: BackgroundTasks):
    """Trigger a health check of all services"""
    background_tasks.add_task(check_all_services)
    return {"message": "Health check triggered", "timestamp": datetime.utcnow().isoformat()}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard page"""
    # Trigger health check if no recent data
    if not service_status or (datetime.utcnow() - datetime.fromisoformat(list(service_status.values())[0]["last_check"].replace('Z', '+00:00'))).seconds > 60:
        await check_all_services()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "services": service_status,
        "timestamp": datetime.utcnow().isoformat(),
        "summary": {
            "total": len(SERVICES),
            "healthy": sum(1 for status in service_status.values() if status.get("status") == "healthy"),
            "unhealthy": sum(1 for status in service_status.values() if status.get("status") != "healthy")
        }
    })

@app.post("/api/log")
async def log_event(request: Request):
    """Log events for audit trail"""
    try:
        log_data = await request.json()
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": log_data.get("event", "unknown"),
            "user_agent": log_data.get("user_agent", ""),
            "data": log_data,
            "ip_address": request.client.host if request.client else "unknown"
        }
        
        # Store in memory (in production, this would go to a database)
        audit_logs.append(log_entry)
        
        # Keep only last 1000 logs to prevent memory issues
        if len(audit_logs) > 1000:
            audit_logs.pop(0)
        
        logger.info(f"Audit log: {log_data.get('event', 'unknown')} from {request.client.host}")
        
        return {"status": "logged", "timestamp": log_entry["timestamp"]}
        
    except Exception as e:
        logger.error(f"Error logging event: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to log event")

@app.get("/api/logs")
async def get_audit_logs(
    limit: int = Query(100, description="Number of logs to return"),
    event_type: Optional[str] = Query(None, description="Filter by event type")
):
    """Get audit logs (for monitoring purposes)"""
    filtered_logs = audit_logs
    
    if event_type:
        filtered_logs = [log for log in audit_logs if log.get("event") == event_type]
    
    return {
        "logs": filtered_logs[-limit:],
        "total_logs": len(audit_logs),
        "filtered_count": len(filtered_logs)
    }

@app.post("/api/alerts/process")
async def process_alerts():
    """Manually trigger alert processing"""
    try:
        result = await alert_dispatcher.process_alerts()
        logger.info(f"Alert processing completed: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process alerts")

@app.get("/api/alerts/status")
async def get_alert_status():
    """Get alert dispatcher status"""
    return {
        "dispatcher_active": True,
        "last_alert_times": alert_dispatcher.last_alert_time,
        "cooldown_period": alert_dispatcher.alert_cooldown,
        "notification_service_url": alert_dispatcher.notification_service_url
    }

def get_uptime() -> float:
    """Get service uptime in seconds"""
    if not hasattr(app.state, 'start_time'):
        app.state.start_time = time.time()
    return time.time() - app.state.start_time

@app.on_event("startup")
async def startup_event():
    """Initialize the monitoring service"""
    app.state.start_time = time.time()
    # Initial health check
    await check_all_services()
    
    # Start alert dispatcher in background
    asyncio.create_task(alert_dispatcher.start_monitoring(interval_seconds=60))
    logger.info("Alert dispatcher started in background")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    pass 
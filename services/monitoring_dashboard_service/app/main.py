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

app = FastAPI(title="Enhanced Monitoring Dashboard", version="2.0.0")

# API Debug Service URL
API_DEBUG_URL = os.getenv("API_DEBUG_URL", "http://api_debug_service:8090")

# Service configuration with critical services marked
SERVICES = {
    "gateway_service": {"url": "http://gateway_service:8080", "port": 8080, "critical": True, "layer": "infrastructure"},
    "auth_service": {"url": "http://auth_service:8001", "port": 8001, "critical": True, "layer": "security"},
    "ai_modeling_service": {"url": "http://ai_modeling_service:8002", "port": 8002, "critical": True, "layer": "application"},
    "usage_service": {"url": "http://usage_service:8005", "port": 8005, "critical": False, "layer": "business"},
    "notification_service": {"url": "http://notification_service:8006", "port": 8006, "critical": False, "layer": "application"},
    "audit_log_service": {"url": "http://audit_log_service:8007", "port": 8007, "critical": False, "layer": "security"},
    "billing_service": {"url": "http://billing_service:8010", "port": 8010, "critical": False, "layer": "business"},
    "invoice_service": {"url": "http://invoice_service:8011", "port": 8011, "critical": False, "layer": "business"},
    "monitoring_dashboard_service": {"url": "http://monitoring_dashboard_service:8012", "port": 8012, "critical": False, "layer": "infrastructure"},
}

# In-memory storage for service status with caching
service_status = {}
service_metrics = {}
discovered_services = {}
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
        "services_total": len(discovered_services),
        "services_healthy": sum(1 for status in discovered_services.values() if status.get("status") == "healthy"),
        "services_unhealthy": sum(1 for status in discovered_services.values() if status.get("status") != "healthy"),
        "services_virtual": sum(1 for status in discovered_services.values() if status.get("is_virtual", False)),
        "last_check_timestamp": time.time()
    }
    
    # Add per-service metrics
    for service_name, status in discovered_services.items():
        metrics[f"service_{service_name}_status"] = 1 if status.get("status") == "healthy" else 0
        metrics[f"service_{service_name}_response_time_ms"] = status.get("response_time", 0)
    
    return metrics

async def fetch_api_debug_data() -> Dict:
    """Fetch comprehensive service data from api_debug_service"""
    try:
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            # Fetch all services
            async with session.get(f"{API_DEBUG_URL}/api-debug") as response:
                if response.status == 200:
                    services_data = await response.json()
                else:
                    logger.error(f"Failed to fetch services from api_debug: HTTP {response.status}")
                    return {}
            
            # Fetch health summary
            async with session.get(f"{API_DEBUG_URL}/api-debug/health-summary") as response:
                if response.status == 200:
                    health_summary = await response.json()
                else:
                    logger.error(f"Failed to fetch health summary from api_debug: HTTP {response.status}")
                    health_summary = {}
            
            # Fetch catalog
            async with session.get(f"{API_DEBUG_URL}/api-debug/catalog") as response:
                if response.status == 200:
                    catalog_data = await response.json()
                else:
                    logger.error(f"Failed to fetch catalog from api_debug: HTTP {response.status}")
                    catalog_data = {}
            
            return {
                "services": services_data,
                "health_summary": health_summary,
                "catalog": catalog_data
            }
    except Exception as e:
        logger.error(f"Error fetching data from api_debug_service: {str(e)}")
        return {}

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
        "critical": service_config.get("critical", False),
        "layer": service_config.get("layer", "unknown")
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
    global last_cache_update, discovered_services
    
    # First, fetch data from api_debug_service
    api_debug_data = await fetch_api_debug_data()
    
    # Process discovered services
    discovered_services = {}
    if api_debug_data.get("services"):
        for service in api_debug_data["services"]:
            service_name = service.get("service_name", "")
            if service_name:
                discovered_services[service_name] = {
                    "service_name": service_name,
                    "docker_container_name": service.get("docker_container_name", ""),
                    "base_url": service.get("base_url", ""),
                    "status": service.get("status", "unknown"),
                    "discovery_method": service.get("discovery_method", "unknown"),
                    "port": service.get("port", 0),
                    "is_virtual": service.get("is_virtual", False),
                    "last_heartbeat": service.get("last_heartbeat", ""),
                    "catalog_entry": service.get("catalog_entry", {}),
                    "error_details": service.get("error_details", ""),
                    "layer": service.get("catalog_entry", {}).get("description", "").split()[0].lower() if service.get("catalog_entry", {}).get("description") else "unknown"
                }
    
    # Check health of running services
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
    total_services = len(discovered_services)
    healthy_services = sum(1 for status in discovered_services.values() if status.get("status") == "healthy")
    virtual_services = sum(1 for status in discovered_services.values() if status.get("is_virtual", False))
    critical_services = sum(1 for status in discovered_services.values() if status.get("critical", False))
    healthy_critical = sum(1 for status in discovered_services.values() 
                          if status.get("status") == "healthy" and status.get("critical", False))
    
    success_rate = (healthy_services / total_services * 100) if total_services > 0 else 0
    critical_success_rate = (healthy_critical / critical_services * 100) if critical_services > 0 else 0
    
    # Group services by layer
    services_by_layer = {}
    for service_name, service_data in discovered_services.items():
        layer = service_data.get("layer", "unknown")
        if layer not in services_by_layer:
            services_by_layer[layer] = []
        services_by_layer[layer].append({
            "service_name": service_name,
            "status": service_data.get("status", "unknown"),
            "port": service_data.get("port", 0),
            "base_url": service_data.get("base_url", ""),
            "discovery_method": service_data.get("discovery_method", "unknown"),
            "is_virtual": service_data.get("is_virtual", False),
            "last_heartbeat": service_data.get("last_heartbeat", ""),
            "response_time": service_data.get("response_time", 0),
            "error_details": service_data.get("error_details", ""),
            "description": service_data.get("catalog_entry", {}).get("description", "")
        })
    
    # Build response
    response_data = {
        "summary": {
            "total_services": total_services,
            "healthy_services": healthy_services,
            "unhealthy_services": total_services - healthy_services,
            "virtual_services": virtual_services,
            "critical_services": critical_services,
            "healthy_critical": healthy_critical,
            "success_rate": round((healthy_services / total_services * 100), 2) if total_services > 0 else 0,
            "critical_success_rate": round((healthy_critical / critical_services * 100), 2) if critical_services > 0 else 0,
            "last_update": last_cache_update.isoformat() if last_cache_update else None,
            "cache_valid": is_cache_valid()
        },
        "services": discovered_services,
        "services_by_layer": services_by_layer,
        "layers": list(services_by_layer.keys())
    }
    
    if include_metrics:
        response_data["metrics"] = service_metrics
    
    if critical_only:
        response_data["services"] = {
            name: data for name, data in discovered_services.items() 
            if data.get("critical", False)
        }
    
    return response_data

@app.get("/api/services")
async def get_all_services(
    layer: Optional[str] = Query(None, description="Filter by architectural layer"),
    status: Optional[str] = Query(None, description="Filter by health status"),
    discovery_method: Optional[str] = Query(None, description="Filter by discovery method"),
    force_refresh: bool = Query(False, description="Force refresh cache")
):
    """
    Get all discovered services with filtering options.
    
    Supports filtering by layer, status, and discovery method.
    """
    if force_refresh or not is_cache_valid():
        await check_all_services()
    
    services = list(discovered_services.values())
    
    # Apply filters
    if layer:
        services = [s for s in services if s.get("layer", "").lower() == layer.lower()]
    
    if status:
        services = [s for s in services if s.get("status", "").lower() == status.lower()]
    
    if discovery_method:
        services = [s for s in services if s.get("discovery_method", "").lower() == discovery_method.lower()]
    
    return {
        "services": services,
        "total": len(services),
        "filters_applied": {
            "layer": layer,
            "status": status,
            "discovery_method": discovery_method
        }
    }

@app.get("/api/services/{service_name}")
async def get_service_details(
    service_name: str,
    force_refresh: bool = Query(False, description="Force refresh cache")
):
    """
    Get detailed information about a specific service.
    """
    if force_refresh or not is_cache_valid():
        await check_all_services()
    
    service_data = discovered_services.get(service_name)
    if not service_data:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    # Add additional details if available
    service_data["endpoints"] = {
        "health": f"{service_data.get('base_url', '')}/health",
        "docs": f"{service_data.get('base_url', '')}/docs",
        "openapi": f"{service_data.get('base_url', '')}/openapi.json",
        "metrics": f"{service_data.get('base_url', '')}/metrics"
    }
    
    return service_data

@app.get("/api/layers")
async def get_architectural_layers():
    """
    Get all architectural layers and their service counts.
    """
    if not is_cache_valid():
        await check_all_services()
    
    layers = {}
    for service_data in discovered_services.values():
        layer = service_data.get("layer", "unknown")
        if layer not in layers:
            layers[layer] = {
                "name": layer,
                "services": [],
                "healthy_count": 0,
                "total_count": 0
            }
        
        layers[layer]["services"].append(service_data["service_name"])
        layers[layer]["total_count"] += 1
        if service_data.get("status") == "healthy":
            layers[layer]["healthy_count"] += 1
    
    return {
        "layers": list(layers.values()),
        "total_layers": len(layers)
    }

@app.get("/api/status")
async def get_service_status():
    """
    Legacy endpoint for backward compatibility.
    """
    return await get_platform_status()

@app.post("/api/check")
async def trigger_health_check(background_tasks: BackgroundTasks):
    """
    Trigger a manual health check of all services.
    """
    background_tasks.add_task(check_all_services)
    return {"message": "Health check triggered", "timestamp": datetime.utcnow().isoformat()}

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Enhanced monitoring dashboard with real-time service status.
    """
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "api_debug_url": API_DEBUG_URL
    })

@app.post("/api/log")
async def log_event(request: Request):
    """
    Log audit events for the monitoring dashboard.
    """
    try:
        event_data = await request.json()
        event_data["timestamp"] = datetime.utcnow().isoformat()
        event_data["source"] = "monitoring_dashboard"
        
        audit_logs.append(event_data)
        
        # Keep only last 1000 logs
        if len(audit_logs) > 1000:
            audit_logs.pop(0)
        
        logger.info(f"Audit log: {event_data.get('event', 'unknown')}")
        
        return {"status": "logged", "timestamp": event_data["timestamp"]}
        
    except Exception as e:
        logger.error(f"Error logging event: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid log data")

@app.get("/api/logs")
async def get_audit_logs(
    limit: int = Query(100, description="Number of logs to return"),
    event_type: Optional[str] = Query(None, description="Filter by event type")
):
    """
    Get audit logs with optional filtering.
    """
    logs = audit_logs.copy()
    
    if event_type:
        logs = [log for log in logs if log.get("event") == event_type]
    
    return {
        "logs": logs[-limit:],
        "total": len(logs),
        "filtered_by": event_type
    }

@app.post("/api/alerts/process")
async def process_alerts():
    """
    Process and dispatch alerts based on current service status.
    """
    try:
        # Get current status
        if not is_cache_valid():
            await check_all_services()
        
        # Process alerts
        alert_results = await alert_dispatcher.process_alerts(discovered_services)
        
        return {
            "status": "processed",
            "alerts_generated": len(alert_results),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Alert processing failed")

@app.get("/api/alerts/status")
async def get_alert_status():
    """
    Get current alert status and configuration.
    """
    return {
        "alert_system": "active",
        "last_processed": datetime.utcnow().isoformat(),
        "configuration": alert_dispatcher.get_config()
    }

def get_uptime() -> float:
    """Get service uptime in seconds"""
    if not hasattr(app.state, 'start_time'):
        app.state.start_time = time.time()
    return time.time() - app.state.start_time

@app.on_event("startup")
async def startup_event():
    """Initialize the monitoring service on startup"""
    logger.info("Enhanced Monitoring Dashboard starting up...")
    app.state.start_time = time.time()
    
    # Initial health check
    await check_all_services()
    
    logger.info(f"Monitoring Dashboard ready. Discovered {len(discovered_services)} services.")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Enhanced Monitoring Dashboard shutting down...") 
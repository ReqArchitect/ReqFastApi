from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import aiohttp
import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Monitoring Dashboard", version="1.0.0")

# Service configuration
SERVICES = {
    "gateway_service": {"url": "http://gateway_service:8080", "port": 8080},
    "auth_service": {"url": "http://auth_service:8001", "port": 8001},
    "ai_modeling_service": {"url": "http://ai_modeling_service:8002", "port": 8002},
    "usage_service": {"url": "http://usage_service:8000", "port": 8000},
    "billing_service": {"url": "http://billing_service:8010", "port": 8010},
    "invoice_service": {"url": "http://invoice_service:8011", "port": 8010},
    "notification_service": {"url": "http://notification_service:8000", "port": 8000},
}

# In-memory storage for service status
service_status = {}
service_metrics = {}

# Templates setup
templates = Jinja2Templates(directory="app/templates")

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
        "error": None
    }
    
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{service_config['url']}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    status["status"] = data.get("status", "healthy")
                    status["response_time"] = round((time.time() - start_time) * 1000, 2)
                else:
                    status["status"] = "unhealthy"
                    status["error"] = f"HTTP {response.status}"
    except Exception as e:
        status["status"] = "unhealthy"
        status["error"] = str(e)
        status["response_time"] = round((time.time() - start_time) * 1000, 2)
    
    return status

async def check_all_services():
    """Check health of all services concurrently"""
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
                "response_time": 0
            }
        else:
            service_status[service_name] = results[i]

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

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    pass 
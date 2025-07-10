from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import structlog
from typing import List, Optional
from datetime import datetime

from .models import (
    ServiceEndpointMap, HealthSummary, ServiceDiscoveryConfig,
    ServiceStatus, EndpointDiscoveryResult
)
from .service_discovery import ServiceDiscoveryOrchestrator

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Create FastAPI app
app = FastAPI(
    title="API Debug Service",
    description="Non-intrusive service for discovering and visualizing API endpoints across ReqArchitect microservices",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service discovery
config = ServiceDiscoveryConfig()
discovery_orchestrator = ServiceDiscoveryOrchestrator(config)


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("API Debug Service starting up")
    logger.info(f"Configuration: {config.dict()}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("API Debug Service shutting down")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "api_debug_service",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.get("/metrics", tags=["Monitoring"])
async def get_metrics():
    """Get service metrics."""
    try:
        stats = discovery_orchestrator.get_discovery_stats()
        return {
            "service": "api_debug_service",
            "timestamp": datetime.now().isoformat(),
            "stats": stats
        }
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail="Error getting metrics")


@app.get("/api-debug", tags=["API Debug"], response_model=List[ServiceEndpointMap])
async def get_all_service_endpoints(
    use_cache: bool = Query(True, description="Use cached data if available"),
    refresh: bool = Query(False, description="Force refresh cache")
):
    """
    Get endpoint map for all ReqArchitect services.
    
    Returns a comprehensive list of all discovered services with their endpoints,
    health status, and metadata.
    """
    try:
        if refresh:
            await discovery_orchestrator.refresh_cache()
        
        services = await discovery_orchestrator.discover_all_services(use_cache=use_cache)
        
        logger.info(f"Retrieved {len(services)} services")
        return services
        
    except Exception as e:
        logger.error(f"Error getting all service endpoints: {e}")
        raise HTTPException(status_code=500, detail="Error discovering services")


@app.get("/api-debug/{service_name}", tags=["API Debug"], response_model=ServiceEndpointMap)
async def get_service_endpoints(
    service_name: str,
    use_cache: bool = Query(True, description="Use cached data if available")
):
    """
    Get detailed endpoint list for a specific service.
    
    Returns comprehensive information about a specific service including
    all discovered endpoints, health status, and container information.
    """
    try:
        service = await discovery_orchestrator.discover_service(service_name, use_cache=use_cache)
        
        if not service:
            raise HTTPException(
                status_code=404, 
                detail=f"Service '{service_name}' not found or not accessible"
            )
        
        logger.info(f"Retrieved endpoints for service: {service_name}")
        return service
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting endpoints for service {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Error discovering service endpoints")


@app.get("/api-debug/health-summary", tags=["API Debug"], response_model=HealthSummary)
async def get_health_summary(
    use_cache: bool = Query(True, description="Use cached data if available"),
    refresh: bool = Query(False, description="Force refresh cache")
):
    """
    Get comprehensive health summary of all services.
    
    Returns a summary of service health including counts of healthy/unhealthy
    services and detailed health information for each service.
    """
    try:
        if refresh:
            await discovery_orchestrator.refresh_cache()
        
        summary = await discovery_orchestrator.get_health_summary(use_cache=use_cache)
        
        logger.info(f"Health summary: {summary.healthy_services}/{summary.total_services} healthy")
        return summary
        
    except Exception as e:
        logger.error(f"Error getting health summary: {e}")
        raise HTTPException(status_code=500, detail="Error getting health summary")


@app.get("/api-debug/{service_name}/details", tags=["API Debug"])
async def get_service_details(
    service_name: str,
    include_logs: bool = Query(True, description="Include container logs"),
    log_lines: int = Query(20, description="Number of log lines to include")
):
    """
    Get detailed information about a specific service.
    
    Returns comprehensive service information including container details,
    logs, network information, and cache statistics.
    """
    try:
        details = await discovery_orchestrator.get_service_details(service_name)
        
        if not details:
            raise HTTPException(
                status_code=404,
                detail=f"Service '{service_name}' not found or not accessible"
            )
        
        # Limit log lines if requested
        if not include_logs:
            details["logs"] = []
        elif "logs" in details and len(details["logs"]) > log_lines:
            details["logs"] = details["logs"][-log_lines:]
        
        logger.info(f"Retrieved detailed information for service: {service_name}")
        return details
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting details for service {service_name}: {e}")
        raise HTTPException(status_code=500, detail="Error getting service details")


@app.post("/api-debug/refresh", tags=["API Debug"])
async def refresh_cache():
    """
    Force refresh of all cached data.
    
    Invalidates all cached service discovery data and re-discovers
    all services and their endpoints.
    """
    try:
        success = await discovery_orchestrator.refresh_cache()
        
        if success:
            logger.info("Cache refreshed successfully")
            return {"message": "Cache refreshed successfully", "status": "success"}
        else:
            logger.error("Failed to refresh cache")
            raise HTTPException(status_code=500, detail="Failed to refresh cache")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing cache: {e}")
        raise HTTPException(status_code=500, detail="Error refreshing cache")


@app.get("/api-debug/stats", tags=["API Debug"])
async def get_discovery_stats():
    """
    Get discovery service statistics.
    
    Returns detailed statistics about the discovery service including
    cache information, network details, and configuration.
    """
    try:
        stats = discovery_orchestrator.get_discovery_stats()
        
        logger.info("Retrieved discovery statistics")
        return stats
        
    except Exception as e:
        logger.error(f"Error getting discovery stats: {e}")
        raise HTTPException(status_code=500, detail="Error getting discovery statistics")


@app.get("/api-debug/services/healthy", tags=["API Debug"], response_model=List[ServiceEndpointMap])
async def get_healthy_services():
    """
    Get only healthy services.
    
    Returns a list of all services that are currently healthy.
    """
    try:
        all_services = await discovery_orchestrator.discover_all_services()
        healthy_services = [s for s in all_services if s.status == ServiceStatus.HEALTHY]
        
        logger.info(f"Retrieved {len(healthy_services)} healthy services")
        return healthy_services
        
    except Exception as e:
        logger.error(f"Error getting healthy services: {e}")
        raise HTTPException(status_code=500, detail="Error getting healthy services")


@app.get("/api-debug/services/unhealthy", tags=["API Debug"], response_model=List[ServiceEndpointMap])
async def get_unhealthy_services():
    """
    Get only unhealthy services.
    
    Returns a list of all services that are currently unhealthy.
    """
    try:
        all_services = await discovery_orchestrator.discover_all_services()
        unhealthy_services = [s for s in all_services if s.status == ServiceStatus.UNHEALTHY]
        
        logger.info(f"Retrieved {len(unhealthy_services)} unhealthy services")
        return unhealthy_services
        
    except Exception as e:
        logger.error(f"Error getting unhealthy services: {e}")
        raise HTTPException(status_code=500, detail="Error getting unhealthy services")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 
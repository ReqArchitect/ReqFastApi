# Gateway Service Models
# This file contains data models for the gateway service

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ServiceHealth(BaseModel):
    """Health check response model"""
    status: str
    service: str
    timestamp: datetime
    uptime: float
    version: str = "1.0.0"
    environment: str = "development"

class ServiceMetrics(BaseModel):
    """Metrics response model"""
    uptime_seconds: float
    requests_total: int = 0
    errors_total: int = 0
    active_connections: int = 0

class ProxyRequest(BaseModel):
    """Proxy request model"""
    service: str
    path: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    body: Optional[Any] = None

class ProxyResponse(BaseModel):
    """Proxy response model"""
    status_code: int
    headers: Dict[str, str]
    body: Any
    service: str
    response_time: float 
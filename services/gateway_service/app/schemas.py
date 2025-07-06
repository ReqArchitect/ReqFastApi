# Gateway Service Schemas
# This file contains Pydantic schemas for the gateway service

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    service: str
    timestamp: str
    uptime: float
    version: str
    environment: str

class MetricsResponse(BaseModel):
    """Metrics response schema"""
    gateway_uptime_seconds: float
    gateway_requests_total: int
    gateway_errors_total: int
    gateway_active_connections: int

class ProxyRequestSchema(BaseModel):
    """Proxy request schema"""
    service: str
    path: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    body: Optional[Any] = None

class ProxyResponseSchema(BaseModel):
    """Proxy response schema"""
    status_code: int
    headers: Dict[str, str]
    body: Any
    service: str
    response_time: float 
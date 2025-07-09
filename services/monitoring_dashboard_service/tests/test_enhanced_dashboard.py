#!/usr/bin/env python3
"""
Enhanced Monitoring Dashboard Service Tests
Tests for alert dispatcher, frontend panel, and logging functionality
"""

import pytest
import asyncio
import aiohttp
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

# Import the application
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from main import app
from alert_dispatcher import AlertDispatcher, AlertPayload

# Test client
client = TestClient(app)

class TestAlertDispatcher:
    """Test alert dispatcher functionality"""
    
    def test_alert_payload_creation(self):
        """Test alert payload creation"""
        service_data = {
            "status": "degraded",
            "error": "Connection timeout",
            "critical": True,
            "response_time_ms": 2500
        }
        
        alert = AlertPayload(
            service_name="test_service",
            status="degraded",
            error_summary="Connection timeout",
            timestamp="2024-01-01T12:00:00Z",
            critical=True,
            response_time_ms=2500,
            environment="test"
        )
        
        assert alert.service_name == "test_service"
        assert alert.status == "degraded"
        assert alert.critical is True
        assert alert.response_time_ms == 2500
    
    def test_should_send_alert_logic(self):
        """Test alert sending logic"""
        dispatcher = AlertDispatcher()
        
        # Should not send alert for healthy status
        assert not dispatcher.should_send_alert("test_service", "healthy")
        
        # Should send alert for degraded status
        assert dispatcher.should_send_alert("test_service", "degraded")
        
        # Should send alert for unknown status
        assert dispatcher.should_send_alert("test_service", "unknown")
        
        # Test cooldown period
        dispatcher.last_alert_time["test_service"] = datetime.utcnow()
        assert not dispatcher.should_send_alert("test_service", "degraded")
    
    @patch('aiohttp.ClientSession')
    async def test_send_alert_success(self, mock_session):
        """Test successful alert sending"""
        dispatcher = AlertDispatcher()
        alert = AlertPayload(
            service_name="test_service",
            status="degraded",
            error_summary="Test error",
            timestamp="2024-01-01T12:00:00Z",
            critical=True,
            response_time_ms=1000,
            environment="test"
        )
        
        # Mock successful response
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        
        result = await dispatcher.send_alert(alert)
        assert result is True
        assert "test_service" in dispatcher.last_alert_time
    
    @patch('aiohttp.ClientSession')
    async def test_send_alert_failure(self, mock_session):
        """Test failed alert sending"""
        dispatcher = AlertDispatcher()
        alert = AlertPayload(
            service_name="test_service",
            status="degraded",
            error_summary="Test error",
            timestamp="2024-01-01T12:00:00Z",
            critical=True,
            response_time_ms=1000,
            environment="test"
        )
        
        # Mock failed response
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_response
        
        result = await dispatcher.send_alert(alert)
        assert result is False
    
    def test_alert_message_formatting(self):
        """Test alert message formatting"""
        dispatcher = AlertDispatcher()
        alert = AlertPayload(
            service_name="auth_service",
            status="degraded",
            error_summary="Database connection failed",
            timestamp="2024-01-01T12:00:00Z",
            critical=True,
            response_time_ms=3000,
            environment="production"
        )
        
        message = dispatcher._format_alert_message(alert)
        
        assert "🟡" in message
        assert "🚨 CRITICAL" in message
        assert "auth_service" in message
        assert "degraded" in message.upper()
        assert "Database connection failed" in message
        assert "3000ms" in message

class TestDashboardEndpoints:
    """Test dashboard endpoints"""
    
    def test_log_event_endpoint(self):
        """Test audit log endpoint"""
        log_data = {
            "event": "panel_load",
            "user_agent": "Mozilla/5.0",
            "services_count": 5,
            "critical_only": False
        }
        
        response = client.post("/api/log", json=log_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "logged"
        assert "timestamp" in data
    
    def test_get_audit_logs(self):
        """Test getting audit logs"""
        # First, add some test logs
        test_logs = [
            {"event": "panel_load", "user_agent": "test1"},
            {"event": "page_load", "user_agent": "test2"},
            {"event": "panel_load", "user_agent": "test3"}
        ]
        
        for log in test_logs:
            client.post("/api/log", json=log)
        
        # Test getting all logs
        response = client.get("/api/logs")
        assert response.status_code == 200
        
        data = response.json()
        assert "logs" in data
        assert "total_logs" in data
        
        # Test filtering by event type
        response = client.get("/api/logs?event_type=panel_load")
        assert response.status_code == 200
        
        data = response.json()
        assert all(log["data"]["event"] == "panel_load" for log in data["logs"])
    
    def test_alert_status_endpoint(self):
        """Test alert status endpoint"""
        response = client.get("/api/alerts/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "dispatcher_active" in data
        assert "last_alert_times" in data
        assert "cooldown_period" in data
        assert "notification_service_url" in data
    
    @patch('main.alert_dispatcher')
    def test_process_alerts_endpoint(self, mock_dispatcher):
        """Test manual alert processing endpoint"""
        mock_dispatcher.process_alerts.return_value = {
            "processed": True,
            "alerts_sent": 2,
            "critical_issues": [
                {"service": "auth_service", "status": "degraded"}
            ]
        }
        
        response = client.post("/api/alerts/process")
        assert response.status_code == 200
        
        data = response.json()
        assert data["processed"] is True
        assert data["alerts_sent"] == 2

class TestFrontendPanel:
    """Test frontend panel functionality"""
    
    def test_dashboard_page_load(self):
        """Test dashboard page loads correctly"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "ReqArchitect Platform Monitor" in response.text
    
    def test_static_files_served(self):
        """Test static files are served correctly"""
        response = client.get("/static/dashboard.js")
        assert response.status_code == 200
        assert "text/javascript" in response.headers["content-type"]
    
    def test_platform_status_api(self):
        """Test platform status API with different parameters"""
        # Test without parameters
        response = client.get("/platform/status")
        assert response.status_code == 200
        
        data = response.json()
        assert "timestamp" in data
        assert "environment" in data
        assert "summary" in data
        assert "services" in data
        
        # Test with critical_only filter
        response = client.get("/platform/status?critical_only=true")
        assert response.status_code == 200
        
        data = response.json()
        # Should only include critical services
        for service_data in data["services"].values():
            assert service_data.get("critical", False) is True

class TestIntegration:
    """Integration tests for the complete system"""
    
    @patch('aiohttp.ClientSession')
    async def test_alert_dispatcher_integration(self, mock_session):
        """Test alert dispatcher integration with platform status"""
        # Mock platform status response
        mock_platform_status = {
            "environment": "test",
            "services": {
                "auth_service": {
                    "status": "degraded",
                    "error": "Database connection failed",
                    "critical": True,
                    "response_time_ms": 3000
                },
                "gateway_service": {
                    "status": "healthy",
                    "critical": True,
                    "response_time_ms": 150
                }
            }
        }
        
        # Mock notification service response
        mock_notification_response = AsyncMock()
        mock_notification_response.status = 200
        
        mock_session.return_value.__aenter__.return_value.get.return_value.__aenter__.return_value.json.return_value = mock_platform_status
        mock_session.return_value.__aenter__.return_value.post.return_value.__aenter__.return_value = mock_notification_response
        
        dispatcher = AlertDispatcher()
        result = await dispatcher.process_alerts()
        
        assert result["processed"] is True
        assert result["alerts_sent"] == 1  # Only auth_service should trigger alert
        assert len(result["critical_issues"]) == 1
        assert result["critical_issues"][0]["service"] == "auth_service"
    
    def test_complete_workflow(self):
        """Test complete workflow from dashboard load to alert processing"""
        # 1. Load dashboard
        response = client.get("/")
        assert response.status_code == 200
        
        # 2. Log dashboard load
        log_data = {
            "event": "panel_load",
            "user_agent": "test-agent",
            "services_count": 3
        }
        response = client.post("/api/log", json=log_data)
        assert response.status_code == 200
        
        # 3. Get platform status
        response = client.get("/platform/status")
        assert response.status_code == 200
        
        # 4. Check alert status
        response = client.get("/api/alerts/status")
        assert response.status_code == 200
        
        # 5. Get audit logs
        response = client.get("/api/logs")
        assert response.status_code == 200
        data = response.json()
        assert data["total_logs"] > 0

class TestErrorHandling:
    """Test error handling scenarios"""
    
    def test_invalid_log_data(self):
        """Test handling of invalid log data"""
        response = client.post("/api/log", json="invalid json")
        assert response.status_code == 422  # Validation error
    
    def test_alert_processing_error(self):
        """Test alert processing error handling"""
        with patch('main.alert_dispatcher.process_alerts', side_effect=Exception("Test error")):
            response = client.post("/api/alerts/process")
            assert response.status_code == 500
    
    def test_static_file_not_found(self):
        """Test handling of missing static files"""
        response = client.get("/static/nonexistent.js")
        assert response.status_code == 404

class TestPerformance:
    """Test performance characteristics"""
    
    def test_platform_status_caching(self):
        """Test that platform status is properly cached"""
        # First request
        start_time = datetime.utcnow()
        response1 = client.get("/platform/status")
        time1 = datetime.utcnow() - start_time
        
        # Second request (should be cached)
        start_time = datetime.utcnow()
        response2 = client.get("/platform/status")
        time2 = datetime.utcnow() - start_time
        
        # Cached request should be faster
        assert time2 < time1
        
        # Both responses should be identical
        data1 = response1.json()
        data2 = response2.json()
        assert data1["cache_info"]["cache_valid"] is True
        assert data2["cache_info"]["cache_valid"] is True
    
    def test_audit_log_memory_management(self):
        """Test that audit logs don't grow indefinitely"""
        # Add many logs
        for i in range(1100):  # More than the 1000 limit
            client.post("/api/log", json={"event": f"test_event_{i}"})
        
        # Check total logs
        response = client.get("/api/logs")
        data = response.json()
        assert data["total_logs"] <= 1000  # Should be capped

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
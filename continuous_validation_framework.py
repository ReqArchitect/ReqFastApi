#!/usr/bin/env python3
"""
Continuous Validation Framework for ReqArchitect Platform
Automates periodic health checks and API testing for all microservices
"""

import asyncio
import json
import logging
import os
import time
import schedule
import requests
import docker
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('validation_framework.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Data class for storing validation results"""
    service_name: str
    endpoint: str
    method: str
    status_code: Optional[int]
    response_time: Optional[float]
    success: bool
    error_message: Optional[str]
    timestamp: str
    retry_count: int = 0
    response_body: Optional[Dict] = None

@dataclass
class ServiceHealth:
    """Data class for service health metrics"""
    service_name: str
    uptime_percentage: float
    error_rate: float
    api_success_ratio: float
    average_response_time: float
    total_requests: int
    failed_requests: int
    last_check: str
    container_status: str

class ContinuousValidator:
    """Main validation framework class"""
    
    def __init__(self, config_path: str = "validation_config.json"):
        self.config = self._load_config(config_path)
        self.results_history: List[ValidationResult] = []
        self.service_health: Dict[str, ServiceHealth] = {}
        self.docker_client = docker.from_env()
        self.session = requests.Session()
        # self.session.timeout = 30  # Removed: not a valid attribute for requests.Session
        
        # Create output directories
        self.output_dir = Path("validation_outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize service health tracking
        self._initialize_service_health()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load validation configuration"""
        default_config = {
            "services": {
                "gateway_service": {
                    "port": 8080,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/api/v1/health", "method": "GET", "expected_status": 200}
                    ]
                },
                "auth_service": {
                    "port": 8001,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/auth/login", "method": "POST", "expected_status": [200, 401, 422]},
                        {"path": "/auth/roles", "method": "GET", "expected_status": 200}
                    ]
                },
                "ai_modeling_service": {
                    "port": 8002,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/ai_modeling/generate", "method": "POST", "expected_status": [200, 401, 422, 500]},
                        {"path": "/ai_modeling/history/{user_id}", "method": "GET", "expected_status": [200, 401, 404]}
                    ]
                },
                "usage_service": {
                    "port": 8005,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/usage/tenant/{tenant_id}", "method": "GET", "expected_status": [200, 401, 403]},
                        {"path": "/usage/user/{user_id}", "method": "GET", "expected_status": [200, 401, 404]}
                    ]
                },
                "notification_service": {
                    "port": 8006,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/notification/send", "method": "POST", "expected_status": [200, 401, 404]}
                    ]
                },
                "audit_log_service": {
                    "port": 8007,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/audit_log/query", "method": "GET", "expected_status": [200, 401, 404]}
                    ]
                },
                "billing_service": {
                    "port": 8010,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/billing/tenant/{tenant_id}", "method": "GET", "expected_status": [200, 401, 403]},
                        {"path": "/billing/plans", "method": "GET", "expected_status": 200},
                        {"path": "/billing/usage_report", "method": "GET", "expected_status": [200, 405]}
                    ]
                },
                "invoice_service": {
                    "port": 8011,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/invoices/{tenant_id}", "method": "GET", "expected_status": 200},
                        {"path": "/invoices/generate/{tenant_id}", "method": "POST", "expected_status": [200, 202]}
                    ]
                },
                "monitoring_dashboard_service": {
                    "port": 8012,
                    "endpoints": [
                        {"path": "/health", "method": "GET", "expected_status": 200},
                        {"path": "/metrics", "method": "GET", "expected_status": 200},
                        {"path": "/dashboard", "method": "GET", "expected_status": [200, 404]}
                    ]
                }
            },
            "test_data": {
                "tenant_id": "test-tenant-123",
                "user_id": "test-user-456",
                "email": "test@example.com",
                "password": "testpass123",
                "role": "Admin"
            },
            "validation_settings": {
                "retry_attempts": 3,
                "retry_delay": 2,
                "timeout": 30,
                "check_interval_minutes": 15,
                "history_retention_days": 7
            },
            "jwt_settings": {
                "enabled": True,
                "secret": "supersecret",
                "algorithm": "HS256",
                "expiration_hours": 24
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Merge user config with defaults
                default_config.update(user_config)
        
        return default_config
    
    def _initialize_service_health(self):
        """Initialize service health tracking"""
        for service_name in self.config["services"].keys():
            self.service_health[service_name] = ServiceHealth(
                service_name=service_name,
                uptime_percentage=0.0,
                error_rate=0.0,
                api_success_ratio=0.0,
                average_response_time=0.0,
                total_requests=0,
                failed_requests=0,
                last_check=datetime.now().isoformat(),
                container_status="unknown"
            )
    
    def _get_jwt_token(self) -> Optional[str]:
        """Get JWT token for authenticated endpoints"""
        try:
            import jwt
            payload = {
                "user_id": self.config["test_data"]["user_id"],
                "tenant_id": self.config["test_data"]["tenant_id"],
                "role": self.config["test_data"]["role"],
                "exp": datetime.utcnow() + timedelta(hours=self.config["jwt_settings"]["expiration_hours"])
            }
            token = jwt.encode(
                payload, 
                self.config["jwt_settings"]["secret"], 
                algorithm=self.config["jwt_settings"]["algorithm"]
            )
            return token
        except ImportError:
            logger.warning("PyJWT not installed, skipping JWT authentication")
            return None
        except Exception as e:
            logger.error(f"Failed to generate JWT token: {e}")
            return None
    
    def _get_container_status(self, service_name: str) -> str:
        """Get container status for a service"""
        try:
            container = self.docker_client.containers.get(service_name)
            return container.status
        except Exception as e:
            logger.warning(f"Could not get container status for {service_name}: {e}")
            return "unknown"
    
    def _test_endpoint(self, service_name: str, endpoint_config: Dict, retry_count: int = 0) -> ValidationResult:
        """Test a single endpoint with retry logic"""
        service_config = self.config["services"][service_name]
        port = service_config["port"]
        path = endpoint_config["path"]
        method = endpoint_config["method"]
        expected_status = endpoint_config["expected_status"]
        
        # Replace placeholders in path
        if "{tenant_id}" in path:
            path = path.replace("{tenant_id}", self.config["test_data"]["tenant_id"])
        if "{user_id}" in path:
            path = path.replace("{user_id}", self.config["test_data"]["user_id"])
        
        url = f"http://localhost:{port}{path}"
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "X-Tenant-ID": self.config["test_data"]["tenant_id"],
            "X-User-ID": self.config["test_data"]["user_id"]
        }
        
        # Add JWT token if enabled
        if self.config["jwt_settings"]["enabled"]:
            token = self._get_jwt_token()
            if token:
                headers["Authorization"] = f"Bearer {token}"
        
        # Prepare request data for POST requests
        data = None
        if method == "POST":
            if "login" in path:
                data = {
                    "email": self.config["test_data"]["email"],
                    "password": self.config["test_data"]["password"],
                    "tenant_id": self.config["test_data"]["tenant_id"]
                }
            elif "generate" in path:
                data = {
                    "tenant_id": self.config["test_data"]["tenant_id"],
                    "user_id": self.config["test_data"]["user_id"],
                    "input_type": "goal",
                    "input_text": "Optimize supply chain efficiency"
                }
            elif "send" in path:
                data = {
                    "tenant_id": self.config["test_data"]["tenant_id"],
                    "user_id": self.config["test_data"]["user_id"],
                    "type": "email",
                    "subject": "Test Notification",
                    "message": "This is a test notification",
                    "recipient": "test@example.com"
                }
        
        start_time = time.time()
        
        try:
            if method == "GET":
                response = self.session.get(url, headers=headers)
            elif method == "POST":
                response = self.session.post(url, json=data, headers=headers)
            elif method == "PUT":
                response = self.session.put(url, json=data, headers=headers)
            elif method == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Check if status code is expected
            if isinstance(expected_status, list):
                success = response.status_code in expected_status
            else:
                success = response.status_code == expected_status
            
            # Parse response body
            response_body = None
            try:
                if response.content:
                    # Try to parse as JSON, fallback to None if not JSON
                    response_body = response.json()
            except Exception:
                response_body = None
            
            return ValidationResult(
                service_name=service_name,
                endpoint=path,
                method=method,
                status_code=response.status_code,
                response_time=response_time,
                success=success,
                error_message=None,
                timestamp=datetime.now().isoformat(),
                retry_count=retry_count,
                response_body=response_body
            )
            
        except requests.exceptions.ConnectionError as e:
            return ValidationResult(
                service_name=service_name,
                endpoint=path,
                method=method,
                status_code=None,
                response_time=None,
                success=False,
                error_message=f"Connection refused: {str(e)}",
                timestamp=datetime.now().isoformat(),
                retry_count=retry_count
            )
        except requests.exceptions.Timeout as e:
            return ValidationResult(
                service_name=service_name,
                endpoint=path,
                method=method,
                status_code=None,
                response_time=None,
                success=False,
                error_message=f"Request timeout: {str(e)}",
                timestamp=datetime.now().isoformat(),
                retry_count=retry_count
            )
        except Exception as e:
            return ValidationResult(
                service_name=service_name,
                endpoint=path,
                method=method,
                status_code=None,
                response_time=None,
                success=False,
                error_message=str(e),
                timestamp=datetime.now().isoformat(),
                retry_count=retry_count
            )
    
    def _test_endpoint_with_retry(self, service_name: str, endpoint_config: Dict) -> ValidationResult:
        """Test endpoint with retry logic"""
        max_retries = self.config["validation_settings"]["retry_attempts"]
        retry_delay = self.config["validation_settings"]["retry_delay"]
        
        for attempt in range(max_retries):
            result = self._test_endpoint(service_name, endpoint_config, attempt)
            
            if result.success:
                return result
            
            if attempt < max_retries - 1:
                logger.info(f"Retrying {service_name}{result.endpoint} (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
        
        return result
    
    def run_validation_cycle(self) -> List[ValidationResult]:
        """Run a complete validation cycle for all services"""
        logger.info("Starting validation cycle...")
        cycle_results = []
        
        for service_name, service_config in self.config["services"].items():
            logger.info(f"Validating {service_name}...")
            
            # Update container status
            container_status = self._get_container_status(service_name)
            self.service_health[service_name].container_status = container_status
            
            for endpoint_config in service_config["endpoints"]:
                result = self._test_endpoint_with_retry(service_name, endpoint_config)
                cycle_results.append(result)
                
                # Log result
                # Use ASCII icons for Windows console compatibility
                if result.success:
                    status_icon = "[OK]"
                else:
                    status_icon = "[FAIL]"
                logger.info(f"  {status_icon} {result.method} {result.endpoint}: {result.status_code} ({result.response_time:.2f}ms)")
                
                if result.error_message:
                    logger.warning(f"    Error: {result.error_message}")
        
        # Update results history
        self.results_history.extend(cycle_results)
        
        # Update service health metrics
        self._update_service_health(cycle_results)
        
        # Save results
        self._save_cycle_results(cycle_results)
        
        logger.info(f"Validation cycle completed. {len(cycle_results)} endpoints tested.")
        return cycle_results
    
    def _update_service_health(self, cycle_results: List[ValidationResult]):
        """Update service health metrics"""
        # Group results by service
        service_results = {}
        for result in cycle_results:
            if result.service_name not in service_results:
                service_results[result.service_name] = []
            service_results[result.service_name].append(result)
        
        # Calculate metrics for each service
        for service_name, results in service_results.items():
            total_requests = len(results)
            failed_requests = sum(1 for r in results if not r.success)
            successful_requests = total_requests - failed_requests
            
            # Calculate response times (excluding failed requests)
            response_times = [r.response_time for r in results if r.response_time is not None]
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            
            # Update service health
            health = self.service_health[service_name]
            health.total_requests += total_requests
            health.failed_requests += failed_requests
            health.average_response_time = avg_response_time
            health.api_success_ratio = (successful_requests / total_requests) * 100 if total_requests > 0 else 0
            health.error_rate = (failed_requests / total_requests) * 100 if total_requests > 0 else 0
            health.last_check = datetime.now().isoformat()
            
            # Calculate uptime percentage (simplified)
            health.uptime_percentage = 100 - health.error_rate
    
    def _save_cycle_results(self, cycle_results: List[ValidationResult]):
        """Save validation cycle results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save JSON results
        json_file = self.output_dir / f"validation_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "cycle_results": [asdict(r) for r in cycle_results],
                "service_health": {name: asdict(health) for name, health in self.service_health.items()}
            }, f, indent=2)
        
        # Save Markdown report
        md_file = self.output_dir / f"validation_report_{timestamp}.md"
        self._generate_markdown_report(cycle_results, md_file)
        
        logger.info(f"Results saved to {json_file} and {md_file}")
    
    def _generate_markdown_report(self, cycle_results: List[ValidationResult], output_file: Path):
        """Generate Markdown validation report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Group results by service
        service_results = {}
        for result in cycle_results:
            if result.service_name not in service_results:
                service_results[result.service_name] = []
            service_results[result.service_name].append(result)
        
        with open(output_file, 'w') as f:
            f.write(f"# ReqArchitect Validation Report\n")
            f.write(f"Generated: {timestamp}\n\n")
            
            # Summary
            total_tests = len(cycle_results)
            successful_tests = sum(1 for r in cycle_results if r.success)
            failed_tests = total_tests - successful_tests
            
            f.write(f"## Summary\n")
            f.write(f"- **Total Tests**: {total_tests}\n")
            f.write(f"- **Successful**: {successful_tests}\n")
            f.write(f"- **Failed**: {failed_tests}\n")
            f.write(f"- **Success Rate**: {(successful_tests/total_tests*100):.1f}%\n\n")
            
            # Service Health Dashboard
            f.write(f"## Service Health Dashboard\n")
            f.write(f"| Service | Uptime % | Error Rate % | Success Ratio % | Avg Response Time | Container Status |\n")
            f.write(f"|---------|----------|--------------|-----------------|-------------------|------------------|\n")
            
            for service_name, health in self.service_health.items():
                f.write(f"| {service_name} | {health.uptime_percentage:.1f}% | {health.error_rate:.1f}% | {health.api_success_ratio:.1f}% | {health.average_response_time:.2f}ms | {health.container_status} |\n")
            
            f.write(f"\n")
            
            # Detailed Results
            f.write(f"## Detailed Results\n")
            for service_name, results in service_results.items():
                service_success = sum(1 for r in results if r.success)
                service_total = len(results)
                service_rate = (service_success/service_total*100) if service_total > 0 else 0
                
                f.write(f"\n### {service_name.upper()}\n")
                f.write(f"**Success Rate**: {service_rate:.1f}% ({service_success}/{service_total})\n\n")
                
                f.write(f"| Endpoint | Method | Status Code | Response Time | Success |\n")
                f.write(f"|----------|--------|-------------|---------------|---------|\n")
                
                for result in results:
                    status_icon = "✅" if result.success else "❌"
                    status_code = result.status_code or "N/A"
                    response_time = f"{result.response_time:.2f}ms" if result.response_time else "N/A"
                    
                    f.write(f"| {result.endpoint} | {result.method} | {status_code} | {response_time} | {status_icon} |\n")
                    
                    if result.error_message:
                        f.write(f"  *Error: {result.error_message}*\n")
    
    def generate_dashboard(self) -> str:
        """Generate a summary dashboard"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Calculate overall metrics
        total_requests = sum(health.total_requests for health in self.service_health.values())
        total_failures = sum(health.failed_requests for health in self.service_health.values())
        overall_success_rate = ((total_requests - total_failures) / total_requests * 100) if total_requests > 0 else 0
        
        dashboard = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ReqArchitect Platform - Validation Dashboard              ║
║                              {timestamp}                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Overall Success Rate: {overall_success_rate:.1f}% ({total_requests - total_failures}/{total_requests})  ║
║  Total Services: {len(self.service_health)}                                                              ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Service Health Status:                                                      ║
║                                                                              ║"""
        
        for service_name, health in self.service_health.items():
            status_icon = "🟢" if health.uptime_percentage > 90 else "🟡" if health.uptime_percentage > 70 else "🔴"
            dashboard += f"\n║  {status_icon} {service_name:<25} {health.uptime_percentage:>5.1f}% uptime | {health.api_success_ratio:>5.1f}% success | {health.container_status}"
            dashboard += " " * (70 - len(f"  {status_icon} {service_name} {health.uptime_percentage:.1f}% uptime | {health.api_success_ratio:.1f}% success | {health.container_status}")) + "║"
        
        dashboard += f"""
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        return dashboard
    
    def cleanup_old_results(self):
        """Clean up old validation results"""
        retention_days = self.config["validation_settings"]["history_retention_days"]
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Clean up old files
        for file_path in self.output_dir.glob("validation_*"):
            if file_path.stat().st_mtime < cutoff_date.timestamp():
                file_path.unlink()
                logger.info(f"Cleaned up old file: {file_path}")
        
        # Clean up old results from history
        self.results_history = [
            result for result in self.results_history
            if datetime.fromisoformat(result.timestamp) > cutoff_date
        ]
    
    def run_scheduler(self):
        """Run the validation scheduler"""
        interval_minutes = self.config["validation_settings"]["check_interval_minutes"]
        
        logger.info(f"Starting validation scheduler (every {interval_minutes} minutes)")
        
        # Schedule the validation
        schedule.every(interval_minutes).minutes.do(self.run_validation_cycle)
        
        # Run initial validation
        self.run_validation_cycle()
        
        # Start the scheduler loop
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
                # Cleanup old results daily
                if datetime.now().hour == 0 and datetime.now().minute == 0:
                    self.cleanup_old_results()
                    
            except KeyboardInterrupt:
                logger.info("Validation scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(60)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Continuous Validation Framework")
    parser.add_argument("--config", default="validation_config.json", help="Configuration file path")
    parser.add_argument("--run-once", action="store_true", help="Run validation once and exit")
    parser.add_argument("--dashboard", action="store_true", help="Show dashboard and exit")
    parser.add_argument("--scheduler", action="store_true", help="Run continuous scheduler")
    
    args = parser.parse_args()
    
    try:
        validator = ContinuousValidator(args.config)
        
        if args.dashboard:
            print(validator.generate_dashboard())
        elif args.run_once:
            results = validator.run_validation_cycle()
            print(validator.generate_dashboard())
        elif args.scheduler:
            validator.run_scheduler()
        else:
            # Default: run once
            results = validator.run_validation_cycle()
            print(validator.generate_dashboard())
            
    except Exception as e:
        logger.error(f"Validation framework error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
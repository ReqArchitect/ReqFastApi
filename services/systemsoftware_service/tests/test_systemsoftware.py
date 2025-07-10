import pytest
import uuid
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db_session
from app.models import SystemSoftware, SoftwareLink
from app.schemas import (
    SystemSoftwareCreate, SoftwareLinkCreate,
    SoftwareType, LicenseType, LifecycleState
)
from app.services import SystemSoftwareService, SoftwareLinkService
from app.config import settings

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = override_get_db

# Test client
client = TestClient(app)

# Test data
test_tenant_id = uuid.uuid4()
test_user_id = uuid.uuid4()
test_system_software_id = uuid.uuid4()

@pytest.fixture
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch('app.deps.get_redis_client') as mock:
        mock_redis = Mock()
        mock.return_value = mock_redis
        yield mock_redis

@pytest.fixture
def mock_auth():
    """Mock authentication."""
    with patch('app.deps.get_current_user') as mock:
        mock.return_value = {
            "user_id": str(test_user_id),
            "tenant_id": str(test_tenant_id),
            "role": "Admin",
            "permissions": ["system_software:create", "system_software:read", "system_software:update", "system_software:delete"]
        }
        yield mock

@pytest.fixture
def sample_system_software_data():
    """Sample system software data for testing."""
    return {
        "name": "Ubuntu 22.04 LTS",
        "description": "Linux operating system for servers",
        "software_type": SoftwareType.OS,
        "version": "22.04.3",
        "vendor": "Canonical",
        "license_type": LicenseType.OPEN_SOURCE,
        "lifecycle_state": LifecycleState.ACTIVE,
        "vulnerability_score": 2.5,
        "update_channel": "lts",
        "deployment_environment": "production"
    }

@pytest.fixture
def sample_software_link_data():
    """Sample software link data for testing."""
    return {
        "linked_element_id": uuid.uuid4(),
        "linked_element_type": "node",
        "link_type": "runs_on",
        "relationship_strength": "strong",
        "dependency_level": "high"
    }

class TestSystemSoftwareModel:
    """Test SystemSoftware model."""
    
    def test_create_system_software(self, db_session):
        """Test creating a SystemSoftware instance."""
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            description="Linux operating system",
            software_type="os",
            version="22.04.3",
            vendor="Canonical",
            license_type="open_source",
            lifecycle_state="active"
        )
        
        db_session.add(system_software)
        db_session.commit()
        db_session.refresh(system_software)
        
        assert system_software.id == test_system_software_id
        assert system_software.name == "Ubuntu 22.04 LTS"
        assert system_software.software_type == "os"
        assert system_software.tenant_id == test_tenant_id
    
    def test_system_software_relationships(self, db_session):
        """Test SystemSoftware relationships."""
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="PostgreSQL 15.2",
            software_type="database",
            version="15.2"
        )
        
        software_link = SoftwareLink(
            id=uuid.uuid4(),
            system_software_id=test_system_software_id,
            linked_element_id=uuid.uuid4(),
            linked_element_type="node",
            link_type="runs_on",
            created_by=test_user_id
        )
        
        db_session.add(system_software)
        db_session.add(software_link)
        db_session.commit()
        
        assert len(system_software.links) == 1
        assert system_software.links[0].id == software_link.id

class TestSystemSoftwareService:
    """Test SystemSoftwareService."""
    
    def test_create_system_software(self, db_session, mock_redis):
        """Test creating system software."""
        service = SystemSoftwareService(db_session, mock_redis)
        
        system_software_data = SystemSoftwareCreate(
            name="Ubuntu 22.04 LTS",
            description="Linux operating system",
            software_type=SoftwareType.OS,
            version="22.04.3",
            vendor="Canonical",
            license_type=LicenseType.OPEN_SOURCE,
            lifecycle_state=LifecycleState.ACTIVE
        )
        
        system_software = service.create_system_software(
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            system_software_data=system_software_data
        )
        
        assert system_software.name == "Ubuntu 22.04 LTS"
        assert system_software.tenant_id == test_tenant_id
        assert system_software.user_id == test_user_id
        assert system_software.software_type == "os"
    
    def test_get_system_software(self, db_session, mock_redis):
        """Test getting system software by ID."""
        # Create test data
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3"
        )
        db_session.add(system_software)
        db_session.commit()
        
        service = SystemSoftwareService(db_session, mock_redis)
        result = service.get_system_software(test_system_software_id, test_tenant_id)
        
        assert result is not None
        assert result.id == test_system_software_id
        assert result.name == "Ubuntu 22.04 LTS"
    
    def test_list_system_software(self, db_session, mock_redis):
        """Test listing system software with filtering."""
        # Create test data
        system_software1 = SystemSoftware(
            id=uuid.uuid4(),
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3",
            vendor="Canonical"
        )
        system_software2 = SystemSoftware(
            id=uuid.uuid4(),
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="PostgreSQL 15.2",
            software_type="database",
            version="15.2",
            vendor="PostgreSQL Global Development Group"
        )
        db_session.add_all([system_software1, system_software2])
        db_session.commit()
        
        service = SystemSoftwareService(db_session, mock_redis)
        results = service.list_system_software(
            tenant_id=test_tenant_id,
            software_type="os"
        )
        
        assert len(results) == 1
        assert results[0].software_type == "os"
    
    def test_update_system_software(self, db_session, mock_redis):
        """Test updating system software."""
        # Create test data
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3"
        )
        db_session.add(system_software)
        db_session.commit()
        
        service = SystemSoftwareService(db_session, mock_redis)
        update_data = SystemSoftwareCreate( # Changed to SystemSoftwareCreate for consistency with create
            name="Ubuntu 22.04.3 LTS",
            vulnerability_score=1.5
        )
        
        result = service.update_system_software(
            test_system_software_id,
            test_tenant_id,
            update_data
        )
        
        assert result.name == "Ubuntu 22.04.3 LTS"
        assert result.vulnerability_score == 1.5
    
    def test_delete_system_software(self, db_session, mock_redis):
        """Test deleting system software."""
        # Create test data
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3"
        )
        db_session.add(system_software)
        db_session.commit()
        
        service = SystemSoftwareService(db_session, mock_redis)
        success = service.delete_system_software(test_system_software_id, test_tenant_id)
        
        assert success is True
        
        # Verify deletion
        result = service.get_system_software(test_system_software_id, test_tenant_id)
        assert result is None
    
    def test_get_dependency_map(self, db_session, mock_redis):
        """Test getting dependency map."""
        # Create test data
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3",
            dependencies='{"packages": ["openssl", "nginx"]}',
            dependent_components='{"apps": ["web-app", "api-service"]}',
            integration_points='{"apis": ["rest-api", "grpc-api"]}'
        )
        db_session.add(system_software)
        db_session.commit()
        
        service = SystemSoftwareService(db_session, mock_redis)
        dependency_map = service.get_dependency_map(test_system_software_id, test_tenant_id)
        
        assert dependency_map is not None
        assert dependency_map.system_software_id == test_system_software_id
        assert "dependencies" in dependency_map.dependency_health
    
    def test_get_compliance_check(self, db_session, mock_redis):
        """Test getting compliance check."""
        # Create test data
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3",
            vulnerability_score=2.5,
            compliance_status="compliant",
            compliance_certifications='{"iso": "27001", "soc": "2"}'
        )
        db_session.add(system_software)
        db_session.commit()
        
        service = SystemSoftwareService(db_session, mock_redis)
        compliance_check = service.get_compliance_check(test_system_software_id, test_tenant_id)
        
        assert compliance_check is not None
        assert compliance_check.system_software_id == test_system_software_id
        assert "compliance_status" in compliance_check.compliance_status
    
    def test_analyze_system_software(self, db_session, mock_redis):
        """Test analyzing system software."""
        # Create test data
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3",
            vulnerability_score=2.5,
            uptime_percentage=99.9,
            resource_usage=45.5
        )
        db_session.add(system_software)
        db_session.commit()
        
        service = SystemSoftwareService(db_session, mock_redis)
        analysis = service.analyze_system_software(test_system_software_id, test_tenant_id)
        
        assert analysis is not None
        assert analysis.system_software_id == test_system_software_id
        assert "operational_health" in analysis.operational_health
        assert "security_status" in analysis.security_status

class TestSoftwareLinkService:
    """Test SoftwareLinkService."""
    
    def test_create_software_link(self, db_session, mock_redis):
        """Test creating software link."""
        # Create system software first
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3"
        )
        db_session.add(system_software)
        db_session.commit()
        
        service = SoftwareLinkService(db_session, mock_redis)
        link_data = SoftwareLinkCreate(
            linked_element_id=uuid.uuid4(),
            linked_element_type="node",
            link_type="runs_on",
            relationship_strength="strong",
            dependency_level="high"
        )
        
        software_link = service.create_software_link(
            test_system_software_id,
            test_tenant_id,
            test_user_id,
            link_data
        )
        
        assert software_link is not None
        assert software_link.system_software_id == test_system_software_id
        assert software_link.link_type == "runs_on"
    
    def test_get_software_link(self, db_session, mock_redis):
        """Test getting software link by ID."""
        # Create test data
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3"
        )
        link_id = uuid.uuid4()
        software_link = SoftwareLink(
            id=link_id,
            system_software_id=test_system_software_id,
            linked_element_id=uuid.uuid4(),
            linked_element_type="node",
            link_type="runs_on",
            created_by=test_user_id
        )
        db_session.add_all([system_software, software_link])
        db_session.commit()
        
        service = SoftwareLinkService(db_session, mock_redis)
        result = service.get_software_link(link_id, test_tenant_id)
        
        assert result is not None
        assert result.id == link_id
        assert result.link_type == "runs_on"
    
    def test_list_software_links(self, db_session, mock_redis):
        """Test listing software links."""
        # Create test data
        system_software = SystemSoftware(
            id=test_system_software_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Ubuntu 22.04 LTS",
            software_type="os",
            version="22.04.3"
        )
        software_link1 = SoftwareLink(
            id=uuid.uuid4(),
            system_software_id=test_system_software_id,
            linked_element_id=uuid.uuid4(),
            linked_element_type="node",
            link_type="runs_on",
            created_by=test_user_id
        )
        software_link2 = SoftwareLink(
            id=uuid.uuid4(),
            system_software_id=test_system_software_id,
            linked_element_id=uuid.uuid4(),
            linked_element_type="application_component",
            link_type="supports",
            created_by=test_user_id
        )
        db_session.add_all([system_software, software_link1, software_link2])
        db_session.commit()
        
        service = SoftwareLinkService(db_session, mock_redis)
        results = service.list_software_links(test_system_software_id, test_tenant_id)
        
        assert len(results) == 2
        assert any(link.link_type == "runs_on" for link in results)
        assert any(link.link_type == "supports" for link in results)

class TestAPIEndpoints:
    """Test API endpoints."""
    
    def test_create_system_software_endpoint(self, mock_auth, mock_redis):
        """Test creating system software via API."""
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "description": "Linux operating system",
            "software_type": "os",
            "version": "22.04.3",
            "vendor": "Canonical",
            "license_type": "open_source",
            "lifecycle_state": "active"
        }
        
        response = client.post("/api/v1/system-software/", json=system_software_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Ubuntu 22.04 LTS"
        assert data["software_type"] == "os"
        assert "id" in data
    
    def test_get_system_software_endpoint(self, mock_auth, mock_redis):
        """Test getting system software via API."""
        # First create a system software
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "os",
            "version": "22.04.3"
        }
        create_response = client.post("/api/v1/system-software/", json=system_software_data)
        system_software_id = create_response.json()["id"]
        
        # Then get it
        response = client.get(f"/api/v1/system-software/{system_software_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Ubuntu 22.04 LTS"
        assert data["id"] == system_software_id
    
    def test_list_system_software_endpoint(self, mock_auth, mock_redis):
        """Test listing system software via API."""
        # Create some test data
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "os",
            "version": "22.04.3"
        }
        client.post("/api/v1/system-software/", json=system_software_data)
        
        response = client.get("/api/v1/system-software/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_update_system_software_endpoint(self, mock_auth, mock_redis):
        """Test updating system software via API."""
        # First create a system software
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "os",
            "version": "22.04.3"
        }
        create_response = client.post("/api/v1/system-software/", json=system_software_data)
        system_software_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Ubuntu 22.04.3 LTS",
            "vulnerability_score": 1.5
        }
        response = client.put(f"/api/v1/system-software/{system_software_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Ubuntu 22.04.3 LTS"
        assert data["vulnerability_score"] == 1.5
    
    def test_delete_system_software_endpoint(self, mock_auth, mock_redis):
        """Test deleting system software via API."""
        # First create a system software
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "os",
            "version": "22.04.3"
        }
        create_response = client.post("/api/v1/system-software/", json=system_software_data)
        system_software_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/v1/system-software/{system_software_id}")
        
        assert response.status_code == 204
    
    def test_get_dependency_map_endpoint(self, mock_auth, mock_redis):
        """Test getting dependency map via API."""
        # First create a system software
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "os",
            "version": "22.04.3",
            "dependencies": '{"packages": ["openssl", "nginx"]}'
        }
        create_response = client.post("/api/v1/system-software/", json=system_software_data)
        system_software_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/system-software/{system_software_id}/dependency-map")
        
        assert response.status_code == 200
        data = response.json()
        assert data["system_software_id"] == system_software_id
        assert "dependency_health" in data
    
    def test_get_compliance_check_endpoint(self, mock_auth, mock_redis):
        """Test getting compliance check via API."""
        # First create a system software
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "os",
            "version": "22.04.3",
            "vulnerability_score": 2.5,
            "compliance_status": "compliant"
        }
        create_response = client.post("/api/v1/system-software/", json=system_software_data)
        system_software_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/system-software/{system_software_id}/compliance-check")
        
        assert response.status_code == 200
        data = response.json()
        assert data["system_software_id"] == system_software_id
        assert "compliance_status" in data
    
    def test_get_analysis_endpoint(self, mock_auth, mock_redis):
        """Test getting analysis via API."""
        # First create a system software
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "os",
            "version": "22.04.3",
            "vulnerability_score": 2.5,
            "uptime_percentage": 99.9
        }
        create_response = client.post("/api/v1/system-software/", json=system_software_data)
        system_software_id = create_response.json()["id"]
        
        response = client.get(f"/api/v1/system-software/{system_software_id}/analysis")
        
        assert response.status_code == 200
        data = response.json()
        assert data["system_software_id"] == system_software_id
        assert "operational_health" in data
        assert "security_status" in data
    
    def test_get_software_types_endpoint(self, mock_auth):
        """Test getting software types enumeration."""
        response = client.get("/api/v1/system-software/software-types")
        
        assert response.status_code == 200
        data = response.json()
        assert "values" in data
        assert "os" in data["values"]
        assert "database" in data["values"]
    
    def test_get_license_types_endpoint(self, mock_auth):
        """Test getting license types enumeration."""
        response = client.get("/api/v1/system-software/license-types")
        
        assert response.status_code == 200
        data = response.json()
        assert "values" in data
        assert "proprietary" in data["values"]
        assert "open_source" in data["values"]

class TestAuthenticationAndAuthorization:
    """Test authentication and authorization."""
    
    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints."""
        response = client.get("/api/v1/system-software/")
        assert response.status_code == 401
    
    def test_insufficient_permissions(self, mock_redis):
        """Test insufficient permissions."""
        with patch('app.deps.get_current_user') as mock_auth:
            mock_auth.return_value = {
                "user_id": str(test_user_id),
                "tenant_id": str(test_tenant_id),
                "role": "Viewer",
                "permissions": ["system_software:read"]
            }
            
            # Try to create system software with Viewer role
            system_software_data = {
                "name": "Ubuntu 22.04 LTS",
                "software_type": "os",
                "version": "22.04.3"
            }
            response = client.post("/api/v1/system-software/", json=system_software_data)
            
            assert response.status_code == 403

class TestValidation:
    """Test input validation."""
    
    def test_invalid_software_type(self, mock_auth, mock_redis):
        """Test invalid software type."""
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "invalid_type",
            "version": "22.04.3"
        }
        
        response = client.post("/api/v1/system-software/", json=system_software_data)
        
        assert response.status_code == 422
    
    def test_invalid_vulnerability_score(self, mock_auth, mock_redis):
        """Test invalid vulnerability score."""
        system_software_data = {
            "name": "Ubuntu 22.04 LTS",
            "software_type": "os",
            "version": "22.04.3",
            "vulnerability_score": 15.0  # Invalid: should be 0-10
        }
        
        response = client.post("/api/v1/system-software/", json=system_software_data)
        
        assert response.status_code == 422
    
    def test_missing_required_fields(self, mock_auth, mock_redis):
        """Test missing required fields."""
        system_software_data = {
            "name": "Ubuntu 22.04 LTS"
            # Missing software_type and version
        }
        
        response = client.post("/api/v1/system-software/", json=system_software_data)
        
        assert response.status_code == 422

class TestErrorHandling:
    """Test error handling."""
    
    def test_not_found_error(self, mock_auth, mock_redis):
        """Test 404 error for non-existent resource."""
        non_existent_id = str(uuid.uuid4())
        response = client.get(f"/api/v1/system-software/{non_existent_id}")
        
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_invalid_uuid_error(self, mock_auth, mock_redis):
        """Test error for invalid UUID."""
        response = client.get("/api/v1/system-software/invalid-uuid")
        
        assert response.status_code == 422

class TestHealthAndMetrics:
    """Test health and metrics endpoints."""
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "version" in data
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]
    
    def test_ready_endpoint(self):
        """Test readiness check endpoint."""
        response = client.get("/ready")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "checks" in data
    
    def test_live_endpoint(self):
        """Test liveness check endpoint."""
        response = client.get("/live")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "alive"

if __name__ == "__main__":
    pytest.main([__file__]) 
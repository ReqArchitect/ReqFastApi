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
from app.models import Artifact, ArtifactLink
from app.schemas import ArtifactCreate, ArtifactLinkCreate
from app.services import ArtifactService, ArtifactLinkService
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

# Create tables
Base.metadata.create_all(bind=engine)

# Test client
client = TestClient(app)

# Mock data
test_tenant_id = uuid.uuid4()
test_user_id = uuid.uuid4()
test_artifact_id = uuid.uuid4()
test_link_id = uuid.uuid4()

# Mock JWT token
mock_jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiY2Y5YzM5YzAtYzM5Yy0xMWVlLWE5ZTAtYzM5YzM5YzM5YzM5YyIsInRlbmFudF9pZCI6ImNmOWMzOWMwLWMzOWMtMTFlZS1hOWUwLWMzOWMzOWMzOWMzOWMiLCJyb2xlIjoiQWRtaW4iLCJleHAiOjk5OTk5OTk5OTl9.mock_signature"

@pytest.fixture
def mock_redis():
    """Mock Redis client."""
    with patch('app.deps.get_redis_client') as mock:
        mock_redis_client = Mock()
        mock_redis_client.ping.return_value = True
        mock_redis_client.exists.return_value = True
        mock_redis_client.get.return_value = "1"
        mock_redis_client.incr.return_value = 1
        mock_redis_client.expire.return_value = True
        mock_redis_client.publish.return_value = 1
        mock_redis_client.pipeline.return_value.__enter__.return_value = mock_redis_client
        mock_redis_client.pipeline.return_value.__exit__.return_value = None
        mock.return_value = mock_redis_client
        yield mock_redis_client

@pytest.fixture
def mock_auth():
    """Mock authentication."""
    with patch('app.deps.get_current_user') as mock:
        mock.return_value = {
            "user_id": str(test_user_id),
            "tenant_id": str(test_tenant_id),
            "role": "Admin",
            "permissions": ["artifact:create", "artifact:read", "artifact:update", "artifact:delete"]
        }
        yield mock

class TestArtifactModels:
    """Test artifact models."""
    
    def test_artifact_creation(self):
        """Test artifact model creation."""
        artifact = Artifact(
            id=test_artifact_id,
            tenant_id=test_tenant_id,
            user_id=test_user_id,
            name="Test Artifact",
            description="Test description",
            artifact_type="source",
            version="1.0.0",
            format="docker",
            storage_location="/path/to/artifact",
            checksum="sha256:abc123",
            build_tool="docker",
            lifecycle_state="active",
            size_mb=100.0,
            file_count=10,
            deployment_environment="production",
            integrity_verified=True,
            security_scan_passed=True,
            vulnerability_count=0,
            security_score=9.0,
            access_level="read",
            public_access=False,
            backup_enabled=True,
            compliance_status="compliant",
            data_classification="internal",
            quality_score=0.9,
            test_coverage=85.0,
            documentation_status="complete",
            operational_hours="24x7",
            incident_count=0,
            license_type="open_source",
            license_cost=0.0
        )
        
        assert artifact.id == test_artifact_id
        assert artifact.name == "Test Artifact"
        assert artifact.artifact_type == "source"
        assert artifact.version == "1.0.0"
        assert artifact.integrity_verified == True
        assert artifact.security_scan_passed == True

    def test_artifact_link_creation(self):
        """Test artifact link model creation."""
        link = ArtifactLink(
            id=test_link_id,
            artifact_id=test_artifact_id,
            linked_element_id=uuid.uuid4(),
            linked_element_type="application_component",
            link_type="implements",
            relationship_strength="strong",
            dependency_level="high",
            implementation_status="active",
            deployment_status="deployed",
            deployment_environment="production",
            communication_frequency="frequent",
            communication_type="synchronous",
            performance_impact="medium",
            business_criticality="high",
            business_value="high",
            risk_level="medium",
            monitoring_enabled=True,
            alerting_enabled=True,
            logging_level="info",
            created_by=test_user_id
        )
        
        assert link.id == test_link_id
        assert link.artifact_id == test_artifact_id
        assert link.link_type == "implements"
        assert link.relationship_strength == "strong"
        assert link.monitoring_enabled == True

class TestArtifactService:
    """Test artifact service."""
    
    def test_create_artifact(self, mock_redis):
        """Test creating an artifact."""
        db = TestingSessionLocal()
        service = ArtifactService(db, mock_redis)
        
        artifact_data = ArtifactCreate(
            name="Test Artifact",
            description="Test description",
            artifact_type="source",
            version="1.0.0",
            format="docker",
            storage_location="/path/to/artifact",
            checksum="sha256:abc123",
            build_tool="docker",
            lifecycle_state="active",
            size_mb=100.0,
            file_count=10,
            deployment_environment="production",
            integrity_verified=True,
            security_scan_passed=True,
            vulnerability_count=0,
            security_score=9.0,
            access_level="read",
            public_access=False,
            backup_enabled=True,
            compliance_status="compliant",
            data_classification="internal",
            quality_score=0.9,
            test_coverage=85.0,
            documentation_status="complete",
            operational_hours="24x7",
            incident_count=0,
            license_type="open_source",
            license_cost=0.0
        )
        
        artifact = service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        assert artifact.name == "Test Artifact"
        assert artifact.tenant_id == test_tenant_id
        assert artifact.user_id == test_user_id
        assert artifact.artifact_type == "source"
        assert artifact.integrity_verified == True
        
        db.close()

    def test_get_artifact(self, mock_redis):
        """Test getting an artifact."""
        db = TestingSessionLocal()
        service = ArtifactService(db, mock_redis)
        
        # Create test artifact
        artifact_data = ArtifactCreate(
            name="Test Artifact",
            artifact_type="source",
            version="1.0.0"
        )
        created_artifact = service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        # Get artifact
        artifact = service.get_artifact(created_artifact.id, test_tenant_id)
        
        assert artifact is not None
        assert artifact.name == "Test Artifact"
        assert artifact.tenant_id == test_tenant_id
        
        db.close()

    def test_list_artifacts(self, mock_redis):
        """Test listing artifacts."""
        db = TestingSessionLocal()
        service = ArtifactService(db, mock_redis)
        
        # Create test artifacts
        for i in range(3):
            artifact_data = ArtifactCreate(
                name=f"Test Artifact {i}",
                artifact_type="source",
                version=f"1.{i}.0"
            )
            service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        # List artifacts
        artifacts = service.list_artifacts(test_tenant_id)
        
        assert len(artifacts) == 3
        assert all(artifact.tenant_id == test_tenant_id for artifact in artifacts)
        
        db.close()

    def test_update_artifact(self, mock_redis):
        """Test updating an artifact."""
        db = TestingSessionLocal()
        service = ArtifactService(db, mock_redis)
        
        # Create test artifact
        artifact_data = ArtifactCreate(
            name="Test Artifact",
            artifact_type="source",
            version="1.0.0"
        )
        created_artifact = service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        # Update artifact
        from app.schemas import ArtifactUpdate
        update_data = ArtifactUpdate(
            name="Updated Artifact",
            description="Updated description"
        )
        
        updated_artifact = service.update_artifact(created_artifact.id, update_data, test_tenant_id)
        
        assert updated_artifact.name == "Updated Artifact"
        assert updated_artifact.description == "Updated description"
        
        db.close()

    def test_delete_artifact(self, mock_redis):
        """Test deleting an artifact."""
        db = TestingSessionLocal()
        service = ArtifactService(db, mock_redis)
        
        # Create test artifact
        artifact_data = ArtifactCreate(
            name="Test Artifact",
            artifact_type="source",
            version="1.0.0"
        )
        created_artifact = service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        # Delete artifact
        success = service.delete_artifact(created_artifact.id, test_tenant_id)
        
        assert success == True
        
        # Verify deletion
        artifact = service.get_artifact(created_artifact.id, test_tenant_id)
        assert artifact is None
        
        db.close()

    def test_get_artifact_dependency_map(self, mock_redis):
        """Test getting artifact dependency map."""
        db = TestingSessionLocal()
        service = ArtifactService(db, mock_redis)
        
        # Create test artifact with dependencies
        artifact_data = ArtifactCreate(
            name="Test Artifact",
            artifact_type="source",
            version="1.0.0",
            dependencies='[{"name": "dep1", "version": "1.0.0"}]',
            dependent_artifacts='[{"name": "dep2", "version": "2.0.0"}]'
        )
        created_artifact = service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        # Get dependency map
        dependency_map = service.get_artifact_dependency_map(created_artifact.id, test_tenant_id)
        
        assert dependency_map is not None
        assert "artifact_id" in dependency_map
        assert "direct_dependencies" in dependency_map
        assert "indirect_dependencies" in dependency_map
        
        db.close()

    def test_check_artifact_integrity(self, mock_redis):
        """Test checking artifact integrity."""
        db = TestingSessionLocal()
        service = ArtifactService(db, mock_redis)
        
        # Create test artifact
        artifact_data = ArtifactCreate(
            name="Test Artifact",
            artifact_type="source",
            version="1.0.0",
            integrity_verified=True,
            security_scan_passed=True,
            vulnerability_count=0,
            security_score=9.0
        )
        created_artifact = service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        # Check integrity
        integrity_check = service.check_artifact_integrity(created_artifact.id, test_tenant_id)
        
        assert integrity_check is not None
        assert "artifact_id" in integrity_check
        assert "checksum_valid" in integrity_check
        assert "security_scan_passed" in integrity_check
        assert "integrity_score" in integrity_check
        
        db.close()

class TestArtifactLinkService:
    """Test artifact link service."""
    
    def test_create_artifact_link(self, mock_redis):
        """Test creating an artifact link."""
        db = TestingSessionLocal()
        service = ArtifactLinkService(db, mock_redis)
        
        # Create test artifact first
        artifact_service = ArtifactService(db, mock_redis)
        artifact_data = ArtifactCreate(
            name="Test Artifact",
            artifact_type="source",
            version="1.0.0"
        )
        artifact = artifact_service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        # Create link
        link_data = ArtifactLinkCreate(
            linked_element_id=uuid.uuid4(),
            linked_element_type="application_component",
            link_type="implements",
            relationship_strength="strong",
            dependency_level="high",
            implementation_status="active",
            deployment_status="deployed",
            deployment_environment="production",
            communication_frequency="frequent",
            communication_type="synchronous",
            performance_impact="medium",
            business_criticality="high",
            business_value="high",
            risk_level="medium",
            monitoring_enabled=True,
            alerting_enabled=True,
            logging_level="info"
        )
        
        link = service.create_artifact_link(artifact.id, link_data, test_tenant_id, test_user_id)
        
        assert link.artifact_id == artifact.id
        assert link.link_type == "implements"
        assert link.relationship_strength == "strong"
        assert link.monitoring_enabled == True
        
        db.close()

    def test_get_artifact_links(self, mock_redis):
        """Test getting artifact links."""
        db = TestingSessionLocal()
        service = ArtifactLinkService(db, mock_redis)
        
        # Create test artifact and links
        artifact_service = ArtifactService(db, mock_redis)
        artifact_data = ArtifactCreate(
            name="Test Artifact",
            artifact_type="source",
            version="1.0.0"
        )
        artifact = artifact_service.create_artifact(artifact_data, test_tenant_id, test_user_id)
        
        # Create links
        for i in range(2):
            link_data = ArtifactLinkCreate(
                linked_element_id=uuid.uuid4(),
                linked_element_type="application_component",
                link_type="implements"
            )
            service.create_artifact_link(artifact.id, link_data, test_tenant_id, test_user_id)
        
        # Get links
        links = service.get_artifact_links(artifact.id, test_tenant_id)
        
        assert len(links) == 2
        assert all(link.artifact_id == artifact.id for link in links)
        
        db.close()

class TestArtifactAPI:
    """Test artifact API endpoints."""
    
    def test_create_artifact_api(self, mock_auth, mock_redis):
        """Test creating artifact via API."""
        artifact_data = {
            "name": "Test Artifact",
            "description": "Test description",
            "artifact_type": "source",
            "version": "1.0.0",
            "format": "docker",
            "storage_location": "/path/to/artifact",
            "checksum": "sha256:abc123",
            "build_tool": "docker",
            "lifecycle_state": "active",
            "size_mb": 100.0,
            "file_count": 10,
            "deployment_environment": "production",
            "integrity_verified": True,
            "security_scan_passed": True,
            "vulnerability_count": 0,
            "security_score": 9.0,
            "access_level": "read",
            "public_access": False,
            "backup_enabled": True,
            "compliance_status": "compliant",
            "data_classification": "internal",
            "quality_score": 0.9,
            "test_coverage": 85.0,
            "documentation_status": "complete",
            "operational_hours": "24x7",
            "incident_count": 0,
            "license_type": "open_source",
            "license_cost": 0.0
        }
        
        response = client.post(
            "/api/v1/artifacts/",
            json=artifact_data,
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Artifact"
        assert data["artifact_type"] == "source"
        assert data["version"] == "1.0.0"

    def test_get_artifact_api(self, mock_auth, mock_redis):
        """Test getting artifact via API."""
        # First create an artifact
        artifact_data = {
            "name": "Test Artifact",
            "artifact_type": "source",
            "version": "1.0.0"
        }
        
        create_response = client.post(
            "/api/v1/artifacts/",
            json=artifact_data,
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        created_artifact = create_response.json()
        
        # Get the artifact
        response = client.get(
            f"/api/v1/artifacts/{created_artifact['id']}",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Artifact"
        assert data["id"] == created_artifact["id"]

    def test_list_artifacts_api(self, mock_auth, mock_redis):
        """Test listing artifacts via API."""
        response = client.get(
            "/api/v1/artifacts/",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_update_artifact_api(self, mock_auth, mock_redis):
        """Test updating artifact via API."""
        # First create an artifact
        artifact_data = {
            "name": "Test Artifact",
            "artifact_type": "source",
            "version": "1.0.0"
        }
        
        create_response = client.post(
            "/api/v1/artifacts/",
            json=artifact_data,
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        created_artifact = create_response.json()
        
        # Update the artifact
        update_data = {
            "name": "Updated Artifact",
            "description": "Updated description"
        }
        
        response = client.put(
            f"/api/v1/artifacts/{created_artifact['id']}",
            json=update_data,
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Artifact"
        assert data["description"] == "Updated description"

    def test_delete_artifact_api(self, mock_auth, mock_redis):
        """Test deleting artifact via API."""
        # First create an artifact
        artifact_data = {
            "name": "Test Artifact",
            "artifact_type": "source",
            "version": "1.0.0"
        }
        
        create_response = client.post(
            "/api/v1/artifacts/",
            json=artifact_data,
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        created_artifact = create_response.json()
        
        # Delete the artifact
        response = client.delete(
            f"/api/v1/artifacts/{created_artifact['id']}",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 204

    def test_get_artifact_dependency_map_api(self, mock_auth, mock_redis):
        """Test getting artifact dependency map via API."""
        # First create an artifact
        artifact_data = {
            "name": "Test Artifact",
            "artifact_type": "source",
            "version": "1.0.0",
            "dependencies": '[{"name": "dep1", "version": "1.0.0"}]'
        }
        
        create_response = client.post(
            "/api/v1/artifacts/",
            json=artifact_data,
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        created_artifact = create_response.json()
        
        # Get dependency map
        response = client.get(
            f"/api/v1/artifacts/{created_artifact['id']}/dependency-map",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "artifact_id" in data
        assert "direct_dependencies" in data

    def test_check_artifact_integrity_api(self, mock_auth, mock_redis):
        """Test checking artifact integrity via API."""
        # First create an artifact
        artifact_data = {
            "name": "Test Artifact",
            "artifact_type": "source",
            "version": "1.0.0",
            "integrity_verified": True,
            "security_scan_passed": True,
            "vulnerability_count": 0,
            "security_score": 9.0
        }
        
        create_response = client.post(
            "/api/v1/artifacts/",
            json=artifact_data,
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        created_artifact = create_response.json()
        
        # Check integrity
        response = client.get(
            f"/api/v1/artifacts/{created_artifact['id']}/integrity-check",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "artifact_id" in data
        assert "checksum_valid" in data
        assert "security_scan_passed" in data

    def test_get_artifact_types_api(self, mock_auth, mock_redis):
        """Test getting artifact types via API."""
        response = client.get(
            "/api/v1/artifacts/artifact-types",
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "values" in data
        assert isinstance(data["values"], list)

    def test_unauthorized_access(self, mock_redis):
        """Test unauthorized access."""
        response = client.get("/api/v1/artifacts/")
        assert response.status_code == 401

    def test_invalid_artifact_data(self, mock_auth, mock_redis):
        """Test invalid artifact data."""
        invalid_data = {
            "name": "",  # Empty name
            "artifact_type": "invalid_type",  # Invalid type
            "version": "1.0.0"
        }
        
        response = client.post(
            "/api/v1/artifacts/",
            json=invalid_data,
            headers={"Authorization": f"Bearer {mock_jwt_token}"}
        )
        
        assert response.status_code == 422

class TestHealthAndMetrics:
    """Test health and metrics endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data

    def test_metrics(self):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "artifact_service_requests_total" in response.text

    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "status" in data

if __name__ == "__main__":
    pytest.main([__file__]) 
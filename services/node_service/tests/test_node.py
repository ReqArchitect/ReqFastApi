import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import json
from unittest.mock import Mock, patch
from datetime import datetime
from uuid import uuid4

from app.main import app
from app.database import Base, get_db_session
from app.models import Node, NodeLink
from app.schemas import NodeCreate, NodeLinkCreate
from app.services import NodeService, NodeLinkService

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override database session for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override database dependency
app.dependency_overrides[get_db_session] = override_get_db

# Test client
client = TestClient(app)

# Mock Redis client
mock_redis = Mock()

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
def mock_redis_client():
    """Mock Redis client."""
    return mock_redis

@pytest.fixture
def sample_node_data():
    """Sample node data for testing."""
    return {
        "name": "Test Node",
        "description": "A test node for unit testing",
        "node_type": "vm",
        "environment": "development",
        "operating_system": "Ubuntu 20.04",
        "hardware_spec": '{"cpu": "4 cores", "memory": "8GB"}',
        "region": "us-east-1",
        "availability_target": 99.9,
        "lifecycle_state": "active",
        "cpu_cores": 4,
        "memory_gb": 8.0,
        "storage_gb": 100.0,
        "network_bandwidth_mbps": 1000.0,
        "ip_address": "192.168.1.100",
        "hostname": "test-node-01",
        "security_level": "standard",
        "encryption_enabled": True,
        "backup_enabled": True,
        "monitoring_enabled": True
    }

@pytest.fixture
def sample_link_data():
    """Sample link data for testing."""
    return {
        "linked_element_id": str(uuid4()),
        "linked_element_type": "application_component",
        "link_type": "hosts",
        "relationship_strength": "strong",
        "dependency_level": "high",
        "deployment_status": "active",
        "communication_protocol": "HTTP",
        "communication_port": 8080,
        "communication_frequency": "frequent",
        "communication_type": "synchronous",
        "performance_impact": "medium",
        "business_criticality": "high",
        "business_value": "high",
        "monitoring_enabled": True,
        "alerting_enabled": True
    }

@pytest.fixture
def mock_jwt_token():
    """Mock JWT token for testing."""
    return {
        "tenant_id": str(uuid4()),
        "user_id": str(uuid4()),
        "role": "Admin",
        "permissions": ["node:create", "node:read", "node:update", "node:delete"]
    }

class TestNodeModel:
    """Test Node model."""
    
    def test_create_node(self, db_session, sample_node_data):
        """Test creating a node."""
        node = Node(
            tenant_id=uuid4(),
            user_id=uuid4(),
            **sample_node_data
        )
        db_session.add(node)
        db_session.commit()
        db_session.refresh(node)
        
        assert node.id is not None
        assert node.name == "Test Node"
        assert node.node_type == "vm"
        assert node.environment == "development"
        assert node.availability_target == 99.9
    
    def test_node_defaults(self, db_session):
        """Test node default values."""
        node = Node(
            tenant_id=uuid4(),
            user_id=uuid4(),
            name="Test Node"
        )
        db_session.add(node)
        db_session.commit()
        db_session.refresh(node)
        
        assert node.node_type == "vm"
        assert node.environment == "production"
        assert node.lifecycle_state == "active"
        assert node.security_level == "standard"
        assert node.encryption_enabled is True
        assert node.backup_enabled is True
        assert node.monitoring_enabled is True

class TestNodeLinkModel:
    """Test NodeLink model."""
    
    def test_create_node_link(self, db_session, sample_link_data):
        """Test creating a node link."""
        # Create a node first
        node = Node(
            tenant_id=uuid4(),
            user_id=uuid4(),
            name="Test Node"
        )
        db_session.add(node)
        db_session.commit()
        
        link = NodeLink(
            node_id=node.id,
            created_by=uuid4(),
            **sample_link_data
        )
        db_session.add(link)
        db_session.commit()
        db_session.refresh(link)
        
        assert link.id is not None
        assert link.node_id == node.id
        assert link.link_type == "hosts"
        assert link.relationship_strength == "strong"
        assert link.deployment_status == "active"

class TestNodeService:
    """Test NodeService."""
    
    def test_create_node(self, db_session, mock_redis_client, sample_node_data):
        """Test creating a node via service."""
        service = NodeService(db_session, mock_redis_client)
        tenant_id = uuid4()
        user_id = uuid4()
        
        node = service.create_node(
            NodeCreate(**sample_node_data),
            tenant_id,
            user_id
        )
        
        assert node.id is not None
        assert node.tenant_id == tenant_id
        assert node.user_id == user_id
        assert node.name == "Test Node"
    
    def test_get_node(self, db_session, mock_redis_client, sample_node_data):
        """Test getting a node."""
        service = NodeService(db_session, mock_redis_client)
        tenant_id = uuid4()
        user_id = uuid4()
        
        # Create a node
        node = service.create_node(
            NodeCreate(**sample_node_data),
            tenant_id,
            user_id
        )
        
        # Get the node
        retrieved_node = service.get_node(node.id, tenant_id)
        
        assert retrieved_node is not None
        assert retrieved_node.id == node.id
        assert retrieved_node.name == "Test Node"
    
    def test_list_nodes(self, db_session, mock_redis_client, sample_node_data):
        """Test listing nodes."""
        service = NodeService(db_session, mock_redis_client)
        tenant_id = uuid4()
        user_id = uuid4()
        
        # Create multiple nodes
        for i in range(3):
            data = sample_node_data.copy()
            data["name"] = f"Test Node {i}"
            service.create_node(NodeCreate(**data), tenant_id, user_id)
        
        # List nodes
        nodes, total = service.list_nodes(tenant_id)
        
        assert len(nodes) == 3
        assert total == 3
    
    def test_update_node(self, db_session, mock_redis_client, sample_node_data):
        """Test updating a node."""
        service = NodeService(db_session, mock_redis_client)
        tenant_id = uuid4()
        user_id = uuid4()
        
        # Create a node
        node = service.create_node(
            NodeCreate(**sample_node_data),
            tenant_id,
            user_id
        )
        
        # Update the node
        from app.schemas import NodeUpdate
        update_data = NodeUpdate(name="Updated Node", description="Updated description")
        updated_node = service.update_node(node.id, update_data, tenant_id)
        
        assert updated_node.name == "Updated Node"
        assert updated_node.description == "Updated description"
    
    def test_delete_node(self, db_session, mock_redis_client, sample_node_data):
        """Test deleting a node."""
        service = NodeService(db_session, mock_redis_client)
        tenant_id = uuid4()
        user_id = uuid4()
        
        # Create a node
        node = service.create_node(
            NodeCreate(**sample_node_data),
            tenant_id,
            user_id
        )
        
        # Delete the node
        success = service.delete_node(node.id, tenant_id)
        
        assert success is True
        
        # Verify node is deleted
        retrieved_node = service.get_node(node.id, tenant_id)
        assert retrieved_node is None

class TestNodeLinkService:
    """Test NodeLinkService."""
    
    def test_create_node_link(self, db_session, mock_redis_client, sample_link_data):
        """Test creating a node link."""
        service = NodeLinkService(db_session, mock_redis_client)
        tenant_id = uuid4()
        user_id = uuid4()
        
        # Create a node first
        node_service = NodeService(db_session, mock_redis_client)
        node = node_service.create_node(
            NodeCreate(name="Test Node"),
            tenant_id,
            user_id
        )
        
        # Create a link
        link = service.create_node_link(
            node.id,
            NodeLinkCreate(**sample_link_data),
            tenant_id,
            user_id
        )
        
        assert link.id is not None
        assert link.node_id == node.id
        assert link.link_type == "hosts"
    
    def test_get_node_link(self, db_session, mock_redis_client, sample_link_data):
        """Test getting a node link."""
        service = NodeLinkService(db_session, mock_redis_client)
        tenant_id = uuid4()
        user_id = uuid4()
        
        # Create a node and link
        node_service = NodeService(db_session, mock_redis_client)
        node = node_service.create_node(
            NodeCreate(name="Test Node"),
            tenant_id,
            user_id
        )
        
        link = service.create_node_link(
            node.id,
            NodeLinkCreate(**sample_link_data),
            tenant_id,
            user_id
        )
        
        # Get the link
        retrieved_link = service.get_node_link(link.id, tenant_id)
        
        assert retrieved_link is not None
        assert retrieved_link.id == link.id

class TestAPIEndpoints:
    """Test API endpoints."""
    
    @patch('app.deps.verify_token')
    def test_create_node_endpoint(self, mock_verify_token, sample_node_data, mock_jwt_token):
        """Test creating a node via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        response = client.post(
            "/nodes/",
            json=sample_node_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Node"
        assert data["node_type"] == "vm"
    
    @patch('app.deps.verify_token')
    def test_get_node_endpoint(self, mock_verify_token, sample_node_data, mock_jwt_token):
        """Test getting a node via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        # Create a node first
        create_response = client.post(
            "/nodes/",
            json=sample_node_data,
            headers={"Authorization": "Bearer test-token"}
        )
        node_id = create_response.json()["id"]
        
        # Get the node
        response = client.get(
            f"/nodes/{node_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == node_id
        assert data["name"] == "Test Node"
    
    @patch('app.deps.verify_token')
    def test_list_nodes_endpoint(self, mock_verify_token, sample_node_data, mock_jwt_token):
        """Test listing nodes via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        # Create multiple nodes
        for i in range(3):
            data = sample_node_data.copy()
            data["name"] = f"Test Node {i}"
            client.post(
                "/nodes/",
                json=data,
                headers={"Authorization": "Bearer test-token"}
            )
        
        # List nodes
        response = client.get(
            "/nodes/",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3
    
    @patch('app.deps.verify_token')
    def test_update_node_endpoint(self, mock_verify_token, sample_node_data, mock_jwt_token):
        """Test updating a node via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        # Create a node first
        create_response = client.post(
            "/nodes/",
            json=sample_node_data,
            headers={"Authorization": "Bearer test-token"}
        )
        node_id = create_response.json()["id"]
        
        # Update the node
        update_data = {"name": "Updated Node", "description": "Updated description"}
        response = client.put(
            f"/nodes/{node_id}",
            json=update_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Node"
        assert data["description"] == "Updated description"
    
    @patch('app.deps.verify_token')
    def test_delete_node_endpoint(self, mock_verify_token, sample_node_data, mock_jwt_token):
        """Test deleting a node via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        # Create a node first
        create_response = client.post(
            "/nodes/",
            json=sample_node_data,
            headers={"Authorization": "Bearer test-token"}
        )
        node_id = create_response.json()["id"]
        
        # Delete the node
        response = client.delete(
            f"/nodes/{node_id}",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 204
    
    @patch('app.deps.verify_token')
    def test_create_node_link_endpoint(self, mock_verify_token, sample_link_data, mock_jwt_token):
        """Test creating a node link via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        # Create a node first
        node_data = {"name": "Test Node", "node_type": "vm"}
        node_response = client.post(
            "/nodes/",
            json=node_data,
            headers={"Authorization": "Bearer test-token"}
        )
        node_id = node_response.json()["id"]
        
        # Create a link
        response = client.post(
            f"/nodes/{node_id}/links",
            json=sample_link_data,
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["node_id"] == node_id
        assert data["link_type"] == "hosts"
    
    @patch('app.deps.verify_token')
    def test_get_deployment_map_endpoint(self, mock_verify_token, sample_node_data, mock_jwt_token):
        """Test getting deployment map via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        # Create a node first
        create_response = client.post(
            "/nodes/",
            json=sample_node_data,
            headers={"Authorization": "Bearer test-token"}
        )
        node_id = create_response.json()["id"]
        
        # Get deployment map
        response = client.get(
            f"/nodes/{node_id}/deployment-map",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["node_id"] == node_id
        assert "deployed_components" in data
        assert "deployment_status" in data
    
    @patch('app.deps.verify_token')
    def test_get_capacity_analysis_endpoint(self, mock_verify_token, sample_node_data, mock_jwt_token):
        """Test getting capacity analysis via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        # Create a node first
        create_response = client.post(
            "/nodes/",
            json=sample_node_data,
            headers={"Authorization": "Bearer test-token"}
        )
        node_id = create_response.json()["id"]
        
        # Get capacity analysis
        response = client.get(
            f"/nodes/{node_id}/capacity-analysis",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["node_id"] == node_id
        assert "current_capacity" in data
        assert "projected_capacity" in data
    
    @patch('app.deps.verify_token')
    def test_analyze_node_endpoint(self, mock_verify_token, sample_node_data, mock_jwt_token):
        """Test analyzing a node via API."""
        mock_verify_token.return_value = mock_jwt_token
        
        # Create a node first
        create_response = client.post(
            "/nodes/",
            json=sample_node_data,
            headers={"Authorization": "Bearer test-token"}
        )
        node_id = create_response.json()["id"]
        
        # Analyze the node
        response = client.get(
            f"/nodes/{node_id}/analysis",
            headers={"Authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["node_id"] == node_id
        assert "operational_health" in data
        assert "performance_metrics" in data

class TestAuthentication:
    """Test authentication and authorization."""
    
    def test_missing_token(self):
        """Test endpoint without authentication token."""
        response = client.get("/nodes/")
        assert response.status_code == 403
    
    @patch('app.deps.verify_token')
    def test_invalid_token(self, mock_verify_token):
        """Test endpoint with invalid token."""
        mock_verify_token.side_effect = Exception("Invalid token")
        
        response = client.get(
            "/nodes/",
            headers={"Authorization": "Bearer invalid-token"}
        )
        assert response.status_code == 401
    
    @patch('app.deps.verify_token')
    def test_insufficient_permissions(self, mock_verify_token):
        """Test endpoint with insufficient permissions."""
        mock_verify_token.return_value = {
            "tenant_id": str(uuid4()),
            "user_id": str(uuid4()),
            "role": "Viewer",
            "permissions": ["node:read"]
        }
        
        response = client.post(
            "/nodes/",
            json={"name": "Test Node"},
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 403

class TestValidation:
    """Test input validation."""
    
    @patch('app.deps.verify_token')
    def test_invalid_node_type(self, mock_verify_token, mock_jwt_token):
        """Test creating node with invalid node type."""
        mock_verify_token.return_value = mock_jwt_token
        
        invalid_data = {
            "name": "Test Node",
            "node_type": "invalid_type"
        }
        
        response = client.post(
            "/nodes/",
            json=invalid_data,
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 422
    
    @patch('app.deps.verify_token')
    def test_invalid_availability_target(self, mock_verify_token, mock_jwt_token):
        """Test creating node with invalid availability target."""
        mock_verify_token.return_value = mock_jwt_token
        
        invalid_data = {
            "name": "Test Node",
            "availability_target": 150.0  # Invalid: > 100
        }
        
        response = client.post(
            "/nodes/",
            json=invalid_data,
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 422

class TestHealthEndpoints:
    """Test health and metrics endpoints."""
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "service" in data
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "node_service_requests_total" in response.text
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "version" in data
        assert "archimate" in data

if __name__ == "__main__":
    pytest.main([__file__]) 
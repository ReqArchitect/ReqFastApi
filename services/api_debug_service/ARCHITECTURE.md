# API Debug Service - Architecture

## Overview

The Enhanced API Debug Service implements a multi-layered discovery strategy to identify and visualize ReqArchitect microservices without modifying existing containers or configurations.

## 🏗️ Architecture Design

### Core Principles

1. **Non-Intrusive Operation**: Read-only access to Docker containers and services
2. **Multi-Method Discovery**: Label-based, catalog fallback, and network scanning
3. **Graceful Degradation**: Service continues operating even if some discovery methods fail
4. **Caching Strategy**: Redis-based caching with configurable TTL
5. **Health Monitoring**: Real-time health checking with multiple endpoint verification

### Component Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Enhanced FastAPI App                     │
├─────────────────────────────────────────────────────────────┤
│  Health Check │ API Endpoints │ Cache Mgmt │ Error Handler │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Enhanced Service Discovery                     │
├─────────────────────────────────────────────────────────────┤
│  • Multi-Method Discovery    │  • Health Assessment        │
│  • Fallback Strategies       │  • Error Handling           │
│  • Container Inspection      │  • Logging & Metrics        │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
┌─────────────────────────┐  ┌─────────────────────────┐
│  Enhanced Docker Service│  │ Enhanced Endpoint Disc. │
├─────────────────────────┤  ├─────────────────────────┤
│  • Label-Based Detection│  │  • Swagger/OpenAPI      │
│  • Catalog Fallback     │  │  • API Reference Docs   │
│  • Network Scanning     │  │  • Known Patterns       │
│  • Health Checking      │  │  • Health Endpoints     │
│  • Virtual Containers   │  │  • Catalog Integration  │
└─────────────────────────┘  └─────────────────────────┘
                    │                   │
                    ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                    Cache Service                           │
├─────────────────────────────────────────────────────────────┤
│  • Redis Integration    │  • TTL Management             │
│  • Serialization       │  • Cache Invalidation         │
│  • Error Handling      │  • Statistics & Monitoring     │
└─────────────────────────────────────────────────────────────┘
```

## 🔍 Discovery Methods

### 1. Label-Based Detection

**Primary Method**: Uses Docker labels to identify ReqArchitect services

**Label Requirements**:
```yaml
labels:
  reqarchitect-service: "true"
  service-name: "goal_service"  # Optional but recommended
```

**Implementation**:
```python
def _discover_labeled_containers(self) -> List[DockerContainerInfo]:
    labeled_containers = self.client.containers.list(
        filters={
            "label": "reqarchitect-service=true",
            "status": "running"
        }
    )
```

**Advantages**:
- Explicit service identification
- Reliable and predictable
- Supports custom metadata

**Fallback**: If no labeled containers found, proceed to catalog fallback

### 2. Service Catalog Fallback

**Secondary Method**: Uses predefined service catalog for discovery

**Catalog Structure**:
```json
[
  {
    "service_name": "goal_service",
    "base_url": "http://goal_service:8013",
    "container_name": "goal_service",
    "routes": ["/goals", "/goals/{id}", "/goals/{id}/assessment"],
    "healthcheck": "/health",
    "port": 8013,
    "description": "Goal management service"
  }
]
```

**Implementation**:
```python
def _discover_catalog_containers(self, existing_containers: List[DockerContainerInfo]) -> List[DockerContainerInfo]:
    for catalog_entry in self.service_catalog:
        if not self._is_already_discovered(catalog_entry, existing_containers):
            container = self._find_container_by_name(catalog_entry["container_name"])
            if container:
                # Use real container
                container_info = self._extract_container_info(container, catalog_entry)
            else:
                # Create virtual container
                container_info = self._create_virtual_container_info(catalog_entry)
```

**Advantages**:
- Works without Docker labels
- Provides known endpoint patterns
- Supports virtual containers for missing services

### 3. Network Scanning

**Tertiary Method**: Scans Docker network for potential ReqArchitect services

**Scanning Criteria**:
- Container name patterns (`_service`, `service_`, `reqarchitect`)
- Image name patterns
- Network membership

**Implementation**:
```python
def _is_reqarchitect_container(self, container) -> bool:
    container_name = container.name.lstrip("/")
    reqarchitect_patterns = ["_service", "service_", "reqarchitect", "reqfastapi"]
    
    if any(pattern in container_name.lower() for pattern in reqarchitect_patterns):
        return True
    
    image_name = container.image.lower()
    if any(pattern in image_name for pattern in reqarchitect_patterns):
        return True
    
    return False
```

**Advantages**:
- Discovers unlabeled services
- Handles legacy containers
- Automatic pattern recognition

## 🛡️ Safety Mechanisms

### Non-Intrusive Design

1. **Read-Only Docker Access**
   ```python
   # Only inspect, never modify
   container_info = container.attrs
   ports = container_info.get("NetworkSettings", {}).get("Ports", {})
   ```

2. **Safe Health Checking**
   ```python
   # Use HEAD requests for verification
   response = await client.head(f"{base_url}{endpoint.path}")
   if response.status_code in [200, 404, 405]:  # 404/405 means endpoint exists
   ```

3. **Error Isolation**
   ```python
   try:
       service_map = await create_service_map_from_container(container)
   except Exception as e:
       logger.error(f"Error processing container {container.name}: {e}")
       continue  # Continue with other containers
   ```

### Graceful Degradation

1. **Docker Client Failure**
   - Log warning and continue with catalog fallback
   - Return empty results rather than crash

2. **Redis Cache Failure**
   - Continue without caching
   - Slower but functional operation

3. **Service Health Check Failure**
   - Mark service as unhealthy
   - Continue discovery process

## 📊 Data Flow

### Discovery Process

```
1. Label-Based Discovery
   ├── Scan for labeled containers
   ├── Extract service information
   └── Verify health status

2. Catalog Fallback (if enabled)
   ├── Load service catalog
   ├── Find matching containers
   ├── Create virtual containers for missing services
   └── Apply known endpoint patterns

3. Network Scanning (if enabled)
   ├── Scan all running containers
   ├── Apply pattern matching
   └── Extract service information

4. Deduplication & Health Checking
   ├── Remove duplicate services
   ├── Perform health checks
   └── Cache results
```

### Health Check Process

```
1. Determine Base URL
   ├── Extract from port mappings
   ├── Parse container network settings
   └── Fallback to catalog entry

2. Test Health Endpoints
   ├── Try /health endpoint
   ├── Try /healthz endpoint
   ├── Try /ping endpoint
   └── Try root endpoint

3. Evaluate Results
   ├── 200: Healthy
   ├── 404/405: Endpoint exists (healthy)
   ├── Timeout/Error: Unhealthy
   └── No response: Unknown
```

## 🔧 Configuration

### Environment Variables

```bash
# Discovery Configuration
ENABLE_CATALOG_FALLBACK=true
ENABLE_NETWORK_SCAN=true
ENABLE_VIRTUAL_CONTAINERS=true

# Docker Configuration
DOCKER_NETWORK=reqarchitect-network
SERVICE_LABEL=reqarchitect-service=true
SERVICE_NAME_LABEL=service-name

# Cache Configuration
REDIS_URL=redis://localhost:6379
CACHE_TTL_SECONDS=300

# Health Check Configuration
HEALTH_CHECK_TIMEOUT=5
ENDPOINT_DISCOVERY_TIMEOUT=10
MAX_RETRIES=3
```

### Service Discovery Config

```python
class ServiceDiscoveryConfig(BaseModel):
    docker_network: str = "reqarchitect-network"
    service_label: str = "reqarchitect-service=true"
    service_name_label: str = "service-name"
    cache_ttl_seconds: int = 300
    health_check_timeout: int = 5
    endpoint_discovery_timeout: int = 10
    max_retries: int = 3
    enable_catalog_fallback: bool = True
    enable_network_scan: bool = True
    enable_virtual_containers: bool = True
```

## 📈 Performance Considerations

### Caching Strategy

1. **Cache Levels**
   - Service discovery results (5 minutes TTL)
   - Health check results (2 minutes TTL)
   - Endpoint discovery results (10 minutes TTL)

2. **Cache Keys**
   ```
   api_debug:all_services
   api_debug:service:{service_name}
   api_debug:health_summary
   api_debug:health:{service_name}
   ```

3. **Cache Invalidation**
   - Manual refresh via API endpoint
   - Automatic TTL expiration
   - Force refresh on errors

### Discovery Performance

1. **Parallel Processing**
   ```python
   # Process containers in parallel
   tasks = [create_service_map_from_container(container) for container in containers]
   results = await asyncio.gather(*tasks, return_exceptions=True)
   ```

2. **Timeout Management**
   ```python
   # Individual timeouts for each operation
   health_check_timeout = 5
   endpoint_discovery_timeout = 10
   docker_operation_timeout = 30
   ```

3. **Resource Limits**
   - Maximum concurrent health checks: 10
   - Maximum retry attempts: 3
   - Maximum cache size: 1000 entries

## 🔄 Error Handling

### Error Categories

1. **Docker Errors**
   - Connection failures
   - Permission denied
   - Container not found

2. **Network Errors**
   - Service unreachable
   - Timeout errors
   - Connection refused

3. **Cache Errors**
   - Redis connection failure
   - Serialization errors
   - Cache corruption

### Error Recovery

1. **Automatic Retry**
   ```python
   for attempt in range(self.max_retries):
       try:
           result = await operation()
           break
       except Exception as e:
           if attempt == self.max_retries - 1:
               raise
           await asyncio.sleep(2 ** attempt)  # Exponential backoff
   ```

2. **Fallback Strategies**
   - Docker failure → Catalog only
   - Health check failure → Mark as unknown
   - Cache failure → No caching

3. **Error Logging**
   ```python
   logger.error(f"Error in {operation}: {e}", 
                extra={"service": service_name, "attempt": attempt})
   ```

## 🧪 Testing Strategy

### Test Scenarios

1. **Label-Based Discovery**
   - Containers with proper labels
   - Containers with missing labels
   - Mixed labeled/unlabeled containers

2. **Catalog Fallback**
   - Services in catalog only
   - Services with containers and catalog
   - Missing services

3. **Network Scanning**
   - Pattern-based discovery
   - Legacy container detection
   - False positive handling

4. **Health Checking**
   - Healthy services
   - Unhealthy services
   - Unreachable services

### Test Data

```yaml
# Test containers
test_containers:
  - name: "goal_service"
    labels: {"reqarchitect-service": "true", "service-name": "goal_service"}
    image: "reqarchitect/goal_service:latest"
    ports: {"8013/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8013"}]}
  
  - name: "legacy_service"
    labels: {}
    image: "old/legacy_service:latest"
    ports: {"8000/tcp": [{"HostIp": "0.0.0.0", "HostPort": "8000"}]}
```

## 🔮 Future Enhancements

### Planned Features

1. **Service Mesh Integration**
   - Istio service discovery
   - Envoy proxy integration
   - mTLS endpoint detection

2. **Kubernetes Support**
   - Pod-based discovery
   - Service account integration
   - Namespace filtering

3. **Advanced Health Checking**
   - Custom health check scripts
   - Dependency health checking
   - Circuit breaker patterns

4. **Real-time Updates**
   - WebSocket notifications
   - Event-driven updates
   - Live health monitoring

### Extension Points

1. **Plugin Architecture**
   - Custom discovery methods
   - Service-specific adapters
   - Third-party integrations

2. **API Extensions**
   - GraphQL endpoint
   - Bulk operations
   - Advanced filtering

3. **Monitoring Integration**
   - Prometheus metrics
   - Grafana dashboards
   - Alert integration 
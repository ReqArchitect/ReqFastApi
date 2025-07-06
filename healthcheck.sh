#!/bin/bash

# Health Check Script for FastAPI Microservices
# This script validates that all services are running and responding correctly

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Service configurations
declare -A SERVICES=(
    ["gateway_service"]="http://localhost:8080/health"
    ["auth_service"]="http://localhost:8001/health"
    ["ai_modeling_service"]="http://localhost:8002/health"
    ["billing_service"]="http://localhost:8010/health"
    ["invoice_service"]="http://localhost:8011/health"
    ["notification_service"]="http://localhost:8000/health"
    ["usage_service"]="http://localhost:8000/health"
    ["analytics_service"]="http://localhost:8000/health"
    ["feedback_service"]="http://localhost:8000/health"
    ["event_bus_service"]="http://localhost:8000/health"
    ["onboarding_state_service"]="http://localhost:8000/health"
    ["audit_log_service"]="http://localhost:8000/health"
)

# Function to check if a service is healthy
check_service() {
    local service_name=$1
    local health_url=$2
    local max_retries=30
    local retry_count=0
    
    echo -e "${YELLOW}Checking ${service_name}...${NC}"
    
    while [ $retry_count -lt $max_retries ]; do
        if curl -f -s "$health_url" > /dev/null 2>&1; then
            echo -e "${GREEN}✅ ${service_name} is healthy${NC}"
            return 0
        else
            echo -e "${YELLOW}⏳ ${service_name} not ready yet (attempt $((retry_count + 1))/$max_retries)${NC}"
            sleep 2
            retry_count=$((retry_count + 1))
        fi
    done
    
    echo -e "${RED}❌ ${service_name} failed health check after $max_retries attempts${NC}"
    return 1
}

# Function to check database connectivity
check_database() {
    echo -e "${YELLOW}Checking database connectivity...${NC}"
    
    if docker exec postgres_db pg_isready -U postgres > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Database is ready${NC}"
        return 0
    else
        echo -e "${RED}❌ Database is not ready${NC}"
        return 1
    fi
}

# Function to check Redis connectivity
check_redis() {
    echo -e "${YELLOW}Checking Redis connectivity...${NC}"
    
    if docker exec event_bus redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Redis is ready${NC}"
        return 0
    else
        echo -e "${RED}❌ Redis is not ready${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo "🚀 Starting health check for FastAPI microservices..."
    echo "=================================================="
    
    # Check infrastructure services first
    check_database
    check_redis
    
    echo ""
    echo "🔍 Checking application services..."
    echo "=================================="
    
    failed_services=()
    
    # Check each service
    for service_name in "${!SERVICES[@]}"; do
        if ! check_service "$service_name" "${SERVICES[$service_name]}"; then
            failed_services+=("$service_name")
        fi
        echo ""
    done
    
    # Summary
    echo "📊 Health Check Summary"
    echo "======================"
    
    if [ ${#failed_services[@]} -eq 0 ]; then
        echo -e "${GREEN}🎉 All services are healthy!${NC}"
        exit 0
    else
        echo -e "${RED}❌ The following services failed health checks:${NC}"
        for service in "${failed_services[@]}"; do
            echo -e "${RED}   - $service${NC}"
        done
        exit 1
    fi
}

# Run main function
main "$@" 
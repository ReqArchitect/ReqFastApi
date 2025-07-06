#!/bin/bash

# Integration Test Runner Script
# This script runs the complete integration test suite for FastAPI microservices

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SERVICES=(
    "gateway_service"
    "auth_service" 
    "ai_modeling_service"
    "usage_service"
    "invoice_service"
    "notification_service"
    "billing_service"
)

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "docker-compose is not installed. Please install it and try again."
        exit 1
    fi
    print_success "docker-compose is available"
}

# Function to check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed. Please install it and try again."
        exit 1
    fi
    print_success "Python 3 is available"
}

# Function to check if required Python packages are installed
check_python_dependencies() {
    print_status "Checking Python dependencies..."
    
    local missing_packages=()
    
    # Check for required packages
    python3 -c "import requests" 2>/dev/null || missing_packages+=("requests")
    python3 -c "import pytest" 2>/dev/null || missing_packages+=("pytest")
    python3 -c "import uuid" 2>/dev/null || missing_packages+=("uuid")
    
    if [ ${#missing_packages[@]} -ne 0 ]; then
        print_warning "Missing Python packages: ${missing_packages[*]}"
        print_status "Installing missing packages..."
        pip3 install "${missing_packages[@]}"
        print_success "Python dependencies installed"
    else
        print_success "All Python dependencies are available"
    fi
}

# Function to start services
start_services() {
    print_status "Starting microservices..."
    
    # Build and start services
    docker-compose build "${SERVICES[@]}"
    
    # Start services in background
    docker-compose up -d "${SERVICES[@]}"
    
    print_success "Services started"
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        print_status "Attempt $attempt/$max_attempts - Checking service health..."
        
        local all_healthy=true
        
        # Check gateway service
        if curl -f http://localhost:8080/health > /dev/null 2>&1; then
            print_success "Gateway service is healthy"
        else
            print_warning "Gateway service not ready yet"
            all_healthy=false
        fi
        
        # Check auth service
        if curl -f http://localhost:8001/health > /dev/null 2>&1; then
            print_success "Auth service is healthy"
        else
            print_warning "Auth service not ready yet"
            all_healthy=false
        fi
        
        # Check AI modeling service
        if curl -f http://localhost:8002/health > /dev/null 2>&1; then
            print_success "AI Modeling service is healthy"
        else
            print_warning "AI Modeling service not ready yet"
            all_healthy=false
        fi
        
        # Check invoice service
        if curl -f http://localhost:8011/health > /dev/null 2>&1; then
            print_success "Invoice service is healthy"
        else
            print_warning "Invoice service not ready yet"
            all_healthy=false
        fi
        
        # Check billing service
        if curl -f http://localhost:8010/health > /dev/null 2>&1; then
            print_success "Billing service is healthy"
        else
            print_warning "Billing service not ready yet"
            all_healthy=false
        fi
        
        if [ "$all_healthy" = true ]; then
            print_success "All services are healthy and ready!"
            return 0
        fi
        
        if [ $attempt -lt $max_attempts ]; then
            print_status "Waiting 10 seconds before next attempt..."
            sleep 10
        fi
        
        ((attempt++))
    done
    
    print_error "Services failed to become healthy within the timeout period"
    return 1
}

# Function to run integration tests
run_integration_tests() {
    print_status "Running integration tests..."
    
    # Run the integration test suite
    if python3 integration_tests.py; then
        print_success "Integration tests completed successfully!"
        return 0
    else
        print_error "Integration tests failed!"
        return 1
    fi
}

# Function to run health checks
run_health_checks() {
    print_status "Running health checks..."
    
    if [ -f "./healthcheck.sh" ]; then
        if ./healthcheck.sh; then
            print_success "Health checks passed!"
            return 0
        else
            print_error "Health checks failed!"
            return 1
        fi
    else
        print_warning "Health check script not found, skipping health checks"
        return 0
    fi
}

# Function to show service logs
show_logs() {
    print_status "Showing service logs..."
    
    echo "=== Gateway Service Logs ==="
    docker-compose logs gateway_service --tail=20
    
    echo "=== Auth Service Logs ==="
    docker-compose logs auth_service --tail=20
    
    echo "=== AI Modeling Service Logs ==="
    docker-compose logs ai_modeling_service --tail=20
    
    echo "=== Invoice Service Logs ==="
    docker-compose logs invoice_service --tail=20
    
    echo "=== Billing Service Logs ==="
    docker-compose logs billing_service --tail=20
}

# Function to stop services
stop_services() {
    print_status "Stopping services..."
    docker-compose down
    print_success "Services stopped"
}

# Function to cleanup
cleanup() {
    print_status "Cleaning up..."
    
    # Stop services
    stop_services
    
    # Remove test containers and networks
    docker-compose down --remove-orphans
    
    print_success "Cleanup completed"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -s, --start-only    Only start services, don't run tests"
    echo "  -t, --test-only     Only run tests, don't start/stop services"
    echo "  -l, --logs          Show service logs after tests"
    echo "  -c, --cleanup       Clean up after tests (default)"
    echo "  --no-cleanup        Don't clean up after tests"
    echo ""
    echo "Examples:"
    echo "  $0                  # Run complete integration test suite"
    echo "  $0 -s               # Only start services"
    echo "  $0 -t               # Only run tests (assumes services are running)"
    echo "  $0 -l               # Show logs after tests"
    echo "  $0 --no-cleanup     # Keep services running after tests"
}

# Main function
main() {
    local start_only=false
    local test_only=false
    local show_logs_flag=false
    local cleanup_flag=true
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -s|--start-only)
                start_only=true
                shift
                ;;
            -t|--test-only)
                test_only=true
                shift
                ;;
            -l|--logs)
                show_logs_flag=true
                shift
                ;;
            -c|--cleanup)
                cleanup_flag=true
                shift
                ;;
            --no-cleanup)
                cleanup_flag=false
                shift
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    print_status "Starting FastAPI Microservices Integration Test Suite"
    echo "================================================================"
    
    # Check prerequisites
    check_docker
    check_docker_compose
    check_python
    check_python_dependencies
    
    # Set up trap to cleanup on exit
    if [ "$cleanup_flag" = true ]; then
        trap cleanup EXIT
    fi
    
    # Start services if not test-only mode
    if [ "$test_only" = false ]; then
        start_services
        wait_for_services
    fi
    
    # Run health checks
    run_health_checks
    
    # Run integration tests if not start-only mode
    if [ "$start_only" = false ]; then
        run_integration_tests
        test_exit_code=$?
        
        # Show logs if requested
        if [ "$show_logs_flag" = true ]; then
            show_logs
        fi
        
        # Exit with test result
        exit $test_exit_code
    else
        print_success "Services started successfully. Use '$0 -t' to run tests."
        print_status "Services will continue running. Use 'docker-compose down' to stop them."
    fi
}

# Run main function with all arguments
main "$@" 
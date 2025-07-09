#!/bin/bash

# ReqArchitect Continuous Validation Framework Runner
# This script provides easy access to the validation framework

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATION_SCRIPT="$SCRIPT_DIR/continuous_validation_framework.py"
CONFIG_FILE="$SCRIPT_DIR/validation_config.json"
OUTPUT_DIR="$SCRIPT_DIR/validation_outputs"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if services are up
check_services() {
    print_status "Checking if ReqArchitect services are running..."
    
    local services=(
        "gateway_service:8080"
        "auth_service:8001"
        "ai_modeling_service:8002"
        "usage_service:8005"
        "notification_service:8006"
        "audit_log_service:8007"
        "billing_service:8010"
        "invoice_service:8011"
        "monitoring_dashboard_service:8012"
    )
    
    local all_services_up=true
    
    for service in "${services[@]}"; do
        local service_name=$(echo $service | cut -d: -f1)
        local port=$(echo $service | cut -d: -f2)
        
        if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
            print_success "$service_name is responding on port $port"
        else
            print_warning "$service_name is not responding on port $port"
            all_services_up=false
        fi
    done
    
    if [ "$all_services_up" = false ]; then
        print_warning "Some services are not responding. Validation may fail for those services."
    else
        print_success "All services are responding"
    fi
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ ! -f "$SCRIPT_DIR/validation_requirements.txt" ]; then
        print_error "validation_requirements.txt not found"
        exit 1
    fi
    
    pip install -r "$SCRIPT_DIR/validation_requirements.txt"
    print_success "Dependencies installed"
}

# Function to run validation once
run_once() {
    print_status "Running validation once..."
    python "$VALIDATION_SCRIPT" --run-once
}

# Function to show dashboard
show_dashboard() {
    print_status "Showing current dashboard..."
    python "$VALIDATION_SCRIPT" --dashboard
}

# Function to start scheduler
start_scheduler() {
    print_status "Starting continuous validation scheduler..."
    print_status "Press Ctrl+C to stop the scheduler"
    python "$VALIDATION_SCRIPT" --scheduler
}

# Function to show recent reports
show_reports() {
    print_status "Recent validation reports:"
    
    if [ ! -d "$OUTPUT_DIR" ]; then
        print_warning "No validation outputs directory found"
        return
    fi
    
    local reports=$(find "$OUTPUT_DIR" -name "validation_report_*.md" -type f | sort -r | head -5)
    
    if [ -z "$reports" ]; then
        print_warning "No validation reports found"
        return
    fi
    
    for report in $reports; do
        local filename=$(basename "$report")
        local timestamp=$(echo "$filename" | sed 's/validation_report_\(.*\)\.md/\1/')
        echo "  - $filename (generated: $timestamp)"
    done
}

# Function to show help
show_help() {
    echo "ReqArchitect Continuous Validation Framework"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  run-once      Run validation once and exit"
    echo "  dashboard     Show current dashboard"
    echo "  scheduler     Start continuous validation scheduler"
    echo "  install       Install Python dependencies"
    echo "  check         Check if services are running"
    echo "  reports       Show recent validation reports"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 run-once     # Run validation once"
    echo "  $0 dashboard    # Show current status"
    echo "  $0 scheduler    # Start continuous monitoring"
    echo ""
}

# Main script logic
case "${1:-help}" in
    "run-once")
        check_docker
        check_services
        run_once
        ;;
    "dashboard")
        show_dashboard
        ;;
    "scheduler")
        check_docker
        check_services
        start_scheduler
        ;;
    "install")
        install_dependencies
        ;;
    "check")
        check_docker
        check_services
        ;;
    "reports")
        show_reports
        ;;
    "help"|*)
        show_help
        ;;
esac 
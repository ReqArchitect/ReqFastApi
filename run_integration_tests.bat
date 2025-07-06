@echo off
REM Integration Test Runner Script for Windows
REM This script runs the complete integration test suite for FastAPI microservices

setlocal enabledelayedexpansion

REM Configuration
set SERVICES=gateway_service auth_service ai_modeling_service usage_service invoice_service notification_service billing_service

REM Colors for output (Windows 10+ supports ANSI colors)
set RED=[91m
set GREEN=[92m
set YELLOW=[93m
set BLUE=[94m
set NC=[0m

REM Function to print colored output
:print_status
echo %BLUE%[%date% %time%]%NC% %~1
goto :eof

:print_success
echo %GREEN%✅ %~1%NC%
goto :eof

:print_warning
echo %YELLOW%⚠️  %~1%NC%
goto :eof

:print_error
echo %RED%❌ %~1%NC%
goto :eof

REM Function to check if Docker is running
:check_docker
docker info >nul 2>&1
if errorlevel 1 (
    call :print_error "Docker is not running. Please start Docker Desktop and try again."
    exit /b 1
)
call :print_success "Docker is running"
goto :eof

REM Function to check if docker-compose is available
:check_docker_compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :print_error "docker-compose is not installed. Please install it and try again."
    exit /b 1
)
call :print_success "docker-compose is available"
goto :eof

REM Function to check if Python is available
:check_python
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        call :print_error "Python is not installed. Please install Python 3 and try again."
        exit /b 1
    )
)
call :print_success "Python is available"
goto :eof

REM Function to check if required Python packages are installed
:check_python_dependencies
call :print_status "Checking Python dependencies..."

set missing_packages=

REM Check for required packages
python -c "import requests" 2>nul || set missing_packages=!missing_packages! requests
python -c "import pytest" 2>nul || set missing_packages=!missing_packages! pytest
python -c "import uuid" 2>nul || set missing_packages=!missing_packages! uuid

if not "!missing_packages!"=="" (
    call :print_warning "Missing Python packages: !missing_packages!"
    call :print_status "Installing missing packages..."
    pip install !missing_packages!
    call :print_success "Python dependencies installed"
) else (
    call :print_success "All Python dependencies are available"
)
goto :eof

REM Function to start services
:start_services
call :print_status "Starting microservices..."

REM Build and start services
docker-compose build %SERVICES%

REM Start services in background
docker-compose up -d %SERVICES%

call :print_success "Services started"
goto :eof

REM Function to wait for services to be ready
:wait_for_services
call :print_status "Waiting for services to be ready..."

set max_attempts=30
set attempt=1

:wait_loop
call :print_status "Attempt !attempt!/!max_attempts! - Checking service health..."

set all_healthy=true

REM Check gateway service
curl -f http://localhost:8080/health >nul 2>&1
if errorlevel 1 (
    call :print_warning "Gateway service not ready yet"
    set all_healthy=false
) else (
    call :print_success "Gateway service is healthy"
)

REM Check auth service
curl -f http://localhost:8001/health >nul 2>&1
if errorlevel 1 (
    call :print_warning "Auth service not ready yet"
    set all_healthy=false
) else (
    call :print_success "Auth service is healthy"
)

REM Check AI modeling service
curl -f http://localhost:8002/health >nul 2>&1
if errorlevel 1 (
    call :print_warning "AI Modeling service not ready yet"
    set all_healthy=false
) else (
    call :print_success "AI Modeling service is healthy"
)

REM Check invoice service
curl -f http://localhost:8011/health >nul 2>&1
if errorlevel 1 (
    call :print_warning "Invoice service not ready yet"
    set all_healthy=false
) else (
    call :print_success "Invoice service is healthy"
)

REM Check billing service
curl -f http://localhost:8010/health >nul 2>&1
if errorlevel 1 (
    call :print_warning "Billing service not ready yet"
    set all_healthy=false
) else (
    call :print_success "Billing service is healthy"
)

if "!all_healthy!"=="true" (
    call :print_success "All services are healthy and ready!"
    goto :eof
)

if !attempt! lss !max_attempts! (
    call :print_status "Waiting 10 seconds before next attempt..."
    timeout /t 10 /nobreak >nul
    set /a attempt+=1
    goto :wait_loop
)

call :print_error "Services failed to become healthy within the timeout period"
exit /b 1

REM Function to run integration tests
:run_integration_tests
call :print_status "Running integration tests..."

REM Run the integration test suite
python integration_tests.py
if errorlevel 1 (
    call :print_error "Integration tests failed!"
    exit /b 1
) else (
    call :print_success "Integration tests completed successfully!"
)
goto :eof

REM Function to run health checks
:run_health_checks
call :print_status "Running health checks..."

if exist "healthcheck.sh" (
    REM Convert Unix script to Windows or use PowerShell
    powershell -ExecutionPolicy Bypass -File healthcheck.ps1
    if errorlevel 1 (
        call :print_error "Health checks failed!"
        exit /b 1
    ) else (
        call :print_success "Health checks passed!"
    )
) else (
    call :print_warning "Health check script not found, skipping health checks"
)
goto :eof

REM Function to show service logs
:show_logs
call :print_status "Showing service logs..."

echo === Gateway Service Logs ===
docker-compose logs gateway_service --tail=20

echo === Auth Service Logs ===
docker-compose logs auth_service --tail=20

echo === AI Modeling Service Logs ===
docker-compose logs ai_modeling_service --tail=20

echo === Invoice Service Logs ===
docker-compose logs invoice_service --tail=20

echo === Billing Service Logs ===
docker-compose logs billing_service --tail=20
goto :eof

REM Function to stop services
:stop_services
call :print_status "Stopping services..."
docker-compose down
call :print_success "Services stopped"
goto :eof

REM Function to cleanup
:cleanup
call :print_status "Cleaning up..."

REM Stop services
call :stop_services

REM Remove test containers and networks
docker-compose down --remove-orphans

call :print_success "Cleanup completed"
goto :eof

REM Function to show help
:show_help
echo Usage: %~nx0 [OPTIONS]
echo.
echo Options:
echo   -h, --help          Show this help message
echo   -s, --start-only    Only start services, don't run tests
echo   -t, --test-only     Only run tests, don't start/stop services
echo   -l, --logs          Show service logs after tests
echo   -c, --cleanup       Clean up after tests ^(default^)
echo   --no-cleanup        Don't clean up after tests
echo.
echo Examples:
echo   %~nx0                  # Run complete integration test suite
echo   %~nx0 -s               # Only start services
echo   %~nx0 -t               # Only run tests ^(assumes services are running^)
echo   %~nx0 -l               # Show logs after tests
echo   %~nx0 --no-cleanup     # Keep services running after tests
goto :eof

REM Main function
:main
set start_only=false
set test_only=false
set show_logs_flag=false
set cleanup_flag=true

REM Parse command line arguments
:parse_args
if "%~1"=="" goto :args_done
if "%~1"=="-h" goto :show_help
if "%~1"=="--help" goto :show_help
if "%~1"=="-s" set start_only=true
if "%~1"=="--start-only" set start_only=true
if "%~1"=="-t" set test_only=true
if "%~1"=="--test-only" set test_only=true
if "%~1"=="-l" set show_logs_flag=true
if "%~1"=="--logs" set show_logs_flag=true
if "%~1"=="-c" set cleanup_flag=true
if "%~1"=="--cleanup" set cleanup_flag=true
if "%~1"=="--no-cleanup" set cleanup_flag=false
shift
goto :parse_args

:args_done
call :print_status "Starting FastAPI Microservices Integration Test Suite"
echo ================================================================

REM Check prerequisites
call :check_docker
if errorlevel 1 exit /b 1

call :check_docker_compose
if errorlevel 1 exit /b 1

call :check_python
if errorlevel 1 exit /b 1

call :check_python_dependencies

REM Start services if not test-only mode
if "%test_only%"=="false" (
    call :start_services
    call :wait_for_services
    if errorlevel 1 exit /b 1
)

REM Run health checks
call :run_health_checks

REM Run integration tests if not start-only mode
if "%start_only%"=="false" (
    call :run_integration_tests
    set test_exit_code=!errorlevel!
    
    REM Show logs if requested
    if "%show_logs_flag%"=="true" (
        call :show_logs
    )
    
    REM Exit with test result
    exit /b !test_exit_code!
) else (
    call :print_success "Services started successfully. Use '%~nx0 -t' to run tests."
    call :print_status "Services will continue running. Use 'docker-compose down' to stop them."
)

goto :eof

REM Run main function
call :main %* 
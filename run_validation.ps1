# ReqArchitect Continuous Validation Framework Runner (PowerShell)
# This script provides easy access to the validation framework on Windows

param(
    [Parameter(Position=0)]
    [string]$Action = "help"
)

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ValidationScript = Join-Path $ScriptDir "continuous_validation_framework.py"
$ConfigFile = Join-Path $ScriptDir "validation_config.json"
$OutputDir = Join-Path $ScriptDir "validation_outputs"

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if Docker is running
function Test-Docker {
    try {
        docker info | Out-Null
        Write-Success "Docker is running"
        return $true
    }
    catch {
        Write-Error "Docker is not running. Please start Docker and try again."
        return $false
    }
}

# Function to check if services are up
function Test-Services {
    Write-Status "Checking if ReqArchitect services are running..."
    
    $services = @(
        @{Name="gateway_service"; Port=8080},
        @{Name="auth_service"; Port=8001},
        @{Name="ai_modeling_service"; Port=8002},
        @{Name="usage_service"; Port=8005},
        @{Name="notification_service"; Port=8006},
        @{Name="audit_log_service"; Port=8007},
        @{Name="billing_service"; Port=8010},
        @{Name="invoice_service"; Port=8011},
        @{Name="monitoring_dashboard_service"; Port=8012}
    )
    
    $allServicesUp = $true
    
    foreach ($service in $services) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$($service.Port)/health" -TimeoutSec 5 -ErrorAction Stop
            Write-Success "$($service.Name) is responding on port $($service.Port)"
        }
        catch {
            Write-Warning "$($service.Name) is not responding on port $($service.Port)"
            $allServicesUp = $false
        }
    }
    
    if (-not $allServicesUp) {
        Write-Warning "Some services are not responding. Validation may fail for those services."
    }
    else {
        Write-Success "All services are responding"
    }
}

# Function to install dependencies
function Install-Dependencies {
    Write-Status "Installing Python dependencies..."
    
    $requirementsFile = Join-Path $ScriptDir "validation_requirements.txt"
    if (-not (Test-Path $requirementsFile)) {
        Write-Error "validation_requirements.txt not found"
        return
    }
    
    try {
        pip install -r $requirementsFile
        Write-Success "Dependencies installed"
    }
    catch {
        Write-Error "Failed to install dependencies: $_"
    }
}

# Function to run validation once
function Start-ValidationOnce {
    Write-Status "Running validation once..."
    python $ValidationScript --run-once
}

# Function to show dashboard
function Show-Dashboard {
    Write-Status "Showing current dashboard..."
    python $ValidationScript --dashboard
}

# Function to start scheduler
function Start-Scheduler {
    Write-Status "Starting continuous validation scheduler..."
    Write-Status "Press Ctrl+C to stop the scheduler"
    python $ValidationScript --scheduler
}

# Function to show recent reports
function Show-Reports {
    Write-Status "Recent validation reports:"
    
    if (-not (Test-Path $OutputDir)) {
        Write-Warning "No validation outputs directory found"
        return
    }
    
    $reports = Get-ChildItem -Path $OutputDir -Filter "validation_report_*.md" | Sort-Object LastWriteTime -Descending | Select-Object -First 5
    
    if (-not $reports) {
        Write-Warning "No validation reports found"
        return
    }
    
    foreach ($report in $reports) {
        $timestamp = $report.Name -replace "validation_report_(.*)\.md", '$1'
        Write-Host "  - $($report.Name) (generated: $timestamp)"
    }
}

# Function to show help
function Show-Help {
    Write-Host "ReqArchitect Continuous Validation Framework" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\run_validation.ps1 [OPTION]"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  run-once      Run validation once and exit"
    Write-Host "  dashboard     Show current dashboard"
    Write-Host "  scheduler     Start continuous validation scheduler"
    Write-Host "  install       Install Python dependencies"
    Write-Host "  check         Check if services are running"
    Write-Host "  reports       Show recent validation reports"
    Write-Host "  help          Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\run_validation.ps1 run-once     # Run validation once"
    Write-Host "  .\run_validation.ps1 dashboard    # Show current status"
    Write-Host "  .\run_validation.ps1 scheduler    # Start continuous monitoring"
    Write-Host ""
}

# Main script logic
switch ($Action.ToLower()) {
    "run-once" {
        if (Test-Docker) {
            Test-Services
            Start-ValidationOnce
        }
    }
    "dashboard" {
        Show-Dashboard
    }
    "scheduler" {
        if (Test-Docker) {
            Test-Services
            Start-Scheduler
        }
    }
    "install" {
        Install-Dependencies
    }
    "check" {
        Test-Docker
        Test-Services
    }
    "reports" {
        Show-Reports
    }
    "help" {
        Show-Help
    }
    default {
        Show-Help
    }
} 
# Health Check Script for Windows PowerShell
# Tests all microservices health endpoints

param(
    [switch]$Verbose,
    [int]$Timeout = 30,
    [int]$Retries = 3
)

# Colors for output
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

# Service configurations
$Services = @(
    @{
        Name = "Gateway Service"
        Url = "http://localhost:8080/health"
        Port = 8080
    },
    @{
        Name = "Auth Service"
        Url = "http://localhost:8001/health"
        Port = 8001
    },
    @{
        Name = "AI Modeling Service"
        Url = "http://localhost:8002/health"
        Port = 8002
    },
    @{
        Name = "Invoice Service"
        Url = "http://localhost:8011/health"
        Port = 8011
    },
    @{
        Name = "Billing Service"
        Url = "http://localhost:8010/health"
        Port = 8010
    }
)

# Infrastructure services
$InfraServices = @(
    @{
        Name = "PostgreSQL Database"
        Url = "http://localhost:5432"
        Port = 5432
    },
    @{
        Name = "Redis Event Bus"
        Url = "http://localhost:6379"
        Port = 6379
    }
)

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = $White
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Status {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-ColorOutput "[$timestamp] $Message" $Blue
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✅ $Message" $Green
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠️  $Message" $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "❌ $Message" $Red
}

function Test-ServiceHealth {
    param(
        [hashtable]$Service,
        [int]$Retries = 3
    )
    
    $serviceName = $Service.Name
    $serviceUrl = $Service.Url
    $servicePort = $Service.Port
    
    Write-Status "Testing $serviceName..."
    
    for ($i = 1; $i -le $Retries; $i++) {
        try {
            # First check if port is open
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $tcpClient.ConnectAsync("localhost", $servicePort).Wait(5000) | Out-Null
            
            if ($tcpClient.Connected) {
                $tcpClient.Close()
                
                # Then check HTTP health endpoint
                $response = Invoke-WebRequest -Uri $serviceUrl -Method GET -TimeoutSec 10 -UseBasicParsing
                
                if ($response.StatusCode -eq 200) {
                    $healthData = $response.Content | ConvertFrom-Json
                    Write-Success "$serviceName is healthy (Status: $($healthData.status))"
                    return $true
                } else {
                    Write-Warning "$serviceName returned status code: $($response.StatusCode)"
                }
            } else {
                Write-Warning "$serviceName port $servicePort is not accessible"
            }
        }
        catch {
            if ($i -lt $Retries) {
                Write-Warning "$serviceName attempt $i failed: $($_.Exception.Message)"
                Start-Sleep -Seconds 2
            } else {
                Write-Error "$serviceName failed after $Retries attempts: $($_.Exception.Message)"
            }
        }
        finally {
            if ($tcpClient) {
                $tcpClient.Close()
            }
        }
    }
    
    return $false
}

function Test-InfrastructureHealth {
    param(
        [hashtable]$Service,
        [int]$Retries = 3
    )
    
    $serviceName = $Service.Name
    $servicePort = $Service.Port
    
    Write-Status "Testing $serviceName..."
    
    for ($i = 1; $i -le $Retries; $i++) {
        try {
            $tcpClient = New-Object System.Net.Sockets.TcpClient
            $tcpClient.ConnectAsync("localhost", $servicePort).Wait(5000) | Out-Null
            
            if ($tcpClient.Connected) {
                Write-Success "$serviceName is accessible on port $servicePort"
                $tcpClient.Close()
                return $true
            } else {
                Write-Warning "$serviceName port $servicePort is not accessible"
            }
        }
        catch {
            if ($i -lt $Retries) {
                Write-Warning "$serviceName attempt $i failed: $($_.Exception.Message)"
                Start-Sleep -Seconds 2
            } else {
                Write-Error "$serviceName failed after $Retries attempts: $($_.Exception.Message)"
            }
        }
        finally {
            if ($tcpClient) {
                $tcpClient.Close()
            }
        }
    }
    
    return $false
}

function Test-DockerServices {
    Write-Status "Checking Docker services status..."
    
    try {
        $containers = docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Select-Object -Skip 1
        
        if ($containers) {
            Write-Success "Docker containers are running:"
            $containers | ForEach-Object {
                Write-Host "  $_" -ForegroundColor $White
            }
            return $true
        } else {
            Write-Error "No Docker containers are running"
            return $false
        }
    }
    catch {
        Write-Error "Failed to check Docker services: $($_.Exception.Message)"
        return $false
    }
}

function Test-DatabaseConnection {
    Write-Status "Testing database connectivity..."
    
    try {
        # Check if PostgreSQL is accessible
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.ConnectAsync("localhost", 5432).Wait(5000) | Out-Null
        
        if ($tcpClient.Connected) {
            Write-Success "PostgreSQL database is accessible"
            $tcpClient.Close()
            return $true
        } else {
            Write-Error "PostgreSQL database is not accessible"
            return $false
        }
    }
    catch {
        Write-Error "Database connection failed: $($_.Exception.Message)"
        return $false
    }
    finally {
        if ($tcpClient) {
            $tcpClient.Close()
        }
    }
}

function Test-RedisConnection {
    Write-Status "Testing Redis connectivity..."
    
    try {
        # Check if Redis is accessible
        $tcpClient = New-Object System.Net.Sockets.TcpClient
        $tcpClient.ConnectAsync("localhost", 6379).Wait(5000) | Out-Null
        
        if ($tcpClient.Connected) {
            Write-Success "Redis event bus is accessible"
            $tcpClient.Close()
            return $true
        } else {
            Write-Error "Redis event bus is not accessible"
            return $false
        }
    }
    catch {
        Write-Error "Redis connection failed: $($_.Exception.Message)"
        return $false
    }
    finally {
        if ($tcpClient) {
            $tcpClient.Close()
        }
    }
}

# Main execution
function Main {
    Write-ColorOutput "🚀 FastAPI Microservices Health Check" $Blue
    Write-ColorOutput "=====================================" $Blue
    Write-Host ""
    
    $overallSuccess = $true
    $passedTests = 0
    $totalTests = 0
    
    # Test Docker services
    $totalTests++
    if (Test-DockerServices) {
        $passedTests++
    } else {
        $overallSuccess = $false
    }
    Write-Host ""
    
    # Test infrastructure services
    Write-ColorOutput "🔧 Infrastructure Services" $Blue
    Write-ColorOutput "=========================" $Blue
    
    foreach ($service in $InfraServices) {
        $totalTests++
        if (Test-InfrastructureHealth -Service $service -Retries $Retries) {
            $passedTests++
        } else {
            $overallSuccess = $false
        }
    }
    Write-Host ""
    
    # Test application services
    Write-ColorOutput "📱 Application Services" $Blue
    Write-ColorOutput "======================" $Blue
    
    foreach ($service in $Services) {
        $totalTests++
        if (Test-ServiceHealth -Service $service -Retries $Retries) {
            $passedTests++
        } else {
            $overallSuccess = $false
        }
    }
    Write-Host ""
    
    # Test database connectivity
    $totalTests++
    if (Test-DatabaseConnection) {
        $passedTests++
    } else {
        $overallSuccess = $false
    }
    
    # Test Redis connectivity
    $totalTests++
    if (Test-RedisConnection) {
        $passedTests++
    } else {
        $overallSuccess = $false
    }
    Write-Host ""
    
    # Summary
    Write-ColorOutput "📊 Health Check Summary" $Blue
    Write-ColorOutput "=======================" $Blue
    Write-ColorOutput "✅ Passed: $passedTests/$totalTests tests" $Green
    Write-ColorOutput "❌ Failed: $($totalTests - $passedTests)/$totalTests tests" $Red
    $successRate = [math]::Round(($passedTests / $totalTests) * 100, 1)
    Write-ColorOutput "📈 Success Rate: $successRate%" $Blue
    
    if ($overallSuccess) {
        Write-ColorOutput "🎉 ALL HEALTH CHECKS PASSED!" $Green
        exit 0
    } else {
        Write-ColorOutput "⚠️  Some health checks failed. Check the output above for details." $Yellow
        exit 1
    }
}

# Run main function
Main 
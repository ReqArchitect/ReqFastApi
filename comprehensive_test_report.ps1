# Comprehensive ReqArchitect Test Report
# Tests both running services and documents ArchiMate service status

Write-Host "🎯 ReqArchitect Comprehensive Test Report" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Testing all services and documenting ArchiMate compliance" -ForegroundColor Yellow
Write-Host ""

# Test running services
$RunningServices = @{
    "auth_service" = "http://localhost:8001/health"
    "gateway_service" = "http://localhost:8080/health"
    "ai_modeling_service" = "http://localhost:8002/health"
    "usage_service" = "http://localhost:8005/health"
    "notification_service" = "http://localhost:8006/health"
    "audit_log_service" = "http://localhost:8007/health"
    "billing_service" = "http://localhost:8010/health"
    "invoice_service" = "http://localhost:8011/health"
    "monitoring_dashboard_service" = "http://localhost:8012/health"
    "api_debug_service" = "http://localhost:8090/health"
}

$Headers = @{
    "Authorization" = "Bearer test-jwt-token"
    "Content-Type" = "application/json"
}

Write-Host "🔧 Testing Running Services" -ForegroundColor Magenta
Write-Host "============================" -ForegroundColor Magenta

$RunningResults = @()
$RunningTotal = 0
$RunningPassed = 0
$RunningFailed = 0

foreach ($Service in $RunningServices.GetEnumerator()) {
    $RunningTotal++
    $ServiceName = $Service.Key
    $Url = $Service.Value
    
    Write-Host "Testing $ServiceName..." -ForegroundColor White
    
    try {
        $Response = Invoke-WebRequest -Uri $Url -Headers $Headers -Method GET -TimeoutSec 10 -ErrorAction Stop
        
        if ($Response.StatusCode -eq 200) {
            try {
                $JsonResponse = $Response.Content | ConvertFrom-Json
                $RunningPassed++
                Write-Host "  ✅ PASS: HTTP 200, Healthy" -ForegroundColor Green
                
                if ($JsonResponse.status) {
                    Write-Host "  Status: $($JsonResponse.status)" -ForegroundColor Gray
                }
                if ($JsonResponse.service) {
                    Write-Host "  Service: $($JsonResponse.service)" -ForegroundColor Gray
                }
                if ($JsonResponse.uptime) {
                    Write-Host "  Uptime: $([math]::Round($JsonResponse.uptime, 1))s" -ForegroundColor Gray
                }
                
                $RunningResults += [PSCustomObject]@{
                    Service = $ServiceName
                    Status = "PASS"
                    Error = $null
                    HealthStatus = $JsonResponse.status
                    Uptime = $JsonResponse.uptime
                }
            } catch {
                $RunningFailed++
                Write-Host "  ❌ FAIL: Invalid JSON" -ForegroundColor Red
                $RunningResults += [PSCustomObject]@{
                    Service = $ServiceName
                    Status = "FAIL"
                    Error = "Invalid JSON"
                    HealthStatus = $null
                    Uptime = $null
                }
            }
        } else {
            $RunningFailed++
            Write-Host "  ❌ FAIL: HTTP $($Response.StatusCode)" -ForegroundColor Red
            $RunningResults += [PSCustomObject]@{
                Service = $ServiceName
                Status = "FAIL"
                Error = "HTTP $($Response.StatusCode)"
                HealthStatus = $null
                Uptime = $null
            }
        }
    } catch {
        $RunningFailed++
        Write-Host "  ❌ FAIL: Connection Error" -ForegroundColor Red
        $RunningResults += [PSCustomObject]@{
            Service = $ServiceName
            Status = "FAIL"
            Error = $_.Exception.Message
            HealthStatus = $null
            Uptime = $null
        }
    }
    
    Write-Host ""
}

# Test API Debug Service Discovery
Write-Host "🔍 Testing API Debug Service Discovery" -ForegroundColor Magenta
Write-Host "=======================================" -ForegroundColor Magenta

try {
    $DebugResponse = Invoke-WebRequest -Uri "http://localhost:8090/api-debug" -Headers $Headers -Method GET -TimeoutSec 10
    if ($DebugResponse.StatusCode -eq 200) {
        $DebugData = $DebugResponse.Content | ConvertFrom-Json
        $DiscoveredServices = $DebugData.value.Count
        Write-Host "✅ API Debug Service: PASS" -ForegroundColor Green
        Write-Host "  Discovered Services: $DiscoveredServices" -ForegroundColor Gray
        Write-Host "  Discovery Method: $($DebugData.value[0].discovery_method)" -ForegroundColor Gray
    } else {
        Write-Host "❌ API Debug Service: FAIL" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ API Debug Service: Connection Error" -ForegroundColor Red
}

Write-Host ""

# ArchiMate Service Status Report
Write-Host "🏗️  ArchiMate Service Status Report" -ForegroundColor Magenta
Write-Host "====================================" -ForegroundColor Magenta

$ArchiMateServices = @{
    "Motivation Layer" = @("goal_service", "driver_service", "requirement_service", "constraint_service")
    "Business Layer" = @("businessfunction_service", "businessrole_service", "businessprocess_service")
    "Application Layer" = @("applicationfunction_service", "applicationcomponent_service", "resource_service")
    "Technology Layer" = @("node_service", "artifact_service", "communicationpath_service", "device_service")
}

$ArchiMateStatus = @()

foreach ($Layer in $ArchiMateServices.GetEnumerator()) {
    $LayerName = $Layer.Key
    $Services = $Layer.Value
    
    Write-Host "$LayerName:" -ForegroundColor White
    
    foreach ($Service in $Services) {
        $Status = "NOT_RUNNING"
        $Error = "Service not deployed or not running"
        
        # Check if service is in running services
        if ($RunningServices.ContainsKey($Service)) {
            $Status = "RUNNING"
            $Error = $null
        }
        
        $ArchiMateStatus += [PSCustomObject]@{
            Layer = $LayerName
            Service = $Service
            Status = $Status
            Error = $Error
        }
        
        $StatusColor = if ($Status -eq "RUNNING") { "Green" } else { "Red" }
        Write-Host "  • $Service: $Status" -ForegroundColor $StatusColor
    }
    
    Write-Host ""
}

# Generate comprehensive summary
Write-Host "📊 Comprehensive Test Summary" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host "Running Services: $RunningTotal" -ForegroundColor White
Write-Host "  Healthy: $RunningPassed" -ForegroundColor Green
Write-Host "  Unhealthy: $RunningFailed" -ForegroundColor Red
Write-Host "  Success Rate: $([math]::Round(($RunningPassed / $RunningTotal) * 100, 1))%" -ForegroundColor Yellow

$ArchiMateTotal = $ArchiMateStatus.Count
$ArchiMateRunning = ($ArchiMateStatus | Where-Object { $_.Status -eq "RUNNING" }).Count
Write-Host ""
Write-Host "ArchiMate Services: $ArchiMateTotal" -ForegroundColor White
Write-Host "  Running: $ArchiMateRunning" -ForegroundColor Green
Write-Host "  Not Running: $($ArchiMateTotal - $ArchiMateRunning)" -ForegroundColor Red
Write-Host "  Coverage: $([math]::Round(($ArchiMateRunning / $ArchiMateTotal) * 100, 1))%" -ForegroundColor Yellow

# Layer coverage
Write-Host ""
Write-Host "🔍 ArchiMate Layer Coverage:" -ForegroundColor Cyan
foreach ($Layer in $ArchiMateServices.GetEnumerator()) {
    $LayerName = $Layer.Key
    $LayerServices = $ArchiMateStatus | Where-Object { $_.Layer -eq $LayerName }
    $LayerRunning = ($LayerServices | Where-Object { $_.Status -eq "RUNNING" }).Count
    $LayerTotal = $LayerServices.Count
    $LayerCoverage = [math]::Round(($LayerRunning / $LayerTotal) * 100, 1)
    
    Write-Host "  $LayerName`: $LayerRunning/$LayerTotal ($LayerCoverage%)" -ForegroundColor $(if ($LayerCoverage -gt 0) { "Green" } else { "Red" })
}

# Export comprehensive results
$ComprehensiveResults = @{
    TestSummary = @{
        RunningServices = @{
            Total = $RunningTotal
            Healthy = $RunningPassed
            Unhealthy = $RunningFailed
            SuccessRate = [math]::Round(($RunningPassed / $RunningTotal) * 100, 1)
        }
        ArchiMateServices = @{
            Total = $ArchiMateTotal
            Running = $ArchiMateRunning
            NotRunning = ($ArchiMateTotal - $ArchiMateRunning)
            Coverage = [math]::Round(($ArchiMateRunning / $ArchiMateTotal) * 100, 1)
        }
    }
    RunningServices = $RunningResults
    ArchiMateStatus = $ArchiMateStatus
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

$ComprehensiveResults | ConvertTo-Json -Depth 3 | Out-File -FilePath "comprehensive_test_report.json" -Encoding UTF8
$RunningResults | Export-Csv -Path "running_services_results.csv" -NoTypeInformation
$ArchiMateStatus | Export-Csv -Path "archimate_status.csv" -NoTypeInformation

Write-Host ""
Write-Host "📄 Reports exported:" -ForegroundColor Green
Write-Host "  • comprehensive_test_report.json" -ForegroundColor Gray
Write-Host "  • running_services_results.csv" -ForegroundColor Gray
Write-Host "  • archimate_status.csv" -ForegroundColor Gray 
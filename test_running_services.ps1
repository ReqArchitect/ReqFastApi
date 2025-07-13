# ReqArchitect Running Services Test Suite
# Tests all currently running services for health and JSON responses

param(
    [string]$BaseUrl = "http://localhost",
    [string]$JwtToken = "test-jwt-token"
)

# Test configuration for running services
$RunningServices = @{
    # Core Services
    "auth_service" = @{ Port = 8001; Endpoint = "health"; Layer = "Core"; Description = "Authentication Service" }
    "gateway_service" = @{ Port = 8080; Endpoint = "health"; Layer = "Core"; Description = "API Gateway" }
    "ai_modeling_service" = @{ Port = 8002; Endpoint = "health"; Layer = "AI"; Description = "AI Modeling Service" }
    
    # Business Services
    "usage_service" = @{ Port = 8005; Endpoint = "health"; Layer = "Business"; Description = "Usage Tracking" }
    "notification_service" = @{ Port = 8006; Endpoint = "health"; Layer = "Business"; Description = "Notifications" }
    "audit_log_service" = @{ Port = 8007; Endpoint = "health"; Layer = "Business"; Description = "Audit Logging" }
    "billing_service" = @{ Port = 8010; Endpoint = "health"; Layer = "Business"; Description = "Billing" }
    "invoice_service" = @{ Port = 8011; Endpoint = "health"; Layer = "Business"; Description = "Invoicing" }
    
    # Infrastructure
    "monitoring_dashboard_service" = @{ Port = 8012; Endpoint = "health"; Layer = "Infrastructure"; Description = "Monitoring Dashboard" }
}

# Headers for requests
$Headers = @{
    "Authorization" = "Bearer $JwtToken"
    "Content-Type" = "application/json"
}

# Test results tracking
$TestResults = @()
$TotalTests = 0
$PassedTests = 0
$FailedTests = 0

Write-Host "🎯 ReqArchitect Running Services Test Suite" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Testing all currently running services for health and JSON responses" -ForegroundColor Yellow
Write-Host ""

function Test-Service {
    param(
        [string]$ServiceName,
        [hashtable]$ServiceConfig
    )
    
    $TotalTests++
    $Url = "$BaseUrl`:$($ServiceConfig.Port)/$($ServiceConfig.Endpoint)"
    $Layer = $ServiceConfig.Layer
    $Description = $ServiceConfig.Description
    
    Write-Host "🔍 Testing $ServiceName ($Layer Layer)..." -ForegroundColor White
    Write-Host "   Description: $Description" -ForegroundColor Gray
    Write-Host "   URL: $Url" -ForegroundColor Gray
    
    try {
        $Response = Invoke-WebRequest -Uri $Url -Headers $Headers -Method GET -TimeoutSec 10 -ErrorAction Stop
        
        # Validate response
        $IsValid = $false
        $ErrorMessage = ""
        $ResponseData = $null
        
        if ($Response.StatusCode -eq 200) {
            try {
                $JsonResponse = $Response.Content | ConvertFrom-Json
                $ResponseData = $JsonResponse
                
                # Check for required health fields
                $HasHealthFields = $JsonResponse -and 
                                 ($JsonResponse.status -or $JsonResponse.service -or $JsonResponse.timestamp)
                
                if ($HasHealthFields) {
                    $IsValid = $true
                    $PassedTests++
                    Write-Host "   ✅ PASS: HTTP 200, Valid health response" -ForegroundColor Green
                    
                    # Show health details
                    if ($JsonResponse.status) {
                        Write-Host "   🟢 Status: $($JsonResponse.status)" -ForegroundColor Green
                    }
                    if ($JsonResponse.service) {
                        Write-Host "   🏷️  Service: $($JsonResponse.service)" -ForegroundColor Gray
                    }
                    if ($JsonResponse.uptime) {
                        Write-Host "   ⏱️  Uptime: $([math]::Round($JsonResponse.uptime, 1))s" -ForegroundColor Gray
                    }
                } else {
                    $ErrorMessage = "Invalid health response structure"
                    Write-Host "   ❌ FAIL: $ErrorMessage" -ForegroundColor Red
                }
            } catch {
                $ErrorMessage = "Invalid JSON response: $($_.Exception.Message)"
                Write-Host "   ❌ FAIL: $ErrorMessage" -ForegroundColor Red
            }
        } else {
            $ErrorMessage = "HTTP $($Response.StatusCode) - Expected 200"
            Write-Host "   ❌ FAIL: $ErrorMessage" -ForegroundColor Red
        }
        
    } catch {
        $ErrorMessage = "Connection failed: $($_.Exception.Message)"
        Write-Host "   ❌ FAIL: $ErrorMessage" -ForegroundColor Red
    }
    
    if (-not $IsValid) {
        $FailedTests++
    }
    
    # Store test result
    $TestResults += [PSCustomObject]@{
        ServiceName = $ServiceName
        Layer = $Layer
        Description = $Description
        Url = $Url
        Status = if ($IsValid) { "PASS" } else { "FAIL" }
        ErrorMessage = $ErrorMessage
        ResponseData = $ResponseData
        Timestamp = Get-Date
    }
    
    Write-Host ""
}

# Test all running services by layer
$Layers = @("Core", "AI", "Business", "Infrastructure")

foreach ($Layer in $Layers) {
    Write-Host "🏗️  Testing $Layer Layer Services" -ForegroundColor Magenta
    Write-Host "--------------------------------" -ForegroundColor Magenta
    
    $LayerServices = $RunningServices.GetEnumerator() | Where-Object { $_.Value.Layer -eq $Layer }
    
    if ($LayerServices.Count -eq 0) {
        Write-Host "   ⚠️  No services found for $Layer layer" -ForegroundColor Yellow
    } else {
        foreach ($Service in $LayerServices) {
            Test-Service -ServiceName $Service.Key -ServiceConfig $Service.Value
        }
    }
    
    Write-Host ""
}

# Test API Debug Service
Write-Host "🔍 Testing API Debug Service" -ForegroundColor Magenta
Write-Host "----------------------------" -ForegroundColor Magenta
Test-Service -ServiceName "api_debug_service" -ServiceConfig @{ Port = 8090; Endpoint = "health"; Layer = "Debug"; Description = "API Debug Service" }

# Generate test summary
Write-Host "📊 Test Summary" -ForegroundColor Cyan
Write-Host "===============" -ForegroundColor Cyan
Write-Host "Total Tests: $TotalTests" -ForegroundColor White
Write-Host "Passed: $PassedTests" -ForegroundColor Green
Write-Host "Failed: $FailedTests" -ForegroundColor Red
Write-Host "Success Rate: $([math]::Round(($PassedTests / $TotalTests) * 100, 1))%" -ForegroundColor Yellow

# Show failed tests
if ($FailedTests -gt 0) {
    Write-Host ""
    Write-Host "❌ Failed Tests:" -ForegroundColor Red
    $FailedResults = $TestResults | Where-Object { $_.Status -eq "FAIL" }
    foreach ($Result in $FailedResults) {
        Write-Host "   • $($Result.ServiceName) ($($Result.Layer)): $($Result.ErrorMessage)" -ForegroundColor Red
    }
}

# Generate layer coverage report
Write-Host ""
Write-Host "🔍 Service Layer Coverage Report" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

$LayerCoverage = $TestResults | Group-Object Layer | ForEach-Object {
    $LayerName = $_.Name
    $LayerTests = $_.Group
    $PassedInLayer = ($LayerTests | Where-Object { $_.Status -eq "PASS" }).Count
    $TotalInLayer = $LayerTests.Count
    $Coverage = if ($TotalInLayer -gt 0) { [math]::Round(($PassedInLayer / $TotalInLayer) * 100, 1) } else { 0 }
    
    [PSCustomObject]@{
        Layer = $LayerName
        TotalServices = $TotalInLayer
        HealthyServices = $PassedInLayer
        Coverage = "$Coverage%"
    }
}

$LayerCoverage | Format-Table -AutoSize

# Show healthy services summary
Write-Host ""
Write-Host "✅ Healthy Services Summary" -ForegroundColor Green
Write-Host "============================" -ForegroundColor Green
$HealthyServices = $TestResults | Where-Object { $_.Status -eq "PASS" }
foreach ($Service in $HealthyServices) {
    Write-Host "   • $($Service.ServiceName) - $($Service.Description)" -ForegroundColor Green
}

# Export results to JSON
$ResultsExport = @{
    TestSummary = @{
        TotalTests = $TotalTests
        PassedTests = $PassedTests
        FailedTests = $FailedTests
        SuccessRate = [math]::Round(($PassedTests / $TotalTests) * 100, 1)
    }
    LayerCoverage = $LayerCoverage
    HealthyServices = $HealthyServices | Select-Object ServiceName, Layer, Description, Url
    DetailedResults = $TestResults | Select-Object ServiceName, Layer, Description, Status, ErrorMessage, Timestamp
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

$ResultsExport | ConvertTo-Json -Depth 3 | Out-File -FilePath "running_services_test_results.json" -Encoding UTF8
Write-Host ""
Write-Host "📄 Detailed results exported to: running_services_test_results.json" -ForegroundColor Green

# Return exit code
if ($FailedTests -gt 0) {
    exit 1
} else {
    exit 0
} 
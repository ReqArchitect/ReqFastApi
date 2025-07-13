# ArchiMate Services Test Suite
# Tests ArchiMate-compliant microservices for health and JSON responses

param(
    [string]$BaseUrl = "http://localhost",
    [string]$JwtToken = "test-jwt-token"
)

# Test configuration for ArchiMate services
$ArchiMateServices = @{
    # Motivation Layer
    "goal_service" = @{ Port = 8013; Endpoint = "goals"; Layer = "Motivation"; Method = "GET" }
    "driver_service" = @{ Port = 8014; Endpoint = "drivers"; Layer = "Motivation"; Method = "GET" }
    "requirement_service" = @{ Port = 8015; Endpoint = "requirements"; Layer = "Motivation"; Method = "GET" }
    "constraint_service" = @{ Port = 8016; Endpoint = "constraints"; Layer = "Motivation"; Method = "GET" }
    
    # Business Layer
    "businessfunction_service" = @{ Port = 8017; Endpoint = "business-functions"; Layer = "Business"; Method = "GET" }
    "businessrole_service" = @{ Port = 8018; Endpoint = "business-roles"; Layer = "Business"; Method = "GET" }
    "businessprocess_service" = @{ Port = 8019; Endpoint = "business-processes"; Layer = "Business"; Method = "GET" }
    
    # Application Layer
    "applicationfunction_service" = @{ Port = 8080; Endpoint = "application-functions"; Layer = "Application"; Method = "GET" }
    "applicationcomponent_service" = @{ Port = 8020; Endpoint = "application-components"; Layer = "Application"; Method = "GET" }
    "resource_service" = @{ Port = 8021; Endpoint = "resources"; Layer = "Application"; Method = "GET" }
    
    # Technology Layer
    "node_service" = @{ Port = 8022; Endpoint = "nodes"; Layer = "Technology"; Method = "GET" }
    "artifact_service" = @{ Port = 8023; Endpoint = "artifacts"; Layer = "Technology"; Method = "GET" }
    "communicationpath_service" = @{ Port = 8024; Endpoint = "communication-paths"; Layer = "Technology"; Method = "GET" }
    "device_service" = @{ Port = 8025; Endpoint = "devices"; Layer = "Technology"; Method = "GET" }
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

Write-Host "🎯 ArchiMate Services Test Suite" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Testing ArchiMate 3.2 layer services for health and JSON responses" -ForegroundColor Yellow
Write-Host ""

function Test-ArchiMateService {
    param(
        [string]$ServiceName,
        [hashtable]$ServiceConfig
    )
    
    $TotalTests++
    $Url = "$BaseUrl`:$($ServiceConfig.Port)/$($ServiceConfig.Endpoint)"
    $Layer = $ServiceConfig.Layer
    $Method = $ServiceConfig.Method
    
    Write-Host "🔍 Testing $ServiceName ($Layer Layer)..." -ForegroundColor White
    Write-Host "   URL: $Url" -ForegroundColor Gray
    Write-Host "   Method: $Method" -ForegroundColor Gray
    
    try {
        $Response = Invoke-WebRequest -Uri $Url -Headers $Headers -Method $Method -TimeoutSec 10 -ErrorAction Stop
        
        # Validate response
        $IsValid = $false
        $ErrorMessage = ""
        $ResponseData = $null
        
        if ($Response.StatusCode -eq 200) {
            try {
                $JsonResponse = $Response.Content | ConvertFrom-Json
                $ResponseData = $JsonResponse
                
                # Check for required fields (id, name, tenant_id, etc.)
                $HasRequiredFields = $JsonResponse -and 
                                   ($JsonResponse.id -or $JsonResponse.Count -or $JsonResponse.value -or $JsonResponse.items)
                
                if ($HasRequiredFields) {
                    $IsValid = $true
                    $PassedTests++
                    Write-Host "   ✅ PASS: HTTP 200, Valid JSON with required fields" -ForegroundColor Green
                    
                    # Show response details
                    if ($JsonResponse.Count) {
                        Write-Host "   📊 Records: $($JsonResponse.Count)" -ForegroundColor Gray
                    } elseif ($JsonResponse.value -and $JsonResponse.value.Count) {
                        Write-Host "   📊 Records: $($JsonResponse.value.Count)" -ForegroundColor Gray
                    } elseif ($JsonResponse.items -and $JsonResponse.items.Count) {
                        Write-Host "   📊 Records: $($JsonResponse.items.Count)" -ForegroundColor Gray
                    }
                    
                    # Check for ArchiMate-specific fields
                    if ($JsonResponse.tenant_id -or ($JsonResponse.value -and $JsonResponse.value[0].tenant_id)) {
                        Write-Host "   🏢 Multi-tenant: Yes" -ForegroundColor Gray
                    }
                    if ($JsonResponse.created_at -or ($JsonResponse.value -and $JsonResponse.value[0].created_at)) {
                        Write-Host "   📅 Traceability: Yes" -ForegroundColor Gray
                    }
                } else {
                    $ErrorMessage = "Invalid JSON structure - missing required fields"
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
        Url = $Url
        Method = $Method
        Status = if ($IsValid) { "PASS" } else { "FAIL" }
        ErrorMessage = $ErrorMessage
        ResponseData = $ResponseData
        Timestamp = Get-Date
    }
    
    Write-Host ""
}

# Test all ArchiMate services by layer
$Layers = @("Motivation", "Business", "Application", "Technology")

foreach ($Layer in $Layers) {
    Write-Host "🏗️  Testing $Layer Layer Services" -ForegroundColor Magenta
    Write-Host "--------------------------------" -ForegroundColor Magenta
    
    $LayerServices = $ArchiMateServices.GetEnumerator() | Where-Object { $_.Value.Layer -eq $Layer }
    
    if ($LayerServices.Count -eq 0) {
        Write-Host "   ⚠️  No services found for $Layer layer" -ForegroundColor Yellow
    } else {
        foreach ($Service in $LayerServices) {
            Test-ArchiMateService -ServiceName $Service.Key -ServiceConfig $Service.Value
        }
    }
    
    Write-Host ""
}

# Test core services that are actually running
Write-Host "🔧 Testing Core Running Services" -ForegroundColor Magenta
Write-Host "=================================" -ForegroundColor Magenta

$CoreServices = @{
    "auth_service" = @{ Port = 8001; Endpoint = "health"; Layer = "Core"; Method = "GET" }
    "gateway_service" = @{ Port = 8080; Endpoint = "health"; Layer = "Core"; Method = "GET" }
    "ai_modeling_service" = @{ Port = 8002; Endpoint = "health"; Layer = "AI"; Method = "GET" }
    "usage_service" = @{ Port = 8005; Endpoint = "health"; Layer = "Business"; Method = "GET" }
    "notification_service" = @{ Port = 8006; Endpoint = "health"; Layer = "Business"; Method = "GET" }
    "audit_log_service" = @{ Port = 8007; Endpoint = "health"; Layer = "Business"; Method = "GET" }
    "billing_service" = @{ Port = 8010; Endpoint = "health"; Layer = "Business"; Method = "GET" }
    "invoice_service" = @{ Port = 8011; Endpoint = "health"; Layer = "Business"; Method = "GET" }
    "monitoring_dashboard_service" = @{ Port = 8012; Endpoint = "health"; Layer = "Infrastructure"; Method = "GET" }
    "api_debug_service" = @{ Port = 8090; Endpoint = "health"; Layer = "Debug"; Method = "GET" }
}

foreach ($Service in $CoreServices.GetEnumerator()) {
    Test-ArchiMateService -ServiceName $Service.Key -ServiceConfig $Service.Value
}

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
Write-Host "🔍 ArchiMate Layer Coverage Report" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

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
    Write-Host "   • $($Service.ServiceName) ($($Service.Layer))" -ForegroundColor Green
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
    HealthyServices = $HealthyServices | Select-Object ServiceName, Layer, Url, Method
    DetailedResults = $TestResults | Select-Object ServiceName, Layer, Status, ErrorMessage, Timestamp
    Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
}

$ResultsExport | ConvertTo-Json -Depth 3 | Out-File -FilePath "archimate_test_results.json" -Encoding UTF8
Write-Host ""
Write-Host "📄 Detailed results exported to: archimate_test_results.json" -ForegroundColor Green

# Return exit code
if ($FailedTests -gt 0) {
    exit 1
} else {
    exit 0
} 
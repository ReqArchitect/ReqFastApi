# ArchiMate Services Test Suite
# Tests all ArchiMate 3.2 layer services for health and JSON responses

param(
    [string]$BaseUrl = "http://localhost",
    [string]$JwtToken = "test-jwt-token"
)

# Test configuration
$Services = @{
    # Motivation Layer
    "goal_service" = @{ Port = 8013; Endpoint = "goals"; Layer = "Motivation" }
    "driver_service" = @{ Port = 8014; Endpoint = "drivers"; Layer = "Motivation" }
    "requirement_service" = @{ Port = 8015; Endpoint = "requirements"; Layer = "Motivation" }
    "constraint_service" = @{ Port = 8016; Endpoint = "constraints"; Layer = "Motivation" }
    
    # Business Layer
    "businessfunction_service" = @{ Port = 8017; Endpoint = "business-functions"; Layer = "Business" }
    "businessrole_service" = @{ Port = 8018; Endpoint = "business-roles"; Layer = "Business" }
    "businessprocess_service" = @{ Port = 8019; Endpoint = "business-processes"; Layer = "Business" }
    
    # Application Layer
    "applicationfunction_service" = @{ Port = 8080; Endpoint = "application-functions"; Layer = "Application" }
    "applicationcomponent_service" = @{ Port = 8020; Endpoint = "application-components"; Layer = "Application" }
    "resource_service" = @{ Port = 8021; Endpoint = "resources"; Layer = "Application" }
    
    # Technology Layer
    "node_service" = @{ Port = 8022; Endpoint = "nodes"; Layer = "Technology" }
    "artifact_service" = @{ Port = 8023; Endpoint = "artifacts"; Layer = "Technology" }
    "communicationpath_service" = @{ Port = 8024; Endpoint = "communication-paths"; Layer = "Technology" }
    "device_service" = @{ Port = 8025; Endpoint = "devices"; Layer = "Technology" }
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
Write-Host "Testing all ArchiMate 3.2 layer services for health and JSON responses" -ForegroundColor Yellow
Write-Host ""

function Test-Service {
    param(
        [string]$ServiceName,
        [hashtable]$ServiceConfig
    )
    
    $TotalTests++
    $Url = "$BaseUrl`:$($ServiceConfig.Port)/$($ServiceConfig.Endpoint)"
    $Layer = $ServiceConfig.Layer
    
    Write-Host "🔍 Testing $ServiceName ($Layer Layer)..." -ForegroundColor White
    Write-Host "   URL: $Url" -ForegroundColor Gray
    
    try {
        $Response = Invoke-WebRequest -Uri $Url -Headers $Headers -Method GET -TimeoutSec 10 -ErrorAction Stop
        
        # Validate response
        $IsValid = $false
        $ErrorMessage = ""
        
        if ($Response.StatusCode -eq 200) {
            try {
                $JsonResponse = $Response.Content | ConvertFrom-Json
                
                # Check for required fields
                $HasRequiredFields = $JsonResponse -and 
                                   ($JsonResponse.id -or $JsonResponse.Count -or $JsonResponse.value)
                
                if ($HasRequiredFields) {
                    $IsValid = $true
                    $PassedTests++
                    Write-Host "   ✅ PASS: HTTP 200, Valid JSON with required fields" -ForegroundColor Green
                    
                    # Show sample data structure
                    if ($JsonResponse.Count) {
                        Write-Host "   📊 Records: $($JsonResponse.Count)" -ForegroundColor Gray
                    } elseif ($JsonResponse.value -and $JsonResponse.value.Count) {
                        Write-Host "   📊 Records: $($JsonResponse.value.Count)" -ForegroundColor Gray
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
        Status = if ($IsValid) { "PASS" } else { "FAIL" }
        ErrorMessage = $ErrorMessage
        Timestamp = Get-Date
    }
    
    Write-Host ""
}

# Test all services by layer
$Layers = @("Motivation", "Business", "Application", "Technology")

foreach ($Layer in $Layers) {
    Write-Host "🏗️  Testing $Layer Layer Services" -ForegroundColor Magenta
    Write-Host "--------------------------------" -ForegroundColor Magenta
    
    $LayerServices = $Services.GetEnumerator() | Where-Object { $_.Value.Layer -eq $Layer }
    
    foreach ($Service in $LayerServices) {
        Test-Service -ServiceName $Service.Key -ServiceConfig $Service.Value
    }
    
    Write-Host ""
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

# Generate trace coverage report
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

# Export results to JSON
$ResultsExport = @{
    TestSummary = @{
        TotalTests = $TotalTests
        PassedTests = $PassedTests
        FailedTests = $FailedTests
        SuccessRate = [math]::Round(($PassedTests / $TotalTests) * 100, 1)
    }
    LayerCoverage = $LayerCoverage
    DetailedResults = $TestResults
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
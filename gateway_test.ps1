# Gateway Service Test
# Tests gateway service functionality and identifies issues

Write-Host "🔍 Gateway Service Test" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan

$BaseUrl = "http://localhost:8080"
$Headers = @{
    "Authorization" = "Bearer test-jwt-token"
    "Content-Type" = "application/json"
}

# Test basic health endpoint (should work)
Write-Host "Testing /health endpoint..." -ForegroundColor White
try {
    $Response = Invoke-WebRequest -Uri "$BaseUrl/health" -Method GET -TimeoutSec 5
    if ($Response.StatusCode -eq 200) {
        $HealthData = $Response.Content | ConvertFrom-Json
        Write-Host "  ✅ PASS: HTTP 200" -ForegroundColor Green
        Write-Host "  Status: $($HealthData.status)" -ForegroundColor Gray
        Write-Host "  Service: $($HealthData.service)" -ForegroundColor Gray
        Write-Host "  Version: $($HealthData.version)" -ForegroundColor Gray
        Write-Host "  Uptime: $([math]::Round($HealthData.uptime, 1))s" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test metrics endpoint (should work without auth)
Write-Host "Testing /metrics endpoint..." -ForegroundColor White
try {
    $Response = Invoke-WebRequest -Uri "$BaseUrl/metrics" -Method GET -TimeoutSec 5
    if ($Response.StatusCode -eq 200) {
        $MetricsData = $Response.Content | ConvertFrom-Json
        Write-Host "  ✅ PASS: HTTP 200" -ForegroundColor Green
        Write-Host "  Gateway Uptime: $($MetricsData.gateway_uptime_seconds)s" -ForegroundColor Gray
        Write-Host "  Total Requests: $($MetricsData.gateway_requests_total)" -ForegroundColor Gray
        Write-Host "  Total Errors: $($MetricsData.gateway_errors_total)" -ForegroundColor Gray
    }
} catch {
    Write-Host "  ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test gateway-health endpoint (should work without auth)
Write-Host "Testing /gateway-health endpoint..." -ForegroundColor White
try {
    $Response = Invoke-WebRequest -Uri "$BaseUrl/gateway-health" -Method GET -TimeoutSec 5
    if ($Response.StatusCode -eq 200) {
        $GatewayHealthData = $Response.Content | ConvertFrom-Json
        Write-Host "  ✅ PASS: HTTP 200" -ForegroundColor Green
        Write-Host "  Status: $($GatewayHealthData.status)" -ForegroundColor Gray
        if ($GatewayHealthData.service_health) {
            Write-Host "  Healthy Services: $($GatewayHealthData.service_health.healthy_count)" -ForegroundColor Gray
            Write-Host "  Unhealthy Services: $($GatewayHealthData.service_health.unhealthy_count)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "  ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test services endpoint (requires auth)
Write-Host "Testing /services endpoint (with auth)..." -ForegroundColor White
try {
    $Response = Invoke-WebRequest -Uri "$BaseUrl/services" -Headers $Headers -Method GET -TimeoutSec 5
    if ($Response.StatusCode -eq 200) {
        $ServicesData = $Response.Content | ConvertFrom-Json
        Write-Host "  ✅ PASS: HTTP 200" -ForegroundColor Green
        if ($ServicesData.Count) {
            Write-Host "  Services Found: $($ServicesData.Count)" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "  ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test services endpoint (without auth - should fail)
Write-Host "Testing /services endpoint (without auth)..." -ForegroundColor White
try {
    $Response = Invoke-WebRequest -Uri "$BaseUrl/services" -Method GET -TimeoutSec 5
    Write-Host "  ❌ UNEXPECTED: Got HTTP $($Response.StatusCode) instead of 401" -ForegroundColor Red
} catch {
    if ($_.Exception.Message -like "*401*") {
        Write-Host "  ✅ EXPECTED: Authentication required (401)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# Test dynamic routing to a non-existent service
Write-Host "Testing dynamic routing to non-existent service..." -ForegroundColor White
try {
    $Response = Invoke-WebRequest -Uri "$BaseUrl/non-existent-service/test" -Headers $Headers -Method GET -TimeoutSec 5
    Write-Host "  ❌ UNEXPECTED: Got HTTP $($Response.StatusCode) instead of 404" -ForegroundColor Red
} catch {
    if ($_.Exception.Message -like "*404*") {
        Write-Host "  ✅ EXPECTED: Service not found (404)" -ForegroundColor Green
    } elseif ($_.Exception.Message -like "*401*") {
        Write-Host "  ✅ EXPECTED: Authentication required (401)" -ForegroundColor Green
    } else {
        Write-Host "  ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Gateway Service Test Complete" -ForegroundColor Cyan 
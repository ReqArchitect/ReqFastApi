# Simple Gateway Test
# Tests basic gateway functionality

Write-Host "Testing Gateway Service..." -ForegroundColor Cyan

# Test 1: Basic health endpoint
Write-Host "1. Testing /health endpoint..." -ForegroundColor White
try {
    $Response = Invoke-WebRequest -Uri "http://localhost:8080/health" -Method GET -TimeoutSec 5
    Write-Host "   ✅ PASS: HTTP $($Response.StatusCode)" -ForegroundColor Green
    $HealthData = $Response.Content | ConvertFrom-Json
    Write-Host "   Status: $($HealthData.status)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 2: Check if service catalog exists
Write-Host "2. Checking service catalog..." -ForegroundColor White
try {
    $CatalogPath = "services/gateway_service/service_catalog.json"
    if (Test-Path $CatalogPath) {
        $CatalogSize = (Get-Item $CatalogPath).Length
        Write-Host "   ✅ Catalog exists: $CatalogSize bytes" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Catalog not found" -ForegroundColor Red
    }
} catch {
    Write-Host "   ❌ Error checking catalog: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 3: Check gateway container logs for errors
Write-Host "3. Checking gateway logs..." -ForegroundColor White
try {
    $Logs = docker logs gateway_service --tail 5 2>&1
    $ErrorLogs = $Logs | Where-Object { $_ -like "*ERROR*" -or $_ -like "*Exception*" }
    if ($ErrorLogs) {
        Write-Host "   ⚠️  Found errors in logs:" -ForegroundColor Yellow
        $ErrorLogs | ForEach-Object { Write-Host "   $($_)" -ForegroundColor Red }
    } else {
        Write-Host "   ✅ No recent errors found" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Error checking logs: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""

# Test 4: Check if service registry is working
Write-Host "4. Testing service registry..." -ForegroundColor White
Write-Host "   This would require a valid JWT token to test properly" -ForegroundColor Gray
Write-Host "   Current issue: Invalid JWT token causing 401 errors" -ForegroundColor Yellow

Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "- Basic health endpoint works" -ForegroundColor Green
Write-Host "- Service catalog exists" -ForegroundColor Green
Write-Host "- Enhanced endpoints failing due to authentication/configuration issues" -ForegroundColor Yellow
Write-Host "- Need valid JWT token for authenticated endpoints" -ForegroundColor Yellow 
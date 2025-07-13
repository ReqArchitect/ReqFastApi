# Simple ReqArchitect Services Test
# Tests currently running services

$Services = @{
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

Write-Host "Testing ReqArchitect Services..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$Results = @()
$Total = 0
$Passed = 0
$Failed = 0

foreach ($Service in $Services.GetEnumerator()) {
    $Total++
    $ServiceName = $Service.Key
    $Url = $Service.Value
    
    Write-Host "Testing $ServiceName..." -ForegroundColor White
    
    try {
        $Response = Invoke-WebRequest -Uri $Url -Headers $Headers -Method GET -TimeoutSec 10 -ErrorAction Stop
        
        if ($Response.StatusCode -eq 200) {
            try {
                $JsonResponse = $Response.Content | ConvertFrom-Json
                $Passed++
                Write-Host "  PASS: HTTP 200, Valid JSON" -ForegroundColor Green
                
                if ($JsonResponse.status) {
                    Write-Host "  Status: $($JsonResponse.status)" -ForegroundColor Gray
                }
                if ($JsonResponse.service) {
                    Write-Host "  Service: $($JsonResponse.service)" -ForegroundColor Gray
                }
                
                $Results += [PSCustomObject]@{
                    Service = $ServiceName
                    Status = "PASS"
                    Error = $null
                }
            } catch {
                $Failed++
                Write-Host "  FAIL: Invalid JSON" -ForegroundColor Red
                $Results += [PSCustomObject]@{
                    Service = $ServiceName
                    Status = "FAIL"
                    Error = "Invalid JSON"
                }
            }
        } else {
            $Failed++
            Write-Host "  FAIL: HTTP $($Response.StatusCode)" -ForegroundColor Red
            $Results += [PSCustomObject]@{
                Service = $ServiceName
                Status = "FAIL"
                Error = "HTTP $($Response.StatusCode)"
            }
        }
    } catch {
        $Failed++
        Write-Host "  FAIL: Connection Error" -ForegroundColor Red
        $Results += [PSCustomObject]@{
            Service = $ServiceName
            Status = "FAIL"
            Error = $_.Exception.Message
        }
    }
    
    Write-Host ""
}

Write-Host "Test Summary" -ForegroundColor Cyan
Write-Host "============" -ForegroundColor Cyan
Write-Host "Total: $Total" -ForegroundColor White
Write-Host "Passed: $Passed" -ForegroundColor Green
Write-Host "Failed: $Failed" -ForegroundColor Red
Write-Host "Success Rate: $([math]::Round(($Passed / $Total) * 100, 1))%" -ForegroundColor Yellow

if ($Failed -gt 0) {
    Write-Host ""
    Write-Host "Failed Services:" -ForegroundColor Red
    $FailedResults = $Results | Where-Object { $_.Status -eq "FAIL" }
    foreach ($Result in $FailedResults) {
        Write-Host "  • $($Result.Service): $($Result.Error)" -ForegroundColor Red
    }
}

$Results | Export-Csv -Path "service_test_results.csv" -NoTypeInformation
Write-Host ""
Write-Host "Results exported to: service_test_results.csv" -ForegroundColor Green 
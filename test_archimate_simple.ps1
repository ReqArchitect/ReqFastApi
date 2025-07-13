# Simple ArchiMate Services Test
# Tests ArchiMate-compliant microservices

$Services = @{
    # Motivation Layer
    "goal_service" = "http://localhost:8013/goals"
    "driver_service" = "http://localhost:8014/drivers"
    "requirement_service" = "http://localhost:8015/requirements"
    "constraint_service" = "http://localhost:8016/constraints"
    
    # Business Layer
    "businessfunction_service" = "http://localhost:8017/business-functions"
    "businessrole_service" = "http://localhost:8018/business-roles"
    "businessprocess_service" = "http://localhost:8019/business-processes"
    
    # Application Layer
    "applicationfunction_service" = "http://localhost:8080/application-functions"
    "applicationcomponent_service" = "http://localhost:8020/application-components"
    "resource_service" = "http://localhost:8021/resources"
    
    # Technology Layer
    "node_service" = "http://localhost:8022/nodes"
    "artifact_service" = "http://localhost:8023/artifacts"
    "communicationpath_service" = "http://localhost:8024/communication-paths"
    "device_service" = "http://localhost:8025/devices"
}

$Headers = @{
    "Authorization" = "Bearer test-jwt-token"
    "Content-Type" = "application/json"
}

Write-Host "Testing ArchiMate Services..." -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

$Results = @()
$Total = 0
$Passed = 0
$Failed = 0

foreach ($Service in $Services.GetEnumerator()) {
    $Total++
    $ServiceName = $Service.Key
    $Url = $Service.Value
    
    Write-Host "Testing $ServiceName..." -ForegroundColor White
    Write-Host "  URL: $Url" -ForegroundColor Gray
    
    try {
        $Response = Invoke-WebRequest -Uri $Url -Headers $Headers -Method GET -TimeoutSec 10 -ErrorAction Stop
        
        if ($Response.StatusCode -eq 200) {
            try {
                $JsonResponse = $Response.Content | ConvertFrom-Json
                $Passed++
                Write-Host "  PASS: HTTP 200, Valid JSON" -ForegroundColor Green
                
                # Check for ArchiMate fields
                if ($JsonResponse.Count) {
                    Write-Host "  Records: $($JsonResponse.Count)" -ForegroundColor Gray
                } elseif ($JsonResponse.value -and $JsonResponse.value.Count) {
                    Write-Host "  Records: $($JsonResponse.value.Count)" -ForegroundColor Gray
                }
                
                $Results += [PSCustomObject]@{
                    Service = $ServiceName
                    Status = "PASS"
                    Error = $null
                    Records = if ($JsonResponse.Count) { $JsonResponse.Count } elseif ($JsonResponse.value) { $JsonResponse.value.Count } else { 0 }
                }
            } catch {
                $Failed++
                Write-Host "  FAIL: Invalid JSON" -ForegroundColor Red
                $Results += [PSCustomObject]@{
                    Service = $ServiceName
                    Status = "FAIL"
                    Error = "Invalid JSON"
                    Records = 0
                }
            }
        } else {
            $Failed++
            Write-Host "  FAIL: HTTP $($Response.StatusCode)" -ForegroundColor Red
            $Results += [PSCustomObject]@{
                Service = $ServiceName
                Status = "FAIL"
                Error = "HTTP $($Response.StatusCode)"
                Records = 0
            }
        }
    } catch {
        $Failed++
        Write-Host "  FAIL: Connection Error" -ForegroundColor Red
        $Results += [PSCustomObject]@{
            Service = $ServiceName
            Status = "FAIL"
            Error = $_.Exception.Message
            Records = 0
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

$Results | Export-Csv -Path "archimate_test_results.csv" -NoTypeInformation
Write-Host ""
Write-Host "Results exported to: archimate_test_results.csv" -ForegroundColor Green 
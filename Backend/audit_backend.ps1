# ============================================================
# AI Buddy - Final Backend Audit
# Safe / Non-Destructive API Tests
# ============================================================

$BaseUrl = "http://127.0.0.1:8000"
$UserId = 1

$results = @()

function Test-Endpoint {
    param (
        [string]$Name,
        [string]$Method,
        [string]$Uri,
        [string]$Body = $null
    )

    try {
        $params = @{
            UseBasicParsing = $true
            Uri             = $Uri
            Method          = $Method
            Headers         = @{ "accept" = "application/json" }
        }

        if ($Body) {
            $params["ContentType"] = "application/json"
            $params["Body"] = $Body
        }

        $response = Invoke-WebRequest @params

        if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 300) {
            Write-Host "[PASS] $Name" -ForegroundColor Green

            $script:results += [PSCustomObject]@{
                Test   = $Name
                Status = "PASS"
                Code   = $response.StatusCode
            }
        }
        else {
            Write-Host "[FAIL] $Name - HTTP $($response.StatusCode)" -ForegroundColor Red

            $script:results += [PSCustomObject]@{
                Test   = $Name
                Status = "FAIL"
                Code   = $response.StatusCode
            }
        }

        return $response
    }
    catch {
        Write-Host "[FAIL] $Name - $($_.Exception.Message)" -ForegroundColor Red

        $script:results += [PSCustomObject]@{
            Test   = $Name
            Status = "FAIL"
            Code   = "ERROR"
        }

        return $null
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "             AI BUDDY BACKEND FINAL AUDIT" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# CORE API
# ============================================================

Test-Endpoint `
    -Name "Root API" `
    -Method "GET" `
    -Uri "$BaseUrl/"

Test-Endpoint `
    -Name "Health API" `
    -Method "GET" `
    -Uri "$BaseUrl/health"

# ============================================================
# SCHEDULER
# ============================================================

Test-Endpoint `
    -Name "Scheduler Status" `
    -Method "GET" `
    -Uri "$BaseUrl/api/scheduler/status"

Test-Endpoint `
    -Name "Scheduler Database Jobs" `
    -Method "GET" `
    -Uri "$BaseUrl/api/scheduler/database-jobs?user_id=$UserId"

# ============================================================
# TASKS
# ============================================================

Test-Endpoint `
    -Name "Tasks API" `
    -Method "GET" `
    -Uri "$BaseUrl/api/tasks/?user_id=$UserId"

# ============================================================
# MEMORY
# ============================================================

Test-Endpoint `
    -Name "Memory Status" `
    -Method "GET" `
    -Uri "$BaseUrl/api/memory/status"

Test-Endpoint `
    -Name "Memory History" `
    -Method "GET" `
    -Uri "$BaseUrl/api/memory/history?user_id=$UserId"

Test-Endpoint `
    -Name "Memory All" `
    -Method "GET" `
    -Uri "$BaseUrl/api/memory/all?user_id=$UserId"

# ============================================================
# NOTIFICATIONS
# ============================================================

Test-Endpoint `
    -Name "Notifications API" `
    -Method "GET" `
    -Uri "$BaseUrl/api/notifications/?user_id=$UserId"

# ============================================================
# SECURITY
# ============================================================

Test-Endpoint `
    -Name "Security Status" `
    -Method "GET" `
    -Uri "$BaseUrl/api/security/status/$UserId"

Test-Endpoint `
    -Name "Security Components" `
    -Method "GET" `
    -Uri "$BaseUrl/api/security/components"

Test-Endpoint `
    -Name "Security Permission List" `
    -Method "GET" `
    -Uri "$BaseUrl/api/security/permission/$UserId"

Test-Endpoint `
    -Name "Security Audit Logs" `
    -Method "GET" `
    -Uri "$BaseUrl/api/security/audit-logs"

# ============================================================
# AI BRAIN - GET TIME
# ============================================================

$timeBody = @{
    message = "What time is it right now?"
    user_id = $UserId
} | ConvertTo-Json

$timeResponse = Test-Endpoint `
    -Name "AI Brain - GET_TIME" `
    -Method "POST" `
    -Uri "$BaseUrl/api/chat" `
    -Body $timeBody

if ($timeResponse) {
    try {
        $timeJson = $timeResponse.Content | ConvertFrom-Json

        if ($timeJson.intent.intent -eq "GET_TIME") {
            Write-Host "[PASS] GET_TIME Intent Routing" -ForegroundColor Green

            $results += [PSCustomObject]@{
                Test   = "GET_TIME Intent Routing"
                Status = "PASS"
                Code   = "OK"
            }
        }
        else {
            Write-Host "[FAIL] GET_TIME Intent Routing" -ForegroundColor Red

            $results += [PSCustomObject]@{
                Test   = "GET_TIME Intent Routing"
                Status = "FAIL"
                Code   = "WRONG_INTENT"
            }
        }
    }
    catch {
        Write-Host "[FAIL] GET_TIME Response Parsing" -ForegroundColor Red

        $results += [PSCustomObject]@{
            Test   = "GET_TIME Response Parsing"
            Status = "FAIL"
            Code   = "ERROR"
        }
    }
}

# ============================================================
# AI BRAIN - GET DATE
# ============================================================

$dateBody = @{
    message = "What is today's date?"
    user_id = $UserId
} | ConvertTo-Json

$dateResponse = Test-Endpoint `
    -Name "AI Brain - GET_DATE" `
    -Method "POST" `
    -Uri "$BaseUrl/api/chat" `
    -Body $dateBody

if ($dateResponse) {
    try {
        $dateJson = $dateResponse.Content | ConvertFrom-Json

        if ($dateJson.intent.intent -eq "GET_DATE") {
            Write-Host "[PASS] GET_DATE Intent Routing" -ForegroundColor Green

            $results += [PSCustomObject]@{
                Test   = "GET_DATE Intent Routing"
                Status = "PASS"
                Code   = "OK"
            }
        }
        else {
            Write-Host "[FAIL] GET_DATE Intent Routing" -ForegroundColor Red

            $results += [PSCustomObject]@{
                Test   = "GET_DATE Intent Routing"
                Status = "FAIL"
                Code   = "WRONG_INTENT"
            }
        }
    }
    catch {
        Write-Host "[FAIL] GET_DATE Response Parsing" -ForegroundColor Red

        $results += [PSCustomObject]@{
            Test   = "GET_DATE Response Parsing"
            Status = "FAIL"
            Code   = "ERROR"
        }
    }
}

# ============================================================
# GEMINI / GENERAL AI
# ============================================================

$aiBody = @{
    message = "What is artificial intelligence?"
    user_id = $UserId
} | ConvertTo-Json

$aiResponse = Test-Endpoint `
    -Name "Gemini / General AI Query" `
    -Method "POST" `
    -Uri "$BaseUrl/api/chat" `
    -Body $aiBody

if ($aiResponse) {
    try {
        $aiJson = $aiResponse.Content | ConvertFrom-Json

        if ($aiJson.success -eq $true) {
            Write-Host "[PASS] Gemini AI Response" -ForegroundColor Green

            $results += [PSCustomObject]@{
                Test   = "Gemini AI Response"
                Status = "PASS"
                Code   = "OK"
            }
        }
        else {
            Write-Host "[FAIL] Gemini AI Response" -ForegroundColor Red

            $results += [PSCustomObject]@{
                Test   = "Gemini AI Response"
                Status = "FAIL"
                Code   = "FAILED"
            }
        }
    }
    catch {
        Write-Host "[FAIL] Gemini Response Parsing" -ForegroundColor Red

        $results += [PSCustomObject]@{
            Test   = "Gemini Response Parsing"
            Status = "FAIL"
            Code   = "ERROR"
        }
    }
}

# ============================================================
# PYTHON COMPILE CHECK
# ============================================================

Write-Host ""
Write-Host "Checking Python compilation..." -ForegroundColor Yellow

python -m compileall app -q

if ($LASTEXITCODE -eq 0) {
    Write-Host "[PASS] Python Compile Check" -ForegroundColor Green

    $results += [PSCustomObject]@{
        Test   = "Python Compile Check"
        Status = "PASS"
        Code   = "OK"
    }
}
else {
    Write-Host "[FAIL] Python Compile Check" -ForegroundColor Red

    $results += [PSCustomObject]@{
        Test   = "Python Compile Check"
        Status = "FAIL"
        Code   = "ERROR"
    }
}

# ============================================================
# FINAL SUMMARY
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "                    AUDIT SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$results | Format-Table -AutoSize

$passCount = ($results | Where-Object { $_.Status -eq "PASS" }).Count
$failCount = ($results | Where-Object { $_.Status -eq "FAIL" }).Count
$totalCount = $results.Count

Write-Host ""
Write-Host "Total Tests : $totalCount"
Write-Host "Passed      : $passCount" -ForegroundColor Green
Write-Host "Failed      : $failCount" -ForegroundColor Red

if ($failCount -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "       ALL SAFE BACKEND AUDIT TESTS PASSED" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
}
else {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "       SOME BACKEND AUDIT TESTS FAILED" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
}
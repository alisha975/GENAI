# Jenkinsfile Unit Test Runner (PowerShell)
# This script runs unit tests for the Jenkinsfile on Windows

param(
    [switch]$Verbose = $false,
    [switch]$StopOnError = $true
)

$ErrorActionPreference = if ($StopOnError) { "Stop" } else { "Continue" }

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "Jenkinsfile Unit Test Runner (PowerShell)" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Jenkinsfile exists
if (-not (Test-Path "Jenkinsfile")) {
    Write-Host "❌ Error: Jenkinsfile not found in current directory" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Jenkinsfile found" -ForegroundColor Green

# Load and parse Jenkinsfile
$jenkinsfileContent = Get-Content "Jenkinsfile" -Raw

$testResults = @()

# Test 1: Pipeline definition
Write-Host ""
Write-Host "Test 1: Verifying pipeline definition..." -ForegroundColor Yellow
if ($jenkinsfileContent -match "pipeline\s*\{" -and $jenkinsfileContent -match "agent\s+any") {
    Write-Host "PASSED: Pipeline definition exists" -ForegroundColor Green
    $testResults += @{Test = "Pipeline Definition"; Result = "PASSED" }
} else {
    Write-Host "FAILED: Pipeline definition not found" -ForegroundColor Red
    $testResults += @{Test = "Pipeline Definition"; Result = "FAILED" }
}

# Test 2: Environment variables
Write-Host ""
Write-Host "Test 2: Verifying environment variables..." -ForegroundColor Yellow
$requiredEnvVars = @(
    "PROJECT_DIR",
    "DOCKER_REGISTRY",
    "DOCKER_IMAGE_NAME",
    "DOCKER_IMAGE_TAG",
    "GIT_REPOSITORY",
    "GIT_BRANCH",
    "VM_HOST",
    "VM_PORT",
    "VM_USER",
    "VM_DEPLOY_DIR",
    "DOCKER_COMPOSE_FILE",
    "APP_PORT",
    "FRONTEND_PORT"
)

$allEnvVarsFound = $true
foreach ($envVar in $requiredEnvVars) {
    if ($jenkinsfileContent -match $envVar) {
        if ($Verbose) {
            Write-Host "  ✓ Found: $envVar" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ Missing: $envVar" -ForegroundColor Red
        $allEnvVarsFound = $false
    }
}

if ($allEnvVarsFound) {
    Write-Host "✓ PASSED: All environment variables found" -ForegroundColor Green
    $testResults += @{Test = "Environment Variables"; Result = "PASSED" }
} else {
    Write-Host "✗ FAILED: Some environment variables missing" -ForegroundColor Red
    $testResults += @{Test = "Environment Variables"; Result = "FAILED" }
}

# Test 3: Required stages
Write-Host ""
Write-Host "Test 3: Verifying required stages..." -ForegroundColor Yellow
$requiredStages = @(
    "Clone Repository",
    "Verify Project Structure",
    "Install Backend Dependencies",
    "Install Frontend Dependencies",
    "Build Frontend",
    "Lint and Test Backend",
    "Setup Environment Variables",
    "Docker Build",
    "Docker Compose Down",
    "Docker Compose Build",
    "Docker Compose Up",
    "Health Check",
    "API Health Check",
    "Verify Local Deployment",
    "Push Docker Image to Registry",
    "Deploy to Virtual Machine",
    "Build and Deploy Docker on VM",
    "Deploy Docker Compose on VM",
    "Health Check on VM",
    "Verify VM Deployment"
)

$allStagesFound = $true
foreach ($stage in $requiredStages) {
    $stagePattern = "stage\('$stage'\)"
    if ($jenkinsfileContent -match [regex]::Escape($stagePattern)) {
        if ($Verbose) {
            Write-Host "  ✓ Found: $stage" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ Missing: $stage" -ForegroundColor Red
        $allStagesFound = $false
    }
}

if ($allStagesFound) {
    Write-Host "✓ PASSED: All required stages found ($($requiredStages.Count) stages)" -ForegroundColor Green
    $testResults += @{Test = "Required Stages"; Result = "PASSED" }
} else {
    Write-Host "✗ FAILED: Some stages missing" -ForegroundColor Red
    $testResults += @{Test = "Required Stages"; Result = "FAILED" }
}

# Test 4: Deployment configuration
Write-Host ""
Write-Host "Test 4: Verifying deployment configuration..." -ForegroundColor Yellow
$deploymentChecks = @{
    "VM_HOST" = "136.113.95.72";
    "VM_USER" = "orion-dev";
    "FRONTEND_PORT" = "5173";
    "APP_PORT" = "2024"
}

$allDeploymentConfigOk = $true
foreach ($key in $deploymentChecks.Keys) {
    $value = $deploymentChecks[$key]
    $pattern = "$key\s*=\s*[`"']$value[`"']"
    if ($jenkinsfileContent -match $pattern) {
        if ($Verbose) {
            Write-Host "  ✓ $key = $value" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ $key configuration incorrect" -ForegroundColor Red
        $allDeploymentConfigOk = $false
    }
}

if ($allDeploymentConfigOk) {
    Write-Host "✓ PASSED: Deployment configuration correct" -ForegroundColor Green
    $testResults += @{Test = "Deployment Configuration"; Result = "PASSED" }
} else {
    Write-Host "✗ FAILED: Deployment configuration incorrect" -ForegroundColor Red
    $testResults += @{Test = "Deployment Configuration"; Result = "FAILED" }
}

# Test 5: SSH configuration
Write-Host ""
Write-Host "Test 5: Verifying SSH configuration..." -ForegroundColor Yellow
$sshChecks = @(
    "StrictHostKeyChecking=no",
    "`${VM_SSH_KEY}",
    "`${VM_PORT}",
    "`${VM_USER}@`${VM_HOST}"
)

$allSSHChecksOk = $true
foreach ($check in $sshChecks) {
    if ($jenkinsfileContent -match [regex]::Escape($check)) {
        if ($Verbose) {
            Write-Host "  ✓ Found: $check" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ Missing: $check" -ForegroundColor Red
        $allSSHChecksOk = $false
    }
}

if ($allSSHChecksOk) {
    Write-Host "✓ PASSED: SSH configuration correct" -ForegroundColor Green
    $testResults += @{Test = "SSH Configuration"; Result = "PASSED" }
} else {
    Write-Host "✗ FAILED: SSH configuration incorrect" -ForegroundColor Red
    $testResults += @{Test = "SSH Configuration"; Result = "FAILED" }
}

# Test 6: Docker commands
Write-Host ""
Write-Host "Test 6: Verifying Docker commands..." -ForegroundColor Yellow
$dockerChecks = @(
    "docker build",
    "docker-compose",
    "docker push",
    "docker ps",
    "docker images"
)

$allDockerChecksOk = $true
foreach ($check in $dockerChecks) {
    if ($jenkinsfileContent -match $check) {
        if ($Verbose) {
            Write-Host "  ✓ Found: $check" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ Missing: $check" -ForegroundColor Red
        $allDockerChecksOk = $false
    }
}

if ($allDockerChecksOk) {
    Write-Host "✓ PASSED: All Docker commands present" -ForegroundColor Green
    $testResults += @{Test = "Docker Commands"; Result = "PASSED" }
} else {
    Write-Host "✗ FAILED: Some Docker commands missing" -ForegroundColor Red
    $testResults += @{Test = "Docker Commands"; Result = "FAILED" }
}

# Test 7: File transfer (SCP)
Write-Host ""
Write-Host "Test 7: Verifying file transfer mechanisms..." -ForegroundColor Yellow
$fileTransferChecks = @(
    "scp",
    "Dockerfile",
    "docker-compose.yml",
    ".env"
)

$allFileTransferChecksOk = $true
foreach ($check in $fileTransferChecks) {
    if ($jenkinsfileContent -match $check) {
        if ($Verbose) {
            Write-Host "  ✓ Found: $check" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ Missing: $check" -ForegroundColor Red
        $allFileTransferChecksOk = $false
    }
}

if ($allFileTransferChecksOk) {
    Write-Host "✓ PASSED: File transfer mechanisms configured" -ForegroundColor Green
    $testResults += @{Test = "File Transfer"; Result = "PASSED" }
} else {
    Write-Host "✗ FAILED: File transfer configuration incomplete" -ForegroundColor Red
    $testResults += @{Test = "File Transfer"; Result = "FAILED" }
}

# Test 8: Health checks
Write-Host ""
Write-Host "Test 8: Verifying health check endpoints..." -ForegroundColor Yellow
$healthCheckChecks = @(
    "curl",
    "health",
    "localhost"
)

$allHealthCheckChecksOk = $true
foreach ($check in $healthCheckChecks) {
    if ($jenkinsfileContent -match $check) {
        if ($Verbose) {
            Write-Host "  ✓ Found: $check" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ Missing: $check" -ForegroundColor Red
        $allHealthCheckChecksOk = $false
    }
}

if ($allHealthCheckChecksOk) {
    Write-Host "✓ PASSED: Health check endpoints configured" -ForegroundColor Green
    $testResults += @{Test = "Health Checks"; Result = "PASSED" }
} else {
    Write-Host "✗ FAILED: Health check configuration incomplete" -ForegroundColor Red
    $testResults += @{Test = "Health Checks"; Result = "FAILED" }
}

# Test 9: Post-build actions
Write-Host ""
Write-Host "Test 9: Verifying post-build actions..." -ForegroundColor Yellow
$postActionChecks = @(
    "post\s*\{",
    "success\s*\{",
    "failure\s*\{",
    "always\s*\{"
)

$allPostActionChecksOk = $true
foreach ($check in $postActionChecks) {
    if ($jenkinsfileContent -match $check) {
        if ($Verbose) {
            Write-Host "  ✓ Found: $check" -ForegroundColor Green
        }
    } else {
        Write-Host "  ✗ Missing: $check" -ForegroundColor Red
        $allPostActionChecksOk = $false
    }
}

if ($allPostActionChecksOk) {
    Write-Host "✓ PASSED: Post-build actions configured" -ForegroundColor Green
    $testResults += @{Test = "Post Actions"; Result = "PASSED" }
} else {
    Write-Host "✗ FAILED: Post-build actions incomplete" -ForegroundColor Red
    $testResults += @{Test = "Post Actions"; Result = "FAILED" }
}

# Summary
Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "TEST SUMMARY" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

$passCount = ($testResults | Where-Object { $_.Result -eq "PASSED" }).Count
$failCount = ($testResults | Where-Object { $_.Result -eq "FAILED" }).Count
$totalCount = $testResults.Count

# Display results table
$testResults | Format-Table -AutoSize -Property @(
    @{Label = "Test Name"; Expression = { $_.Test } },
    @{Label = "Result"; Expression = { $_.Result } }
)

Write-Host ""
Write-Host "Total Tests: $totalCount" -ForegroundColor Cyan
Write-Host "Passed: $passCount" -ForegroundColor Green
Write-Host "Failed: $failCount" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($failCount -eq 0) {
    Write-Host "✓ ALL TESTS PASSED!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "✗ SOME TESTS FAILED!" -ForegroundColor Red
    exit 1
}

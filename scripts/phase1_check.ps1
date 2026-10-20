# Phase 1 Windows/PowerShell project check
# Run from the repository root:
# powershell -ExecutionPolicy Bypass -File .\scripts\phase1_check.ps1
$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "=== OS PBL Phase 1 project check ==="
Write-Host "Project: Integrated National Citizen Services Platform"
python --version

$requiredFiles = @(
    "main.py",
    "os_platform/models.py",
    "os_platform/scheduler.py",
    "os_platform/storage.py",
    "tests/test_scheduler.py",
    "tests/test_storage.py"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "OK: $file"
    } else {
        throw "Required project file missing: $file"
    }
}

Write-Host ""
Write-Host "=== Running unit tests ==="
python -m unittest discover -s tests -v
if ($LASTEXITCODE -ne 0) { throw "Unit tests failed with exit code $LASTEXITCODE" }

Write-Host ""
Write-Host "=== Running synthetic CLI demonstration ==="
python main.py
if ($LASTEXITCODE -ne 0) { throw "CLI demo failed with exit code $LASTEXITCODE" }

Write-Host ""
Write-Host "Phase 1 project check completed successfully."

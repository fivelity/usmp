# Ultimate Sensor Monitor Server Startup Script for PowerShell
# Run this script from the server directory

param(
    [switch]$Force,
    [switch]$InstallDeps
)

$ErrorActionPreference = "Stop"

# Get script directory
$ServerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ServerDir

Write-Host "=== Ultimate Sensor Monitor Server ===" -ForegroundColor Cyan
Write-Host "Server Directory: $ServerDir" -ForegroundColor Gray

# Use environment detector for better Python environment handling
$EnvDetectorPath = Join-Path $ServerDir "env_detector.py"
if (Test-Path $EnvDetectorPath) {
    Write-Host "Detecting Python environment..." -ForegroundColor Gray
    $EnvInfo = python $EnvDetectorPath
    Write-Host $EnvInfo -ForegroundColor Cyan
}

# Check if virtual environment exists
$VenvPath = Join-Path $ServerDir "venv"
$PythonExe = Join-Path $VenvPath "Scripts\python.exe"

if (-not (Test-Path $PythonExe)) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Yellow
    
    # Create virtual environment using the setup script
    $SetupScript = Join-Path $ServerDir "setup_venv.py"
    if (Test-Path $SetupScript) {
        python $SetupScript
    } else {
        # Fallback to direct venv creation
        python -m venv venv
    }
    
    if (-not $?) {
        Write-Error "Failed to create virtual environment"
        exit 1
    }
}

# Install/update dependencies if requested
if ($InstallDeps -or $Force) {
    Write-Host "Installing/updating dependencies..." -ForegroundColor Yellow
    & $PythonExe -m pip install --upgrade pip
    & $PythonExe -m pip install -r requirements.txt
    
    if (-not $?) {
        Write-Error "Failed to install dependencies"
        exit 1
    }
}

# Check if required packages are installed
Write-Host "Checking dependencies..." -ForegroundColor Gray
$RequiredPackages = @("fastapi", "uvicorn", "python-dotenv")

foreach ($Package in $RequiredPackages) {
    try {
        $null = & $PythonExe -c "import $Package" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Missing package: $Package. Installing dependencies..." -ForegroundColor Yellow
            & $PythonExe -m pip install -r requirements.txt
            break
        }
    }
    catch {
        Write-Host "Missing package: $Package. Installing dependencies..." -ForegroundColor Yellow
        & $PythonExe -m pip install -r requirements.txt
        break
    }
}

# Start the server
Write-Host "Starting server..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

try {
    & $PythonExe start_server.py
}
catch {
    Write-Error "Failed to start server: $_"
    exit 1
}

param(
    [switch]$NoAdmin,
    [switch]$QuickStart,
    [switch]$Verbose
)

# Set console title
$Host.UI.RawUI.WindowTitle = "Ultimate Sensor Monitor - PowerShell Launcher"

# Color functions
function Write-ColorText {
    param([string]$Text, [string]$Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Write-Success { param([string]$Text) Write-ColorText "✓ $Text" "Green" }
function Write-Error { param([string]$Text) Write-ColorText "✗ $Text" "Red" }
function Write-Warning { param([string]$Text) Write-ColorText "⚠ $Text" "Yellow" }
function Write-Info { param([string]$Text) Write-ColorText "ℹ $Text" "Cyan" }

# Header
Write-ColorText "========================================" "Cyan"
Write-ColorText "    Ultimate Sensor Monitor Launcher   " "Cyan"
Write-ColorText "========================================" "Cyan"
Write-Host ""

# Check administrator privileges
if (-not $NoAdmin) {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    
    if ($isAdmin) {
        Write-Success "Running with Administrator privileges"
    } else {
        Write-Warning "Not running as Administrator"
        Write-Warning "Hardware sensors may not be accessible"
        
        $response = Read-Host "Continue anyway? (Y/N)"
        if ($response -ne "Y" -and $response -ne "y") {
            exit 1
        }
    }
}

# Quick start mode
if ($QuickStart) {
    Write-Info "Quick start mode enabled - minimal validation"
    
    # Kill existing processes
    Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.MainWindowTitle -like "*Ultimate Sensor Monitor*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    Get-Process | Where-Object {$_.ProcessName -eq "node" -and $_.MainWindowTitle -like "*Ultimate Sensor Monitor*"} | Stop-Process -Force -ErrorAction SilentlyContinue
    
    # Start services
    Write-Info "Starting backend..."
    Start-Process -FilePath "cmd" -ArgumentList "/k", "cd server && python -m app.main" -WindowStyle Normal
    
    Write-Info "Starting frontend..."
    Start-Process -FilePath "cmd" -ArgumentList "/k", "cd client && npm run dev" -WindowStyle Normal
    
    Start-Sleep -Seconds 8
    Write-Info "Opening dashboard..."
    Start-Process "http://localhost:5501"
    
    Write-Success "Quick start completed!"
    Read-Host "Press Enter to close this launcher"
    exit 0
}

# Full validation mode
Write-Info "Validating project structure..."

if (-not (Test-Path "server")) {
    Write-Error "Server directory not found"
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "client")) {
    Write-Error "Client directory not found"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Success "Project structure validated"

# Check dependencies
Write-Info "Checking dependencies..."

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Python found: $pythonVersion"
    } else {
        throw "Python not found"
    }
} catch {
    Write-Error "Python not found in PATH"
    Write-Error "Please install Python 3.8+ from https://python.org"
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    $nodeVersion = node --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Node.js found: $nodeVersion"
    } else {
        throw "Node.js not found"
    }
} catch {
    Write-Error "Node.js not found in PATH"
    Write-Error "Please install Node.js from https://nodejs.org"
    Read-Host "Press Enter to exit"
    exit 1
}

# Stop existing services
Write-Info "Checking for existing services..."

$backendProcesses = Get-NetTCPConnection -LocalPort 8100 -ErrorAction SilentlyContinue
if ($backendProcesses) {
    Write-Warning "Stopping existing backend services..."
    $backendProcesses | ForEach-Object {
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

$frontendProcesses = Get-NetTCPConnection -LocalPort 5501 -ErrorAction SilentlyContinue
if ($frontendProcesses) {
    Write-Warning "Stopping existing frontend services..."
    $frontendProcesses | ForEach-Object {
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}

# Start backend
Write-Host ""
Write-Info "Starting Backend Server..."
$backendProcess = Start-Process -FilePath "cmd" -ArgumentList "/k", "cd server && python -m app.main" -WindowStyle Normal -PassThru

# Wait for backend
Write-Info "Waiting for backend to initialize..."
$maxAttempts = 15
$attempt = 0

do {
    Start-Sleep -Seconds 2
    $attempt++
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8100/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Success "Backend server is ready"
            break
        }
    } catch {
        if ($Verbose) {
            Write-Warning "Still waiting... ($attempt/$maxAttempts)"
        }
    }
    
    if ($attempt -ge $maxAttempts) {
        Write-Error "Backend failed to start within 30 seconds"
        Write-Error "Check the backend console for errors"
        Read-Host "Press Enter to exit"
        exit 1
    }
} while ($true)

# Start frontend
Write-Host ""
Write-Info "Starting Frontend Server..."
$frontendProcess = Start-Process -FilePath "cmd" -ArgumentList "/k", "cd client && npm run dev" -WindowStyle Normal -PassThru

# Wait for frontend
Write-Info "Waiting for frontend to initialize..."
$attempt = 0

do {
    Start-Sleep -Seconds 2
    $attempt++
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5501" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Success "Frontend server is ready"
            break
        }
    } catch {
        if ($Verbose) {
            Write-Warning "Still waiting... ($attempt/$maxAttempts)"
        }
    }
    
    if ($attempt -ge $maxAttempts) {
        Write-Error "Frontend failed to start within 30 seconds"
        Write-Error "Check the frontend console for errors"
        Read-Host "Press Enter to exit"
        exit 1
    }
} while ($true)

# Success
Write-Host ""
Write-ColorText "========================================" "Green"
Write-ColorText "    Ultimate Sensor Monitor Ready!     " "Green"
Write-ColorText "========================================" "Green"
Write-Host ""

Write-ColorText "Services running:" "White"
Write-ColorText "  Dashboard:    http://localhost:5501" "Cyan"
Write-ColorText "  API Server:   http://localhost:8100" "Cyan"
Write-ColorText "  API Docs:     http://localhost:8100/docs" "Cyan"
Write-ColorText "  WebSocket:    ws://localhost:8100/ws" "Cyan"
Write-Host ""

Write-Info "Opening dashboard in your default browser..."
Start-Sleep -Seconds 3
Start-Process "http://localhost:5501"

Write-Host ""
Write-ColorText "Press any key to close this launcher..." "White"
Write-Warning "Note: Backend and Frontend will continue running"
Write-Warning "Use stop_ultimon.bat to safely stop all services"
Read-Host

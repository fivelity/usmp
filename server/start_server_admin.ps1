#Requires -RunAsAdministrator

<#
.SYNOPSIS
    Ultimate Sensor Monitor - Admin Server Starter
    
.DESCRIPTION
    Starts the Ultimate Sensor Monitor server with administrator privileges for enhanced hardware access.
    Features:
    - Administrator privilege checking and elevation
    - Process cleanup and port management  
    - System.IO.Ports assembly fixing
    - Comprehensive error handling
    - Real-time status monitoring
    
.NOTES
    Author: Auto-generated
    Version: 2.0
    Requires: PowerShell 5.1+, Python 3.8+
#>

param(
    [string]$Port = "8100",
    [string]$ServerHost = "0.0.0.0",
    [switch]$SkipPortCheck,
    [switch]$SkipProcessCleanup,
    [switch]$Verbose
)

# Script configuration
$script:ServerDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$script:ProjectRoot = Split-Path -Parent $script:ServerDir
$script:LogFile = Join-Path $script:ServerDir "admin_startup.log"

# Colors for output
$script:Colors = @{
    Success = "Green"
    Warning = "Yellow" 
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Type = "Info",
        [switch]$NoNewLine
    )
    
    $color = $script:Colors[$Type]
    if ($NoNewLine) {
        Write-Host $Message -ForegroundColor $color -NoNewline
    } else {
        Write-Host $Message -ForegroundColor $color
    }
    
    # Also log to file
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "[$timestamp] [$Type] $Message" | Out-File -FilePath $script:LogFile -Append -Encoding utf8
}

function Show-Header {
    Clear-Host
    Write-ColorOutput "=================================================================" "Header"
    Write-ColorOutput "🚀 Ultimate Sensor Monitor - Admin Server Starter v2.0" "Header"
    Write-ColorOutput "=================================================================" "Header"
    Write-ColorOutput ""
}

function Test-AdminPrivileges {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Request-AdminElevation {
    if (-not (Test-AdminPrivileges)) {
        Write-ColorOutput "❌ Administrator privileges required!" "Error"
        Write-ColorOutput "🔄 Attempting to restart as administrator..." "Warning"
        
        $arguments = "-File `"$($MyInvocation.MyCommand.Path)`""
        if ($Port -ne "8100") { $arguments += " -Port $Port" }
        if ($ServerHost -ne "0.0.0.0") { $arguments += " -ServerHost $ServerHost" }
        if ($SkipPortCheck) { $arguments += " -SkipPortCheck" }
        if ($SkipProcessCleanup) { $arguments += " -SkipProcessCleanup" }
        if ($Verbose) { $arguments += " -Verbose" }
        
        try {
            Start-Process -FilePath "powershell.exe" -ArgumentList $arguments -Verb RunAs
            exit 0
        } catch {
            Write-ColorOutput "❌ Failed to elevate privileges: $($_.Exception.Message)" "Error"
            exit 1
        }
    }
    
    Write-ColorOutput "✅ Administrator privileges confirmed" "Success"
}

function Stop-ExistingProcesses {
    if ($SkipProcessCleanup) {
        Write-ColorOutput "⏭️ Skipping process cleanup (requested)" "Warning"
        return
    }
    
    Write-ColorOutput "🧹 Cleaning up existing processes..." "Info"
    
    # Kill existing Python uvicorn processes
    $pythonProcesses = Get-Process -Name "python*" -ErrorAction SilentlyContinue | 
        Where-Object { $_.CommandLine -like "*uvicorn*" -or $_.CommandLine -like "*8100*" }
    
    foreach ($process in $pythonProcesses) {
        try {
            Write-ColorOutput "  🔫 Stopping process: $($process.Name) (PID: $($process.Id))" "Info"
            $process | Stop-Process -Force
            Start-Sleep -Milliseconds 500
        } catch {
            Write-ColorOutput "    ⚠️ Could not stop process $($process.Id): $($_.Exception.Message)" "Warning"
        }
    }
    
    # Check for port conflicts
    if (-not $SkipPortCheck) {
        $portCheck = netstat -ano | Select-String ":$Port "
        if ($portCheck) {
            Write-ColorOutput "⚠️ Port $Port appears to be in use:" "Warning"
            $portCheck | ForEach-Object { Write-ColorOutput "    $_" "Warning" }
            
            # Try to kill processes using the port
            $pids = $portCheck | ForEach-Object { 
                ($_ -split '\s+')[-1] 
            } | Sort-Object -Unique
            
            foreach ($pid in $pids) {
                if ($pid -match '^\d+$' -and $pid -ne 0) {
                    try {
                        $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
                        if ($proc) {
                            Write-ColorOutput "  🔫 Killing process using port $Port`: $($proc.Name) (PID: $pid)" "Info"
                            Stop-Process -Id $pid -Force
                        }
                    } catch {
                        Write-ColorOutput "    ⚠️ Could not kill process $pid`: $($_.Exception.Message)" "Warning"
                    }
                }
            }
        }
    }
    
    # Wait for cleanup
    Start-Sleep -Seconds 2
    Write-ColorOutput "✅ Process cleanup completed" "Success"
}

function Install-SystemIOPorts {
    Write-ColorOutput "🔧 Attempting to fix System.IO.Ports assembly..." "Info"
    
    try {
        # Check if we can load System.IO.Ports
        $portsAssembly = [System.Reflection.Assembly]::LoadWithPartialName("System.IO.Ports")
        if ($portsAssembly) {
            Write-ColorOutput "✅ System.IO.Ports assembly already available" "Success"
            return $true
        }
    } catch {
        Write-ColorOutput "❌ System.IO.Ports not available: $($_.Exception.Message)" "Warning"
    }
    
    # Try to install via .NET SDK if available
    try {
        $dotnetInfo = dotnet --info 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  📦 .NET SDK detected, checking NuGet packages..." "Info"
            
            # This would require a project file, skip for now
            Write-ColorOutput "  ℹ️ System.IO.Ports can be installed via NuGet in project context" "Info"
        }
    } catch {
        Write-ColorOutput "  ⚠️ .NET SDK not available for package installation" "Warning"
    }
    
    # Check Windows Features
    try {
        Write-ColorOutput "  🔍 Checking Windows .NET Framework installations..." "Info"
        
        $netVersions = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP" -Recurse |
            Get-ItemProperty -Name Version, Release -ErrorAction SilentlyContinue |
            Where-Object { $_.Version -like "4.*" }
        
        if ($netVersions) {
            Write-ColorOutput "  ✅ .NET Framework 4.x detected" "Success"
            foreach ($version in $netVersions) {
                Write-ColorOutput "    - Version: $($version.Version)" "Info"
            }
        }
    } catch {
        Write-ColorOutput "  ⚠️ Could not check .NET Framework versions" "Warning"
    }
    
    Write-ColorOutput "ℹ️ System.IO.Ports may need manual installation or project configuration" "Info"
    return $false
}

function Test-PythonEnvironment {
    Write-ColorOutput "🐍 Checking Python environment..." "Info"
    
    # Check if we're in the server directory
    if (-not (Test-Path "app/main.py")) {
        Write-ColorOutput "❌ Not in server directory! Changing to: $script:ServerDir" "Error"
        Set-Location $script:ServerDir
        
        if (-not (Test-Path "app/main.py")) {
            Write-ColorOutput "❌ Cannot find app/main.py in server directory!" "Error"
            return $false
        }
    }
    
    # Check virtual environment
    if (Test-Path "venv/Scripts/activate.ps1") {
        Write-ColorOutput "✅ Virtual environment found" "Success"
        
        # Activate virtual environment
        try {
            & "./venv/Scripts/activate.ps1"
            Write-ColorOutput "✅ Virtual environment activated" "Success"
        } catch {
            Write-ColorOutput "⚠️ Could not activate virtual environment: $($_.Exception.Message)" "Warning"
        }
    } else {
        Write-ColorOutput "⚠️ No virtual environment found, using system Python" "Warning"
    }
    
    # Test Python and uvicorn
    try {
        $pythonVersion = python --version 2>&1
        Write-ColorOutput "✅ Python: $pythonVersion" "Success"
        
        $uvicornVersion = python -m uvicorn --version 2>&1
        Write-ColorOutput "✅ Uvicorn: $uvicornVersion" "Success"
        
        return $true
    } catch {
        Write-ColorOutput "❌ Python/Uvicorn not available: $($_.Exception.Message)" "Error"
        return $false
    }
}

function Start-SensorServer {
    Write-ColorOutput "🚀 Starting Ultimate Sensor Monitor server..." "Info"
    Write-ColorOutput "📡 Host: $ServerHost" "Info"
    Write-ColorOutput "🔌 Port: $Port" "Info"
    Write-ColorOutput "🔗 URL: http://$ServerHost`:$Port" "Info"
    Write-ColorOutput "📊 Docs: http://$ServerHost`:$Port/docs" "Info"
    Write-ColorOutput "🔌 WebSocket: ws://$ServerHost`:$Port/ws" "Info"
    Write-ColorOutput ""
    
    # Set environment variables for enhanced permissions
    $env:PYTHONPATH = $script:ServerDir
    $env:USM_ADMIN_MODE = "1"
    $env:USM_LOG_LEVEL = if ($Verbose) { "DEBUG" } else { "INFO" }
    
    Write-ColorOutput "🔄 Launching server with enhanced privileges..." "Info"
    Write-ColorOutput "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" "Header"
    
    try {
        # Start the server
        $arguments = @(
            "-m", "uvicorn"
            "app.main:app"
            "--host", $ServerHost
            "--port", $Port
            "--reload"
        )
        
        if ($Verbose) {
            $arguments += "--log-level", "debug"
        }
        
        & python $arguments
        
    } catch [System.Management.Automation.HaltCommandException] {
        Write-ColorOutput "🛑 Server stopped by user (Ctrl+C)" "Warning"
    } catch {
        Write-ColorOutput "❌ Server startup failed: $($_.Exception.Message)" "Error"
        Write-ColorOutput "📋 Full error details:" "Error"
        Write-ColorOutput $_.Exception.ToString() "Error"
        return $false
    }
    
    Write-ColorOutput "✅ Server shutdown complete" "Success"
    return $true
}

function Main {
    Show-Header
    
    # Check admin privileges and elevate if needed
    Request-AdminElevation
    
    Write-ColorOutput "🔧 System Information:" "Info"
    Write-ColorOutput "  📁 Project Root: $script:ProjectRoot" "Info"
    Write-ColorOutput "  📂 Server Dir: $script:ServerDir" "Info"
    Write-ColorOutput "  📄 Log File: $script:LogFile" "Info"
    Write-ColorOutput "  💻 PowerShell: $($PSVersionTable.PSVersion)" "Info"
    Write-ColorOutput "  🖥️ OS: $([Environment]::OSVersion.VersionString)" "Info"
    Write-ColorOutput ""
    
    # System preparation
    Stop-ExistingProcesses
    Install-SystemIOPorts
    
    # Test environment
    if (-not (Test-PythonEnvironment)) {
        Write-ColorOutput "❌ Python environment check failed!" "Error"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-ColorOutput ""
    Write-ColorOutput "🎯 All systems ready! Starting server..." "Success"
    Write-ColorOutput ""
    
    # Start the server
    $success = Start-SensorServer
    
    if ($success) {
        Write-ColorOutput "✅ Server operation completed successfully" "Success"
    } else {
        Write-ColorOutput "❌ Server operation failed" "Error"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Trap Ctrl+C for clean shutdown
trap {
    Write-ColorOutput "" "Info"
    Write-ColorOutput "🛑 Shutdown signal received..." "Warning"
    Write-ColorOutput "🧹 Cleaning up..." "Info"
    
    # Stop any running Python processes we started
    Get-Process -Name "python*" -ErrorAction SilentlyContinue | 
        Where-Object { $_.CommandLine -like "*uvicorn*" } |
        ForEach-Object { 
            Write-ColorOutput "  🔫 Stopping: $($_.Name) (PID: $($_.Id))" "Info"
            $_ | Stop-Process -Force 
        }
    
    Write-ColorOutput "✅ Cleanup complete. Goodbye!" "Success"
    exit 0
}

# Run main function
Main 
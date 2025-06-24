<#
.SYNOPSIS
    Ultimate Sensor Monitor - System Health Check
    
.DESCRIPTION
    Comprehensive diagnostic script to check for potential issues
    and validate the sensor monitoring system setup.
    
.NOTES
    Version: 2.0
    Can be run without admin privileges
#>

# Colors for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow" 
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-Check {
    param(
        [string]$Message,
        [string]$Status = "Info",
        [switch]$NoNewLine
    )
    
    $color = $Colors[$Status]
    $icon = switch ($Status) {
        "Success" { "[OK] " }
        "Warning" { "[WARN] " }
        "Error" { "[ERROR] " }
        default { "[INFO] " }
    }
    
    if ($NoNewLine) {
        Write-Host "$icon $Message" -ForegroundColor $color -NoNewline
    } else {
        Write-Host "$icon $Message" -ForegroundColor $color
    }
}

function Show-Header {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor Magenta
    Write-Host "Ultimate Sensor Monitor - System Health Check v2.0" -ForegroundColor Magenta
    Write-Host "=================================================================" -ForegroundColor Magenta
    Write-Host ""
}

function Test-AdminPrivileges {
    Write-Check "Checking administrator privileges..." "Info"
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if ($isAdmin) {
        Write-Check "Administrator privileges: AVAILABLE" "Success"
    } else {
        Write-Check "Administrator privileges: NOT AVAILABLE (recommended for full hardware access)" "Warning"
    }
    return $isAdmin
}

function Test-PythonSetup {
    Write-Host ""
    Write-Check "Checking Python environment..." "Info"
    
    # Check current directory
    if (-not (Test-Path "app/main.py")) {
        Write-Check "Not in server directory - checking if we can find it..." "Warning"
        
        $serverDir = Split-Path -Parent $MyInvocation.MyCommand.Path
        if (Test-Path (Join-Path $serverDir "app/main.py")) {
            Set-Location $serverDir
            Write-Check "Changed to server directory: $serverDir" "Success"
        } else {
            Write-Check "Cannot find server directory with app/main.py!" "Error"
            return $false
        }
    } else {
        Write-Check "Server directory: OK" "Success"
    }
    
    # Check virtual environment
    if (Test-Path "venv/Scripts/python.exe") {
        Write-Check "Virtual environment: FOUND" "Success"
        
        try {
            $pythonPath = Resolve-Path "venv/Scripts/python.exe"
            Write-Check "Python path: $pythonPath" "Info"
            
            $pythonVersion = & $pythonPath --version 2>&1
            Write-Check "Python version: $pythonVersion" "Success"
        } catch {
            Write-Check "Virtual environment Python: ERROR - $($_.Exception.Message)" "Error"
        }
    } else {
        Write-Check "Virtual environment: NOT FOUND" "Warning"
        
        try {
            $pythonVersion = python --version 2>&1
            Write-Check "System Python: $pythonVersion" "Success"
        } catch {
            Write-Check "System Python: NOT AVAILABLE" "Error"
            return $false
        }
    }
    
    # Check required packages
    try {
        if (Test-Path "venv/Scripts/python.exe") {
            $pipList = & "./venv/Scripts/python.exe" -m pip list 2>&1
        } else {
            $pipList = python -m pip list 2>&1
        }
        
        $requiredPackages = @("fastapi", "uvicorn", "pythonnet", "aiofiles")
        foreach ($package in $requiredPackages) {
            if ($pipList -match $package) {
                Write-Check "Package $package`: INSTALLED" "Success"
            } else {
                Write-Check "Package $package`: MISSING" "Error"
            }
        }
    } catch {
        Write-Check "Could not check installed packages: $($_.Exception.Message)" "Warning"
    }
    
    return $true
}

function Test-NetFramework {
    Write-Host ""
    Write-Check "Checking .NET Framework..." "Info"
    
    try {
        # Check .NET Framework versions
        $netVersions = Get-ChildItem "HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP" -Recurse |
            Get-ItemProperty -Name Version, Release -ErrorAction SilentlyContinue |
            Where-Object { $_.Version -like "4.*" }
        
        if ($netVersions) {
            Write-Check ".NET Framework 4.x: INSTALLED" "Success"
            foreach ($version in $netVersions) {
                Write-Check "  - Version: $($version.Version)" "Info"
            }
        } else {
            Write-Check ".NET Framework 4.x: NOT FOUND" "Error"
        }
        
        # Check System.Management
        try {
            $mgmtPaths = @(
                "C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Management.dll",
                "C:\Windows\Microsoft.NET\Framework\v4.0.30319\System.Management.dll"
            )
            
            $foundMgmt = $false
            foreach ($path in $mgmtPaths) {
                if (Test-Path $path) {
                    Write-Check "System.Management found: $path" "Success"
                    $foundMgmt = $true
                    break
                }
            }
            
            if (-not $foundMgmt) {
                Write-Check "System.Management: NOT FOUND" "Error"
            }
        } catch {
            Write-Check "System.Management check failed: $($_.Exception.Message)" "Warning"
        }
        
        # Check System.IO.Ports
        try {
            $portsAssembly = [System.Reflection.Assembly]::LoadWithPartialName("System.IO.Ports")
            if ($portsAssembly) {
                Write-Check "System.IO.Ports: AVAILABLE" "Success"
            } else {
                Write-Check "System.IO.Ports: NOT AVAILABLE (controllers will be disabled)" "Warning"
            }
        } catch {
            Write-Check "System.IO.Ports: NOT AVAILABLE - $($_.Exception.Message)" "Warning"
        }
        
    } catch {
        Write-Check ".NET Framework check failed: $($_.Exception.Message)" "Error"
    }
}

function Test-HardwareFiles {
    Write-Host ""
    Write-Check "Checking hardware monitoring files..." "Info"
    
    # Check LibreHardwareMonitor DLL
    if (Test-Path "LibreHardwareMonitorLib.dll") {
        $dllInfo = Get-Item "LibreHardwareMonitorLib.dll"
        Write-Check "LibreHardwareMonitor DLL: FOUND ($($dllInfo.Length) bytes)" "Success"
        Write-Check "  Path: $($dllInfo.FullName)" "Info"
        Write-Check "  Modified: $($dllInfo.LastWriteTime)" "Info"
    } else {
        Write-Check "LibreHardwareMonitor DLL: NOT FOUND" "Error"
    }
    
    # Check if we're in project root or server directory
    if (Test-Path "../LibreHardwareMonitorLib.dll") {
        Write-Check "LibreHardwareMonitor DLL also found in parent directory" "Info"
    }
    
    # Check sensor files
    $sensorFiles = @(
        "app/sensors/lhm_sensor.py",
        "app/sensors/hwinfo_sensor.py", 
        "app/main.py"
    )
    
    foreach ($file in $sensorFiles) {
        if (Test-Path $file) {
            Write-Check "Sensor file $file`: FOUND" "Success"
        } else {
            Write-Check "Sensor file $file`: MISSING" "Error"
        }
    }
}

function Test-PortConflicts {
    Write-Host ""
    Write-Check "Checking for port conflicts..." "Info"
    
    $port = "8100"
    $portCheck = netstat -ano | Select-String ":$port "
    
    if ($portCheck) {
        Write-Check "Port $port is currently in use:" "Warning"
        $portCheck | ForEach-Object { Write-Check "  $_" "Warning" }
        
        # Show process details
        $pids = $portCheck | ForEach-Object { 
            ($_ -split '\s+')[-1] 
        } | Sort-Object -Unique
        
        foreach ($pid in $pids) {
            if ($pid -match '^\d+$' -and $pid -ne 0) {
                try {
                    $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
                    if ($proc) {
                        Write-Check "  Process: $($proc.Name) (PID: $pid)" "Warning"
                    }
                } catch {
                    Write-Check "  Could not get process info for PID: $pid" "Warning"
                }
            }
        }
    } else {
        Write-Check "Port $port`: AVAILABLE" "Success"
    }
}

function Test-Permissions {
    Write-Host ""
    Write-Check "Checking file permissions..." "Info"
    
    # Test write access to current directory
    try {
        $testFile = "test_write_$(Get-Random).tmp"
        "test" | Out-File $testFile -ErrorAction Stop
        Remove-Item $testFile -ErrorAction SilentlyContinue
        Write-Check "Write access to current directory: OK" "Success"
    } catch {
        Write-Check "Write access to current directory: DENIED" "Error"
    }
    
    # Test DLL access
    if (Test-Path "LibreHardwareMonitorLib.dll") {
        try {
            $dllAccess = Get-Acl "LibreHardwareMonitorLib.dll"
            Write-Check "DLL file access: OK" "Success"
        } catch {
            Write-Check "DLL file access: LIMITED" "Warning"
        }
    }
}

function Show-Summary {
    Write-Host ""
    Write-Host "=================================================================" -ForegroundColor Magenta
    Write-Host "SUMMARY AND RECOMMENDATIONS" -ForegroundColor Magenta  
    Write-Host "=================================================================" -ForegroundColor Magenta
    Write-Host ""
    
    Write-Check "System Status Summary:" "Info"
    Write-Host ""
    
    # Admin check
    if (Test-AdminPrivileges) {
        Write-Check "Running with administrator privileges" "Success"
        Write-Check "  Full hardware monitoring capabilities available" "Info"
    } else {
        Write-Check "Not running as administrator" "Warning"
        Write-Check "  Some hardware sensors may be limited" "Warning"
        Write-Check "  Run start_admin.bat for full capabilities" "Info"
    }
    
    Write-Host ""
    Write-Check "Startup Options:" "Info"
    Write-Check "  - Regular startup: python -m uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload" "Info"
    Write-Check "  - Admin startup: .\start_admin.bat or .\start_server_admin.ps1" "Info"
    Write-Check "  - Batch launcher: .\start_admin.bat (recommended)" "Info"
    
    Write-Host ""
    Write-Check "URLs when running:" "Info"
    Write-Check "  - Main API: http://127.0.0.1:8100" "Info"
    Write-Check "  - Documentation: http://127.0.0.1:8100/docs" "Info"
    Write-Check "  - WebSocket: ws://127.0.0.1:8100/ws" "Info"
}

function Main {
    Show-Header
    
    # Run all checks
    Test-AdminPrivileges | Out-Null
    Test-PythonSetup | Out-Null
    Test-NetFramework
    Test-HardwareFiles
    Test-PortConflicts
    Test-Permissions
    
    # Show summary
    Show-Summary
    
    Write-Host ""
    Write-Check "System check complete!" "Success"
    Write-Host ""
}

# Run main function
Main

# Keep window open
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 
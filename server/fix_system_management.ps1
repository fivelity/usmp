# System.Management Fix Script for Ultimate Sensor Monitor
# This script aggressively fixes System.Management loading issues

param(
    [switch]$RunAsAdmin
)

# Self-elevate if needed
if (-not $RunAsAdmin) {
    if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "🔒 Restarting as administrator to fix System.Management..." -ForegroundColor Yellow
        Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -RunAsAdmin" -Verb RunAs
        exit
    }
}

Write-Host "`n🛠️  ULTIMATE SENSOR MONITOR - SYSTEM.MANAGEMENT FIX" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "🎯 Goal: Enable FULL hardware monitoring (not minimal!)" -ForegroundColor Green
Write-Host ""

# Function to test .NET assembly loading
function Test-DotNetAssembly {
    param([string]$AssemblyName)
    try {
        [System.Reflection.Assembly]::LoadWithPartialName($AssemblyName) | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Function to register System.Management in GAC
function Register-SystemManagement {
    Write-Host "🔧 Attempting to register System.Management in GAC..." -ForegroundColor Yellow
    
    $gacutil = @(
        "${env:ProgramFiles(x86)}\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\gacutil.exe",
        "${env:ProgramFiles(x86)}\Microsoft SDKs\Windows\v8.1A\bin\NETFX 4.5.1 Tools\gacutil.exe",
        "${env:ProgramFiles}\Microsoft SDKs\Windows\v10.0A\bin\NETFX 4.8 Tools\x64\gacutil.exe"
    )
    
    $systemMgmtDlls = @(
        "$env:WINDIR\Microsoft.NET\Framework64\v4.0.30319\System.Management.dll",
        "$env:WINDIR\Microsoft.NET\Framework\v4.0.30319\System.Management.dll"
    )
    
    foreach ($gac in $gacutil) {
        if (Test-Path $gac) {
            foreach ($dll in $systemMgmtDlls) {
                if (Test-Path $dll) {
                    try {
                        & $gac /i $dll /f
                        Write-Host "✅ Registered $dll in GAC" -ForegroundColor Green
                        return $true
                    } catch {
                        Write-Host "⚠️ Failed to register $dll" -ForegroundColor Yellow
                    }
                }
            }
        }
    }
    return $false
}

# 1. Check current System.Management status
Write-Host "🔍 Checking System.Management status..." -ForegroundColor White
if (Test-DotNetAssembly "System.Management") {
    Write-Host "✅ System.Management is loadable in PowerShell" -ForegroundColor Green
} else {
    Write-Host "❌ System.Management cannot be loaded in PowerShell" -ForegroundColor Red
}

# 2. Check available System.Management DLLs
Write-Host "`n📂 Checking System.Management DLL locations..." -ForegroundColor White
$dlls = Get-ChildItem -Path "$env:WINDIR\Microsoft.NET\Framework*\v*\System.Management.dll" -ErrorAction SilentlyContinue
foreach ($dll in $dlls) {
    $version = $dll.VersionInfo.FileVersion
    Write-Host "   📄 $($dll.FullName) (v$version)" -ForegroundColor Cyan
}

# 3. Test WMI functionality (requires System.Management)
Write-Host "`n🖥️ Testing WMI functionality..." -ForegroundColor White
try {
    $wmi = Get-WmiObject -Class Win32_ComputerSystem -ErrorAction Stop
    Write-Host "✅ WMI is working - System: $($wmi.Model)" -ForegroundColor Green
    
    # Test hardware enumeration
    $cpu = Get-WmiObject -Class Win32_Processor -ErrorAction Stop | Select-Object -First 1
    Write-Host "✅ CPU detection working - $($cpu.Name)" -ForegroundColor Green
    
    $storage = Get-WmiObject -Class Win32_DiskDrive -ErrorAction Stop | Select-Object -First 1
    Write-Host "✅ Storage detection working - $($storage.Model)" -ForegroundColor Green
    
} catch {
    Write-Host "❌ WMI is not working properly: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔧 This will prevent full hardware monitoring!" -ForegroundColor Yellow
}

# 4. Attempt fixes
Write-Host "`n🛠️ Attempting System.Management fixes..." -ForegroundColor White

# Fix 1: Re-register WMI
Write-Host "🔧 Re-registering WMI components..." -ForegroundColor Yellow
try {
    & winmgmt /resetrepository
    & winmgmt /regserver
    Write-Host "✅ WMI components re-registered" -ForegroundColor Green
} catch {
    Write-Host "⚠️ WMI re-registration failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Fix 2: Enable WMI service
Write-Host "🔧 Checking WMI service..." -ForegroundColor Yellow
$wmiService = Get-Service -Name "winmgmt" -ErrorAction SilentlyContinue
if ($wmiService) {
    if ($wmiService.Status -ne "Running") {
        try {
            Start-Service -Name "winmgmt" -ErrorAction Stop
            Write-Host "✅ WMI service started" -ForegroundColor Green
        } catch {
            Write-Host "❌ Failed to start WMI service: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "✅ WMI service is already running" -ForegroundColor Green
    }
} else {
    Write-Host "❌ WMI service not found!" -ForegroundColor Red
}

# Fix 3: Force load System.Management
Write-Host "`n🔧 Force-loading System.Management assembly..." -ForegroundColor Yellow
try {
    Add-Type -AssemblyName "System.Management" -ErrorAction Stop
    Write-Host "✅ System.Management loaded successfully" -ForegroundColor Green
    
    # Test ManagementScope
    $scope = New-Object System.Management.ManagementScope
    Write-Host "✅ ManagementScope creation successful" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Failed to load System.Management: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try alternative loading methods
    Write-Host "🔧 Trying alternative loading methods..." -ForegroundColor Yellow
    Register-SystemManagement
}

# 5. Test Python.NET compatibility
Write-Host "`n🐍 Testing Python.NET compatibility..." -ForegroundColor White
$pythonPath = if (Test-Path "venv\Scripts\python.exe") { "venv\Scripts\python.exe" } else { "python" }

$testScript = @"
import sys
try:
    print('⚙️ Loading Python.NET...')
    import pythonnet
    pythonnet.load('coreclr')
    
    import clr
    print('⚙️ Testing System.Management loading...')
    
    methods = [
        ('GAC Reference', lambda: clr.AddReference('System.Management')),
        ('Full Name', lambda: clr.AddReference('System.Management, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b03f5f7f11d50a3a')),
        ('Direct Path x64', lambda: clr.AddReference(r'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\System.Management.dll')),
        ('Direct Path x86', lambda: clr.AddReference(r'C:\Windows\Microsoft.NET\Framework\v4.0.30319\System.Management.dll'))
    ]
    
    success = False
    for name, method in methods:
        try:
            method()
            print(f'✅ {name} method succeeded!')
            success = True
            break
        except Exception as e:
            print(f'❌ {name} method failed: {e}')
    
    if success:
        print('🎯 Testing LibreHardwareMonitor...')
        clr.AddReference('LibreHardwareMonitorLib.dll')
        from LibreHardwareMonitor.Hardware import Computer
        
        c = Computer()
        c.IsCpuEnabled = True
        c.IsGpuEnabled = True
        c.IsMemoryEnabled = True
        c.IsStorageEnabled = True
        c.IsMotherboardEnabled = True
        
        c.Open()
        
        hardware_count = len(list(c.Hardware))
        print(f'🚀 SUCCESS! Detected {hardware_count} hardware components')
        print('🎉 FULL MONITORING SHOULD NOW WORK!')
        
        c.Close()
    else:
        print('💥 FAILED - System.Management could not be loaded')
        sys.exit(1)
        
except Exception as e:
    print(f'💥 ERROR: {e}')
    sys.exit(1)
"@

$testScript | Out-File -FilePath "test_system_management.py" -Encoding utf8

try {
    Write-Host "🧪 Running Python.NET test..." -ForegroundColor Yellow
    & $pythonPath "test_system_management.py"
    $pythonTestResult = $LASTEXITCODE
    
    if ($pythonTestResult -eq 0) {
        Write-Host "`n🎉 SUCCESS! System.Management is now working with Python.NET!" -ForegroundColor Green
        Write-Host "🚀 You should now get FULL hardware monitoring instead of minimal mode!" -ForegroundColor Green
    } else {
        Write-Host "`n💥 Python.NET test failed!" -ForegroundColor Red
        Write-Host "⚠️ You may still get minimal monitoring only." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Failed to run Python test: $($_.Exception.Message)" -ForegroundColor Red
}

# Cleanup
if (Test-Path "test_system_management.py") {
    Remove-Item "test_system_management.py" -Force
}

Write-Host "`n✨ Fix attempt completed!" -ForegroundColor Cyan
Write-Host "🔄 Restart your sensor monitor server to test the changes." -ForegroundColor White

Read-Host "`nPress Enter to continue..." 
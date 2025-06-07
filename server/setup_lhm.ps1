param(
    [switch]$RunAsAdmin
)

# Self-elevate if needed
if (-not $RunAsAdmin) {
    if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
        Write-Host "Restarting as administrator..."
        Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -RunAsAdmin" -Verb RunAs
        exit
    }
}

# Working directory
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

Write-Host "`n=== Ultimate Sensor Monitor - LHM Setup ==="
Write-Host "============================================`n"

function Install-DotNetComponent {
    param (
        [string]$Name,
        [string]$InstallCommand
    )
    Write-Host "Checking $Name..."
    try {
        # Try to load assembly
        [System.Reflection.Assembly]::LoadWithPartialName($Name) | Out-Null
        Write-Host "✅ $Name is already installed"
        return $true
    } catch {
        Write-Host "⚙️ Installing $Name..."
        try {
            Invoke-Expression $InstallCommand
            Write-Host "✅ $Name installed successfully"
            return $true
        } catch {
            Write-Host "❌ Failed to install $Name: $_"
            return $false
        }
    }
}

# Check and install System.Management
Install-DotNetComponent "System.Management" {
    Add-Type -AssemblyName "System.Management"
}

# Check Python environment
Write-Host "`nChecking Python environment..."
try {
    $venvPath = "venv"
    $pythonPath = if (Test-Path "$venvPath\Scripts\python.exe") {
        "$venvPath\Scripts\python.exe"
    } else {
        "python"
    }

    # Verify Python and pip
    & $pythonPath -c "import sys; print(f'✅ Python {sys.version_info.major}.{sys.version_info.minor} found')"
    & $pythonPath -m pip --version | Out-Null
    Write-Host "✅ pip is available"

    # Install/update required packages
    Write-Host "`nInstalling/updating required packages..."
    & $pythonPath -m pip install --upgrade pythonnet HardwareMonitor setuptools wheel
    Write-Host "✅ Packages installed successfully"

    # Verify LibreHardwareMonitor setup
    Write-Host "`nVerifying LibreHardwareMonitor setup..."
    $testScript = @"
import sys
import clr
import os
from pathlib import Path

try:
    print('⚙️ Initializing Python.NET...')
    import pythonnet
    pythonnet.load('coreclr')
    
    print('⚙️ Loading System.Management...')
    clr.AddReference('System.Management')
    
    print('⚙️ Loading LibreHardwareMonitorLib...')
    dll_path = Path('LibreHardwareMonitorLib.dll')
    if not dll_path.exists():
        print('❌ LibreHardwareMonitorLib.dll not found')
        sys.exit(1)
    
    clr.AddReference(str(dll_path.absolute()))
    from LibreHardwareMonitor.Hardware import Computer
    
    print('⚙️ Creating Computer instance...')
    c = Computer()
    c.IsCpuEnabled = True
    c.IsGpuEnabled = True
    c.IsMemoryEnabled = True
    c.IsMotherboardEnabled = True
    
    print('⚙️ Opening computer...')
    c.Open()
    
    print('\nDetected Hardware:')
    for hardware in c.Hardware:
        print(f'- {hardware.Name}')
    
    c.Close()
    print('\n✅ LibreHardwareMonitor test successful!')

except Exception as e:
    print(f'\n❌ Error: {e}')
    sys.exit(1)
"@

    # Save and run test script
    $testScript | Out-File -FilePath "test_lhm.py" -Encoding utf8
    Write-Host "`nRunning test script..."
    & $pythonPath "test_lhm.py"

    Write-Host "`n✅ Setup completed successfully!"
    
} catch {
    Write-Host "❌ Error: $_"
}

# Keep window open
Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Install .NET Framework Dependencies for Hardware Monitoring
# ============================================================
#
# This script helps install the necessary .NET Framework components
# to resolve System.Management dependency issues for LHMSensor.

param(
    [switch]$Force,
    [switch]$Verbose,
    [switch]$SkipDownload
)

# Set error action preference
$ErrorActionPreference = "Continue"

Write-Host "🔧 .NET Framework Dependency Installer for Hardware Monitoring" -ForegroundColor Cyan
Write-Host "=============================================================" -ForegroundColor Cyan

# Check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Administrator)) {
    Write-Warning "⚠️  This script should be run as Administrator for best results"
    Write-Host "   Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    if (-not $Force) {
        $continue = Read-Host "Continue anyway? (y/N)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            exit 1
        }
    }
}

# Function to check if a component is installed
function Test-ComponentInstalled {
    param([string]$ComponentName, [string]$RegistryPath)
    
    try {
        if (Test-Path $RegistryPath) {
            Write-Host "   ✅ $ComponentName is installed" -ForegroundColor Green
            return $true
        } else {
            Write-Host "   ❌ $ComponentName is not installed" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "   ⚠️  Cannot determine $ComponentName installation status" -ForegroundColor Yellow
        return $false
    }
}

# Function to download file
function Download-File {
    param([string]$Url, [string]$OutputPath)
    
    try {
        Write-Host "   🔽 Downloading from $Url..."
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($Url, $OutputPath)
        
        if (Test-Path $OutputPath) {
            $fileSize = (Get-Item $OutputPath).Length
            Write-Host "   ✅ Downloaded successfully ($([math]::Round($fileSize/1MB, 2)) MB)" -ForegroundColor Green
            return $true
        } else {
            Write-Host "   ❌ Download failed" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "   ❌ Download error: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Check current .NET Framework installations
Write-Host "`n📊 Checking Current .NET Framework Installation..." -ForegroundColor White
Write-Host "--------------------------------------------" -ForegroundColor Gray

# Check .NET Framework versions
$dotNetVersions = @(
    @{ Version = "4.8"; Registry = "HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full\"; ValueName = "Release"; MinValue = 528040 },
    @{ Version = "4.7.2"; Registry = "HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full\"; ValueName = "Release"; MinValue = 461808 },
    @{ Version = "4.7.1"; Registry = "HKLM:\SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full\"; ValueName = "Release"; MinValue = 461308 }
)

$hasCompatibleFramework = $false

foreach ($version in $dotNetVersions) {
    try {
        $releaseValue = Get-ItemProperty -Path $version.Registry -Name $version.ValueName -ErrorAction SilentlyContinue
        if ($releaseValue -and $releaseValue.Release -ge $version.MinValue) {
            Write-Host "   ✅ .NET Framework $($version.Version) is installed" -ForegroundColor Green
            $hasCompatibleFramework = $true
            break
        }
    } catch {
        # Continue checking
    }
}

if (-not $hasCompatibleFramework) {
    Write-Host "   ❌ Compatible .NET Framework version not found" -ForegroundColor Red
}

# Check Developer Pack
$devPackInstalled = Test-ComponentInstalled -ComponentName ".NET Framework 4.8 Developer Pack" -RegistryPath "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\{87A1A2F7-6B97-4182-9A62-C5C7E7C8F8E4}"

if (-not $devPackInstalled) {
    $devPackInstalled = Test-ComponentInstalled -ComponentName ".NET Framework 4.8 Developer Pack (x64)" -RegistryPath "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{87A1A2F7-6B97-4182-9A62-C5C7E7C8F8E4}"
}

# Check Windows SDK
$sdkInstalled = Test-ComponentInstalled -ComponentName "Windows 10 SDK" -RegistryPath "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Microsoft SDKs\Windows\v10.0"

# Recommendations and downloads
Write-Host "`n💡 Recommendations..." -ForegroundColor White
Write-Host "--------------------" -ForegroundColor Gray

$needsDevPack = -not $devPackInstalled
$needsFramework = -not $hasCompatibleFramework

if ($needsFramework) {
    Write-Host "   🚨 CRITICAL: Install .NET Framework 4.8" -ForegroundColor Red
    Write-Host "      This is required for System.Management support"
    
    if (-not $SkipDownload) {
        $frameworkUrl = "https://download.microsoft.com/download/9/4/7/947A87C6-DAF9-4B6C-9D35-F6BF5F8A7E8F/ndp48-web.exe"
        $frameworkPath = "$env:TEMP\ndp48-web.exe"
        
        Write-Host "`n📥 Downloading .NET Framework 4.8..."
        if (Download-File -Url $frameworkUrl -OutputPath $frameworkPath) {
            Write-Host "   💡 To install: Run $frameworkPath as Administrator" -ForegroundColor Yellow
            Write-Host "   ⚠️  This requires a system restart" -ForegroundColor Yellow
        }
    }
}

if ($needsDevPack) {
    Write-Host "   ⚠️  RECOMMENDED: Install .NET Framework 4.8 Developer Pack" -ForegroundColor Yellow
    Write-Host "      This provides additional development libraries"
    
    if (-not $SkipDownload) {
        $devPackUrl = "https://download.microsoft.com/download/7/4/0/740e1e3a-8aae-4464-a0b5-6b22a1dfdb14/ndp48-devpack-enu.exe"
        $devPackPath = "$env:TEMP\ndp48-devpack-enu.exe"
        
        Write-Host "`n📥 Downloading .NET Framework 4.8 Developer Pack..."
        if (Download-File -Url $devPackUrl -OutputPath $devPackPath) {
            Write-Host "   💡 To install: Run $devPackPath as Administrator" -ForegroundColor Yellow
        }
    }
}

if (-not $sdkInstalled) {
    Write-Host "   💡 OPTIONAL: Install Windows 10 SDK" -ForegroundColor Cyan
    Write-Host "      This provides additional Windows APIs"
    Write-Host "      Download from: https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/"
}

# System.Management specific check
Write-Host "`n🔍 Testing System.Management Assembly..." -ForegroundColor White
Write-Host "----------------------------------------" -ForegroundColor Gray

try {
    Add-Type -AssemblyName "System.Management"
    Write-Host "   ✅ System.Management assembly loaded successfully" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Failed to load System.Management assembly" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   💡 This confirms the need for .NET Framework installation" -ForegroundColor Yellow
}

# Python.NET test
Write-Host "`n🐍 Testing Python.NET Integration..." -ForegroundColor White
Write-Host "------------------------------------" -ForegroundColor Gray

try {
    $pythonOutput = python -c "import pythonnet; pythonnet.load('coreclr'); import clr; clr.AddReference('System.Management'); print('SUCCESS')" 2>&1
    
    if ($pythonOutput -like "*SUCCESS*") {
        Write-Host "   ✅ Python.NET with System.Management working" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Python.NET with System.Management failed" -ForegroundColor Red
        Write-Host "   Output: $pythonOutput" -ForegroundColor Gray
    }
} catch {
    Write-Host "   ❌ Python.NET test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Final recommendations
Write-Host "`n📋 Summary and Next Steps..." -ForegroundColor White
Write-Host "=============================" -ForegroundColor Gray

if ($needsFramework) {
    Write-Host "🚨 CRITICAL ACTIONS REQUIRED:" -ForegroundColor Red
    Write-Host "   1. Install .NET Framework 4.8 (downloaded to $env:TEMP)" -ForegroundColor Red
    Write-Host "   2. Restart your computer" -ForegroundColor Red
    Write-Host "   3. Re-run this script to verify installation" -ForegroundColor Red
} elseif ($needsDevPack) {
    Write-Host "⚠️  RECOMMENDED ACTIONS:" -ForegroundColor Yellow
    Write-Host "   1. Install .NET Framework 4.8 Developer Pack (downloaded to $env:TEMP)" -ForegroundColor Yellow
    Write-Host "   2. Re-run hardware monitoring tests" -ForegroundColor Yellow
} else {
    Write-Host "✅ .NET Framework appears to be properly installed!" -ForegroundColor Green
    Write-Host "   If you're still experiencing issues:" -ForegroundColor Green
    Write-Host "   1. Run: python system_diagnostics.py" -ForegroundColor Green
    Write-Host "   2. Run: python dependency_installer.py" -ForegroundColor Green
}

Write-Host "`n🔧 Additional Tools:" -ForegroundColor Cyan
Write-Host "   • system_diagnostics.py - Comprehensive system check" -ForegroundColor Cyan
Write-Host "   • dependency_installer.py - Automated dependency fixes" -ForegroundColor Cyan

Write-Host "`nDone! 🎉" -ForegroundColor Green 
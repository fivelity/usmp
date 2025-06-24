@echo off
REM Hardware Monitoring Fix Script with Admin Privileges
REM ====================================================

echo 🔧 Hardware Monitoring Comprehensive Fix
echo ====================================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running with Administrator privileges
) else (
    echo ⚠️  Not running as Administrator
    echo    Requesting elevated privileges...
    echo.
    
    REM Request admin privileges and re-run this script
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

echo.
echo Starting comprehensive hardware monitoring fix...
echo.

REM Run the Python fix script
python fix_hardware_monitoring.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ Fix completed successfully!
) else (
    echo.
    echo ⚠️  Fix completed with issues
    echo Check the output above for details
)

echo.
echo Press any key to continue...
pause >nul 
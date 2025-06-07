@echo off
title Ultimate Sensor Monitor - Admin Launcher

echo ========================================
echo Ultimate Sensor Monitor - Admin Launcher
echo ========================================
echo.
echo This will start the server with administrator privileges
echo for enhanced hardware monitoring capabilities.
echo.
echo Features:
echo - Full hardware sensor access
echo - Automatic process cleanup
echo - Port conflict resolution
echo - System.IO.Ports optimization
echo.
pause

echo.
echo Starting PowerShell admin script...
echo.

powershell.exe -ExecutionPolicy Bypass -File "%~dp0start_server_admin.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo *** Error occurred during startup ***
    echo Check the admin_startup.log file for details.
    echo.
    pause
) 
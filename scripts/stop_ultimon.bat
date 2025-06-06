@echo off
setlocal enabledelayedexpansion
title Ultimate Sensor Monitor - Service Stopper

:: Color codes
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "CYAN=[96m"
set "RESET=[0m"

echo %CYAN%========================================%RESET%
echo %CYAN%   Ultimate Sensor Monitor - Stopper   %RESET%
echo %CYAN%========================================%RESET%
echo.

echo %YELLOW%Stopping Ultimate Sensor Monitor services...%RESET%
echo.

:: Stop processes by port
echo %YELLOW%Checking for backend services (port 8100)...%RESET%
set backend_found=0
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8100') do (
    set backend_found=1
    echo %YELLOW%  Stopping backend process (PID: %%a)%RESET%
    taskkill /f /pid %%a >nul 2>&1
    if !errorLevel! == 0 (
        echo %GREEN%  ✓ Backend stopped successfully%RESET%
    ) else (
        echo %RED%  ✗ Failed to stop backend process%RESET%
    )
)
if %backend_found% == 0 echo %GREEN%  ✓ No backend services running%RESET%

echo.
echo %YELLOW%Checking for frontend services (port 5501)...%RESET%
set frontend_found=0
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5501') do (
    set frontend_found=1
    echo %YELLOW%  Stopping frontend process (PID: %%a)%RESET%
    taskkill /f /pid %%a >nul 2>&1
    if !errorLevel! == 0 (
        echo %GREEN%  ✓ Frontend stopped successfully%RESET%
    ) else (
        echo %RED%  ✗ Failed to stop frontend process%RESET%
    )
)
if %frontend_found% == 0 echo %GREEN%  ✓ No frontend services running%RESET%

:: Stop any remaining Python/Node processes related to our app
echo.
echo %YELLOW%Cleaning up related processes...%RESET%
taskkill /f /im "python.exe" /fi "WINDOWTITLE eq Ultimate Sensor Monitor - Backend*" >nul 2>&1
taskkill /f /im "node.exe" /fi "WINDOWTITLE eq Ultimate Sensor Monitor - Frontend*" >nul 2>&1

:: Close any remaining console windows
taskkill /f /fi "WINDOWTITLE eq Ultimate Sensor Monitor - Backend*" >nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Ultimate Sensor Monitor - Frontend*" >nul 2>&1

echo.
echo %GREEN%========================================%RESET%
echo %GREEN%     All services stopped cleanly!     %RESET%
echo %GREEN%========================================%RESET%
echo.
echo %YELLOW%You can now safely close this window or restart the application.%RESET%
echo.
pause

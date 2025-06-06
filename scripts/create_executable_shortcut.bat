@echo off
setlocal enabledelayedexpansion
title Ultimate Sensor Monitor - Shortcut Creator

echo ========================================
echo    Ultimate Sensor Monitor Setup
echo    Creating Desktop and Start Menu
echo ========================================
echo.

:: Get current directory
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

:: Desktop shortcut
echo Creating desktop shortcut...
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT_PATH=%DESKTOP%\Ultimate Sensor Monitor.lnk"

:: Create VBS script to make shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%SHORTCUT_PATH%" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%\start_ultimon_full.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Ultimate Sensor Monitor - Professional Hardware Monitoring Dashboard" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\System32\perfmon.exe,0" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

cscript //nologo "%TEMP%\CreateShortcut.vbs"
del "%TEMP%\CreateShortcut.vbs"

if exist "%SHORTCUT_PATH%" (
    echo ✓ Desktop shortcut created successfully
) else (
    echo ✗ Failed to create desktop shortcut
)

:: Start Menu folder
echo.
echo Creating Start Menu entries...
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Ultimate Sensor Monitor"

if not exist "%START_MENU%" mkdir "%START_MENU%"

:: Main launcher shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%START_MENU%\Ultimate Sensor Monitor.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%\start_ultimon_full.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Ultimate Sensor Monitor - Full Launcher" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\System32\perfmon.exe,0" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

cscript //nologo "%TEMP%\CreateShortcut.vbs"

:: Quick start shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%START_MENU%\Quick Start.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%\start_ultimon_quick.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Ultimate Sensor Monitor - Quick Start" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\System32\perfmon.exe,1" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

cscript //nologo "%TEMP%\CreateShortcut.vbs"

:: Stop application shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\CreateShortcut.vbs"
echo sLinkFile = "%START_MENU%\Stop Application.lnk" >> "%TEMP%\CreateShortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\CreateShortcut.vbs"
echo oLink.TargetPath = "%CURRENT_DIR%\stop_ultimon.bat" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Description = "Stop Ultimate Sensor Monitor Services" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.IconLocation = "%SystemRoot%\System32\perfmon.exe,2" >> "%TEMP%\CreateShortcut.vbs"
echo oLink.Save >> "%TEMP%\CreateShortcut.vbs"

cscript //nologo "%TEMP%\CreateShortcut.vbs"

del "%TEMP%\CreateShortcut.vbs"

echo ✓ Start Menu shortcuts created successfully

:: Summary
echo.
echo ========================================
echo           Setup Complete!
echo ========================================
echo.
echo Created shortcuts:
echo   • Desktop: Ultimate Sensor Monitor.lnk
echo   • Start Menu: Ultimate Sensor Monitor folder
echo     - Ultimate Sensor Monitor (main launcher)
echo     - Quick Start (fast launcher)
echo     - Stop Application (service stopper)
echo.
echo You can now:
echo   1. Double-click the desktop shortcut to launch
echo   2. Find it in your Start Menu
echo   3. Pin it to taskbar for easy access
echo.
echo Press any key to close...
pause >nul

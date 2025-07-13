@echo off
title FUSION 360 BRIDGE SERVER
cd /d "%~dp0"

echo 🌐 Starting Fusion 360 Bridge Server...
echo.

:: Check Python
echo [1/2] Checking Python...
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo ✅ Found: %%i
    goto :start_server
)

py --version >nul 2>&1  
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('py --version 2^>^&1') do echo ✅ Found: %%i
    set PYTHON_CMD=py
    goto :start_server
)

echo ❌ Python not found! 
echo 💡 Run PYTHON-INSTALLER.bat first
pause
exit /b 1

:start_server
echo.
echo [2/2] Starting bridge server...
echo 🌐 Server will run on: http://localhost:8766
echo 🎮 Browser will open automatically
echo ⚠️  Keep this window open
echo 💻 Press Ctrl+C to stop
echo.

if not exist bridge_server.py (
    echo ❌ bridge_server.py not found!
    echo 💡 Run CREATE-BRIDGE-FILES-FIXED.bat first
    pause
    exit /b 1
)

if defined PYTHON_CMD (
    %PYTHON_CMD% bridge_server.py
) else (
    python bridge_server.py
)

pause

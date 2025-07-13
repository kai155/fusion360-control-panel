@echo off
title WEBSOCKET INSTALLER FOR FUSION 360
cls

echo.
echo ==========================================
echo    WEBSOCKET CLIENT INSTALLER
echo    FOR FUSION 360 REMOTE CONTROL
echo ==========================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo.
    echo 💡 SOLUTION:
    echo    1. Download Python from: https://python.org/downloads
    echo    2. During installation, CHECK "Add Python to PATH"
    echo    3. Restart computer after installation
    echo    4. Run this installer again
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Found: %PYTHON_VERSION%

echo.
echo [2/3] Installing websocket-client package...

:: Method 1: User install
echo 🔄 Attempting user installation...
python -m pip install websocket-client --user --upgrade --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS: User installation completed
    goto :test
)

:: Method 2: System install
echo 🔄 Attempting system installation...
python -m pip install websocket-client --upgrade --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS: System installation completed
    goto :test
)

:: Method 3: Direct pip
echo 🔄 Attempting direct pip installation...
pip install websocket-client --user --upgrade --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS: Direct pip installation completed
    goto :test
)

:: Method 4: Force install
echo 🔄 Attempting force installation...
python -m pip install websocket-client --user --force-reinstall --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS: Force installation completed
    goto :test
)

echo ❌ ERROR: All installation methods failed!
echo.
echo 💡 MANUAL SOLUTION:
echo    1. Open Command Prompt as Administrator
echo    2. Run: pip install websocket-client
echo    3. If that fails, try: python -m pip install websocket-client
echo.
pause
exit /b 1

:test
echo.
echo [3/3] Testing installation...
python -c "import websocket; print('✅ websocket-client is working!')" 2>nul
if %errorlevel% == 0 (
    echo ✅ INSTALLATION SUCCESSFUL!
    echo.
    echo ==========================================
    echo    INSTALLATION COMPLETED SUCCESSFULLY!
    echo ==========================================
    echo.
    echo 📋 NEXT STEPS:
    echo    1. Go back to Fusion 360
    echo    2. UTILITIES → ADD-INS → Find "HTLM"
    echo    3. Click "Stop" then "Run"
    echo    4. You should see: "🌐 Remote Control Connected!"
    echo.
    echo 🎉 No more "WebSocket not available" error!
    echo.
) else (
    echo ❌ ERROR: Installation completed but import test failed
    echo.
    echo 💡 SOLUTION:
    echo    1. Restart Fusion 360 completely
    echo    2. Try running this installer as Administrator
    echo    3. Restart your computer if needed
    echo.
)

pause

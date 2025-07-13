@echo off
echo 🔧 WEBSOCKET CLIENT INSTALLER
echo ============================
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔑 This needs Administrator privileges to install packages
    echo 💡 Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo ✅ Running with Administrator privileges
echo.

echo 📦 Installing websocket-client for Fusion 360...
echo.

:: Try multiple Python installation methods
echo 🔍 Method 1: Using python...
python -m pip install websocket-client --user --upgrade --force-reinstall
if %errorlevel% == 0 (
    echo ✅ SUCCESS! websocket-client installed via python
    goto :success
)

echo 🔍 Method 2: Using pip directly...
pip install websocket-client --user --upgrade --force-reinstall
if %errorlevel% == 0 (
    echo ✅ SUCCESS! websocket-client installed via pip
    goto :success
)

echo 🔍 Method 3: Using py launcher...
py -m pip install websocket-client --user --upgrade --force-reinstall
if %errorlevel% == 0 (
    echo ✅ SUCCESS! websocket-client installed via py
    goto :success
)

echo ❌ All installation methods failed!
echo.
echo 💡 Please try:
echo 1. Install Python from https://python.org
echo 2. Make sure "Add Python to PATH" is checked
echo 3. Restart computer
echo 4. Try again
echo.
pause
exit /b 1

:success
echo.
echo 🎉 INSTALLATION COMPLETE!
echo.
echo 📋 Next steps:
echo 1. Close Fusion 360 completely
echo 2. Restart Fusion 360
echo 3. Go to UTILITIES → ADD-INS → HTLM → Run
echo 4. Should see "🌐 Remote Control Connected!" popup
echo.
echo ✅ No more "WebSocket not available" error!
echo.
pause

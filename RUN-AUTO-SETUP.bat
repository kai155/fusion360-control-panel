@echo off
echo 🤖 STARTING AUTO-SETUP...
echo.

:: Check for admin rights and elevate if needed
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔑 Requesting Administrator privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b 0
)

echo ✅ Running with Administrator privileges
echo.

:: Install websocket-client directly
echo 📦 Installing websocket-client package...
python -m pip install websocket-client --upgrade --force-reinstall
if errorlevel 1 (
    pip install websocket-client --upgrade --force-reinstall
    if errorlevel 1 (
        py -m pip install websocket-client --upgrade --force-reinstall
    )
)

echo ✅ Package installation complete!
echo.

:: Run PowerShell script with execution policy bypass
echo 🚀 Starting setup script...
powershell -ExecutionPolicy Bypass -File "%~dp0auto-setup.ps1"

echo.
echo ✅ Auto-setup finished!
echo.
echo 💡 Now restart Fusion 360 and run the HTLM add-in!
pause

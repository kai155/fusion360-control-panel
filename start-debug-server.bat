@echo off
echo 🔧 FUSION 360 SERVER DEBUG
echo ========================
echo.

cd /d "%~dp0"
echo 📁 Working directory: %CD%
echo.

echo 🐍 Checking Python...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

echo 📦 Installing required packages...
pip install websockets --quiet --upgrade

echo.
echo 🚀 Starting debug server...
echo 🌐 Server will be available at: ws://localhost:8765
echo 📱 Browser interface: https://kai155.github.io/fusion360-control-panel/remote-control.html
echo.
echo ⚡ Starting now...
echo.

python debug_server.py

echo.
echo 🛑 Server stopped.
pause

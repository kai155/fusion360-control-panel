@echo off
echo 🚀 FUSION 360 REMOTE CONTROL SERVER
echo =====================================
echo.

echo 📁 Starting from: %CD%
echo 🐍 Using Python virtual environment...

if not exist ".venv" (
    echo ❌ Virtual environment not found. Creating...
    python -m venv .venv
)

echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 📦 Installing/updating packages...
pip install websockets websocket-client --quiet --upgrade

echo 🌐 Starting WebSocket server...
echo 🔗 Server will run on: ws://localhost:8765
echo 📱 Browser interface: https://kai155.github.io/fusion360-control-panel/remote-control.html
echo.
echo ⚡ Server is starting... Press Ctrl+C to stop
echo.

python remote_server_simple.py
pause

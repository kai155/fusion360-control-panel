@echo off
echo 🚀 Starting Fusion 360 Remote Control Server...
echo.
echo This will start the WebSocket server for remote control.
echo Keep this window open while using remote control.
echo.

cd /d "%~dp0"

REM Check if Python virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Python virtual environment not found!
    echo Please run setup first or check installation.
    pause
    exit /b 1
)

REM Check if required packages are installed
".venv\Scripts\python.exe" -c "import websockets; import asyncio" 2>nul
if errorlevel 1 (
    echo 📦 Installing required packages...
    ".venv\Scripts\pip.exe" install websockets websocket-client
)

echo ✅ Starting WebSocket server on port 8765...
echo.
echo 🌐 Server will be available at:
echo    Local:    ws://localhost:8765
echo    Network:  ws://[your-ip]:8765
echo.
echo 📱 Open remote-control.html in any browser to control Fusion 360
echo.
echo Press Ctrl+C to stop the server
echo.

".venv\Scripts\python.exe" remote_server_simple.py

echo.
echo Server stopped.
pause

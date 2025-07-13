@echo off
echo ====================================
echo 🔍 FUSION 360 REMOTE CONTROL DEBUG
echo ====================================
echo.

cd /d "%~dp0"

echo ✅ Step 1: Testing Python environment...
".venv\Scripts\python.exe" --version
if errorlevel 1 (
    echo ❌ Python not found!
    pause
    exit /b 1
)

echo.
echo ✅ Step 2: Testing WebSocket packages...
".venv\Scripts\python.exe" -c "import websockets; print('✅ websockets OK')"
if errorlevel 1 (
    echo ❌ Installing websockets...
    ".venv\Scripts\pip.exe" install websockets websocket-client
)

echo ✅ Step 2.5: Installing additional packages...
".venv\Scripts\pip.exe" install websocket-client --upgrade

echo.
echo ✅ Step 3: Checking if server is already running...
netstat -an | findstr :8765
if not errorlevel 1 (
    echo ⚠️  Port 8765 is already in use
    echo.
)

echo.
echo ✅ Step 4: Starting WebSocket server...
echo 🌐 Server URL: ws://localhost:8765
echo 📱 Browser interface: remote-control-browser.html
echo.
echo Keep this window open and follow these steps:
echo.
echo 1. ✅ Server will start below
echo 2. 🔄 Restart Fusion 360 add-in (HTLM)  
echo 3. 🌐 Click CONNECT in browser interface
echo 4. 🎯 Test commands (Create Box, Save, etc)
echo.
echo Press Ctrl+C to stop server
echo ====================================
echo.

".venv\Scripts\python.exe" remote_server_simple.py

echo.
echo Server stopped.
pause

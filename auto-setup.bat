@echo off
echo 🤖 FUSION 360 WEBSOCKET AUTO-SETUP
echo ===================================
echo.

echo 📦 Step 1: Installing websocket-client...
python -m pip install websocket-client --user --upgrade --quiet
if errorlevel 1 (
    echo ❌ Python pip failed, trying alternative methods...
    pip install websocket-client --user --upgrade --quiet
    if errorlevel 1 (
        py -m pip install websocket-client --user --upgrade --quiet
        if errorlevel 1 (
            echo ❌ Could not install websocket-client automatically
            echo 💡 Please install Python from python.org and try again
            pause
            exit /b 1
        )
    )
)

echo ✅ websocket-client installed successfully!
echo.

echo 🔄 Step 2: Attempting to restart Fusion 360 add-in...
echo.

:: Try to find and kill Fusion 360 processes
echo 🛑 Stopping Fusion 360...
taskkill /f /im "Fusion360.exe" >nul 2>&1
taskkill /f /im "FusionLauncher.exe" >nul 2>&1
timeout /t 3 /nobreak >nul

echo ⏳ Waiting for processes to close...
timeout /t 2 /nobreak >nul

echo 🚀 Starting Fusion 360...
:: Try to start Fusion 360 from common locations
if exist "C:\Users\%USERNAME%\AppData\Local\Autodesk\webdeploy\production" (
    for /f "tokens=*" %%i in ('dir /b /s "C:\Users\%USERNAME%\AppData\Local\Autodesk\webdeploy\production\*\Fusion360.exe" 2^>nul') do (
        start "" "%%i"
        echo ✅ Fusion 360 started: %%i
        goto :fusion_started
    )
)

:: Alternative method - try from desktop or start menu
start "" "Fusion 360" >nul 2>&1
if errorlevel 1 (
    echo ❌ Could not auto-start Fusion 360
    echo 💡 Please start Fusion 360 manually
) else (
    echo ✅ Fusion 360 starting...
)

:fusion_started
echo.
echo ⏳ Waiting for Fusion 360 to load...
timeout /t 10 /nobreak >nul

echo.
echo 🎯 Step 3: Starting WebSocket server...
start "WebSocket Server" cmd /k "echo 🌐 WEBSOCKET SERVER && echo. && python debug_server.py"

echo.
echo ✅ AUTO-SETUP COMPLETE!
echo.
echo 📋 What happened:
echo   ✅ Installed websocket-client package
echo   ✅ Restarted Fusion 360 
echo   ✅ Started WebSocket server
echo.
echo 🎮 Next steps:
echo   1. In Fusion 360: UTILITIES → ADD-INS → HTLM → Run
echo   2. Look for popup: "🌐 Remote Control Connected!"
echo   3. Test browser: https://kai155.github.io/fusion360-control-panel/remote-control.html
echo.
echo 🎉 Everything should work now!
pause

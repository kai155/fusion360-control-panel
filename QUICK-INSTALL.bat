@echo off
cls
echo 🔧 INSTANT WEBSOCKET INSTALLER
echo =============================
echo.

echo 📍 Current directory: %CD%
echo 🐍 Testing Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo 💡 Install Python from https://python.org
    echo    Make sure to check "Add Python to PATH"
    pause
    exit /b 1
) else (
    python --version
    echo ✅ Python found
)

echo.
echo 📦 Installing websocket-client package...
echo 🔄 Method 1: Using python -m pip...

python -m pip install websocket-client --user --upgrade --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS via python -m pip
    goto :test
)

echo 🔄 Method 2: Using pip directly...
pip install websocket-client --user --upgrade --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS via pip
    goto :test
)

echo 🔄 Method 3: Using py launcher...
py -m pip install websocket-client --user --upgrade --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS via py launcher
    goto :test
)

echo ❌ All methods failed!
echo 💡 Try running as Administrator
pause
exit /b 1

:test
echo.
echo 🧪 Testing websocket-client import...
python -c "import websocket; print('✅ websocket-client works!')"
if %errorlevel% == 0 (
    echo 🎉 INSTALLATION COMPLETE!
    echo.
    echo 📋 Next steps:
    echo 1. Close this window
    echo 2. In Fusion 360: Stop and Run the HTLM add-in
    echo 3. Should see "🌐 Remote Control Connected!"
) else (
    echo ❌ Import test failed
    echo 💡 Try restarting Fusion 360
)

echo.
pause

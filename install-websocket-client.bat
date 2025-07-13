@echo off
echo 📦 INSTALLING WEBSOCKET CLIENT FOR FUSION 360
echo ============================================
echo.

echo 🔍 Finding Python executable...

:: Try common Python paths
set PYTHON_EXE=""

:: Method 1: Try system Python
where python >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_EXE=python
    echo ✅ Found system Python
    goto :install
)

:: Method 2: Try Fusion 360's Python (typical locations)
if exist "C:\Users\%USERNAME%\AppData\Local\Autodesk\webdeploy\production\*\Python\python.exe" (
    for /f "tokens=*" %%i in ('dir /b /s "C:\Users\%USERNAME%\AppData\Local\Autodesk\webdeploy\production\*\Python\python.exe" 2^>nul') do (
        set PYTHON_EXE="%%i"
        echo ✅ Found Fusion 360 Python: %%i
        goto :install
    )
)

:: Method 3: Try Python from PATH
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_EXE=python3
    echo ✅ Found Python3
    goto :install
)

:: Method 4: Manual detection
echo ❌ Python not found automatically
echo.
echo 💡 Please install Python from: https://www.python.org/downloads/
echo    Make sure to check "Add Python to PATH" during installation
echo.
pause
exit /b 1

:install
echo.
echo 🚀 Installing websocket-client package...
echo 📍 Using: %PYTHON_EXE%
echo.

%PYTHON_EXE% -m pip install websocket-client --user --upgrade

if %errorlevel% == 0 (
    echo.
    echo ✅ SUCCESS! websocket-client installed successfully!
    echo.
    echo 🔄 Now restart Fusion 360 and the add-in should work!
    echo.
) else (
    echo.
    echo ❌ Installation failed!
    echo.
    echo 💡 Try running this as Administrator:
    echo    Right-click on this file and select "Run as administrator"
    echo.
)

pause

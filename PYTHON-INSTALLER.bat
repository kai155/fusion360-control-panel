@echo off
title PYTHON + WEBSOCKET INSTALLER FOR FUSION 360
cls

echo.
echo ==========================================
echo    PYTHON + WEBSOCKET INSTALLER
echo    FOR FUSION 360 REMOTE CONTROL
echo ==========================================
echo.

echo [1/4] Checking Python installation...

:: Check for python command
python --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Found: !PYTHON_VERSION!
    goto :install_websocket
)

:: Check for py launcher
py --version >nul 2>&1
if not errorlevel 1 (
    for /f "tokens=*" %%i in ('py --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Found Python Launcher: !PYTHON_VERSION!
    set PYTHON_CMD=py
    goto :install_websocket
)

:: Python not found
echo ❌ ERROR: Python not found in PATH!
echo.
echo 🔍 Searching for Python installations...

:: Check common Python installation paths
set PYTHON_FOUND=0

for %%p in (
    "C:\Python*\python.exe"
    "C:\Program Files\Python*\python.exe"
    "C:\Program Files (x86)\Python*\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
    "%APPDATA%\Local\Programs\Python\Python*\python.exe"
) do (
    for /f "delims=" %%f in ('dir "%%p" /b /s 2^>nul') do (
        echo 🔍 Found Python at: %%f
        set PYTHON_FOUND=1
        set PYTHON_PATH=%%f
    )
)

if %PYTHON_FOUND%==1 (
    echo.
    echo ✅ Python is installed but not in PATH!
    echo.
    echo 💡 QUICK FIX - Adding to PATH temporarily...
    for %%f in ("%PYTHON_PATH%") do set PYTHON_DIR=%%~dpf
    set PATH=%PYTHON_DIR%;%PYTHON_DIR%Scripts;%PATH%
    set PYTHON_CMD=python
    echo ✅ Python added to PATH for this session
    goto :install_websocket
)

echo.
echo ❌ Python is not installed on this system!
echo.
echo 🚀 AUTO-DOWNLOAD PYTHON:
echo.
choice /c YN /m "Do you want to download Python automatically? (Y/N)"
if errorlevel 2 goto :manual_install
if errorlevel 1 goto :auto_download

:auto_download
echo.
echo [2/4] Downloading Python...
echo 🔄 Downloading Python 3.12 installer...

:: Download Python installer
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile '%TEMP%\python-installer.exe'}"

if not exist "%TEMP%\python-installer.exe" (
    echo ❌ Download failed! Using manual method...
    goto :manual_install
)

echo ✅ Download completed!
echo.
echo [3/4] Installing Python...
echo 🔄 Running Python installer...
echo.
echo ⚠️  IMPORTANT: During installation:
echo    ✅ CHECK "Add Python to PATH"
echo    ✅ CHECK "Install for all users" (if prompted)
echo.
pause

:: Run installer with automatic PATH addition
"%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

echo.
echo ✅ Python installation completed!
echo 🔄 Reloading environment...

:: Refresh environment variables
call :refresh_env

:: Test Python again
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python still not accessible. Please restart this installer.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python is now available: %PYTHON_VERSION%
set PYTHON_CMD=python
goto :install_websocket

:manual_install
echo.
echo 📋 MANUAL PYTHON INSTALLATION:
echo.
echo 1. 🌐 Open: https://python.org/downloads
echo 2. 📥 Download "Python 3.12" (latest version)
echo 3. 🖱️  Run the installer
echo 4. ✅ IMPORTANT: Check "Add Python to PATH"
echo 5. 🔄 Restart your computer after installation
echo 6. 🚀 Run this installer again
echo.
echo 💡 Alternative: Run this installer as Administrator for auto-install
echo.
pause
exit /b 1

:install_websocket
echo.
echo [3/4] Installing websocket-client package...

if not defined PYTHON_CMD set PYTHON_CMD=python

:: Method 1: User install with py launcher
echo 🔄 Attempting installation with %PYTHON_CMD%...
%PYTHON_CMD% -m pip install websocket-client --user --upgrade --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS: Installation completed
    goto :test
)

:: Method 2: System install
echo 🔄 Attempting system installation...
%PYTHON_CMD% -m pip install websocket-client --upgrade --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS: System installation completed
    goto :test
)

:: Method 3: Force install
echo 🔄 Attempting force installation...
%PYTHON_CMD% -m pip install websocket-client --user --force-reinstall --quiet
if %errorlevel% == 0 (
    echo ✅ SUCCESS: Force installation completed
    goto :test
)

echo ❌ ERROR: Package installation failed!
goto :test

:test
echo.
echo [4/4] Testing installation...
%PYTHON_CMD% -c "import websocket; print('✅ websocket-client is working!')" 2>nul
if %errorlevel% == 0 (
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
    echo 🎉 Remote control should now work perfectly!
    echo.
) else (
    echo ❌ ERROR: Installation completed but import test failed
    echo.
    echo 💡 SOLUTION:
    echo    1. Restart Fusion 360 completely
    echo    2. Restart your computer
    echo    3. Try running this installer as Administrator
    echo.
)

pause
goto :end

:refresh_env
:: Refresh environment variables without restart
for /f "usebackq tokens=2,*" %%A in (`reg query HKCU\Environment /v PATH 2^>nul`) do set UserPath=%%B
for /f "usebackq tokens=2,*" %%A in (`reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH 2^>nul`) do set SystemPath=%%B
set PATH=%SystemPath%;%UserPath%
exit /b

:end

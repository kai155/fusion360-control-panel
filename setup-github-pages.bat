@echo off
echo ========================================
echo   FUSION 360 HTML CONTROL PANEL
echo   GitHub Pages Auto Setup
echo ========================================
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)

echo ✅ Git detected

REM Get user input
set /p USERNAME="Enter your GitHub username: "
set /p REPONAME="Enter repository name (default: fusion360-control-panel): "

if "%REPONAME%"=="" set REPONAME=fusion360-control-panel

echo.
echo 📋 Setup Information:
echo Username: %USERNAME%
echo Repository: %REPONAME%
echo URL will be: https://%USERNAME%.github.io/%REPONAME%/online-index.html
echo.

set /p CONFIRM="Continue? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo ❌ Setup cancelled
    pause
    exit /b 0
)

echo.
echo 🚀 Starting setup...

REM Create a temporary directory for the repo
set TEMP_DIR=%TEMP%\%REPONAME%
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"

REM Copy files to temp directory
echo 📁 Copying files...
copy "commands\paletteShow\resources\html\online-index.html" "%TEMP_DIR%\" >nul
copy "README-ONLINE.md" "%TEMP_DIR%\README.md" >nul

REM Create .gitignore
echo node_modules/ > "%TEMP_DIR%\.gitignore"
echo .DS_Store >> "%TEMP_DIR%\.gitignore"
echo *.log >> "%TEMP_DIR%\.gitignore"

REM Change to temp directory
cd /d "%TEMP_DIR%"

REM Git operations
echo 🔧 Initializing Git...
git init
git add .
git commit -m "Add Fusion 360 HTML Control Panel"
git branch -M main

echo.
echo 📤 Ready to push to GitHub!
echo.
echo ⚠️  IMPORTANT: You need to create the repository on GitHub first!
echo 1. Go to https://github.com/new
echo 2. Repository name: %REPONAME%
echo 3. Make it PUBLIC
echo 4. Don't initialize with README
echo 5. Click "Create repository"
echo.

set /p CREATED="Have you created the repository on GitHub? (y/n): "
if /i not "%CREATED%"=="y" (
    echo ❌ Please create the repository first, then run this script again
    pause
    exit /b 0
)

echo 🚀 Pushing to GitHub...
git remote add origin https://github.com/%USERNAME%/%REPONAME%.git
git push -u origin main

if errorlevel 1 (
    echo ❌ Failed to push to GitHub
    echo Please check:
    echo - Repository exists and is public
    echo - You have push access
    echo - Username/repository name are correct
    pause
    exit /b 1
)

echo.
echo ✅ Files uploaded successfully!
echo.
echo 📋 Next steps:
echo 1. Go to https://github.com/%USERNAME%/%REPONAME%/settings/pages
echo 2. Source: Deploy from a branch
echo 3. Branch: main
echo 4. Folder: / (root)
echo 5. Click Save
echo.
echo 🌐 Your URL will be: https://%USERNAME%.github.io/%REPONAME%/online-index.html
echo.

REM Update entry.py
echo 🔧 Updating entry.py...
cd /d "%~dp0"

powershell -Command "(Get-Content 'commands\paletteShow\entry.py') -replace 'https://your-username\.github\.io/[^/]+/online-index\.html', 'https://%USERNAME%.github.io/%REPONAME%/online-index.html' | Set-Content 'commands\paletteShow\entry.py'"

echo ✅ entry.py updated with your GitHub Pages URL
echo.
echo 🎉 Setup complete!
echo Wait 1-2 minutes for GitHub Pages to deploy, then restart your Fusion 360 add-in.

REM Cleanup
rmdir /s /q "%TEMP_DIR%"

pause

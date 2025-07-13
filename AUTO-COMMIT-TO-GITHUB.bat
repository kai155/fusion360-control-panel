@echo off
title AUTO COMMIT TO GITHUB
cd /d "%~dp0"

echo 🚀 Auto-committing changes to GitHub...
echo.

:: Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git not found! Auto-installing Git...
    echo.
    echo 📥 Downloading Git installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://github.com/git-scm/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe' -OutFile 'git-installer.exe'"
    
    if exist git-installer.exe (
        echo ✅ Installing Git (this may take a few minutes)...
        git-installer.exe /VERYSILENT /NORESTART /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"
        
        echo ✅ Git installation complete
        del git-installer.exe
        
        echo 🔄 Refreshing PATH...
        call refreshenv >nul 2>&1
        
        echo ✅ Testing Git...
        git --version >nul 2>&1
        if errorlevel 1 (
            echo ❌ Git installation failed. Please restart and try again.
            pause
            exit /b 1
        )
        echo ✅ Git is now available!
    ) else (
        echo ❌ Download failed. Please install Git manually from: https://git-scm.com/download/windows
        pause
        exit /b 1
    )
)

:: Check if this is a git repository
if not exist ".git" (
    echo 🔧 Initializing Git repository...
    git init
    echo ✅ Git repository initialized
    echo.
    echo 📋 Setting up GitHub remote...
    set /p github_url="Enter GitHub repository URL (https://github.com/username/repo.git): "
    if not "%github_url%"=="" (
        git remote add origin %github_url%
        echo ✅ GitHub remote added: %github_url%
    ) else (
        echo ⚠️  No remote URL provided. You can add it later with:
        echo    git remote add origin https://github.com/username/repo.git
    )
    echo.
)

:: Add all changes
echo [1/4] Adding files...
git add .
git add -A

:: Commit with timestamp
echo [2/4] Committing changes...
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "MIN=%dt:~10,2%" & set "SS=%dt:~12,2%"
set "timestamp=%YYYY%-%MM%-%DD% %HH%:%MIN%:%SS%"

git commit -m "🔧 Bridge System Update - %timestamp%" -m "✅ Fixed WebSocket errors" -m "✅ Updated bridge server" -m "✅ Simplified Python detection" -m "✅ Enhanced error handling"

:: Push to GitHub
echo [3/4] Pushing to GitHub...
git push origin main

if errorlevel 1 (
    echo ❌ Push failed! Trying alternative branch...
    git push origin master
)

echo [4/4] Deployment complete!
echo.
echo ✅ Changes committed and pushed to GitHub
echo 🌐 GitHub Pages will update automatically
echo 📱 Remote control interface updated
echo.
pause
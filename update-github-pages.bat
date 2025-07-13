@echo off
echo 🔄 UPDATING GITHUB PAGES WITH FIXED REMOTE CONTROL
echo ==============================================
echo.

:: Copy updated files to GitHub Pages
echo 📁 Copying files to GitHub repository...
xcopy /Y "commands\paletteShow\resources\html\remote-control.html" "c:\Users\Admin\AppData\Local\Temp\fusion360-control-panel\"

echo.
echo 📝 GitHub Pages files updated with:
echo ✅ Fixed WebSocket client registration (browser_client type)
echo ✅ Improved command handling 
echo ✅ Better error messages
echo ✅ Vietnamese interface text
echo.
echo 🚀 Now commit and push via GitHub Desktop to deploy fixes!
echo 🌐 URL: https://kai155.github.io/fusion360-control-panel/remote-control.html
echo.
pause

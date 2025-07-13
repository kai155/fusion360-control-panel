@echo off
title FUSION 360 REMOTE CONTROL - COMPLETE SETUP
cls

echo.
echo =====================================================
echo    🚀 FUSION 360 REMOTE CONTROL SETUP
echo =====================================================
echo.

echo [STEP 1/3] Starting Bridge Server...
echo.
start "Bridge Server" python bridge_server.py
timeout 3 >nul

echo ✅ Bridge server started on port 8766
echo.

echo [STEP 2/3] Opening Web Interface...
start http://localhost:8766
timeout 2 >nul

echo ✅ Web interface opened
echo.

echo [STEP 3/3] LOAD FUSION 360 ADD-IN:
echo.
echo 📋 Manual steps required:
echo    1. Open Fusion 360
echo    2. Go to UTILITIES → ADD-INS
echo    3. Find "HTLM" in the list
echo    4. Click "RUN" button
echo    5. You should see: "Bridge Control Started!"
echo.

echo ⚠️  IMPORTANT: You MUST load the add-in in Fusion 360!
echo    The web interface alone is not enough.
echo    The add-in reads commands from fusion_commands.json
echo.

echo 🎯 Test sequence:
echo    1. Load add-in in Fusion 360 (see steps above)
echo    2. In web browser, click "Connect to Bridge"  
echo    3. Click "Create Box" button
echo    4. You should see a box appear in Fusion 360
echo.

echo =====================================================
echo    🔗 WEB INTERFACE: http://localhost:8766
echo    📁 FUSION ADD-IN: UTILITIES → ADD-INS → HTLM → RUN
echo =====================================================
echo.

pause

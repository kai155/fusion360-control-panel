# 🤖 AUTO-SETUP FUSION 360 WEBSOCKET
# =====================================

Write-Host "🤖 FUSION 360 WEBSOCKET AUTO-SETUP" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install websocket-client
Write-Host "📦 Step 1: Installing websocket-client..." -ForegroundColor Yellow
try {
    $result = python -m pip install websocket-client --user --upgrade --quiet 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ websocket-client installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Installation failed, trying alternatives..." -ForegroundColor Red
        pip install websocket-client --user --upgrade --quiet
        if ($LASTEXITCODE -ne 0) {
            py -m pip install websocket-client --user --upgrade --quiet
        }
    }
} catch {
    Write-Host "❌ Package installation failed: $_" -ForegroundColor Red
    Read-Host "Press Enter to continue anyway"
}

Write-Host ""

# Step 2: Stop Fusion 360 if running
Write-Host "🛑 Step 2: Stopping Fusion 360 processes..." -ForegroundColor Yellow
try {
    Get-Process -Name "Fusion360" -ErrorAction SilentlyContinue | Stop-Process -Force
    Get-Process -Name "FusionLauncher" -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 2
    Write-Host "✅ Fusion 360 processes stopped" -ForegroundColor Green
} catch {
    Write-Host "⚠️ No Fusion 360 processes to stop" -ForegroundColor Yellow
}

# Step 3: Start WebSocket Server
Write-Host "🌐 Step 3: Starting WebSocket server..." -ForegroundColor Yellow
try {
    $serverPath = Join-Path $PWD "debug_server.py"
    if (Test-Path $serverPath) {
        Start-Process python -ArgumentList "debug_server.py" -WindowStyle Normal
        Start-Sleep -Seconds 2
        Write-Host "✅ WebSocket server started" -ForegroundColor Green
    } else {
        Write-Host "❌ WebSocket server script not found" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Failed to start WebSocket server: $_" -ForegroundColor Red
}

# Step 4: Start Fusion 360
Write-Host "🚀 Step 4: Starting Fusion 360..." -ForegroundColor Yellow
try {
    # Try to find Fusion 360 executable
    $fusion360Paths = @(
        "$env:LOCALAPPDATA\Autodesk\webdeploy\production\*\Fusion360.exe",
        "${env:ProgramFiles}\Autodesk\Fusion 360\Fusion360.exe",
        "${env:ProgramFiles(x86)}\Autodesk\Fusion 360\Fusion360.exe"
    )
    
    $fusion360Found = $false
    foreach ($path in $fusion360Paths) {
        $executable = Get-ChildItem -Path $path -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($executable) {
            Start-Process $executable.FullName
            Write-Host "✅ Fusion 360 started: $($executable.FullName)" -ForegroundColor Green
            $fusion360Found = $true
            break
        }
    }
    
    if (-not $fusion360Found) {
        # Try starting from Start Menu
        Start-Process "fusion360:" -ErrorAction SilentlyContinue
        Write-Host "⚠️ Attempted to start Fusion 360 via protocol" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "❌ Could not start Fusion 360 automatically: $_" -ForegroundColor Red
    Write-Host "💡 Please start Fusion 360 manually" -ForegroundColor Blue
}

# Step 5: Wait and open browser
Write-Host "⏳ Step 5: Waiting for Fusion 360 to load..." -ForegroundColor Yellow
Start-Sleep -Seconds 8

Write-Host "🌐 Step 6: Opening browser interface..." -ForegroundColor Yellow
try {
    Start-Process "https://kai155.github.io/fusion360-control-panel/remote-control.html"
    Write-Host "✅ Browser interface opened" -ForegroundColor Green
} catch {
    Write-Host "❌ Failed to open browser" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎯 AUTO-SETUP COMPLETE!" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "1. In Fusion 360: UTILITIES → ADD-INS → HTLM → Run" -ForegroundColor White
Write-Host "2. Look for popup: '🌐 Remote Control Connected!'" -ForegroundColor White
Write-Host "3. In browser: Click 'Connect to Fusion 360'" -ForegroundColor White
Write-Host "4. Test: Click 'Create Box' button" -ForegroundColor White
Write-Host ""
Write-Host "🎉 Everything should work now!" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to close"

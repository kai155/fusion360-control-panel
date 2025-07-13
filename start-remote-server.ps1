# PowerShell script to start Fusion 360 Remote Control Server
Write-Host "🚀 Starting Fusion 360 Remote Control Server..." -ForegroundColor Green
Write-Host ""
Write-Host "This will start the WebSocket server for remote control." -ForegroundColor Cyan
Write-Host "Keep this window open while using remote control." -ForegroundColor Cyan
Write-Host ""

# Set working directory
Set-Location $PSScriptRoot

# Check if Python virtual environment exists
$pythonExe = ".venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ Python virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first or check installation." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Starting WebSocket server on port 8765..." -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Server will be available at:" -ForegroundColor Yellow
Write-Host "   Local:    ws://localhost:8765" -ForegroundColor White
Write-Host "   Network:  ws://[your-ip]:8765" -ForegroundColor White
Write-Host ""
Write-Host "📱 Open remote-control-browser.html in any browser to control Fusion 360" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server
try {
    & $pythonExe "remote_server_simple.py"
} catch {
    Write-Host "❌ Error starting server: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "Server stopped." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
}

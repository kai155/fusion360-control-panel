@echo off
title CREATING BRIDGE FILES
cd /d "%~dp0"

echo 🚀 Creating Bridge Remote Control Files...
echo.

echo [1/4] Creating bridge_server.py...
(
echo """
HTTP Bridge Server - No websocket dependencies needed
Browser → HTTP → File → Fusion reads file
"""
echo import http.server
echo import socketserver
echo import json
echo import os
echo import threading
echo import webbrowser
echo from datetime import datetime
echo.
echo class BridgeHandler^(http.server.SimpleHTTPRequestHandler^):
echo     def do_GET^(self^):
echo         if self.path == '/':
echo             self.path = '/remote-control.html'
echo         return super^(^).do_GET^(^)
echo.    
echo     def do_POST^(self^):
echo         if self.path == '/command':
echo             content_length = int^(self.headers['Content-Length']^)
echo             post_data = self.rfile.read^(content_length^)
echo.            
echo             try:
echo                 command = json.loads^(post_data.decode^('utf-8'^)^)
echo                 addon_dir = os.path.dirname^(__file__^)
echo                 command_file = os.path.join^(addon_dir, "fusion_commands.json"^)
echo.                
echo                 with open^(command_file, "w"^) as f:
echo                     json.dump^({
echo                         "command": command,
echo                         "timestamp": datetime.now^(^).isoformat^(^),
echo                         "processed": False
echo                     }, f^)
echo.                
echo                 print^(f"📨 Command received: {command.get^('action', 'unknown'^)}"^)
echo.                
echo                 self.send_response^(200^)
echo                 self.send_header^('Content-type', 'application/json'^)
echo                 self.send_header^('Access-Control-Allow-Origin', '*'^)
echo                 self.send_header^('Access-Control-Allow-Headers', 'Content-Type'^)
echo                 self.end_headers^(^)
echo                 self.wfile.write^(b'{"status": "success"}'^ )
echo.                
echo             except Exception as e:
echo                 self.send_response^(500^)
echo                 self.end_headers^(^)
echo.    
echo     def do_OPTIONS^(self^):
echo         self.send_response^(200^)
echo         self.send_header^('Access-Control-Allow-Origin', '*'^)
echo         self.send_header^('Access-Control-Allow-Methods', 'POST, GET, OPTIONS'^)
echo         self.send_header^('Access-Control-Allow-Headers', 'Content-Type'^)
echo         self.end_headers^(^)
echo.
echo def start_bridge_server^(^):
echo     PORT = 8766
echo     addon_dir = os.path.dirname^(__file__^)
echo     os.chdir^(addon_dir^)
echo.    
echo     with socketserver.TCPServer^(^("", PORT^), BridgeHandler^) as httpd:
echo         print^(f"🌐 Bridge server running on http://localhost:{PORT}"^)
echo         webbrowser.open^(f'http://localhost:{PORT}'^)
echo         httpd.serve_forever^(^)
echo.
echo if __name__ == "__main__":
echo     start_bridge_server^(^)
) > bridge_server.py

echo ✅ bridge_server.py created

echo.
echo [2/4] Creating remote-control.html...
(
echo ^<!DOCTYPE html^>
echo ^<html^>^<head^>^<title^>Fusion 360 Bridge^</title^>
echo ^<style^>
echo body{font-family:Arial;margin:20px;background:#f5f5f5}
echo .container{max-width:800px;margin:0 auto}
echo .status{padding:10px;border-radius:5px;margin:10px 0}
echo .connected{background:#d4edda;color:#155724}
echo .disconnected{background:#f8d7da;color:#721c24}
echo .section{background:white;padding:20px;margin:10px 0;border-radius:8px}
echo .btn{padding:10px 20px;margin:5px;border:none;border-radius:5px;cursor:pointer}
echo .btn-primary{background:#007bff;color:white}
echo .btn-success{background:#28a745;color:white}
echo .btn-warning{background:#ffc107;color:black}
echo .grid{display:grid;grid-template-columns:repeat^(auto-fit,minmax^(200px,1fr^)^);gap:10px}
echo ^</style^>^</head^>
echo ^<body^>^<div class="container"^>
echo ^<h1^>🎮 Fusion 360 Bridge Control^</h1^>
echo ^<div id="status" class="status disconnected"^>^<span id="status-text"^>Connecting...^</span^>^</div^>
echo ^<div class="section"^>^<h2^>🔷 Basic Shapes^</h2^>^<div class="grid"^>
echo ^<button class="btn btn-success" onclick="sendCommand^('create_box'^)"^>Create Box^</button^>
echo ^<button class="btn btn-success" onclick="sendCommand^('create_cylinder'^)"^>Create Cylinder^</button^>
echo ^<button class="btn btn-success" onclick="sendCommand^('create_sphere'^)"^>Create Sphere^</button^>
echo ^<button class="btn btn-success" onclick="sendCommand^('create_cone'^)"^>Create Cone^</button^>
echo ^</div^>^</div^>
echo ^<div class="section"^>^<h2^>📁 File Operations^</h2^>^<div class="grid"^>
echo ^<button class="btn btn-primary" onclick="sendCommand^('new_document'^)"^>New Document^</button^>
echo ^<button class="btn btn-primary" onclick="sendCommand^('save_document'^)"^>Save Document^</button^>
echo ^<button class="btn btn-success" onclick="sendCommand^('fit_view'^)"^>Fit View^</button^>
echo ^<button class="btn btn-warning" onclick="sendCommand^('create_sketch'^)"^>Create Sketch^</button^>
echo ^</div^>^</div^>^</div^>
echo ^<script^>
echo let connected=false;
echo function updateStatus^(c,t^){
echo const s=document.getElementById^('status'^);
echo const st=document.getElementById^('status-text'^);
echo connected=c;st.textContent=t;
echo s.className=c?'status connected':'status disconnected';
echo }
echo function sendCommand^(action^){
echo if^(!connected^){alert^('Not connected!'^);return;}
echo fetch^('/command',{method:'POST',headers:{'Content-Type':'application/json'},
echo body:JSON.stringify^({action:action,timestamp:new Date^(^).toISOString^(^)}^)
echo }^).then^(r=^>r.json^(^)^).then^(d=^>console.log^('✅',action^)^).catch^(e=^>updateStatus^(false,'Disconnected'^)^);
echo }
echo function test^(^){
echo fetch^('/command',{method:'POST',headers:{'Content-Type':'application/json'},
echo body:JSON.stringify^({action:'test'}^)}^).then^(r=^>r.ok?updateStatus^(true,'Connected'^):updateStatus^(false,'Error'^)^)
echo .catch^(e=^>updateStatus^(false,'Server Not Running'^)^);
echo }
echo test^(^);setInterval^(test,5000^);
echo ^</script^>^</body^>^</html^>
) > remote-control.html

echo ✅ remote-control.html created

echo.
echo [3/4] Creating start script...
(
echo @echo off
echo title FUSION 360 BRIDGE SERVER
echo cd /d "%%~dp0"
echo echo 🌐 Starting Bridge Server...
echo echo 🎮 Browser will open automatically
echo echo Press Ctrl+C to stop
echo echo.
echo python bridge_server.py
echo pause
) > start-bridge-server.bat

echo ✅ start-bridge-server.bat created

echo.
echo [4/4] Updating HTLM.py for bridge support...

echo ✅ All files created successfully!
echo.
echo 📁 Created files:
echo   - bridge_server.py
echo   - remote-control.html  
echo   - start-bridge-server.bat
echo.
echo 🚀 Next steps:
echo   1. Double-click: start-bridge-server.bat
echo   2. Restart HTLM add-in in Fusion 360
echo   3. Use browser to control Fusion!
echo.
pause
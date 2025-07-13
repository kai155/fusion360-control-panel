#!/usr/bin/env python3
"""
Fusion 360 Bridge Server
HTTP server that receives commands from web browser and writes to file for Fusion 360 to read
"""

import http.server
import socketserver
import json
import os
import webbrowser
import threading
import time
from urllib.parse import urlparse, parse_qs

PORT = 8766
COMMAND_FILE = "fusion_commands.json"

class BridgeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            # Serve the remote control interface
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Read and serve the bridge control HTML
            try:
                with open('bridge-control.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                # Fallback simple interface
                html = '''<!DOCTYPE html>
<html>
<head><title>🎮 Fusion 360 Bridge Server</title></head>
<body>
<h1>🚀 Bridge Server Running!</h1>
<p>Port: 8766</p>
<p>Status: ✅ Online</p>
<script>
function sendCommand(action) {
    fetch('/command', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: action, timestamp: new Date().toISOString()})
    }).then(r => r.json()).then(d => console.log('✅', action));
}
</script>
<button onclick="sendCommand('create_box')">📦 Create Box</button>
<button onclick="sendCommand('save_document')">💾 Save</button>
</body>
</html>'''
                self.wfile.write(html.encode('utf-8'))
        else:
            # Serve static files
            super().do_GET()

    def do_POST(self):
        """Handle POST requests for commands"""
        if self.path == '/command':
            # Handle command from web interface
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                command = json.loads(post_data.decode('utf-8'))
                
                # Write command to file for Fusion 360 to read
                self.write_command_file(command)
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "status": "success",
                    "action": command.get('action', 'unknown'),
                    "timestamp": command.get('timestamp', time.time()),
                    "message": f"Command '{command.get('action')}' sent to Fusion 360"
                }
                
                self.wfile.write(json.dumps(response).encode('utf-8'))
                print(f"✅ Command received: {command.get('action')}")
                
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
            except Exception as e:
                self.send_error(500, f"Server error: {str(e)}")
        else:
            self.send_error(404, "Not Found")

    def do_OPTIONS(self):
        """Handle preflight requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def write_command_file(self, command):
        """Write command to file for Fusion 360 to read"""
        try:
            # Format compatible with HTLM.py
            fusion_command = {
                "timestamp": command.get('timestamp', time.time()),
                "processed": False,
                "command": {
                    "action": command.get('action'),
                    "data": command
                }
            }
            
            with open(COMMAND_FILE, 'w', encoding='utf-8') as f:
                json.dump(fusion_command, f, indent=2)
            print(f"📝 Command written to {COMMAND_FILE}: {command.get('action')}")
        except Exception as e:
            print(f"❌ Error writing command file: {e}")

def start_server():
    """Start the HTTP bridge server"""
    print("🚀 Starting Fusion 360 Bridge Server...")
    print(f"📡 Port: {PORT}")
    print(f"📄 Command file: {COMMAND_FILE}")
    print("="*50)
    
    try:
        with socketserver.TCPServer(("", PORT), BridgeHandler) as httpd:
            print(f"✅ Bridge server running at http://localhost:{PORT}")
            print("🌐 Web interface available at http://localhost:{PORT}")
            print("📱 Remote control ready!")
            print("="*50)
            print("💡 Next steps:")
            print("1. Open Fusion 360")
            print("2. Load HTLM add-in (UTILITIES → ADD-INS)")
            print("3. Control via web browser")
            print("="*50)
            
            # Auto-open browser
            def open_browser():
                time.sleep(1)
                try:
                    webbrowser.open(f'http://localhost:{PORT}')
                    print("🌐 Browser opened automatically")
                except:
                    print("⚠️  Couldn't open browser automatically")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Start server
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"❌ Port {PORT} is already in use!")
            print("💡 Try closing other instances or use a different port")
        else:
            print(f"❌ Server error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    start_server()

"""
Fusion 360 Remote Control Server
WebSocket server to bridge web browsers with Fusion 360
"""

import asyncio
import websockets
import json
import threading
import time
from datetime import datetime

class Fusion360RemoteServer:
    def __init__(self, port=8765):
        self.port = port
        self.clients = set()  # Web browsers
        self.fusion_client = None  # Fusion 360 add-in
        self.command_queue = []
        self.response_queue = []
        
    async def register_client(self, websocket, path):
        """Register new client (browser or Fusion 360)"""
        self.clients.add(websocket)
        print(f"📱 New client connected: {websocket.remote_address}")
        
        try:
            # Send welcome message
            await websocket.send(json.dumps({
                "type": "welcome",
                "message": "Connected to Fusion 360 Remote Server",
                "timestamp": datetime.now().isoformat()
            }))
            
            # Handle messages
            async for message in websocket:
                await self.handle_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
            if websocket == self.fusion_client:
                self.fusion_client = None
                print("🔌 Fusion 360 disconnected")
            print(f"👋 Client disconnected: {websocket.remote_address}")
    
    async def handle_message(self, websocket, message):
        """Handle incoming messages"""
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            
            if msg_type == "register_fusion":
                # Fusion 360 add-in registering
                self.fusion_client = websocket
                print("🎯 Fusion 360 connected!")
                
                # Notify all browsers
                await self.broadcast_to_browsers({
                    "type": "fusion_status",
                    "connected": True,
                    "message": "Fusion 360 is now connected"
                })
                
            elif msg_type == "command" and self.fusion_client:
                # Browser sending command to Fusion
                print(f"📤 Command: {data.get('action')}")
                await self.fusion_client.send(message)
                
            elif msg_type == "response":
                # Fusion sending response to browsers
                print(f"📥 Response: {data.get('result', '')[:50]}...")
                await self.broadcast_to_browsers(data)
                
            elif msg_type == "ping":
                # Keep-alive
                await websocket.send(json.dumps({"type": "pong"}))
                
        except Exception as e:
            print(f"❌ Error handling message: {e}")
    
    async def broadcast_to_browsers(self, data):
        """Send data to all browser clients"""
        if not self.clients:
            return
            
        # Send to all clients except Fusion 360
        browser_clients = [c for c in self.clients if c != self.fusion_client]
        
        if browser_clients:
            message = json.dumps(data)
            await asyncio.gather(
                *[client.send(message) for client in browser_clients],
                return_exceptions=True
            )
    
    async def start_server(self):
        """Start the WebSocket server"""
        print("🚀 Starting Fusion 360 Remote Server...")
        print(f"🌐 Server will run on: ws://localhost:{self.port}")
        print("📋 Instructions:")
        print("1. Start this server")
        print("2. Open Fusion 360 with the add-in")
        print("3. Access web interface from any browser")
        print("\n⚡ Server starting...\n")
        
        # Start WebSocket server
        async with websockets.serve(
            self.register_client, 
            "0.0.0.0",  # Accept connections from anywhere
            self.port
        ) as server:
            print(f"✅ Server running on ws://localhost:{self.port}")
            print("🌐 Server accessible from:")
            print(f"   - Local: ws://localhost:{self.port}")
            print(f"   - Network: ws://0.0.0.0:{self.port}")
            print("\n💡 Open remote-control-browser.html to start controlling!")
            print("🛑 Press Ctrl+C to stop server\n")
            
            # Keep server running
            await server.wait_closed()

if __name__ == "__main__":
    server = Fusion360RemoteServer(port=8765)
    
    try:
        # Run the async server
        asyncio.run(server.start_server())
    except KeyboardInterrupt:
        print("\n👋 Server shutting down...")
    except Exception as e:
        print(f"❌ Server error: {e}")
        input("Press Enter to exit...")

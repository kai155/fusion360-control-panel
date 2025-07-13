#!/usr/bin/env python3
"""
Debug and start WebSocket server for Fusion 360 remote control
"""
import asyncio
import websockets
import json
import logging
import sys
import os
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Store connected clients
clients = set()
fusion_clients = set()
browser_clients = set()

async def handle_client(websocket):
    """Handle new WebSocket client connection"""
    client_ip = websocket.remote_address[0] if websocket.remote_address else "unknown"
    logger.info(f"🔗 New client connected from {client_ip}")
    
    clients.add(websocket)
    
    try:
        # Send welcome message
        await websocket.send(json.dumps({
            "type": "welcome",
            "message": "Connected to Fusion 360 Remote Control Server",
            "timestamp": datetime.now().isoformat(),
            "server_status": "running"
        }))
        
        async for message in websocket:
            try:
                logger.info(f"📨 Received: {message}")
                data = json.loads(message)
                
                # Identify client type
                if data.get("type") == "fusion_client":
                    fusion_clients.add(websocket)
                    logger.info(f"✅ Fusion 360 client registered from {client_ip}")
                    await broadcast_to_browsers({
                        "type": "fusion_status", 
                        "status": "connected",
                        "message": "Fusion 360 connected"
                    })
                    
                elif data.get("type") == "browser_client":
                    browser_clients.add(websocket)
                    logger.info(f"🌐 Browser client registered from {client_ip}")
                    
                    # Send current Fusion status
                    fusion_connected = len(fusion_clients) > 0
                    await websocket.send(json.dumps({
                        "type": "fusion_status",
                        "status": "connected" if fusion_connected else "disconnected",
                        "message": f"Fusion 360 {'connected' if fusion_connected else 'not connected'}"
                    }))
                    
                elif data.get("type") == "command":
                    # Forward command to Fusion 360
                    logger.info(f"🎮 Forwarding command: {data.get('action')}")
                    await broadcast_to_fusion(data)
                    
                elif data.get("type") == "response":
                    # Forward response to browsers
                    logger.info(f"📤 Forwarding response: {data.get('status')}")
                    await broadcast_to_browsers(data)
                    
                else:
                    logger.warning(f"❓ Unknown message type: {data.get('type')}")
                    
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON decode error: {e}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                logger.error(f"❌ Message handling error: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"🔌 Client {client_ip} disconnected")
    except Exception as e:
        logger.error(f"❌ Client error: {e}")
    finally:
        # Cleanup
        clients.discard(websocket)
        fusion_clients.discard(websocket)
        browser_clients.discard(websocket)
        
        # Notify browsers if Fusion disconnected
        if websocket in fusion_clients:
            await broadcast_to_browsers({
                "type": "fusion_status",
                "status": "disconnected", 
                "message": "Fusion 360 disconnected"
            })

async def broadcast_to_fusion(data):
    """Send data to all Fusion 360 clients"""
    if fusion_clients:
        disconnected = []
        for client in fusion_clients.copy():
            try:
                await client.send(json.dumps(data))
            except:
                disconnected.append(client)
        
        # Remove disconnected clients
        for client in disconnected:
            fusion_clients.discard(client)
            clients.discard(client)

async def broadcast_to_browsers(data):
    """Send data to all browser clients"""
    if browser_clients:
        disconnected = []
        for client in browser_clients.copy():
            try:
                await client.send(json.dumps(data))
            except:
                disconnected.append(client)
        
        # Remove disconnected clients
        for client in disconnected:
            browser_clients.discard(client)
            clients.discard(client)

async def main():
    """Start the WebSocket server"""
    host = "localhost"
    port = 8765
    
    print("🚀 FUSION 360 REMOTE CONTROL SERVER")
    print("=" * 40)
    print(f"🌐 Starting WebSocket server on {host}:{port}")
    print(f"🔗 Browser interface: https://kai155.github.io/fusion360-control-panel/remote-control.html")
    print(f"📱 Local test: file://{os.path.abspath('commands/paletteShow/resources/html/remote-control.html')}")
    print("=" * 40)
    
    try:
        async with websockets.serve(handle_client, host, port):
            print(f"✅ WebSocket server running on ws://{host}:{port}")
            print("📡 Waiting for connections...")
            print("⚡ Press Ctrl+C to stop")
            print()
            
            # Keep the server running
            await asyncio.Future()  # Run forever
            
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use!")
            print("💡 Try: netstat -ano | findstr :8765")
            print("💡 Then: taskkill /PID <PID> /F")
        else:
            print(f"❌ Server error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        input("Press Enter to exit...")

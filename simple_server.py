#!/usr/bin/env python3
"""
Ultra Simple WebSocket Server for Fusion 360 Remote Control
Fixed compatibility with all websockets versions
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store connected clients
clients = set()
fusion_client = None

async def handler(websocket):
    """Handle WebSocket connections - modern websockets syntax"""
    global clients, fusion_client
    
    # Add client to set
    clients.add(websocket)
    client_addr = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    logger.info(f"📱 Client connected: {client_addr}")
    
    try:
        # Send welcome message
        welcome = {
            "type": "welcome",
            "message": "Connected to Fusion 360 Server",
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send(json.dumps(welcome))
        
        # Handle messages
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type', 'command')
                
                logger.info(f"📨 Received: {msg_type} from {client_addr}")
                
                if msg_type == 'register':
                    client_type = data.get('client_type', 'browser')
                    if client_type == 'fusion360':
                        fusion_client = websocket
                        logger.info(f"🎯 Fusion 360 registered: {client_addr}")
                        
                        # Notify browsers that Fusion 360 is connected
                        fusion_status = {
                            "type": "fusion_status",
                            "connected": True,
                            "message": "Fusion 360 connected"
                        }
                        await broadcast_to_browsers(fusion_status)
                    else:
                        logger.info(f"🌐 Browser registered: {client_addr}")
                
                elif msg_type == 'command':
                    # Forward command to Fusion 360
                    if fusion_client and fusion_client in clients:
                        await fusion_client.send(message)
                        logger.info(f"➡️ Command forwarded to Fusion 360")
                        
                        # Send confirmation to browser
                        response = {
                            "type": "response",
                            "success": True,
                            "message": "Command sent to Fusion 360"
                        }
                        await websocket.send(json.dumps(response))
                    else:
                        # No Fusion 360 connected
                        error_response = {
                            "type": "error",
                            "message": "Fusion 360 not connected"
                        }
                        await websocket.send(json.dumps(error_response))
                        
            except json.JSONDecodeError:
                logger.error(f"❌ Invalid JSON from {client_addr}")
            except Exception as e:
                logger.error(f"❌ Message error: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"🔌 Client disconnected: {client_addr}")
    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
    finally:
        # Clean up
        clients.discard(websocket)
        if websocket == fusion_client:
            fusion_client = None
            logger.info("🎯 Fusion 360 disconnected")
            
            # Notify browsers
            fusion_status = {
                "type": "fusion_status", 
                "connected": False,
                "message": "Fusion 360 disconnected"
            }
            await broadcast_to_browsers(fusion_status)

async def broadcast_to_browsers(message):
    """Send message to all browser clients"""
    if not clients:
        return
        
    # Send to all clients except Fusion 360
    browser_clients = [client for client in clients if client != fusion_client]
    if browser_clients:
        await asyncio.gather(
            *[client.send(json.dumps(message)) for client in browser_clients],
            return_exceptions=True
        )

async def main():
    """Start the WebSocket server"""
    host = "localhost"
    port = 8765
    
    logger.info("🚀 Starting Fusion 360 Remote Server...")
    logger.info(f"🌐 Server will run on: ws://{host}:{port}")
    
    try:
        # Start server with modern websockets syntax
        async with websockets.serve(handler, host, port):
            logger.info(f"✅ Server running on ws://{host}:{port}")
            logger.info("🌐 Server accessible from:")
            logger.info(f"   - Local: ws://{host}:{port}")
            logger.info(f"   - Network: ws://0.0.0.0:{port}")
            logger.info("")
            logger.info("💡 Open remote-control-browser.html to start controlling!")
            logger.info("🛑 Press Ctrl+C to stop server")
            logger.info("")
            
            # Keep server running
            await asyncio.Future()  # Run forever
            
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Fatal error: {e}")

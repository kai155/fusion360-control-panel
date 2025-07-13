"""
Ultra Simple WebSocket Server for Fusion 360 Remote Control
Compatible with all websockets versions
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Store connected clients
clients = set()
fusion_client = None

async def handle_client(websocket):
    """Handle each WebSocket connection - modern syntax"""
    global clients, fusion_client
    
    # Add client to set
    clients.add(websocket)
    try:
        client_addr = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    except:
        client_addr = "unknown"
    
    logger.info(f"📱 Client connected: {client_addr}")
    
    try:
        # Send welcome message
        welcome_msg = {
            "type": "welcome",
            "message": "Connected to Fusion 360 Remote Server",
            "timestamp": datetime.now().isoformat(),
            "server_info": "Fusion 360 WebSocket Bridge v2.0"
        }
        await websocket.send(json.dumps(welcome_msg))
        
        # Listen for messages
        async for message in websocket:
            try:
                data = json.loads(message)
                msg_type = data.get('type', 'unknown')
                
                logger.info(f"📨 Message from {client_addr}: {msg_type}")
                
                if msg_type == 'register':
                    client_type = data.get('client_type', 'browser')
                    if client_type == 'fusion360':
                        fusion_client = websocket
                        logger.info(f"🎯 Fusion 360 client registered: {client_addr}")
                        
                        # Notify all browsers
                        await broadcast_to_browsers({
                            "type": "fusion_connected",
                            "message": "Fusion 360 is now connected and ready"
                        })
                    else:
                        logger.info(f"🌐 Browser client registered: {client_addr}")
                
                elif msg_type == 'command':
                    # Forward command to Fusion 360
                    if fusion_client and fusion_client in clients:
                        try:
                            await fusion_client.send(message)
                            logger.info(f"🚀 Command forwarded: {data.get('command', 'unknown')}")
                            
                            # Send confirmation back to browser
                            if websocket != fusion_client:
                                await websocket.send(json.dumps({
                                    "type": "command_sent",
                                    "message": f"Command '{data.get('command')}' sent to Fusion 360"
                                }))
                        except Exception as e:
                            logger.error(f"❌ Failed to forward command: {e}")
                            await websocket.send(json.dumps({
                                "type": "error",
                                "message": "Failed to send command to Fusion 360"
                            }))
                    else:
                        logger.warning("⚠️ No Fusion 360 client connected")
                        await websocket.send(json.dumps({
                            "type": "error",
                            "message": "Fusion 360 not connected. Please start Fusion 360 with the add-in."
                        }))
                
                elif msg_type == 'response':
                    # Forward response to browsers
                    await broadcast_to_browsers(data)
                
                else:
                    logger.warning(f"❓ Unknown message type: {msg_type}")
                    
            except json.JSONDecodeError:
                logger.error(f"❌ Invalid JSON from {client_addr}")
            except Exception as e:
                logger.error(f"❌ Error handling message: {e}")
                
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"🔌 Client disconnected: {client_addr}")
    except Exception as e:
        logger.error(f"❌ Connection error: {e}")
    finally:
        # Remove client from set
        clients.discard(websocket)
        if websocket == fusion_client:
            fusion_client = None
            logger.info("🔌 Fusion 360 disconnected")
            
            # Notify remaining browsers
            await broadcast_to_browsers({
                "type": "fusion_disconnected",
                "message": "Fusion 360 disconnected"
            })

async def broadcast_to_browsers(message):
    """Send message to all browser clients"""
    if not clients:
        return
        
    # Send to all clients except Fusion 360
    browser_clients = [client for client in clients if client != fusion_client]
    if browser_clients:
        tasks = []
        for client in browser_clients:
            try:
                tasks.append(client.send(json.dumps(message)))
            except:
                pass
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    """Main server function"""
    port = 8765
    host = "localhost"
    
    logger.info("🚀 Starting Fusion 360 Remote Server...")
    logger.info(f"🌐 Server will run on: ws://{host}:{port}")
    logger.info("📋 Instructions:")
    logger.info("1. Start this server")
    logger.info("2. Open Fusion 360 with the add-in")
    logger.info("3. Access web interface from any browser")
    logger.info("\n⚡ Server starting...\n")
    
    try:
        # Start WebSocket server with modern syntax
        async with websockets.serve(handle_client, host, port):
            logger.info(f"✅ Server running on ws://{host}:{port}")
            logger.info("🌐 Server accessible from:")
            logger.info(f"   - Local: ws://{host}:{port}")
            logger.info(f"   - Network: ws://0.0.0.0:{port}")
            logger.info("")
            logger.info("💡 Open remote-control-browser.html to start controlling!")
            logger.info("🛑 Press Ctrl+C to stop server")
            logger.info("")
            
            # Keep server running forever
            await asyncio.Future()  # Run forever
            
    except KeyboardInterrupt:
        logger.info("👋 Server shutting down gracefully...")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        raise

if __name__ == "__main__":
    try:
        # Run the server
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server shutting down gracefully...")
    except Exception as e:
        print(f"❌ Server error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

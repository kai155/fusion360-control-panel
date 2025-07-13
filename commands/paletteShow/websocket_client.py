"""
Fusion 360 WebSocket Client for Add-in
Connects the Fusion 360 add-in to the remote server
"""

import adsk.core
import json
import threading
import time
import websocket

class Fusion360WebSocketClient:
    def __init__(self, server_url="ws://localhost:8765"):
        self.server_url = server_url
        self.ws = None
        self.connected = False
        self.message_handler = None
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        
    def set_message_handler(self, handler):
        """Set the function to handle incoming commands"""
        self.message_handler = handler
    
    def connect(self):
        """Connect to the WebSocket server"""
        try:
            def on_open(ws):
                self.connected = True
                print("🌐 Connected to remote server")
                
                # Register as Fusion 360 client
                register_msg = {
                    "type": "register_fusion",
                    "message": "Fusion 360 add-in connected",
                    "timestamp": time.time()
                }
                ws.send(json.dumps(register_msg))
            
            def on_message(ws, message):
                try:
                    data = json.loads(message)
                    if data.get("type") == "command" and self.message_handler:
                        # Handle command from web browser
                        result = self.message_handler(data)
                        
                        # Send response back
                        response = {
                            "type": "response",
                            "action": data.get("action"),
                            "result": result,
                            "timestamp": time.time()
                        }
                        ws.send(json.dumps(response))
                        
                except Exception as e:
                    print(f"❌ Error handling message: {e}")
            
            def on_error(ws, error):
                print(f"❌ WebSocket error: {error}")
                self.connected = False
            
            def on_close(ws, close_status_code, close_msg):
                print("🔌 Disconnected from remote server")
                self.connected = False
            
            # Create WebSocket connection
            self.ws = websocket.WebSocketApp(
                self.server_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            
            # Run in separate thread
            def run_websocket():
                self.ws.run_forever()
            
            thread = threading.Thread(target=run_websocket, daemon=True)
            thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        if self.ws:
            self.ws.close()
            self.connected = False
    
    def send_message(self, message):
        """Send message to server"""
        if self.connected and self.ws:
            self.ws.send(json.dumps(message))
    
    def is_connected(self):
        """Check if connected to server"""
        return self.connected

# Global WebSocket client instance
websocket_client = None

def start_remote_connection():
    """Start the remote connection"""
    global websocket_client
    
    if websocket_client and websocket_client.is_connected():
        return "Already connected to remote server"
    
    try:
        websocket_client = Fusion360WebSocketClient()
        
        # Set the message handler (this will be the palette_incoming function)
        def handle_remote_command(data):
            """Handle commands from remote browsers"""
            try:
                # Create a mock HTML args object
                class MockHTMLArgs:
                    def __init__(self, action, data_dict):
                        self.action = action
                        self.data = json.dumps(data_dict)
                        self.returnData = ""
                
                # Import the palette_incoming function
                from . import entry
                
                # Create mock args
                mock_args = MockHTMLArgs(data.get("action"), data.get("data", {}))
                
                # Call the existing palette handler
                entry.palette_incoming(mock_args)
                
                return mock_args.returnData
                
            except Exception as e:
                return f"Error executing command: {str(e)}"
        
        websocket_client.set_message_handler(handle_remote_command)
        
        if websocket_client.connect():
            return "✅ Connected to remote server successfully!"
        else:
            return "❌ Failed to connect to remote server"
            
    except Exception as e:
        return f"❌ Error starting remote connection: {str(e)}"

def stop_remote_connection():
    """Stop the remote connection"""
    global websocket_client
    
    if websocket_client:
        websocket_client.disconnect()
        websocket_client = None
        return "Disconnected from remote server"
    else:
        return "Not connected to remote server"

def get_remote_connection_status():
    """Get current connection status"""
    global websocket_client
    
    if websocket_client and websocket_client.is_connected():
        return "Connected to remote server"
    else:
        return "Not connected to remote server"

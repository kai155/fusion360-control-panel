import websocket
import json
import time

def test_connection():
    print("🔍 Testing WebSocket connection to server...")
    
    def on_message(ws, message):
        print(f"📨 Received: {message}")
    
    def on_error(ws, error):
        print(f"❌ Error: {error}")
    
    def on_close(ws, close_status_code, close_msg):
        print("🔌 Connection closed")
    
    def on_open(ws):
        print("✅ Connected to server!")
        # Test browser registration
        ws.send(json.dumps({
            "type": "register", 
            "client_type": "browser"
        }))
        
        # Wait a bit then send test command
        time.sleep(1)
        ws.send(json.dumps({
            "type": "command",
            "command": "create_box"
        }))
        
        # Close after test
        time.sleep(2)
        ws.close()
    
    try:
        ws = websocket.WebSocketApp("ws://localhost:8765",
                                  on_open=on_open,
                                  on_message=on_message, 
                                  on_error=on_error,
                                  on_close=on_close)
        ws.run_forever()
        print("✅ Connection test completed")
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
    input("Press Enter to exit...")

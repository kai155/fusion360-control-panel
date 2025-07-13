#!/usr/bin/env python3
"""
Install websocket-client for Fusion 360 add-in
"""
import subprocess
import sys
import os

def install_websocket():
    """Install websocket-client package"""
    print("🔧 INSTALLING WEBSOCKET CLIENT")
    print("=" * 30)
    
    try:
        # Check if already installed
        import websocket
        print("✅ websocket-client is already installed!")
        return True
    except ImportError:
        print("❌ websocket-client not found, installing...")
    
    try:
        # Install package
        print(f"📍 Using Python: {sys.executable}")
        
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "websocket-client", "--user", "--upgrade"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Installation successful!")
            print("\n🔄 Please restart Fusion 360 to use the WebSocket client")
            return True
        else:
            print(f"❌ Installation failed:")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False

def test_websocket():
    """Test websocket connection"""
    try:
        import websocket
        print("\n🧪 Testing WebSocket connection...")
        
        # Create a simple test connection
        def on_open(ws):
            print("✅ WebSocket test connection successful!")
            ws.close()
            
        def on_error(ws, error):
            print(f"❌ WebSocket test error: {error}")
            
        # Quick connection test
        ws = websocket.WebSocketApp("ws://echo.websocket.org/",
                                  on_open=on_open,
                                  on_error=on_error)
        
        # Test with timeout
        import threading
        import time
        
        def run_test():
            ws.run_forever()
            
        test_thread = threading.Thread(target=run_test, daemon=True)
        test_thread.start()
        test_thread.join(timeout=5)
        
        return True
        
    except Exception as e:
        print(f"❌ WebSocket test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 FUSION 360 WEBSOCKET SETUP")
    print("=" * 40)
    
    if install_websocket():
        test_websocket()
        print("\n🎉 Setup complete!")
        print("\n📋 Next steps:")
        print("1. Restart Fusion 360")
        print("2. Start WebSocket server (start-debug-server.bat)")
        print("3. Add-in will auto-connect to server")
    else:
        print("\n❌ Setup failed!")
        print("\n💡 Try:")
        print("1. Run as Administrator")
        print("2. Install Python from python.org")
        print("3. Run: pip install websocket-client")
    
    input("\nPress Enter to close...")

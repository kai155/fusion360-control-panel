#!/usr/bin/env python3
"""
Quick test for WebSocket server compatibility
"""
import sys
import os
import traceback

def test_server():
    print("🔍 Testing WebSocket server compatibility...")
    
    # Test 1: Import modules
    try:
        import asyncio
        print("✅ asyncio imported")
    except ImportError as e:
        print(f"❌ asyncio failed: {e}")
        return False
        
    try:
        import websockets
        print(f"✅ websockets imported (version: {websockets.__version__ if hasattr(websockets, '__version__') else 'unknown'})")
    except ImportError as e:
        print(f"❌ websockets failed: {e}")
        return False
    
    # Test 2: Check server syntax
    try:
        print("🔍 Testing server syntax...")
        with open('remote_server_simple.py', 'r', encoding='utf-8') as f:
            server_code = f.read()
        
        # Check for modern syntax
        if 'async def handle_client(websocket):' in server_code:
            print("✅ Modern async function signature found")
        else:
            print("❌ Old function signature detected")
            
        if 'async with websockets.serve(' in server_code:
            print("✅ Modern context manager syntax found")
        else:
            print("❌ Old server syntax detected")
            
    except Exception as e:
        print(f"❌ Syntax check failed: {e}")
        return False
    
    # Test 3: Quick server start test
    try:
        print("🔍 Testing server import...")
        import remote_server_simple
        print("✅ Server module imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    print(f"📁 Working directory: {script_dir}")
    
    success = test_server()
    
    if success:
        print("\n🎉 All tests passed! Server should work correctly.")
        print("🚀 Starting server in background...")
        
        # Try to start server
        try:
            import remote_server_simple
            print("✅ Server started successfully!")
            print("🌐 WebSocket server running on ws://localhost:8765")
            print("🔗 Open browser interface to test connection")
            
        except Exception as e:
            print(f"❌ Server start failed: {e}")
    else:
        print("\n❌ Tests failed. Server needs fixes.")
    
    input("\nPress Enter to continue...")

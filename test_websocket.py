import websockets
import asyncio
import sys

print("🔍 Testing WebSocket server setup...")
print(f"Python version: {sys.version}")
print(f"AsyncIO version: {asyncio.__version__ if hasattr(asyncio, '__version__') else 'Built-in'}")
print(f"WebSockets version: {websockets.__version__}")

async def test_server():
    print("✅ Creating test server...")
    
    async def handle_test(websocket, path):
        print(f"📱 Test connection from: {websocket.remote_address}")
        await websocket.send("Hello Test!")
    
    server = await websockets.serve(handle_test, "localhost", 8765)
    print("✅ Test server created successfully!")
    print("🛑 Stopping test server...")
    server.close()
    await server.wait_closed()
    print("✅ Test completed - WebSocket setup is working!")

if __name__ == "__main__":
    try:
        asyncio.run(test_server())
        print("\n🎉 SUCCESS: WebSocket server can be started!")
        print("✅ You can now run the remote control server")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to continue...")

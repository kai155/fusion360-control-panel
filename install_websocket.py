import sys
import subprocess

def install_websocket_client():
    """Install websocket-client package for Fusion 360"""
    try:
        import websocket
        print("✅ websocket-client already installed")
        return True
    except ImportError:
        print("❌ websocket-client not found, installing...")
        
        try:
            # Get Fusion 360's Python executable
            python_exe = sys.executable
            print(f"📍 Using Python: {python_exe}")
            
            # Install websocket-client
            result = subprocess.run([
                python_exe, "-m", "pip", "install", "websocket-client"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ websocket-client installed successfully!")
                return True
            else:
                print(f"❌ Installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False

if __name__ == "__main__":
    install_websocket_client()

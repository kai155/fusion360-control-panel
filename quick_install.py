#!/usr/bin/env python3
"""
Quick WebSocket client installer - runs from add-in directory
"""
import subprocess
import sys
import os

def quick_install():
    print("🔧 QUICK WEBSOCKET INSTALLER")
    print("=" * 30)
    print(f"📍 Working from: {os.getcwd()}")
    print(f"🐍 Python: {sys.executable}")
    print()
    
    # Test import first
    try:
        import websocket
        print("✅ websocket-client already installed!")
        print("🎉 The add-in should work now")
        return True
    except ImportError:
        print("❌ websocket-client not found, installing...")
    
    # Install methods
    methods = [
        ([sys.executable, "-m", "pip", "install", "websocket-client", "--user", "--upgrade"], "python -m pip"),
        (["pip", "install", "websocket-client", "--user", "--upgrade"], "pip direct"),
        (["py", "-m", "pip", "install", "websocket-client", "--user", "--upgrade"], "py launcher"),
    ]
    
    for cmd, name in methods:
        try:
            print(f"🔄 Trying {name}...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ Success with {name}!")
                
                # Test import
                try:
                    import websocket
                    print("✅ Import test passed!")
                    print("🎉 Installation complete!")
                    return True
                except ImportError:
                    print("⚠️ Install OK but import failed - may need restart")
                    return True
            else:
                print(f"❌ {name} failed: {result.stderr.strip()[:50]}")
                
        except FileNotFoundError:
            print(f"❌ {name} command not found")
        except Exception as e:
            print(f"❌ {name} error: {e}")
    
    print("❌ All installation methods failed!")
    return False

def main():
    success = quick_install()
    
    print("\n" + "=" * 30)
    if success:
        print("🎉 INSTALLATION SUCCESSFUL!")
        print("\n📋 Next steps:")
        print("1. In Fusion 360: UTILITIES → ADD-INS")
        print("2. Find HTLM → Stop → Run")
        print("3. Look for: '🌐 Remote Control Connected!'")
    else:
        print("❌ INSTALLATION FAILED!")
        print("\n💡 Try:")
        print("1. Run as Administrator")
        print("2. Install Python from python.org")
        print("3. Restart computer")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")

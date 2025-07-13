#!/usr/bin/env python3
"""
Websocket Client Installer for Fusion 360 Add-in
Fixes the "WebSocket not available!" error
"""
import subprocess
import sys
import os

def check_python():
    """Check Python installation"""
    print(f"🐍 Python version: {sys.version}")
    print(f"📍 Python executable: {sys.executable}")
    return True

def test_websocket_import():
    """Test if websocket-client can be imported"""
    try:
        import websocket
        print("✅ websocket-client is available")
        print(f"📦 Version: {getattr(websocket, '__version__', 'unknown')}")
        return True
    except ImportError as e:
        print(f"❌ websocket-client not available: {e}")
        return False

def install_websocket_client():
    """Install websocket-client using multiple methods"""
    print("📦 Installing websocket-client...")
    
    commands = [
        [sys.executable, "-m", "pip", "install", "websocket-client", "--user", "--upgrade"],
        [sys.executable, "-m", "pip", "install", "websocket-client", "--upgrade", "--force-reinstall"],
        ["pip", "install", "websocket-client", "--user", "--upgrade"],
        ["py", "-m", "pip", "install", "websocket-client", "--user", "--upgrade"],
    ]
    
    for i, cmd in enumerate(commands, 1):
        try:
            print(f"\n🔄 Method {i}: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print(f"✅ Success with method {i}!")
                print("📝 Output:", result.stdout.strip())
                return True
            else:
                print(f"❌ Failed with method {i}")
                print("📝 Error:", result.stderr.strip())
                
        except FileNotFoundError:
            print(f"❌ Command not found: {cmd[0]}")
        except subprocess.TimeoutExpired:
            print(f"❌ Timeout with method {i}")
        except Exception as e:
            print(f"❌ Error with method {i}: {e}")
    
    return False

def main():
    print("🔧 WEBSOCKET CLIENT INSTALLER FOR FUSION 360")
    print("=" * 45)
    print()
    
    # Check Python
    check_python()
    print()
    
    # Check current status
    print("🔍 Checking current websocket-client status...")
    if test_websocket_import():
        print("\n🎉 websocket-client is already working!")
        print("✅ The 'WebSocket not available!' error should be fixed")
        print("\n📋 Next steps:")
        print("1. Restart Fusion 360 completely")
        print("2. Enable HTLM add-in: UTILITIES → ADD-INS → HTLM → Run")
        print("3. Should see '🌐 Remote Control Connected!' popup")
    else:
        print("\n📦 websocket-client needs to be installed...")
        
        if install_websocket_client():
            print("\n🎉 Installation completed!")
            
            # Test again
            print("\n🧪 Testing installation...")
            if test_websocket_import():
                print("✅ Installation verified successfully!")
                print("✅ The 'WebSocket not available!' error is now fixed")
            else:
                print("⚠️ Installation may need system restart")
                
            print("\n📋 Next steps:")
            print("1. Restart Fusion 360 completely")
            print("2. Enable HTLM add-in: UTILITIES → ADD-INS → HTLM → Run")
            print("3. Should see '🌐 Remote Control Connected!' popup")
            
        else:
            print("\n❌ All installation methods failed!")
            print("\n💡 Manual solutions:")
            print("1. Run this script as Administrator")
            print("2. Install Python from https://python.org (check 'Add to PATH')")
            print("3. Open Command Prompt as Admin and run:")
            print("   pip install websocket-client")
    
    print("\n" + "=" * 45)
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        print("💡 Try running as Administrator")
        input("Press Enter to exit...")

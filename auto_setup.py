#!/usr/bin/env python3
"""
Automatic setup for Fusion 360 WebSocket remote control
- Installs websocket-client
- Starts WebSocket server
- Opens browser interface
"""
import subprocess
import sys
import os
import time
import webbrowser
import threading

def install_packages():
    """Install required packages"""
    print("📦 Installing websocket-client...")
    
    packages = ["websocket-client"]
    
    for package in packages:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", package, "--user", "--upgrade"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
    
    return True

def start_websocket_server():
    """Start WebSocket server in background"""
    try:
        print("🌐 Starting WebSocket server...")
        
        # Start server in background
        server_process = subprocess.Popen([
            sys.executable, "debug_server.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Give server time to start
        time.sleep(3)
        
        # Check if server is running
        if server_process.poll() is None:
            print("✅ WebSocket server started successfully")
            return server_process
        else:
            print("❌ WebSocket server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Server start error: {e}")
        return None

def open_browser_interface():
    """Open browser interface"""
    try:
        print("🌐 Opening browser interface...")
        url = "https://kai155.github.io/fusion360-control-panel/remote-control.html"
        webbrowser.open(url)
        print(f"✅ Browser opened: {url}")
        return True
    except Exception as e:
        print(f"❌ Browser open error: {e}")
        return False

def show_instructions():
    """Show user instructions"""
    print("\n" + "="*50)
    print("🎯 FUSION 360 SETUP COMPLETE!")
    print("="*50)
    print()
    print("📋 Next steps:")
    print("1. In Fusion 360:")
    print("   → UTILITIES → ADD-INS")
    print("   → Find 'HTLM' and click 'Run'")
    print("   → Look for popup: '🌐 Remote Control Connected!'")
    print()
    print("2. In Browser (should auto-open):")
    print("   → Click 'Connect to Fusion 360'")
    print("   → Try 'Create Box' button")
    print()
    print("🎉 If you see 'Connected ✅' - everything works!")
    print("❌ If issues persist - restart Fusion 360 completely")
    print()

def main():
    """Main setup function"""
    print("🤖 FUSION 360 WEBSOCKET AUTO-SETUP")
    print("="*40)
    print()
    
    # Step 1: Install packages
    if not install_packages():
        print("❌ Package installation failed")
        input("Press Enter to exit...")
        return
    
    # Step 2: Start WebSocket server
    server_process = start_websocket_server()
    if not server_process:
        print("❌ Server startup failed")
        input("Press Enter to exit...")
        return
    
    # Step 3: Open browser
    open_browser_interface()
    
    # Step 4: Show instructions
    show_instructions()
    
    # Keep server running
    try:
        print("⚡ Server running... Press Ctrl+C to stop")
        server_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        server_process.terminate()
        print("👋 Goodbye!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        input("Press Enter to exit...")

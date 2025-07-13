"""
Install websocket-client directly to Fusion 360's Python environment
This script should be run INSIDE Fusion 360 (as a script)
"""
import sys
import subprocess
import os
import adsk.core

def install_to_fusion_python():
    """Install websocket-client to Fusion 360's Python environment"""
    
    app = adsk.core.Application.get()
    ui = app.userInterface
    
    try:
        ui.messageBox('🔍 Starting installation to Fusion Python environment...', 'Installing WebSocket')
        
        print("🔍 Fusion 360 Python Environment:")
        print(f"Python executable: {sys.executable}")
        print(f"Python version: {sys.version}")
        print(f"Python path: {sys.path}")
        
        # Try multiple installation methods
        success = False
        
        # Method 1: Direct pip install
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "websocket-client", "--user", "--upgrade"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ Method 1 SUCCESS: User installation")
                success = True
            else:
                print(f"❌ Method 1 failed: {result.stderr}")
        except Exception as e:
            print(f"❌ Method 1 exception: {e}")
        
        # Method 2: System install (if method 1 failed)
        if not success:
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "websocket-client", "--upgrade"
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print("✅ Method 2 SUCCESS: System installation")
                    success = True
                else:
                    print(f"❌ Method 2 failed: {result.stderr}")
            except Exception as e:
                print(f"❌ Method 2 exception: {e}")
        
        # Method 3: Force reinstall
        if not success:
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "websocket-client", "--force-reinstall"
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    print("✅ Method 3 SUCCESS: Force installation")
                    success = True
                else:
                    print(f"❌ Method 3 failed: {result.stderr}")
            except Exception as e:
                print(f"❌ Method 3 exception: {e}")
        
        # Test import
        try:
            import websocket
            print("✅ Import test successful!")
            ui.messageBox('✅ SUCCESS!\n\nwebsocket-client installed successfully!\n\nNow restart the HTLM add-in:\n1. Stop add-in\n2. Run add-in\n3. Look for "🌐 Remote Control Connected!"', 'Installation Complete')
            return True
        except ImportError as e:
            print(f"❌ Import test failed: {e}")
            ui.messageBox(f'❌ Installation failed!\n\nImport error: {str(e)}\n\nTry running PYTHON-INSTALLER.bat as Administrator', 'Installation Failed')
            return False
            
    except Exception as e:
        print(f"❌ Installation error: {e}")
        ui.messageBox(f'❌ Installation error!\n\n{str(e)}\n\nTry manual installation', 'Error')
        return False

def run(context):
    """Main function - called when script is run in Fusion 360"""
    install_to_fusion_python()
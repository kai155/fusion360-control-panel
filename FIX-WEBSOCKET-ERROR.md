# 🔧 WEBSOCKET CLIENT INSTALLATION

## ❌ Error Message:
```
WebSocket not available!
Please install: pip install websocket-client
```

## ✅ SOLUTION - 3 Easy Methods:

### Method 1: Double-Click Install (Easiest)
```
🖱️ Double-click: install-websocket-client.bat
```
- Automatically finds Python and installs package
- Run as Administrator if permission issues

### Method 2: Python Setup Script
```
🖱️ Double-click: setup-websocket.py  
```
- Installs websocket-client with testing
- Shows detailed installation status

### Method 3: Manual Command Line
```cmd
pip install websocket-client --user --upgrade
```
Or try:
```cmd
python -m pip install websocket-client --user
py -m pip install websocket-client --user
pip3 install websocket-client --user
```

## 🔄 After Installation:

1. **Close Fusion 360** completely
2. **Restart Fusion 360**
3. **Enable add-in**: UTILITIES → ADD-INS → HTLM → Run
4. **Start server**: Double-click `start-debug-server.bat`
5. **Test**: Add-in should show "🌐 Remote Control Connected!"

## 💡 Troubleshooting:

### Python Not Found?
- Install from: https://www.python.org/downloads/
- ✅ Check "Add Python to PATH" during installation

### Still Getting Permission Errors?
- Run Command Prompt as Administrator:
  ```cmd
  Right-click Command Prompt → "Run as administrator"
  pip install websocket-client
  ```

### Alternative: Use Conda
```cmd
conda install websocket-client
```

---

## 🎯 Expected Success:
- ✅ No more "WebSocket not available" error
- ✅ Add-in connects automatically to server  
- ✅ Browser commands work properly
- ✅ Popup: "🌐 Remote Control Connected!"

**After installing websocket-client, everything will work automatically!** 🚀

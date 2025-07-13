# 🤖 AUTO-SETUP - WEBSOCKET CONNECTION

## ✅ AUTOMATED SOLUTION:

### 🖱️ One-Click Setup (Recommended):
```
Double-click: RUN-AUTO-SETUP.bat
```

**What it does automatically:**
- ✅ Installs websocket-client package
- ✅ Stops/restarts Fusion 360
- ✅ Starts WebSocket server
- ✅ Opens browser interface
- ✅ Shows step-by-step instructions

### 🎯 Alternative Auto-Scripts:

#### Option 2: Python Auto-Setup
```
Double-click: auto_setup.py
```
- More detailed logging
- Keeps server running
- Real-time status updates

#### Option 3: PowerShell Script
```
Right-click auto-setup.ps1 → "Run with PowerShell"
```
- Advanced Fusion 360 process management
- Better error handling

## 🔄 Manual Method (If Auto Fails):

### Method 1: Restart via Fusion 360 GUI
1. In Fusion 360 → **UTILITIES** → **ADD-INS**
2. Find **HTLM** add-in
3. Click **Stop** button
4. Wait 2 seconds
5. Click **Run** button
6. Add-in will reload with new WebSocket client code

### Method 2: Restart Fusion 360 (Recommended)
1. Close Fusion 360 completely
2. Restart Fusion 360
3. Add-in will auto-load with new code

## 🚀 Testing After Setup:

1. **WebSocket Server:** Should auto-start
2. **Browser Interface:** Should auto-open
3. **Add-in Connection:** Enable via UTILITIES → ADD-INS → HTLM → Run
4. **Test Commands:** Try "Create Box" button

## 🔍 Expected Results:
```
🚀 Starting WebSocket remote control client...
🔄 Connecting to WebSocket server (attempt 1/5)...
✅ WebSocket connection opened
```

## ❓ If Auto-Setup Fails:
1. Run as Administrator: Right-click → "Run as administrator"
2. Check Python installation: `python --version`
3. Manual install: `pip install websocket-client --user`
4. Restart Fusion 360 manually

---

**🎉 After auto-setup, everything should work automatically!**

---
title: Fusion 360 Remote Control
description: Control Autodesk Fusion 360 remotely from any web browser
---

# Fusion 360 Remote Control Add-in

🚀 **Remote control system for Autodesk Fusion 360**

## 📱 Live Demo
- **Bridge System**: [Remote Control Interface](https://kai155.github.io/fusion360-control-panel/remote-control.html)
- **WebSocket System**: [Browser Interface](https://kai155.github.io/fusion360-control-panel/remote-control-browser.html)

## 🔧 Setup Instructions

### 1. Download & Install
```bash
git clone https://github.com/kai155/fusion360-control-panel.git
cd fusion360-control-panel
```

### 2. Start Bridge Server
```bash
start-bridge-server.bat
```

### 3. Load Fusion 360 Add-in
1. Open Fusion 360
2. Go to **UTILITIES** → **ADD-INS**
3. Select **HTLM** → **Run**

## 🌐 How It Works

### Bridge System (Recommended)
```
Web Browser → HTTP POST → Local Server → File → Fusion 360
```

### WebSocket System
```
Web Browser ↔ WebSocket ↔ Local Server ↔ Fusion 360
```

## ✨ Features

- 🎯 **Zero Dependencies** - Bridge system requires no packages
- 📱 **Cross-Platform** - Works on mobile, tablet, desktop
- 🔄 **Real-time Control** - Instant command execution
- 🌐 **Remote Access** - Control from anywhere
- 🛡️ **Dual Architecture** - WebSocket + HTTP fallbacks

## 🚀 Available Commands

- **File Operations**: New, Save, Open, Close
- **View Controls**: Fit, Zoom, Home
- **Basic Shapes**: Box, Cylinder, Sphere, Cone  
- **Sketch Tools**: Line, Circle, Rectangle
- **3D Operations**: Extrude, Revolve, Sweep, Loft
- **Modify Tools**: Fillet, Chamfer, Shell, Delete

## 📦 Download

**[📥 Download Latest Release](https://github.com/kai155/fusion360-control-panel/archive/refs/heads/master.zip)**

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/kai155/fusion360-control-panel/issues)
- **Documentation**: [Complete Guide](https://github.com/kai155/fusion360-control-panel/blob/master/README.md)

---
*Made with ❤️ for the Fusion 360 community*

# 🚀 Fusion 360 Remote Control Add-in

**Dual-architecture remote control system for Autodesk Fusion 360 with WebSocket and HTTP Bridge technologies.**

## ✨ Features

- 🌐 **Remote Control** - Control Fusion 360 from any web browser
- 🔄 **Dual Architecture** - WebSocket + HTTP Bridge systems for maximum compatibility
- 📱 **Cross-Platform** - Works on desktop, mobile, and tablet browsers
- 🔧 **Auto-Installation** - Automated Python and dependency setup
- 🎯 **Zero Dependencies** - Bridge system requires no external packages
- 🚀 **GitHub Pages** - Deploy your control interface online

## 🎯 Quick Start

### Method 1: Bridge System (Recommended)
```bash
# Start the bridge server
start-bridge-server.bat
```

### Method 2: WebSocket System  
```bash
# Start the WebSocket server
start-remote-server.bat
```

### Method 3: Fusion 360 Add-in
1. Open Fusion 360
2. Go to **UTILITIES** → **ADD-INS** 
3. Select **HTLM** → **Run**

## 📱 Remote Control Interface

### Available Commands
- **Create Box** - Add primitive cube
- **Create Cylinder** - Add primitive cylinder  
- **Create Sphere** - Add primitive sphere
- **Sketch** - Start new sketch
- **Extrude** - Extrude selected profile
- **Revolve** - Revolve selected profile
- **Save** - Save current document
- **Undo/Redo** - Undo or redo last action

## 🔧 Architecture

### Bridge System
```
Browser → HTTP POST → bridge_server.py → fusion_commands.json → Fusion 360 API
```

### WebSocket System  
```
Browser ↔ WebSocket ↔ remote_server.py ↔ Fusion 360 API
```

## 🛠️ Installation

### Automatic Setup
```bash
# Complete auto-installation
AUTO-COMMIT-TO-GITHUB.bat

# Python + packages only
PYTHON-INSTALLER.bat

# Bridge files only
CREATE-BRIDGE-FILES.bat
```

### Manual Setup
1. Install Python 3.7+
2. Install websocket-client: `pip install websocket-client`
3. Run bridge server: `python bridge_server.py`
4. Open Fusion 360 and load the add-in

## 📦 Project Structure

```
HTLM/
├── HTLM.py                    # Main add-in entry point
├── bridge_server.py           # HTTP bridge server
├── remote_server.py           # WebSocket server
├── commands/paletteShow/      # Fusion 360 palette commands
├── remote-control.html        # Bridge system interface
├── remote-control-browser.html # WebSocket interface
└── start-bridge-server.bat    # Quick start script
```

## 🌐 Online Deployment

The add-in supports **GitHub Pages** for remote access:

1. Fork this repository
2. Enable GitHub Pages in repository settings
3. Update URLs in configuration files
4. Access from any device at: `https://username.github.io/fusion360-control-panel`

## 🔧 Configuration

### Local Mode
```python
USE_ONLINE_VERSION = False  # Use local HTML files
```

### Online Mode  
```python
USE_ONLINE_VERSION = True   # Use GitHub Pages URLs
```

### Server Ports
- **Bridge Server**: 8766
- **WebSocket Server**: 8765

## 🚨 Troubleshooting

### WebSocket Issues
- Use Bridge system instead (no dependencies required)
- Check `DEBUG-WEBSOCKET.md` for detailed solutions

### Python Issues  
- Run `PYTHON-INSTALLER.bat` for automatic setup
- Check `PYTHON-INSTALLATION-GUIDE.md`

### Connection Issues
- Ensure Fusion 360 add-in is running
- Check Windows firewall settings  
- Verify correct port numbers

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for Autodesk Fusion 360 API
- Uses WebSocket and HTTP technologies
- Inspired by remote CAD workflows

---

**⚡ Made with ❤️ for the Fusion 360 community**

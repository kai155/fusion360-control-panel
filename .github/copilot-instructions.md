# Fusion 360 Remote Control Add-in

## Project Architecture

This is a **dual-architecture** Fusion 360 add-in with both **WebSocket** and **HTTP Bridge** remote control systems.

### Core Components

- **`HTLM.py`** - Main add-in entry point with file-based bridge control
- **`commands/paletteShow/entry.py`** - Local HTML palette with Fusion 360 API integration  
- **`commands/paletteShow/resources/html/`** - Local control interface
- **`bridge_server.py`** - HTTP server for browser→file→Fusion communication
- **`remote_server.py`** - WebSocket server for real-time browser↔Fusion communication

### Communication Patterns

**Bridge System (Primary):**
```
Browser → HTTP POST → bridge_server.py → fusion_commands.json → watch_command_file() → Fusion 360 API
```

**WebSocket System (Legacy):**
```
Browser ↔ WebSocket ↔ remote_server.py ↔ websocket_client.py ↔ Fusion 360 API
```

**Local Palette:**
```
HTML/JS ↔ palette.sendInfoToHTML() ↔ entry.py ↔ Fusion 360 API
```

## Development Workflows

### Command Processing Pattern
All commands follow this structure in `palette_incoming()`:
```python
if action == "create_box":
    ui.commandDefinitions.itemById('PrimitiveCubeCommand').execute()
```

Use Fusion 360's built-in command IDs, not custom implementations.

### Adding New Commands
1. Add button to HTML interface (`remote-control.html` or `index.html`)
2. Add JavaScript function: `sendCommand('new_action')`  
3. Add handler in `process_bridge_command()` or `palette_incoming()`
4. Use Fusion's command ID: `ui.commandDefinitions.itemById('CommandId').execute()`

### Server Startup Sequence
1. **Bridge**: `start-bridge-server.bat` → `bridge_server.py` → Browser opens `remote-control.html`
2. **WebSocket**: `start-remote-server.bat` → `remote_server.py` → Browser opens `remote-control-browser.html`
3. **Add-in**: Fusion 360 → UTILITIES → ADD-INS → HTLM → Run → Starts file watcher

## Project-Specific Conventions

### File Organization
- `/commands/` - Fusion 360 palette commands (follows add-in template)
- Root level - Server scripts and HTML interfaces
- `/resources/html/` - Local palette interfaces only
- Auto-generated installers: `CREATE-BRIDGE-FILES.bat`, `PYTHON-INSTALLER.bat`

### Configuration
- **Online mode**: `USE_ONLINE_VERSION = True` uses GitHub Pages URLs
- **Local mode**: `USE_ONLINE_VERSION = False` uses local HTML files  
- **Bridge port**: 8766, **WebSocket port**: 8765

### Error Handling Strategy
Both systems have fallback behavior:
- WebSocket fails → Bridge system activates automatically
- Python missing → Auto-installers trigger (`PYTHON-INSTALLER.bat`)
- Package missing → Multiple installation methods attempt

### Integration Points

**Fusion 360 API**: All commands use official `ui.commandDefinitions.itemById()` pattern
**Browser Interface**: Multiple HTML files for different use cases:
- `index.html` - Local palette interface
- `remote-control.html` - Bridge system interface  
- `remote-control-browser.html` - WebSocket system interface

**File Watcher**: `watch_command_file()` polls `fusion_commands.json` every 300ms
**Package Management**: Multiple Python installation strategies for different environments

## Key Debugging Commands

```bash
# Start bridge system
start-bridge-server.bat

# Create all bridge files  
CREATE-BRIDGE-FILES.bat

# Install Python + packages
PYTHON-INSTALLER.bat

# Test WebSocket system
start-remote-server.bat
```

The add-in automatically detects which system is available and adapts accordingly.

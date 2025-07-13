# Assuming you have not changed the general structure of the template no modification is needed in this file.
from . import commands
from .lib import fusionAddInUtils as futil
import adsk.core, adsk.fusion, adsk.cam, traceback
import threading
import time
import json
import os


def run(context):
    try:
        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.start()
        
        # Start Bridge remote control (no websocket needed)
        start_bridge_control()

    except:
        futil.handle_error('run')


def stop(context):
    try:
        # Remove all of the event handlers your app has created
        futil.clear_handlers()

        # This will run the start function in each of your commands as defined in commands/__init__.py
        commands.stop()

    except:
        futil.handle_error('stop')


def start_bridge_control():
    """Start file-based bridge control - NO WebSocket"""
    try:
        # Start file watcher
        watcher_thread = threading.Thread(target=watch_command_file, daemon=True)
        watcher_thread.start()
        
        ui = adsk.core.Application.get().userInterface
        ui.messageBox('🌐 Bridge Control Started!\n\n✅ File-based bridge active\n✅ No WebSocket needed\n\n📋 Instructions:\n1. Run: start-bridge-server.bat\n2. Use browser interface\n3. Commands processed automatically', 'Bridge Control Active')
        
        futil.log("🚀 Bridge control started successfully")
        return True
        
    except Exception as e:
        futil.log(f"❌ Bridge control error: {e}")
        return False


def watch_command_file():
    """Watch for command file changes"""
    addon_dir = os.path.dirname(__file__)
    command_file = os.path.join(addon_dir, "fusion_commands.json")
    last_processed = ""
    
    futil.log("🔍 Bridge file watcher started")
    
    while True:
        try:
            if os.path.exists(command_file):
                with open(command_file, 'r') as f:
                    data = json.load(f)
                
                timestamp = data.get('timestamp', '')
                processed = data.get('processed', False)
                
                # Process new commands only
                if timestamp != last_processed and not processed:
                    command = data.get('command', {})
                    action = command.get('action')
                    
                    if action and action != 'test':
                        futil.log(f"📨 Bridge command: {action}")
                        process_bridge_command(action, command)
                        
                        # Mark as processed
                        data['processed'] = True
                        with open(command_file, 'w') as f:
                            json.dump(data, f)
                    
                    last_processed = timestamp
            
            time.sleep(0.3)  # Check every 300ms
            
        except Exception as e:
            futil.log(f"❌ Bridge watcher error: {e}")
            time.sleep(1)


def process_bridge_command(action, data):
    """Process commands from bridge server"""
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        if action == "create_box":
            ui.commandDefinitions.itemById('PrimitiveCubeCommand').execute()
        elif action == "create_cylinder":
            ui.commandDefinitions.itemById('PrimitiveCylinderCommand').execute()
        elif action == "create_sphere":
            ui.commandDefinitions.itemById('PrimitiveSphereCommand').execute()
        elif action == "create_cone":
            ui.commandDefinitions.itemById('PrimitiveConeCommand').execute()
        elif action == "new_document":
            ui.commandDefinitions.itemById('NewDesignCommand').execute()
        elif action == "save_document":
            ui.commandDefinitions.itemById('SaveCommand').execute()
        elif action == "fit_view":
            ui.commandDefinitions.itemById('FitViewCommand').execute()
        elif action == "create_sketch":
            ui.commandDefinitions.itemById('SketchCreateCommand').execute()
        
        futil.log(f"✅ Bridge command executed: {action}")
        
    except Exception as e:
        futil.log(f"❌ Bridge command error: {e}")


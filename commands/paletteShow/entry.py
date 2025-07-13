import json
import adsk.core
import adsk.fusion
import os
import webbrowser
from ...lib import fusionAddInUtils as futil
from ... import config
from datetime import datetime

app = adsk.core.Application.get()
ui = app.userInterface

# TODO ********************* Change these names *********************
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_PalleteShow'
CMD_NAME = 'Show My Palette'
CMD_Description = 'A Fusion Add-in Palette'
PALETTE_NAME = 'My Palette Sample'
IS_PROMOTED = False

# Using "global" variables by referencing values from /config.py
PALETTE_ID = config.sample_palette_id

# Configuration for online/local mode
USE_ONLINE_VERSION = True  # Set to False to use local files

if USE_ONLINE_VERSION:
    # GitHub Pages URL - kai155/fusion360-control-panel
    PALETTE_URL = 'https://kai155.github.io/fusion360-control-panel/online-index.html'
    REMOTE_CONTROL_URL = 'https://kai155.github.io/fusion360-control-panel/remote-control.html'
else:
    # Local file path
    PALETTE_URL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', 'html', 'index.html')
    REMOTE_CONTROL_URL = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'remote-control-browser.html')
    # The path function builds a valid OS path. This fixes it to be a valid local URL.
    PALETTE_URL = PALETTE_URL.replace('\\', '/')
    REMOTE_CONTROL_URL = REMOTE_CONTROL_URL.replace('\\', '/')

# Set a default docking behavior for the palette
PALETTE_DOCKING = adsk.core.PaletteDockingStates.PaletteDockStateRight

# TODO *** Define the location where the command button will be created. ***
# This is done by specifying the workspace, the tab, and the panel, and the 
# command it will be inserted beside. Not providing the command to position it
# will insert it at the end.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Add command created handler. The function passed here will be executed when the command is executed.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)
    palette = ui.palettes.itemById(PALETTE_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()

    # Delete the Palette
    if palette:
        palette.deleteMe()


# Event handler that is called when the user clicks the command button in the UI.
# To have a dialog, you create the desired command inputs here. If you don't need
# a dialog, don't create any inputs and the execute event will be immediately fired.
# You also need to connect to any command related events here.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Command created event.')

    # Create the event handlers you will need for this instance of the command
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


# Because no command inputs are being added in the command created event, the execute
# event is immediately fired.
def command_execute(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Command execute event.')

    palettes = ui.palettes
    palette = palettes.itemById(PALETTE_ID)
    if palette is None:
        palette = palettes.add(
            id=PALETTE_ID,
            name=PALETTE_NAME,
            htmlFileURL=PALETTE_URL,
            isVisible=True,
            showCloseButton=True,
            isResizable=True,
            width=650,
            height=600,
            useNewWebBrowser=True
        )
        futil.add_handler(palette.closed, palette_closed)
        futil.add_handler(palette.navigatingURL, palette_navigating)
        futil.add_handler(palette.incomingFromHTML, palette_incoming)
        futil.log(f'{CMD_NAME}: Created a new palette: ID = {palette.id}, Name = {palette.name}')
        
        # Send initial connection test to HTML
        try:
            palette.sendInfoToHTML("showStatus", "Connected to Fusion 360 successfully!")
        except:
            pass

    if palette.dockingState == adsk.core.PaletteDockingStates.PaletteDockStateFloating:
        palette.dockingState = PALETTE_DOCKING

    palette.isVisible = True


# Use this to handle a user closing your palette.
def palette_closed(args: adsk.core.UserInterfaceGeneralEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Palette was closed.')


# Use this to handle a user navigating to a new page in your palette.
def palette_navigating(args: adsk.core.NavigationEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Palette navigating event.')

    # Get the URL the user is navigating to:
    url = args.navigationURL

    log_msg = f"User is attempting to navigate to {url}\n"
    futil.log(log_msg, adsk.core.LogLevels.InfoLogLevel)

    # Check if url is an external site and open in user's default browser.
    if url.startswith("http"):
        args.launchExternally = True


# Use this to handle events sent from javascript in your palette.
def palette_incoming(html_args: adsk.core.HTMLEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Palette incoming event.')

    message_data: dict = json.loads(html_args.data)
    message_action = html_args.action

    log_msg = f"Event received from {html_args.firingEvent.sender.name}\n"
    log_msg += f"Action: {message_action}\n"
    log_msg += f"Data: {message_data}"
    futil.log(log_msg, adsk.core.LogLevels.InfoLogLevel)

    # Handle different commands from HTML interface
    try:
        result = "Command not implemented"
        
        if message_action == 'messageFromPalette':
            # Original sample functionality
            arg1 = message_data.get('arg1', 'arg1 not sent')
            arg2 = message_data.get('arg2', 'arg2 not sent')
            msg = 'An event has been fired from the html to Fusion with the following data:<br/>'
            msg += f'<b>Action</b>: {message_action}<br/><b>arg1</b>: {arg1}<br/><b>arg2</b>: {arg2}'               
            ui.messageBox(msg)
            result = "Message displayed successfully"
            
        elif message_action == 'createNewSketch':
            result = create_new_sketch()
            
        elif message_action == 'drawLine':
            result = draw_line()
            
        elif message_action == 'drawRectangle':
            result = draw_rectangle()
            
        elif message_action == 'drawCircle':
            result = draw_circle()
            
        elif message_action == 'finishSketch':
            result = finish_sketch()
            
        elif message_action == 'extrudeFeature':
            distance = message_data.get('data', {}).get('distance', 10)
            result = extrude_feature(distance)
            
        elif message_action == 'revolveFeature':
            result = revolve_feature()
            
        elif message_action == 'createBox':
            data = message_data.get('data', {})
            length = data.get('length', 20)
            width = data.get('width', 20)
            height = data.get('height', 20)
            result = create_box(length, width, height)
            
        elif message_action == 'createCylinder':
            data = message_data.get('data', {})
            radius = data.get('radius', 10)
            height = data.get('height', 20)
            result = create_cylinder(radius, height)
            
        elif message_action == 'createSphere':
            data = message_data.get('data', {})
            radius = data.get('radius', 10)
            result = create_sphere(radius)
            
        elif message_action == 'fitView':
            result = fit_view()
            
        elif message_action == 'viewHome':
            result = view_home()
            
        elif message_action == 'viewTop':
            result = view_orientation('top')
            
        elif message_action == 'viewFront':
            result = view_orientation('front')
            
        elif message_action == 'viewRight':
            result = view_orientation('right')
            
        elif message_action == 'saveModel':
            file_name = message_data.get('data', {}).get('fileName', 'MyModel')
            result = save_model(file_name)
            
        elif message_action == 'exportSTL':
            file_name = message_data.get('data', {}).get('fileName', 'MyModel')
            result = export_stl(file_name)
            
        elif message_action == 'newDocument':
            result = new_document()
            
        elif message_action == 'executeCustomCommand':
            data = message_data.get('data', {})
            command = data.get('command', '')
            parameters = data.get('parameters', {})
            result = execute_custom_command(command, parameters)
            
        elif message_action == 'testConnection':
            result = test_connection()
            
        elif message_action == 'refreshConnection':
            result = test_connection()
            
        elif message_action == 'openRemoteControl':
            result = open_remote_control()
            
        else:
            result = f"Unknown command: {message_action}"
            
    except Exception as e:
        result = f"Error executing {message_action}: {str(e)}"
        futil.log(f"Error in palette_incoming: {str(e)}", adsk.core.LogLevels.ErrorLogLevel)

    # Return value with timestamp
    now = datetime.now()
    currentTime = now.strftime('%H:%M:%S')
    html_args.returnData = f'{result} - {currentTime}'


# Fusion 360 Command Functions
def create_new_sketch():
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        
        # Create sketch on XY plane
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
        return f"New sketch created: {sketch.name}"
    except Exception as e:
        return f"Error creating sketch: {str(e)}"

def draw_line():
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        
        if sketches.count == 0:
            return "No active sketch. Create a sketch first."
        
        sketch = sketches.item(sketches.count - 1)  # Get last sketch
        lines = sketch.sketchCurves.sketchLines
        
        # Draw a simple line
        startPoint = adsk.core.Point3D.create(0, 0, 0)
        endPoint = adsk.core.Point3D.create(10, 10, 0)
        line = lines.addByTwoPoints(startPoint, endPoint)
        
        return "Line drawn successfully"
    except Exception as e:
        return f"Error drawing line: {str(e)}"

def draw_rectangle():
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        
        if sketches.count == 0:
            return "No active sketch. Create a sketch first."
        
        sketch = sketches.item(sketches.count - 1)
        lines = sketch.sketchCurves.sketchLines
        
        # Draw rectangle
        point1 = adsk.core.Point3D.create(0, 0, 0)
        point2 = adsk.core.Point3D.create(20, 15, 0)
        lines.addTwoPointRectangle(point1, point2)
        
        return "Rectangle drawn successfully"
    except Exception as e:
        return f"Error drawing rectangle: {str(e)}"

def draw_circle():
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        
        if sketches.count == 0:
            return "No active sketch. Create a sketch first."
        
        sketch = sketches.item(sketches.count - 1)
        circles = sketch.sketchCurves.sketchCircles
        
        # Draw circle
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        circle = circles.addByCenterRadius(centerPoint, 10)
        
        return "Circle drawn successfully"
    except Exception as e:
        return f"Error drawing circle: {str(e)}"

def finish_sketch():
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        # Exit sketch mode by switching to model workspace
        workspaces = ui.workspaces
        modelWorkspace = workspaces.itemById('FusionSolidEnvironment')
        if modelWorkspace:
            modelWorkspace.activate()
        
        return "Sketch finished"
    except Exception as e:
        return f"Error finishing sketch: {str(e)}"

def extrude_feature(distance):
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        features = rootComp.features
        
        # Get the last sketch
        sketches = rootComp.sketches
        if sketches.count == 0:
            return "No sketches available for extrusion"
        
        sketch = sketches.item(sketches.count - 1)
        
        # Get the profile
        prof = sketch.profiles.item(0) if sketch.profiles.count > 0 else None
        if not prof:
            return "No profile found in sketch for extrusion"
        
        # Create extrude feature
        extrudes = features.extrudeFeatures
        extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Set distance
        distance_value = adsk.core.ValueInput.createByReal(distance / 10)  # Convert mm to cm
        extrudeInput.setDistanceExtent(False, distance_value)
        
        extrude = extrudes.add(extrudeInput)
        
        return f"Extrude created with distance {distance}mm"
    except Exception as e:
        return f"Error creating extrude: {str(e)}"

def create_box(length, width, height):
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        
        # Create a new sketch on XY plane
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
        # Draw rectangle
        lines = sketch.sketchCurves.sketchLines
        point1 = adsk.core.Point3D.create(0, 0, 0)
        point2 = adsk.core.Point3D.create(length/10, width/10, 0)  # Convert to cm
        rect = lines.addTwoPointRectangle(point1, point2)
        
        # Extrude the rectangle
        prof = sketch.profiles.item(0)
        extrudes = rootComp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        height_value = adsk.core.ValueInput.createByReal(height / 10)  # Convert to cm
        extrudeInput.setDistanceExtent(False, height_value)
        
        extrude = extrudes.add(extrudeInput)
        
        return f"Box created: {length}×{width}×{height}mm"
    except Exception as e:
        return f"Error creating box: {str(e)}"

def create_cylinder(radius, height):
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        
        # Create sketch
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)
        
        # Draw circle
        circles = sketch.sketchCurves.sketchCircles
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        circle = circles.addByCenterRadius(centerPoint, radius/10)  # Convert to cm
        
        # Extrude
        prof = sketch.profiles.item(0)
        extrudes = rootComp.features.extrudeFeatures
        extrudeInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        height_value = adsk.core.ValueInput.createByReal(height / 10)
        extrudeInput.setDistanceExtent(False, height_value)
        
        extrude = extrudes.add(extrudeInput)
        
        return f"Cylinder created: radius {radius}mm, height {height}mm"
    except Exception as e:
        return f"Error creating cylinder: {str(e)}"

def create_sphere(radius):
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        
        # Create sketch
        sketches = rootComp.sketches
        yzPlane = rootComp.yZConstructionPlane
        sketch = sketches.add(yzPlane)
        
        # Draw semicircle
        arcs = sketch.sketchCurves.sketchArcs
        centerPoint = adsk.core.Point3D.create(0, 0, 0)
        startPoint = adsk.core.Point3D.create(0, radius/10, 0)
        endPoint = adsk.core.Point3D.create(0, -radius/10, 0)
        arc = arcs.addByCenterStartEnd(centerPoint, startPoint, endPoint)
        
        # Add diameter line
        lines = sketch.sketchCurves.sketchLines
        line = lines.addByTwoPoints(startPoint, endPoint)
        
        # Revolve
        prof = sketch.profiles.item(0)
        revolves = rootComp.features.revolveFeatures
        revolveInput = revolves.createInput(prof, line, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        angle = adsk.core.ValueInput.createByReal(3.14159)  # 180 degrees in radians
        revolveInput.setAngleExtent(False, angle)
        
        revolve = revolves.add(revolveInput)
        
        return f"Sphere created: radius {radius}mm"
    except Exception as e:
        return f"Error creating sphere: {str(e)}"

def fit_view():
    try:
        app.activeViewport.fit()
        return "View fitted to all objects"
    except Exception as e:
        return f"Error fitting view: {str(e)}"

def view_home():
    try:
        app.activeViewport.goHome()
        return "Home view activated"
    except Exception as e:
        return f"Error setting home view: {str(e)}"

def view_orientation(orientation):
    try:
        viewport = app.activeViewport
        camera = viewport.camera
        
        if orientation == 'top':
            # Set top view
            eye = adsk.core.Point3D.create(0, 0, 100)
            target = adsk.core.Point3D.create(0, 0, 0)
            up = adsk.core.Vector3D.create(0, 1, 0)
        elif orientation == 'front':
            # Set front view
            eye = adsk.core.Point3D.create(0, -100, 0)
            target = adsk.core.Point3D.create(0, 0, 0)
            up = adsk.core.Vector3D.create(0, 0, 1)
        elif orientation == 'right':
            # Set right view
            eye = adsk.core.Point3D.create(100, 0, 0)
            target = adsk.core.Point3D.create(0, 0, 0)
            up = adsk.core.Vector3D.create(0, 0, 1)
        else:
            return f"Unknown orientation: {orientation}"
            
        camera.eye = eye
        camera.target = target
        camera.upVector = up
        viewport.camera = camera
        
        return f"{orientation.title()} view activated"
    except Exception as e:
        return f"Error setting {orientation} view: {str(e)}"

def save_model(file_name):
    try:
        design = app.activeProduct
        if not design:
            return "No active design to save"
        
        # Save as Fusion 360 archive
        exportMgr = design.exportManager
        
        # Set up options for saving
        options = exportMgr.createFusionArchiveExportOptions(file_name)
        exportMgr.execute(options)
        
        return f"Model saved as: {file_name}"
    except Exception as e:
        return f"Error saving model: {str(e)}"

def export_stl(file_name):
    try:
        design = app.activeProduct
        if not design:
            return "No active design to export"
        
        # Get the root component
        rootComp = design.rootComponent
        
        # Create STL export options
        exportMgr = design.exportManager
        stlOptions = exportMgr.createSTLExportOptions(rootComp)
        stlOptions.filename = f"{file_name}.stl"
        stlOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium
        
        exportMgr.execute(stlOptions)
        
        return f"STL exported as: {file_name}.stl"
    except Exception as e:
        return f"Error exporting STL: {str(e)}"

def new_document():
    try:
        # Create new document
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        return "New document created"
    except Exception as e:
        return f"Error creating new document: {str(e)}"

def execute_custom_command(command, parameters):
    try:
        # This is a basic implementation - you can expand this
        # to execute more complex custom commands
        if not command:
            return "No command provided"
        
        # For safety, only allow specific predefined commands
        allowed_commands = [
            'fit_view',
            'create_new_sketch',
            'get_selection_count',
            'get_active_design_name'
        ]
        
        if command == 'get_selection_count':
            selection = ui.activeSelections
            return f"Selected objects: {selection.count}"
        elif command == 'get_active_design_name':
            design = app.activeProduct
            if design:
                return f"Active design: {design.parentDocument.name}"
            else:
                return "No active design"
        elif command in allowed_commands:
            # Execute the function by name
            func = globals().get(command)
            if func:
                return func()
            else:
                return f"Function {command} not found"
        else:
            return f"Command '{command}' not allowed for security reasons"
            
    except Exception as e:
        return f"Error executing custom command: {str(e)}"

def revolve_feature():
    try:
        design = app.activeProduct
        if not design:
            return "No active design"
        
        rootComp = design.rootComponent
        sketches = rootComp.sketches
        
        if sketches.count == 0:
            return "No sketches available for revolve"
        
        sketch = sketches.item(sketches.count - 1)
        
        if sketch.profiles.count == 0:
            return "No profile found in sketch"
        
        prof = sketch.profiles.item(0)
        
        # Get a line to revolve around (use Y-axis if no suitable line found)
        revolveAxis = None
        for line in sketch.sketchCurves.sketchLines:
            revolveAxis = line
            break
        
        if not revolveAxis:
            # Create a construction line on Y-axis
            lines = sketch.sketchCurves.sketchLines
            startPoint = adsk.core.Point3D.create(0, -10, 0)
            endPoint = adsk.core.Point3D.create(0, 10, 0)
            revolveAxis = lines.addByTwoPoints(startPoint, endPoint)
            revolveAxis.isConstruction = True
        
        # Create revolve feature
        revolves = rootComp.features.revolveFeatures
        revolveInput = revolves.createInput(prof, revolveAxis, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Set full revolution (360 degrees)
        angle = adsk.core.ValueInput.createByReal(2 * 3.14159)  # 360 degrees in radians
        revolveInput.setAngleExtent(False, angle)
        
        revolve = revolves.add(revolveInput)
        
        return "Revolve feature created successfully"
    except Exception as e:
        return f"Error creating revolve: {str(e)}"

def open_remote_control():
    """Open remote control interface in default browser"""
    try:
        webbrowser.open(REMOTE_CONTROL_URL)
        ui.messageBox(f'🌐 Remote Control Interface opened!\n\nURL: {REMOTE_CONTROL_URL}\n\nThis interface allows anyone on the internet to control Fusion 360 when connected to a WebSocket server.')
        return {"success": True, "message": "Remote control interface opened"}
    except Exception as e:
        futil.log(f"Error opening remote control: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}

def test_connection():
    """Test connection and show current URLs"""
    try:
        message = f"""
🌐 Fusion 360 Remote Control System

📱 LOCAL INTERFACE (Current):
{PALETTE_URL}

🌍 REMOTE CONTROL (Internet):
{REMOTE_CONTROL_URL}

🔧 WebSocket Server:
ws://localhost:8765

✅ Connection Status: Connected
🎯 Mode: {'Online (GitHub Pages)' if USE_ONLINE_VERSION else 'Local Files'}

💡 To enable remote control:
1. Start WebSocket server (run debug-start-server.bat)
2. Open remote control URL in any browser
3. Connect to WebSocket server
4. Control Fusion 360 from anywhere!
"""
        ui.messageBox(message)
        return {"success": True, "message": "Connection test completed"}
    except Exception as e:
        futil.log(f"Connection test error: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}

# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME}: Command destroy event.')

    global local_handlers
    local_handlers = []

// Utility functions
function getDateString() {
    const today = new Date();
    const date = `${today.getDate()}/${today.getMonth() + 1}/${today.getFullYear()}`;
    const time = `${today.getHours()}:${today.getMinutes()}:${today.getSeconds()}`;
    return `Date: ${date}, Time: ${time}`;
}

function updateReturnValue(message) {
    document.getElementById("returnValue").innerHTML = `[${new Date().toLocaleTimeString()}] ${message}`;
}

function sendCommandToFusion(action, data = {}) {
    const payload = {
        action: action,
        data: data,
        timestamp: getDateString()
    };
    
    return adsk.fusionSendData(action, JSON.stringify(payload)).then((result) => {
        updateReturnValue(result);
        return result;
    }).catch((error) => {
        updateReturnValue(`Error: ${error}`);
        console.error('Command failed:', error);
    });
}

// Original function for compatibility
function sendInfoToFusion() {
    const args = {
        arg1: document.getElementById("sampleData")?.value || "test data",
        arg2: getDateString()
    };
    sendCommandToFusion("messageFromPalette", args);
}

// Sketch Commands
function createNewSketch() {
    sendCommandToFusion("createNewSketch");
}

function drawLine() {
    sendCommandToFusion("drawLine");
}

function drawRectangle() {
    sendCommandToFusion("drawRectangle");
}

function drawCircle() {
    sendCommandToFusion("drawCircle");
}

function finishSketch() {
    sendCommandToFusion("finishSketch");
}

// 3D Modeling Commands
function extrudeFeature() {
    const distance = document.getElementById("extrudeDistance").value;
    sendCommandToFusion("extrudeFeature", { distance: parseFloat(distance) });
}

function revolveFeature() {
    sendCommandToFusion("revolveFeature");
}

function sweepFeature() {
    sendCommandToFusion("sweepFeature");
}

function loftFeature() {
    sendCommandToFusion("loftFeature");
}

// Primitive Creation
function createBox() {
    const length = document.getElementById("boxLength").value;
    const width = document.getElementById("boxWidth").value;
    const height = document.getElementById("boxHeight").value;
    
    sendCommandToFusion("createBox", {
        length: parseFloat(length),
        width: parseFloat(width),
        height: parseFloat(height)
    });
}

function createCylinder() {
    const radius = document.getElementById("cylRadius").value;
    const height = document.getElementById("cylHeight").value;
    
    sendCommandToFusion("createCylinder", {
        radius: parseFloat(radius),
        height: parseFloat(height)
    });
}

function createSphere() {
    const radius = document.getElementById("cylRadius").value;
    sendCommandToFusion("createSphere", { radius: parseFloat(radius) });
}

// View Controls
function fitView() {
    sendCommandToFusion("fitView");
}

function zoomToSelected() {
    sendCommandToFusion("zoomToSelected");
}

function viewHome() {
    sendCommandToFusion("viewHome");
}

function viewTop() {
    sendCommandToFusion("viewTop");
}

function viewFront() {
    sendCommandToFusion("viewFront");
}

function viewRight() {
    sendCommandToFusion("viewRight");
}

// File Operations
function saveModel() {
    const fileName = document.getElementById("fileName").value;
    sendCommandToFusion("saveModel", { fileName: fileName });
}

function exportSTL() {
    const fileName = document.getElementById("fileName").value;
    sendCommandToFusion("exportSTL", { fileName: fileName });
}

function exportStep() {
    const fileName = document.getElementById("fileName").value;
    sendCommandToFusion("exportStep", { fileName: fileName });
}

function newDocument() {
    sendCommandToFusion("newDocument");
}

// Custom Commands
function executeCustomCommand() {
    const command = document.getElementById("customCommand").value;
    let params = {};
    
    try {
        const paramsText = document.getElementById("commandParams").value;
        if (paramsText.trim()) {
            params = JSON.parse(paramsText);
        }
    } catch (e) {
        updateReturnValue("Error: Invalid JSON in parameters");
        return;
    }
    
    sendCommandToFusion("executeCustomCommand", {
        command: command,
        parameters: params
    });
}

// Message handling
function updateMessage(messageString) {
    try {
        const messageData = JSON.parse(messageString);
        
        let displayMessage = `<strong>Message received:</strong><br/>`;
        if (typeof messageData === 'object') {
            for (const [key, value] of Object.entries(messageData)) {
                displayMessage += `<strong>${key}:</strong> ${value}<br/>`;
            }
        } else {
            displayMessage += messageData;
        }
        
        document.getElementById("fusionMessage").innerHTML = displayMessage;
    } catch (e) {
        document.getElementById("fusionMessage").innerHTML = `<strong>Raw message:</strong> ${messageString}`;
    }
}

// Global handler for Fusion 360 communication
window.fusionJavaScriptHandler = {
    handle: function (action, data) {
        try {
            if (action === "updateMessage") {
                updateMessage(data);
            } else if (action === "debugger") {
                debugger;
            } else if (action === "showStatus") {
                updateReturnValue(data);
            } else if (action === "updateUI") {
                // Handle UI updates from Fusion
                const updateData = JSON.parse(data);
                if (updateData.elementId && updateData.value) {
                    const element = document.getElementById(updateData.elementId);
                    if (element) {
                        element.value = updateData.value;
                    }
                }
            } else {
                console.log(`Unhandled action: ${action}, data: ${data}`);
                return `Unhandled command type: ${action}`;
            }
        } catch (e) {
            console.error(e);
            console.error(`Exception caught with command: ${action}, data: ${data}`);
            return `Error processing command: ${action}`;
        }
        return "OK";
    },
};

// Initialize the interface
document.addEventListener('DOMContentLoaded', function() {
    updateReturnValue("Interface loaded. Ready to control Fusion 360!");
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey) {
            switch(e.key) {
                case 's':
                    e.preventDefault();
                    saveModel();
                    break;
                case 'n':
                    e.preventDefault();
                    newDocument();
                    break;
                case 'f':
                    e.preventDefault();
                    fitView();
                    break;
            }
        }
    });
    
    // Update status indicator
    const statusIndicator = document.querySelector('.status-indicator');
    if (statusIndicator) {
        statusIndicator.style.background = '#48bb78'; // Green for active
    }
});

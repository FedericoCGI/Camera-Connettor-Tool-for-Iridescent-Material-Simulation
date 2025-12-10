import maya.cmds as cmds
import sys

# drag this code to the shelf:
# run the tool adding this script to Maya scripts folder
#import sys
#sys.path.append(r"C:\Users\feder\Documents\3D_Reel\01_ErasTour\scripts")
#import cameraConnectorTool
#import importlib
#importlib.reload(cameraConnectorTool)

# list of all cameras loaded in the scene
camera_button=[]
# list of all place3DTexture nodes loaded in the scene
place3dTexture_button=[]

# selected Camera
selCamera = None
# selected place3DTexture node
selP3DT = None

# Make a list of all cameras contained in a scene
def cameraList():
    cameras = cmds.ls(type="camera")
    return cameras

# Make a list of all place3DTextures nodes contained in a scene
def place3DTexList():
    place3D_nodeList = cmds.ls(type="place3dTexture")
    return place3D_nodeList

# Enable p3dt buttons.
def enableP3DTButton(*args):

# Disable all camera buttons.
    for btn in camera_button:
        cmds.button(btn, edit=True, enable=False)
    
    # Enable all place3dTexture buttons.
    for btn in place3dTexture_button:
        cmds.button(btn, edit=True, enable=True)

# Disable p3dt buttons.
def disableP3DTButton(*args):

    # get a list of place3DTexture nodes
    #plc3dnode_list = place3DTexList()

    # disable every node of the list
    for btn in place3dTexture_button:
        cmds.button(btn, edit=True, enable=False)

# enable camera button
def enableCameraButton(*args):

    # enable all camera buttons
    for btn in camera_button:
        cmds.button(btn, edit=True, enable=True)
    
    # disable p3dt buttons
    disableP3DTButton()

    # disable disconnect nodes button
    cmds.button(disconnect_node_btn, edit=True, enable=False)


# Get camera name function
def selectCamera(camera):

    # Get camera and make it global in order to be seen in the whole code
    global selCamera
    selCamera = camera
    print("Selected Camera: " + selCamera)

    # Enable p3dt buttons.
    enableP3DTButton()  


# disconnect connected nodes
def disconnectNodes(*args):

    # check if nodes are connected
    if cmds.isConnected(selCamera + ".rotateY", selP3DT + ".rotateY") and cmds.isConnected(selCamera + ".rotateX", selP3DT + ".rotateX"):
        
        # disconnect camera and place3Dtexture node rotateX and rotateY attributes
        cmds.disconnectAttr(selCamera + ".rotateY", selP3DT + ".rotateY")
        cmds.disconnectAttr(selCamera + ".rotateX", selP3DT + ".rotateX")
  
    
    # check if node disconnection has been successfully
    if not (cmds.isConnected(selCamera + ".rotateY", selP3DT + ".rotateY") and cmds.isConnected(selCamera + ".rotateX", selP3DT + ".rotateX")):
        print(f"{selCamera} - {selP3DT} Disconnected!")
    
        # set rotationX and rotationY attribute at 0 for selP3DT
        cmds.setAttr(selP3DT + ".rotateX", 0)
        cmds.setAttr(selP3DT + ".rotateY", 0)

        # enable camera button
        enableCameraButton()
        
    

    


# Make a connection between selected camera and selected place3D Texture
def camToP3DTConnector(p3dt):
    global selP3DT 
    selP3DT = p3dt
    # check for existing selected place3DTexture node
    if not cmds.objExists(selP3DT):
        print("Error! place3Dtexture node not selected!")
    # check for existing selected camera
    elif not cmds.objExists(selCamera):
        print("Error! camera not selected!")
    else:

        # Get and print the selected 3p3dt node
        print("Selected Node: "+ selP3DT)
        
        # Get camera rotateY
        camRotY = cmds.getAttr(selCamera + ".rotateY")
        print("Camera Rotate Y: " + str(camRotY))

        # Connect rotateY atrribute of selected camera with rotateY attribute of selected place3DTexture node
        cmds.connectAttr(selCamera + ".rotateY", selP3DT + ".rotateY", force=True)
        # Connect rotateX atrribute of selected camera with rotateX attribute of selected place3DTexture node
        cmds.connectAttr(selCamera + ".rotateX", selP3DT + ".rotateX", force=True)

        # disable all the p3DT buttons
        disableP3DTButton()

        # enable node disconnection button
        global disconnect_node_btn
        cmds.button(disconnect_node_btn, edit=True, enable=True)

        
    
        
    '''
    # Enable camera button
    for btn in camera_button:
        cmds.button(btn, edit=True, enable=True) 
    '''  

def cameraConnectorTool():

    #check if a window cameraConnectorWindow exists
    if (cmds.window("cameraConnectorTool", exists=True)):
        cmds.deleteUI("cameraConnectorTool")
    
    # create a new window object
    cameraConnectorWindow=cmds.window("cameraConnectorTool", title="Camera Connector Tool", widthHeight=(600, 300))

    # if you want to add an element to a window, you must first specify a layout. 
    # A columnLayout arranges all the controls we add in a single vertical column.
    # A rowLayout arranges all the controls we add horizontally.
    #cmds.rowLayout(numberOfColumns=2)
    #cmds.columnLayout(rowSpacing=10)

    # Main Layout (text field alligned)
    # We need a row splitted in three columns for texts
    cmds.columnLayout(adjustableColumn=True,)
    cmds.rowLayout(numberOfColumns=3, columnWidth=[(1, 150), (2, 300), (3,300)])

    #Left text: cameras
    # After specified the Layout, we can add controls. We can add a text control.
    cmds.text(label="Select Camera: ", height=30)

    #Center text: place3dtexture nodes:
    # We add a text control for place3DTexture nodes.
    cmds.text(label="Select place3dTexture node to connect: ", height=30)

    #Right text: disconnect Nodes button
    # We add a text cobntrol for disconnect Nodes button
    cmds.text(label="Node Disconnection: ", height=30)

    # Close Text Layout
    cmds.setParent("..")
    
    # Button Layout:
    # We need 1 row splitted in 3 columns, one for camera list, one for p3DT node list and one for disconnection node button.
    cmds.rowLayout(numberOfColumns=3, columnWidth=[(1, 150), (2, 300), (3, 300)])
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    # We can add a control button to our window.
    # We can add some buttons to our window, showing cameras in the scene.

    # Get camera list.
    cameras = cameraList()

    # for each camera (cam) in camera list
    for cam in cameras:

        # get camera name
        camName = cmds.listRelatives(cam, parent=True)[0]

        # Create a button showing camera name
        cam_btn = cmds.button(label=camName, enable=True, command=lambda x, camera=camName: selectCamera(camera))

        # Add button to camera_Button
        camera_button.append(cam_btn)

    #Close camera buttons layout
    cmds.setParent("..")

    #Right Column: place3DTexture nodes.
    cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    # Button Layout:
    # Add buttons for each place3DTexture node in the scene.
    # Get place3DTexture nodes list.
    place3D_nodeList = place3DTexList()

    for node in place3D_nodeList:
        
        # Create a button showing place3DTexture node name
        p3dt_btn = cmds.button(label=node, enable=False, command=lambda x, p3dt=node: camToP3DTConnector(node))

        # Add button to camera_Button
        place3dTexture_button.append(p3dt_btn)
    
    # Close place3Dtex node button layout
    cmds.setParent("..")


    # Disconnect Nodes button layout:
    # add a Disconnect node button
    global disconnect_node_btn
    disconnect_node_btn = cmds.button(label="Disconnect Nodes", enable = False, command=disconnectNodes)
    
    # Close the Main Layout
    cmds.setParent("..")

    # Show our window in Maya
    cmds.showWindow(cameraConnectorWindow)

cameraConnectorTool()
# main file, imports other files and uses them, contains init and run functions
import math
from tkinter import *
from DrawGraph3D import*
from Graph3D import *
from InputModes import *
from SettingsMode import *

# run function and animation framework taken from 15-112 course website
# rgbString funciton taken from 15-112 course website


################################################################################
## MODEL
################################################################################

def init(data):
    # possible modes: graph3D, settings3D, options3D, help
    #                 function3DList, function3DInput,
    #                 parametric3D2PList, parametric3D2PInput,
    #                 parametric3D1PList, parametric3D1PInput,
    data.mode = "graph3D"
    # Try these!
    # data.graphsFunction3D = [
    #     Function3D(["z","=","sin","x","+","sin","y","-","3","\n",
    #                 "(","1","0","0",",","0",",","0",")"])]
    # data.graphsParametric3D2P = [
    #     Parametric3D2P(["x","=","(","4","+","cos","t",")","*","cos","u","\n",
    #                     "y","=","(","4","+","cos","t",")","*","sin","u","\n",
    #                     "z","=","sin","t","\n",
    #                     "0",",","2","*","π",",","π","/","1","0","\n",
    #                     "0",",","2","*","π",",","π","/","1","5","\n",
    #                     "(","0",",","1","0","0",",","0",")"]) ]
    # data.graphsParametric3D1P = [
    #     Parametric3D1P(["x","=","t","*","cos","t","\n",
    #                     "y","=","t","*","sin","t","\n",
    #                     "z","=","t","\n",
    #                     "0",",","3","*","π",",","π","/","1","0","\n",
    #                     "(","2","0","0",",","1","0","0",",","0",")"]) ]
    data.graphsFunction3D = []
    data.graphsParametric3D2P = []
    data.graphsParametric3D1P = []
    data.res = 20
    data.axisMin = [-6, -6, -6]
    data.axisMax = [6, 6, 6]
    data.xyTheta = 0.0
    data.yzTheta = 0.0
    data.xzTheta = 0.0
    data.xScrollSpeed = 0.1
    data.yScrollSpeed = 0.1
    data.zScrollSpeed = 0.1
    data.xZoomSpeed = 1.25
    data.yZoomSpeed = 1.25
    data.zZoomSpeed = 1.25
    data.generalZoomSpeed = 1.25
    data.minDotSize = 0
    data.maxDotSize = 3
    data.centerBoxX = data.width/2
    data.centerBoxZ = data.height/2
    data.boxSize = 0.5
    data.cameraDistance = 5
    data.showPoints = True
    data.showWires = True
    data.showGrid = True
    data.showGridNums = True
    data.showBoundary = True
    data.perspectiveOn = True
    data.backgroundRGB = (255,255,255)
    data.colorFade = 0.8
    data.listScroll = 0
    data.listScrollSpeed = 50
    # input screen
    data.inputs = []
    data.extraKeys = ["(", ")", "+", "-", "*", "/", "^", "~", ",", ".", "="]
    data.cursorListPosition = 0
    data.cursorPosition = [0,0]
    data.modifyIndex = 0
    data.textHeight = int(data.height/25)
    data.textLineHeight = data.textHeight*1.5
    data.textWidth = data.textHeight*0.813
    data.settingsGraphsBoxSize = (data.width*0.2, data.height*0.05)
    data.returnBoxSize = (data.width*0.15, data.height*0.05)
    data.options3DBoxSize = (data.width*0.5, data.height*0.1)
    data.equationBoxSize = (data.width, data.height*0.1)
    data.keyboardMode = "trig"
    data.calcKeyboardTrig = [ ["trig",     ",",    "~", "x", "y", "z", "t", "u"],
                              [ "sin",   "cos",  "tan", "7", "8", "9", "/", "π"],
                              [ "csc",   "sec",  "cot", "4", "5", "6", "*", "e"],
                              [ "log",   "mod",  "abs", "1", "2", "3", "+", "."],
                              ["ceil", "floor",    "=", "0", "(", ")", "-", "^"] ]
    data.calcKeyboardInv  = [ [ "inv",     ",",    "~", "x", "y", "z", "t", "u"],
                              ["asin",  "acos", "atan", "7", "8", "9", "/", "π"],
                              ["acsc",  "asec", "acot", "4", "5", "6", "*", "e"],
                              [ "log",   "mod",  "abs", "1", "2", "3", "+", "."],
                              ["ceil", "floor",    "=", "0", "(", ")", "-", "^"] ]
    # data.calcKeyboardTrig = [["ass","slap","hein"],[0,0,0],[0,0,0],[0,0,0]]
    data.function3DKeyMask     = [ [1, 1, 1, 1, 1, 1, 0, 0],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1] ]
    data.parametric3D2PKeyMask = [ [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1] ]
    data.parametric3D1PKeyMask = [ [1, 1, 1, 1, 1, 1, 1, 0],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1] ]
    data.settingsKeyMask       = [ [1, 1, 1, 0, 0, 0, 0, 0],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 1, 1, 1, 1, 1, 1],
                                   [1, 1, 0, 1, 1, 1, 1, 1] ]
    data.settingsBoxes = [["xMin: "+str(data.axisMin[0]), "xMax: "+str(data.axisMax[0])],
                          ["yMin: "+str(data.axisMin[1]), "yMax: "+str(data.axisMax[1])],
                          ["xMin: "+str(data.axisMin[2]), "zMax: "+str(data.axisMax[2])],
                          ["Yaw: "+str(data.xyTheta), "Pitch: "+str(data.yzTheta)],
                          ["Roll: "+str(data.xzTheta), "Camera distance: "+str(data.cameraDistance)],
                          ["Show points: "+str(data.showPoints), "Show wires: "+str(data.showWires)],
                          ["Show grid: "+str(data.showGrid), "Show grid numbers: "+str(data.showGridNums)],
                          ["Show boundary: "+str(data.showBoundary), "Perspective on: "+str(data.perspectiveOn)],
                          ["Function resolution: "+str(data.res), "BackgroundRGB: "+str(data.backgroundRGB)]]
    data.settingsNames = [["xMin", "xMax"],
                          ["yMin", "yMax"],
                          ["xMin", "zMax"],
                          ["Yaw", "Pitch"],
                          ["Roll", "Camera distance"],
                          ["Show points", "Show wires"],
                          ["Show grid", "Show grid numbers"],
                          ["Show boundary", "Perspective on"],
                          ["Function resolution", "BackgroundRGB"]]
    data.currentSetting = None

################################################################################
## CONTROLLER
################################################################################

def mousePressed(event, data):
    if data.mode=="graph3D":
        boxWidth, boxHeight =\
            data.settingsGraphsBoxSize[0], data.settingsGraphsBoxSize[1]
        if event.x>=data.width-boxWidth and event.y<=boxHeight:
            refreshSettings(data)
            data.mode = "settings3D"
        elif event.x>=data.width-boxWidth and event.y<=2*boxHeight:
            data.mode = "options3D"
        elif event.x>=data.width-boxWidth and event.y>=data.height-boxHeight:
            data.mode = "help"
    
    elif data.mode in ["options3D",\
        "function3DList", "function3DInput",\
        "parametric3D2PList", "parametric3D2PInput",\
        "parametric3D1PList", "parametric3D1PInput"]:
        mousePressedInputModes(event, data)
    
    elif data.mode in ["settings3D", "settings3DInput"]:
        mousePressedSettings(event, data)
        keyPressed3DOptions(event, data)
    
    elif data.mode=="help":
        # click return box
        boxWidth, boxHeight = data.returnBoxSize[0], data.returnBoxSize[1]
        if event.x<=boxWidth and event.y<=boxHeight:
            data.mode= "graph3D"

def keyPressed(event, data):
    if data.mode=="graph3D":
        # rotations
        if event.keysym=="q":
            data.yzTheta = (data.yzTheta-0.1)%(2*math.pi)
        elif event.keysym=="r":
            data.yzTheta = (data.yzTheta+0.1)%(2*math.pi)
        elif event.keysym=="a":
            data.xzTheta = (data.xzTheta-0.1)%(2*math.pi)
        elif event.keysym=="f":
            data.xzTheta = (data.xzTheta+0.1)%(2*math.pi)
        elif event.keysym=="z":
            data.xyTheta = (data.xyTheta-0.1)%(2*math.pi)
        elif event.keysym=="v":
            data.xyTheta = (data.xyTheta+0.1)%(2*math.pi)
        
        # moving the frame
        elif event.keysym=="Left":
            change = (data.axisMax[0]-data.axisMin[0])*data.xScrollSpeed
            data.axisMin[0] -= change
            data.axisMax[0] -= change
        elif event.keysym=="Right":
            change = (data.axisMax[0]-data.axisMin[0])*data.xScrollSpeed
            data.axisMin[0] += change
            data.axisMax[0] += change
        elif event.keysym=="Down":
            change = (data.axisMax[1]-data.axisMin[1])*data.yScrollSpeed
            data.axisMin[1] -= change
            data.axisMax[1] -= change
        elif event.keysym=="Up":
            change = (data.axisMax[1]-data.axisMin[1])*data.yScrollSpeed
            data.axisMin[1] += change
            data.axisMax[1] += change
        elif event.keysym=="slash":
            change = (data.axisMax[2]-data.axisMin[2])*data.zScrollSpeed
            data.axisMin[2] -= change
            data.axisMax[2] -= change
        elif event.keysym=="quoteright":
            change = (data.axisMax[2]-data.axisMin[2])*data.zScrollSpeed
            data.axisMin[2] += change
            data.axisMax[2] += change
        
        # stretch/shrink axes
        elif event.keysym=="w":
            change = (data.axisMax[0]-data.axisMin[0])*(data.xZoomSpeed-1)
            data.axisMin[0] -= change*0.5
            data.axisMax[0] += change*0.5
        elif event.keysym=="e":
            change = (data.axisMax[0]-data.axisMin[0])*(1-1/data.xZoomSpeed)
            data.axisMin[0] += change*0.5
            data.axisMax[0] -= change*0.5
        elif event.keysym=="s":
            change = (data.axisMax[1]-data.axisMin[1])*(data.yZoomSpeed-1)
            data.axisMin[1] -= change*0.5
            data.axisMax[1] += change*0.5
        elif event.keysym=="d":
            change = (data.axisMax[1]-data.axisMin[1])*(1-1/data.yZoomSpeed)
            data.axisMin[1] += change*0.5
            data.axisMax[1] -= change*0.5
        elif event.keysym=="x":
            change = (data.axisMax[2]-data.axisMin[2])*(data.zZoomSpeed-1)
            data.axisMin[2] -= change*0.5
            data.axisMax[2] += change*0.5
        elif event.keysym=="c":
            change = (data.axisMax[2]-data.axisMin[2])*(1-1/data.zZoomSpeed)
            data.axisMin[2] += change*0.5
            data.axisMax[2] -= change*0.5
        
        # zoom in/out
        elif event.keysym=="minus":
            changeX = (data.axisMax[0]-data.axisMin[0])*(data.generalZoomSpeed-1)
            changeY = (data.axisMax[1]-data.axisMin[1])*(data.generalZoomSpeed-1)
            changeZ = (data.axisMax[2]-data.axisMin[2])*(data.generalZoomSpeed-1)
            data.axisMin[0] -= changeX*0.5
            data.axisMax[0] += changeX*0.5
            data.axisMin[1] -= changeY*0.5
            data.axisMax[1] += changeY*0.5
            data.axisMin[2] -= changeZ*0.5
            data.axisMax[2] += changeZ*0.5
        elif event.keysym=="equal":
            changeX = (data.axisMax[0]-data.axisMin[0])*(1-1/data.generalZoomSpeed)
            changeY = (data.axisMax[1]-data.axisMin[1])*(1-1/data.generalZoomSpeed)
            changeZ = (data.axisMax[2]-data.axisMin[2])*(1-1/data.generalZoomSpeed)
            data.axisMin[0] += changeX*0.5
            data.axisMax[0] -= changeX*0.5
            data.axisMin[1] += changeY*0.5
            data.axisMax[1] -= changeY*0.5
            data.axisMin[2] += changeZ*0.5
            data.axisMax[2] -= changeZ*0.5
        
        # toggle showPoints/showWires/perspectiveOn
        elif event.keysym=="i":
            data.showPoints = not data.showPoints
        elif event.keysym=="o":
            data.showWires = not data.showWires
        elif event.keysym=="p":
            data.perspectiveOn = not data.perspectiveOn
    
    elif data.mode in ["settings3D", "settings3DInput"]:
        keyPressedSettings(event, data)
    
    elif data.mode in ["options3D",\
        "function3DList", "function3DInput",\
        "parametric3D2PList", "parametric3D2PInput",\
        "parametric3D1PList", "parametric3D1PInput"]:
        keyPressed3DOptions(event, data)

################################################################################
## DRAW FUNCTIONS
################################################################################


def redrawAll(canvas, data):
    if data.mode=="graph3D":
        drawGraph3DMode(canvas, data)
    elif data.mode in ["settings3D", "settings3DInput"]:
        drawSettingsMode(canvas, data)
    elif data.mode=="options3D":
        drawOptions3DMode(canvas, data)
    elif data.mode in ["function3DList", "parametric3D2PList", "parametric3D1PList"]:
        draw3DList(canvas, data)
    elif data.mode in ["function3DInput", "parametric3D2PInput", "parametric3D1PInput"]:
        draw3DInput(canvas, data)
    elif data.mode=="help":
        boxWidth, boxHeight = data.returnBoxSize[0], data.returnBoxSize[1]
        canvas.create_rectangle((0,0), (boxWidth,boxHeight), width=1)
        canvas.create_text((boxWidth/2,boxHeight/2), text="Return",\
            font="Arial "+str(int(boxHeight/2)))
        margin = data.height/10
        canvas.create_text((margin,margin), anchor="nw",\
            text="""
The following can be modified in Settings, but these are keyboard shortcuts:

Left and Right arrow keys to move along x-axis
"q" and "r" for yz-rotation (pitch)
"w" and "e" to shrink/stretch the x-axis

Up and Down arrow keys to move along y-axis
"a" and "f" for xz-rotation (roll)
"s" and "d" to shrink/stretch the y-axis

"'" and "/" to move along z-axis
"z" and "v" for xy-rotation (yaw)
"x" and "c" to shrink/stretch the z-axis

"-" and "=" to zoom out and in
"i" to toggle showing points
"o" to toggle showing wires
"p" to toggle perspective

When viewing a list of graphs that goes off screen, Up and Down arrow keys can
be used to scroll.
"""   
            , font="Courier "+str(int(data.height/75)))

################################################################################
## RUN FUNCTION
################################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(800, 800)
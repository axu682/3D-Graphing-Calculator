# handles modes besides graph3D, setting modes, and help
from Graph3D import *

# turns equation list to string
def formEquationString(equation):
    result = ""
    for entry in equation:
        result += str(entry)
    return result

def getCursorPosition(data):
    if len(data.inputs)==0:
        return [0,0]
    row = data.inputs[:data.cursorListPosition].count("\n")
    totalRows = data.inputs.count("\n")
    centerRow = totalRows/2
    textDY = (row-centerRow)*data.textLineHeight
    if data.cursorListPosition==0:
        textDX = 0
    elif data.inputs[data.cursorListPosition-1]=="\n":
        textDX = 0
    else:
        lineStartIndex = data.cursorListPosition-1
        while True:
            if lineStartIndex==0:
                break
            elif data.inputs[lineStartIndex-1] != "\n":
                    lineStartIndex -= 1
            else:
                break
        lineDistance = 0
        for i in range(lineStartIndex, data.cursorListPosition):
            lineDistance += len(str(data.inputs[i]))
        textDX = lineDistance*data.textWidth
    data.cursorPosition = [textDX, textDY]

################################################################################
## KeyPressed
################################################################################

def keyPressed3DOptions(event, data):
    if data.mode in ["function3DList", "parametric3D2PList", "parametric3D1PList"]:
        keyPressed3DList(event, data)
    elif data.mode in ["function3DInput", "parametric3D2PInput", "parametric3D1PInput"]:
        keyPressed3DInput(event, data)

def keyPressed3DList(event, data):
    if data.mode=="function3DList":
        graphList = data.graphsFunction3D
        boxFactor = 1
    elif data.mode=="parametric3D2PList":
        graphList = data.graphsParametric3D2P
        boxFactor = 2
    elif data.mode=="parametric3D1PList":
        graphList = data.graphsParametric3D1P
        boxFactor = 2
    boxHeight = data.equationBoxSize[1]*boxFactor
    if event.keysym=="Up":
        if data.listScroll<0:
            data.listScroll += data.listScrollSpeed
    elif event.keysym=="Down":
        if data.equationBoxSize[1]+(len(graphList)+1)*boxHeight+data.listScroll>=data.height:
            data.listScroll -= data.listScrollSpeed

def keyPressed3DInput(event, data):
    if data.mode=="function3DInput":
        allowedKeysym = "1234567890xyzep"
    elif data.mode=="parametric3D2PInput":
        allowedKeysym = "1234567890xyztuep"
    elif data.mode=="parametric3D1PInput":
        allowedKeysym = "1234567890xyztep"
    
    if event.keysym in allowedKeysym or event.char in data.extraKeys or event.keysym=="Return":
        if event.keysym=="p":
            data.inputs.insert(data.cursorListPosition, "π")
        elif event.keysym=="Return":
            data.inputs.insert(data.cursorListPosition, "\n")
        else:
            data.inputs.insert(data.cursorListPosition, event.char)
        data.cursorListPosition += 1
    elif event.keysym=="BackSpace":
        if data.cursorListPosition>0:
            data.inputs.pop(data.cursorListPosition-1)
            data.cursorListPosition -= 1
    elif event.keysym=="Left":
        if data.cursorListPosition>0:
            data.cursorListPosition -= 1
    elif event.keysym=="Right":
        if data.cursorListPosition<len(data.inputs):
            data.cursorListPosition += 1
    # gets cursor posiion based on string of list
    getCursorPosition(data)

################################################################################
## MousePressed
################################################################################

def mousePressedInputModes(event, data):
    if data.mode=="options3D":
        # click return box
        boxWidth, boxHeight = data.returnBoxSize[0], data.returnBoxSize[1]
        if event.x<=boxWidth and event.y<=boxHeight:
            data.mode = "graph3D"
        # clicking one of the choices (goes to specific lists)
        boxWidth, boxHeight = data.options3DBoxSize[0], data.options3DBoxSize[1]
        if data.width/2-boxWidth/2 <= event.x <= data.width/2+boxWidth/2:
            if boxHeight <= event.y < 2*boxHeight:
                data.mode = "function3DList"
            elif 2*boxHeight <= event.y < 3*boxHeight:
                data.mode = "parametric3D2PList"
            elif 3*boxHeight <= event.y <= 4*boxHeight:
                data.mode = "parametric3D1PList"
    
    elif data.mode in ["function3DList", "parametric3D2PList", "parametric3D1PList"]:
        mousePressed3DList(event, data)
    elif data.mode in ["function3DInput", "parametric3D2PInput", "parametric3D1PInput"]:
        mousePressed3DInput(event, data)


def mousePressed3DList(event, data):
    if data.mode=="function3DList":
        graphList = data.graphsFunction3D
        inputMode = "function3DInput"
        boxFactor = 1
    elif data.mode=="parametric3D2PList":
        graphList = data.graphsParametric3D2P
        inputMode = "parametric3D2PInput"
        boxFactor = 2
    elif data.mode=="parametric3D1PList":        
        graphList = data.graphsParametric3D1P
        inputMode = "parametric3D1PInput"
        boxFactor = 2
    # click return box
    boxWidth, boxHeight = data.returnBoxSize[0], data.returnBoxSize[1]
    if event.x<=boxWidth and event.y<=boxHeight:
        data.mode = "options3D"
    # brings you to input screen
    boxHeight = data.equationBoxSize[1]*boxFactor
    if event.y>=boxHeight/boxFactor:
        whichFunction = int((event.y-boxHeight/boxFactor-data.listScroll)/boxHeight)
        if whichFunction==len(graphList):
            data.modifyIndex = "new"
            data.mode = inputMode
        elif whichFunction<len(graphList):
            data.modifyIndex = whichFunction
            data.inputs = graphList[whichFunction].display
            data.mode = inputMode
            getCursorPosition(data)


def mousePressed3DInput(event, data):
    if data.mode=="function3DInput":
        graphList = data.graphsFunction3D
        listMode = "function3DList"
        classType = Function3D
        keyMask = data.function3DKeyMask
    elif data.mode=="parametric3D2PInput":
        graphList = data.graphsParametric3D2P
        listMode = "parametric3D2PList"
        classType = Parametric3D2P
        keyMask = data.parametric3D2PKeyMask
    elif data.mode=="parametric3D1PInput":
        graphList = data.graphsParametric3D1P
        listMode = "parametric3D1PList"
        classType = Parametric3D1P
        keyMask = data.parametric3D1PKeyMask
    # click return box
    boxWidth, boxHeight = data.returnBoxSize[0], data.returnBoxSize[1]
    if event.x<=boxWidth and event.y<=boxHeight:
        data.mode = listMode
        (data.inputs, data.cursorListPosition, data.cursorPosition) = ([], 0, [0,0])
    # click Go box (enter function)
    elif data.width-boxWidth<=event.x and event.y<=boxHeight:
        if data.modifyIndex=="new":
            try:
                graphList.append(classType(data.inputs))
                (data.inputs, data.cursorListPosition, data.cursorPosition) = ([], 0, [0,0])
                data.mode = listMode
            except:
                pass
        else:
            try:
                graphList[data.modifyIndex] = classType(data.inputs)
                (data.inputs, data.cursorListPosition, data.cursorPosition) = ([], 0, [0,0])
                data.mode = listMode
            except:
                pass
    # click Delete box
    elif data.width-2*boxWidth<=event.x<=data.width-boxWidth and event.y<=boxHeight:
        if data.modifyIndex != "new":
            graphList.pop(data.modifyIndex)
            (data.inputs, data.cursorListPosition, data.cursorPosition) = ([], 0, [0,0])
            data.mode = listMode
    else:
        if data.keyboardMode=="trig":
            keys = data.calcKeyboardTrig
        else:
            keys = data.calcKeyboardInv
        numCols = len(keys[0])
        numRows = len(keys)
        buttonWidth = data.width/numCols
        buttonHeight = buttonWidth*2/3
        topLeft = [0, data.height-numRows*buttonHeight]
        if event.x>=topLeft[0] and event.y>=topLeft[1]:
            col = int((event.x-topLeft[0])/buttonWidth)
            row = int((event.y-topLeft[1])/buttonHeight)
            if (row,col) == (0,0):
                if data.keyboardMode=="trig":
                    data.keyboardMode = "inv"
                else:
                    data.keyboardMode = "trig"
            elif keyMask[row][col]==1:
                data.inputs.insert(data.cursorListPosition, keys[row][col])
                data.cursorListPosition += 1
                getCursorPosition(data)

################################################################################
## DRAW
################################################################################

def drawOptions3DMode(canvas, data):
    # draw return box
    boxWidth, boxHeight = data.returnBoxSize[0], data.returnBoxSize[1]
    canvas.create_rectangle((0,0), (boxWidth,boxHeight), width=1)
    canvas.create_text((boxWidth/2,boxHeight/2), text="Return",\
        font="Arial "+str(int(boxHeight/2)))
    # draws other boxes
    boxWidth, boxHeight = data.options3DBoxSize[0], data.options3DBoxSize[1]
    canvas.create_rectangle((data.width/2-boxWidth/2,boxHeight),\
        (data.width/2+boxWidth/2,2*boxHeight), width=1)
    canvas.create_text((data.width/2,3*boxHeight/2),\
        text="Functions", font="Arial "+str(int(boxHeight/4)))
    
    canvas.create_rectangle((data.width/2-boxWidth/2,2*boxHeight),\
        (data.width/2+boxWidth/2,3*boxHeight), width=1)
    canvas.create_text((data.width/2,5*boxHeight/2),\
        text="Parametric (2 Parameters)", font="Arial "+str(int(boxHeight/4)))
    
    canvas.create_rectangle((data.width/2-boxWidth/2,3*boxHeight),\
        (data.width/2+boxWidth/2,4*boxHeight), width=1)
    canvas.create_text((data.width/2,7*boxHeight/2),\
        text="Parametric (1 Parameter)", font="Arial "+str(int(boxHeight/4)))


def draw3DList(canvas, data):
    if data.mode=="function3DList":
        graphList = data.graphsFunction3D
        boxFactor = 1
    elif data.mode=="parametric3D2PList":
        graphList = data.graphsParametric3D2P
        boxFactor = 2
    elif data.mode=="parametric3D1PList":        
        graphList = data.graphsParametric3D1P
        boxFactor = 2
    # draws every 3D function
    boxWidth, boxHeight = data.equationBoxSize[0], data.equationBoxSize[1]*boxFactor
    margin = data.width/20
    for i in range(len(graphList)+1):
        canvas.create_rectangle((0,boxHeight*i+data.equationBoxSize[1]+data.listScroll),\
            (boxWidth,boxHeight*(i+1)+data.equationBoxSize[1]+data.listScroll), width=1)
        # add function
        if i==len(graphList):
            canvas.create_text((data.width/2,boxHeight*(i+0.5)+data.equationBoxSize[1]+data.listScroll),\
                text="+", fill="lime green", font="Arial "+str(int(boxHeight/2/boxFactor)))
        # existing functions
        else:
            canvas.create_text((margin,boxHeight*(i+0.5)+data.equationBoxSize[1]+data.listScroll),\
                anchor="w", text=formEquationString(graphList[i].display),\
                font="Courier "+str(int(boxHeight/5/boxFactor)))
    canvas.create_rectangle((0,0), (data.width,data.equationBoxSize[1]), width=0, fill="white")
    # draw return box
    boxWidth, boxHeight = data.returnBoxSize[0], data.returnBoxSize[1]
    canvas.create_rectangle((0,0), (boxWidth,boxHeight), width=1)
    canvas.create_text((boxWidth/2,boxHeight/2), text="Return",\
        font="Arial "+str(int(boxHeight/2)))


def draw3DInput(canvas, data):
    if data.mode=="function3DInput":
        keyMask = data.function3DKeyMask
    elif data.mode=="parametric3D2PInput":
        keyMask = data.parametric3D2PKeyMask
    elif data.mode=="parametric3D1PInput":        
        keyMask = data.parametric3D1PKeyMask
    # draw return box
    boxWidth, boxHeight = data.returnBoxSize[0], data.returnBoxSize[1]
    canvas.create_rectangle((0,0), (boxWidth,boxHeight), width=1)
    canvas.create_text((boxWidth/2,boxHeight/2), text="Return",\
        font="Arial "+str(int(boxHeight/2)))
    # draw Go box
    canvas.create_rectangle((data.width-boxWidth,0), (data.width,boxHeight), width=1)
    canvas.create_text((data.width-boxWidth/2,boxHeight/2), text="Go",\
        font="Arial "+str(int(boxHeight/2)))
    # draw Delete box
    if data.modifyIndex != "new":
        canvas.create_rectangle((data.width-2*boxWidth,0), (data.width-boxWidth,boxHeight), width=1)
        canvas.create_text((data.width-3*boxWidth/2,boxHeight/2), fill="red", text="Delete",\
            font="Arial "+str(int(boxHeight/2)))
    
    if data.keyboardMode=="trig":
        keys = data.calcKeyboardTrig
    else:
        keys = data.calcKeyboardInv
    numCols = len(keys[0])
    numRows = len(keys)
    buttonWidth = data.width/numCols
    buttonHeight = buttonWidth*2/3
    topLeft = [0, data.height-numRows*buttonHeight]
    for row in range(numRows):
        for col in range(numCols):
            if keyMask[row][col]==1:
                boxColor = "white"
                textColor = "black"
            else:
                boxColor = "gray70"
                textColor = "gray30"
            canvas.create_rectangle((topLeft[0]+col*buttonWidth,topLeft[1]+row*buttonHeight),\
                (topLeft[0]+(col+1)*buttonWidth,topLeft[1]+(row+1)*buttonHeight), width=1, fill=boxColor)
            canvas.create_text((topLeft[0]+(col+0.5)*buttonWidth,topLeft[1]+(row+0.5)*buttonHeight),\
                text=keys[row][col], fill=textColor, font="Courier "+str(int(buttonHeight/3)))
    margin = data.width/20
    canvas.create_text((margin,data.height/3), anchor="w", text=formEquationString(data.inputs),\
        font="Courier "+str(int(buttonHeight/2)))
    textHeight = data.textHeight
    textWidth = data.textWidth
    canvas.create_line((margin+data.cursorPosition[0],data.height/3+data.cursorPosition[1]-textHeight/2),\
        (margin+data.cursorPosition[0],data.height/3+data.cursorPosition[1]+textHeight/2), width=1)

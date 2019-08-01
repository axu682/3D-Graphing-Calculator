# draws graph3D mode
import math, copy

# rgbString funciton taken from 15-112 course website

################################################################################
## HELPER FUNCTIONS
################################################################################

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

# turns cartesian coordinates to pixel coordinates
def cartesianToPixel(data, cartX, cartY, cartZ):
    pixelX = (cartX-data.axisMin[0])/(data.axisMax[0]-data.axisMin[0])*\
        (data.width*data.boxSize)\
        + (data.centerBoxX-data.width*(0.5*data.boxSize))
    pixelY = (cartY-data.axisMin[1])/(data.axisMax[1]-data.axisMin[1])*\
        (data.width*data.boxSize)\
        - data.width*(0.5*data.boxSize)
    pixelZ = (cartZ-data.axisMin[2])/(data.axisMax[2]-data.axisMin[2])*\
        (data.height*data.boxSize)\
        + (data.centerBoxZ-data.width*(0.5*data.boxSize))
    return (pixelX, pixelY, pixelZ)

# takes pixel coordinates and rotates them
def rotate(data, pixelX, pixelY, pixelZ, cX, cY, cZ):
    aXY, aYZ, aXZ = data.xyTheta, data.yzTheta, data.xzTheta
    x = pixelX-cX
    y = pixelY-cY
    z = pixelZ-cZ
    # xy-rotation
    x, y = x*math.cos(aXY)-y*math.sin(aXY), x*math.sin(aXY)+y*math.cos(aXY)
    # yz-rotation
    y, z = y*math.cos(aYZ)-z*math.sin(aYZ), y*math.sin(aYZ)+z*math.cos(aYZ)
    # xz-rotation
    x, z = x*math.cos(aXZ)-z*math.sin(aXZ), x*math.sin(aXZ)+z*math.cos(aXZ)
    x += cX
    y += cY
    z += cZ
    rotatedX, rotatedY, rotatedZ = x, y, z
    return (rotatedX, rotatedY, rotatedZ)

def perspective(data, rotatedX, rotatedY, rotatedZ, cX, cY, cZ):
    if not data.perspectiveOn:
        return (rotatedX, rotatedZ)
    # default distance is distance from camera at rotatedY=cY
    # rotatedX and rotatedZ coordinates don't contribute to distance
    rotatedX -= cX
    rotatedY -= cY
    rotatedZ -= cZ
    defaultDistance = data.cameraDistance*(data.boxSize*data.width)
    distanceToCamera = rotatedY + defaultDistance
    scaleFactor = defaultDistance/distanceToCamera
    rotatedX, rotatedZ = rotatedX*scaleFactor, rotatedZ*scaleFactor
    rotatedX += cX
    rotatedY += cY
    rotatedZ += cZ
    perspectiveX, perspectiveZ = rotatedX, rotatedZ
    return (perspectiveX, perspectiveZ)

def cartesianToPerspective(data, cartX, cartY, cartZ):
    pixelX, pixelY, pixelZ = cartesianToPixel(data, cartX, cartY, cartZ)
    rotatedX, rotatedY, rotatedZ = rotate(data, pixelX, pixelY, pixelZ,\
        data.centerBoxX, 0, data.centerBoxZ)
    perspX, perspZ = perspective(data, rotatedX, rotatedY, rotatedZ,\
        data.centerBoxX, 0, data.centerBoxZ)
    return (perspX, perspZ)

# gets size of dot based on y coordinate
def getDotSize(data, rotatedY):
    rotatedY /= (data.boxSize*data.width*(3**0.5))
    scaleY = 1 - (rotatedY+0.5)
    dotSize = scaleY*(data.maxDotSize-data.minDotSize) + data.minDotSize
    return dotSize

def fadeColor(defaultR, defaultG, defaultB, R, G, B, fade):
    fadedR = (1-fade)*R + fade*defaultR
    fadedG = (1-fade)*G + fade*defaultG
    fadedB = (1-fade)*B + fade*defaultB
    return rgbString(int(fadedR), int(fadedG), int(fadedB))

def getPointColor(data, rotatedY, printRGB):
    rotatedY /= (data.boxSize*data.width*(3**0.5))
    fade = (rotatedY+0.5)*data.colorFade
    return fadeColor(data.backgroundRGB[0], data.backgroundRGB[1],\
        data.backgroundRGB[2], printRGB[0], printRGB[1], printRGB[2], fade)

def getGridInterval(rangeSize):
    if rangeSize==0.8:
        return .2
    elif rangeSize>0.8:
        powerOfTen = 0
        while rangeSize>=8:
            rangeSize /= 10
            powerOfTen += 1
        if rangeSize>=4:
            return 1*(10**powerOfTen)
        elif rangeSize>=2:
            return 0.5*(10**powerOfTen)
        else:
            return 0.2*(10**powerOfTen)
    else:
        powerOfTen = 0
        while rangeSize<0.8:
            rangeSize *= 10
            powerOfTen -= 1
        if rangeSize>=4:
            return 1*(10**powerOfTen)
        elif rangeSize>=2:
            return 0.5*(10**powerOfTen)
        else:
            return 0.2*(10**powerOfTen)

def getIntervalList(lower, upper, interval):
    result = []
    start = math.ceil(lower/interval)*interval
    while start<=upper:
        result.append(start)
        start += interval
    return result

def getLastDigitPlace(rangeSize):
    return(math.floor(math.log(rangeSize/4,10)))

def roundAxisNum(num, xLastDigitPlace):
    result = round(num, -xLastDigitPlace)
    if result==int(result):
        return int(result)
    return result

################################################################################
## DRAW FUNCTIONS
################################################################################

# takes an axis, draws it
def drawAxis(canvas, data, axis):
    # T refers to text coordinates
    axisColorR = 255-data.backgroundRGB[0]
    axisColorG = 255-data.backgroundRGB[1]
    axisColorB = 255-data.backgroundRGB[2]
    color = rgbString(axisColorR, axisColorG, axisColorB)
    if axis=="x":
        cartX1, cartY1, cartZ1 = data.axisMin[0]-(data.axisMax[0]-data.axisMin[0])*0.1, 0, 0
        cartX2, cartY2, cartZ2 = data.axisMax[0]+(data.axisMax[0]-data.axisMin[0])*0.1, 0, 0
        cartXT, cartYT, cartZT = data.axisMax[0]+(data.axisMax[0]-data.axisMin[0])*0.2, 0, 0
        labelColor = "chocolate3"
    elif axis=="y":
        cartX1, cartY1, cartZ1 = 0, data.axisMin[1]-(data.axisMax[1]-data.axisMin[1])*0.1, 0
        cartX2, cartY2, cartZ2 = 0, data.axisMax[1]+(data.axisMax[1]-data.axisMin[1])*0.1, 0
        cartXT, cartYT, cartZT = 0, data.axisMax[1]+(data.axisMax[1]-data.axisMin[1])*0.2, 0
        labelColor = "dodger blue"
    elif axis=="z":
        cartX1, cartY1, cartZ1 = 0, 0, data.axisMin[2]-(data.axisMax[2]-data.axisMin[2])*0.1
        cartX2, cartY2, cartZ2 = 0, 0, data.axisMax[2]+(data.axisMax[2]-data.axisMin[2])*0.1
        cartXT, cartYT, cartZT = 0, 0, data.axisMax[2]+(data.axisMax[2]-data.axisMin[2])*0.2
        labelColor = "DarkOrchid4"
    perspX1, perspZ1 = cartesianToPerspective(data, cartX1, cartY1, cartZ1)
    perspX2, perspZ2 = cartesianToPerspective(data, cartX2, cartY2, cartZ2)
    perspXT, perspZT = cartesianToPerspective(data, cartXT, cartYT, cartZT)
    canvas.create_line((perspX1,data.height-perspZ1),\
        (perspX2,data.height-perspZ2), width=3, fill=color)
    canvas.create_text((perspXT,data.height-perspZT), text=axis,\
        font="Times "+str(int(data.width/30))+" bold italic", fill=labelColor)

# draws boundary box
def drawBoundary(canvas, data):
    axisColorR = 255-data.backgroundRGB[0]
    axisColorG = 255-data.backgroundRGB[1]
    axisColorB = 255-data.backgroundRGB[2]
    color = fadeColor(data.backgroundRGB[0], data.backgroundRGB[1],\
        data.backgroundRGB[2], axisColorR, axisColorG, axisColorB, 0.6)
    cX = data.centerBoxX
    cZ = data.centerBoxZ
    d = data.width*(0.5*data.boxSize)
    # 8 vertices
    """ positive y: 5---1
                    |   |
                    6---2
                    
        negative y: 7---3
                    |   |
                    8---4
    """
    boundXs = [cX+d, cX+d, cX+d, cX+d, cX-d, cX-d, cX-d, cX-d]
    boundYs = [   d,    d,   -d,   -d,    d,    d,   -d,   -d]
    boundZs = [cZ+d, cZ-d, cZ+d, cZ-d, cZ+d, cZ-d, cZ+d, cZ-d]
    perspBoundXs = [0 for i in range(8)]
    perspBoundYs = [0 for i in range(8)]
    perspBoundZs = [0 for i in range(8)]
    for i in range(8):
        perspBoundXs[i], perspBoundYs[i], perspBoundZs[i] =\
            rotate(data, boundXs[i], boundYs[i], boundZs[i], cX, 0, cZ)
        perspBoundXs[i], perspBoundZs[i] =\
            perspective(data, perspBoundXs[i], perspBoundYs[i], perspBoundZs[i],\
                data.centerBoxX, 0, data.centerBoxZ)
    # 12 edges
    for pair in [(1,5), (2,6), (1,2), (5,6), (3,7), (4,8),\
        (3,4), (7,8), (1,3), (2,4), (5,7), (6,8)]:
        point1 = pair[0]-1
        point2 = pair[1]-1
        canvas.create_line((perspBoundXs[point1],\
            data.height-perspBoundZs[point1]),\
            (perspBoundXs[point2],data.height-perspBoundZs[point2]),\
            width=1, fill=color)

def drawGrids(canvas, data):
    axisColorR = 255-data.backgroundRGB[0]
    axisColorG = 255-data.backgroundRGB[1]
    axisColorB = 255-data.backgroundRGB[2]
    color = fadeColor(data.backgroundRGB[0], data.backgroundRGB[1],\
        data.backgroundRGB[2], axisColorR, axisColorG, axisColorB, 0.8)
    xValues = getIntervalList(data.axisMin[0], data.axisMax[0],\
        getGridInterval(data.axisMax[0]-data.axisMin[0]))
    yValues = getIntervalList(data.axisMin[1], data.axisMax[1],\
        getGridInterval(data.axisMax[1]-data.axisMin[1]))
    zValues = getIntervalList(data.axisMin[2], data.axisMax[2],\
        getGridInterval(data.axisMax[2]-data.axisMin[2]))
    xLastDigitPlace = getLastDigitPlace(data.axisMax[0]-data.axisMin[0])
    yLastDigitPlace = getLastDigitPlace(data.axisMax[1]-data.axisMin[1])
    zLastDigitPlace = getLastDigitPlace(data.axisMax[2]-data.axisMin[2])

    xAlongAxis = []
    xAlongY = []
    xAlongZ = []
    for i in range(len(xValues)):
        xAlongAxis.append([xValues[i],data.axisMin[1],data.axisMin[2]])
        xAxisText = copy.deepcopy(xAlongAxis)
        
        if data.showGrid:
            xAlongAxis[i] = cartesianToPerspective\
                (data, xAlongAxis[i][0], xAlongAxis[i][1], xAlongAxis[i][2])
            
            xAlongY.append([xValues[i],data.axisMax[1],data.axisMin[2]])
            xAlongY[i] = cartesianToPerspective\
                (data, xAlongY[i][0], xAlongY[i][1], xAlongY[i][2])
            canvas.create_line((xAlongAxis[i][0],data.height-xAlongAxis[i][1]),\
                (xAlongY[i][0],data.height-xAlongY[i][1]), fill=color)
            
            xAlongZ.append([xValues[i],data.axisMin[1],data.axisMax[2]])
            xAlongZ[i] = cartesianToPerspective\
                (data, xAlongZ[i][0], xAlongZ[i][1], xAlongZ[i][2])
            canvas.create_line((xAlongAxis[i][0],data.height-xAlongAxis[i][1]),\
                (xAlongZ[i][0],data.height-xAlongZ[i][1]), fill=color)
        
        if data.showGridNums:
            xAxisText[i][1] -= 0.05*(data.axisMax[1]-data.axisMin[1])
            xAxisText[i][2] -= 0.05*(data.axisMax[2]-data.axisMin[2])
            xAxisText[i] = cartesianToPerspective\
                (data, xAxisText[i][0], xAxisText[i][1], xAxisText[i][2])
            canvas.create_text((xAxisText[i][0],data.height-xAxisText[i][1]),\
                text=roundAxisNum(xValues[i],xLastDigitPlace), fill="tan1",\
                font="Courier "+str(int(data.height/60)))
    
    yAlongAxis = []
    yAlongX = []
    yAlongZ = []
    for i in range(len(yValues)):
        yAlongAxis.append([data.axisMin[0],yValues[i],data.axisMin[2]])
        yAxisText = copy.deepcopy(yAlongAxis)
        
        if data.showGrid:
            yAlongAxis[i] = cartesianToPerspective\
                (data, yAlongAxis[i][0], yAlongAxis[i][1], yAlongAxis[i][2])
            
            yAlongX.append([data.axisMax[0],yValues[i],data.axisMin[2]])
            yAlongX[i] = cartesianToPerspective\
                (data, yAlongX[i][0], yAlongX[i][1], yAlongX[i][2])
            canvas.create_line((yAlongAxis[i][0],data.height-yAlongAxis[i][1]),\
                (yAlongX[i][0],data.height-yAlongX[i][1]), fill=color)
            
            yAlongZ.append([data.axisMin[0],yValues[i],data.axisMax[2]])
            yAlongZ[i] = cartesianToPerspective\
                (data, yAlongZ[i][0], yAlongZ[i][1], yAlongZ[i][2])
            canvas.create_line((yAlongAxis[i][0],data.height-yAlongAxis[i][1]),\
                (yAlongZ[i][0],data.height-yAlongZ[i][1]), fill=color)
        
        if data.showGridNums:
            yAxisText[i][0] -= 0.05*(data.axisMax[0]-data.axisMin[0])
            yAxisText[i][2] -= 0.05*(data.axisMax[2]-data.axisMin[2])
            yAxisText[i] = cartesianToPerspective\
                (data, yAxisText[i][0], yAxisText[i][1], yAxisText[i][2])
            canvas.create_text((yAxisText[i][0],data.height-yAxisText[i][1]),\
                text=roundAxisNum(yValues[i],yLastDigitPlace), fill="SteelBlue1",\
                font="Courier "+str(int(data.height/60)))
    
    zAlongAxis = []
    zAlongX = []
    zAlongY = []
    for i in range(len(zValues)):
        zAlongAxis.append([data.axisMin[0],data.axisMin[1],zValues[i]])
        zAxisText = copy.deepcopy(zAlongAxis)
        
        if data.showGrid:
            zAlongAxis[i] = cartesianToPerspective\
                (data, zAlongAxis[i][0], zAlongAxis[i][1], zAlongAxis[i][2])
            
            zAlongX.append([data.axisMax[0],data.axisMin[1],zValues[i]])
            zAlongX[i] = cartesianToPerspective\
                (data, zAlongX[i][0], zAlongX[i][1], zAlongX[i][2])
            canvas.create_line((zAlongAxis[i][0],data.height-zAlongAxis[i][1]),\
                (zAlongX[i][0],data.height-zAlongX[i][1]), fill=color)
            
            zAlongY.append([data.axisMin[0],data.axisMax[1],zValues[i]])
            zAlongY[i] = cartesianToPerspective\
                (data, zAlongY[i][0], zAlongY[i][1], zAlongY[i][2])
            canvas.create_line((zAlongAxis[i][0],data.height-zAlongAxis[i][1]),\
                (zAlongY[i][0],data.height-zAlongY[i][1]), fill=color)
        
        if data.showGridNums:
            zAxisText[i][0] -= 0.05*(data.axisMax[0]-data.axisMin[0])
            zAxisText[i][1] -= 0.05*(data.axisMax[1]-data.axisMin[1])
            zAxisText[i] = cartesianToPerspective\
                (data, zAxisText[i][0], zAxisText[i][1], zAxisText[i][2])
            canvas.create_text((zAxisText[i][0],data.height-zAxisText[i][1]),\
                text=roundAxisNum(zValues[i],zLastDigitPlace), fill="DarkOrchid1",\
                font="Courier "+str(int(data.height/60)))


def drawGraph3DMode(canvas, data):
    canvas.create_rectangle((0,0), (data.width,data.height), width=0,\
        fill=rgbString(data.backgroundRGB[0], data.backgroundRGB[1],\
        data.backgroundRGB[2]))
    if data.showGrid or data.showGridNums:
        drawGrids(canvas, data)
    if data.showBoundary:
        drawBoundary(canvas, data)
    if data.showPoints or data.showWires:
        for graph in data.graphsFunction3D:
            graph.drawPoints(data, canvas)
        for graph in data.graphsParametric3D2P:
            graph.drawPoints(data, canvas)
        for graph in data.graphsParametric3D1P:
            graph.drawPoints(data, canvas)
    if data.showWires:
        for graph in data.graphsFunction3D:
            graph.drawWires(data, canvas)
        for graph in data.graphsParametric3D2P:
            graph.drawWires(data, canvas)
        for graph in data.graphsParametric3D1P:
            graph.drawWires(data, canvas)
    # draw axes
    if (data.axisMin[1]<=0<=data.axisMax[1]) and (data.axisMin[2]<=0<=data.axisMax[2]):
        drawAxis(canvas, data, "x")
    if (data.axisMin[0]<=0<=data.axisMax[0]) and (data.axisMin[2]<=0<=data.axisMax[2]):
        drawAxis(canvas, data, "y")
    if (data.axisMin[0]<=0<=data.axisMax[0]) and (data.axisMin[1]<=0<=data.axisMax[1]):
        drawAxis(canvas, data, "z")
    # settings/graphs/help boxes
    boxWidth, boxHeight =\
        data.settingsGraphsBoxSize[0], data.settingsGraphsBoxSize[1]
    canvas.create_rectangle((data.width-boxWidth,0),\
        (data.width,boxHeight), width=1)
    canvas.create_text((data.width-boxWidth/2,boxHeight/2),\
        text="Settings", font="Arial "+str(int(boxHeight/3)))
    canvas.create_rectangle((data.width-boxWidth,boxHeight),\
        (data.width,2*boxHeight), width=1)
    canvas.create_text((data.width-boxWidth/2,3*boxHeight/2),\
        text="Graphs", font="Arial "+str(int(boxHeight/3)))
    canvas.create_rectangle((data.width-boxWidth,data.height-boxHeight),\
        (data.width,data.height), width=1)
    canvas.create_text((data.width-boxWidth/2,data.height-boxHeight/2),\
        text="Help", font="Arial "+str(int(boxHeight/3)))
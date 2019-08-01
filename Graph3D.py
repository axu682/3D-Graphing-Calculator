# contains classes for the three different graph types
import math, copy
from Evaluator import *
from tkinter import *

# rgbString funciton taken from 15-112 course website

################################################################################
## FUNCTION3D
################################################################################
class Function3D(object):
    def __init__(self, function):
        self.display = copy.copy(function)
        if function[0]=="x":
            self.inVar1 = 1
            self.inVar2 = 2
            self.outVar = 0
            self.in1 = "y"
            self.in2 = "z"
            self.out = "x"
        elif function[0]=="y":
            self.inVar1 = 0
            self.inVar2 = 2
            self.outVar = 1
            self.in1 = "x"
            self.in2 = "z"
            self.out = "y"
        else:
            self.inVar1 = 0
            self.inVar2 = 1
            self.outVar = 2
            self.in1 = "x"
            self.in2 = "y"
            self.out = "z"
        if "\n" in function:
            breakIndex = function.index("\n")
            self.function = function[:breakIndex]
            colorList = fuseNumbers(function[breakIndex+1:])
            self.graphRGB = [0,0,0]
            self.graphRGB[0] = colorList[1]
            self.graphRGB[1] = colorList[3]
            self.graphRGB[2] = colorList[5]
        else:
            self.function = function
            self.graphRGB = [0,0,0]
        self.rotatedPoints = None
    
    def f(self, var1, var2, function):
        funct = copy.copy(function)
        for i in range(len(funct)):
            if funct[i]=="π":
                funct[i] = math.pi
            elif funct[i]=="e":
                funct[i] = math.e
            elif funct[i]==self.in1:
                funct[i] = var1
            elif funct[i]==self.in2:
                funct[i] = var2
        result = evaluateExpression(funct)
        if result==None:
            assert(False)
        return result
    
    def setPoints(self, data):
        self.rotatedPoints = [[[0,0,0] for i in range(data.res+1)] for i in\
            range(data.res+1)]
        function = fuseNumbers(self.function[2:])
        for row in range(data.res+1):
            for col in range(data.res+1):
                # getting cartesian coordinates
                inValue1 = (data.axisMax[self.inVar1]-data.axisMin[self.inVar1]) * (row/data.res) + data.axisMin[self.inVar1]
                inValue2 = (data.axisMax[self.inVar2]-data.axisMin[self.inVar2]) * (col/data.res) + data.axisMin[self.inVar2]
                try:
                    outValue = self.f(inValue1, inValue2, function)
                except:
                    self.rotatedPoints[row][col][self.inVar1] = None
                    continue
                if not (data.axisMin[self.outVar] <= outValue <= data.axisMax[self.outVar]):
                    self.rotatedPoints[row][col][self.inVar1] = None
                else:
                    self.rotatedPoints[row][col][self.inVar1],\
                        self.rotatedPoints[row][col][self.inVar2],\
                        self.rotatedPoints[row][col][self.outVar] =\
                        inValue1, inValue2, outValue
                    x, y, z = self.rotatedPoints[row][col][0], self.rotatedPoints[row][col][1], self.rotatedPoints[row][col][2]
                    pixelX, pixelY, pixelZ = cartesianToPixel(data, x, y, z)
                    rotated = rotate(data, pixelX, pixelY, pixelZ,\
                        data.centerBoxX, 0, data.centerBoxZ)
                    self.rotatedPoints[row][col][0],\
                        self.rotatedPoints[row][col][1],\
                        self.rotatedPoints[row][col][2] = rotated[0],\
                        rotated[1], rotated[2]
    
    def drawPoints(self, data, canvas):
        self.setPoints(data)
        for row in range(data.res+1):
            for col in range(data.res+1):
                try:
                    x, z = perspective(data, self.rotatedPoints[row][col][0],\
                        self.rotatedPoints[row][col][1],\
                        self.rotatedPoints[row][col][2],\
                        data.centerBoxX, 0, data.centerBoxZ)
                    r = getDotSize(data, self.rotatedPoints[row][col][1])
                    color = getPointColor(data, self.rotatedPoints[row][col][1],\
                        self.graphRGB)
                    if data.showPoints:
                        canvas.create_oval((x-r,data.height-z-r),\
                            (x+r,data.height-z+r), width=0, fill=color)
                except:
                    pass
    
    def drawWires(self, data, canvas):
        for row in range(data.res+1):
            for col in range(data.res+1):
                try:
                    perspX1, perspZ1 =\
                        perspective(data, self.rotatedPoints[row][col][0],\
                        self.rotatedPoints[row][col][1],\
                        self.rotatedPoints[row][col][2],\
                        data.centerBoxX, 0, data.centerBoxZ)
                    color = getPointColor(data, self.rotatedPoints[row][col][1],\
                        self.graphRGB)
                except:
                    continue
                try:
                    perspX2, perspZ2 =\
                        perspective(data, self.rotatedPoints[row+1][col][0],\
                        self.rotatedPoints[row+1][col][1],\
                        self.rotatedPoints[row+1][col][2],\
                        data.centerBoxX, 0, data.centerBoxZ)
                    canvas.create_line((perspX1,data.height-perspZ1),\
                        (perspX2,data.height-perspZ2), fill=color)
                except:
                    pass
                try:
                    perspX3, perspZ3 =\
                        perspective(data, self.rotatedPoints[row][col+1][0],\
                        self.rotatedPoints[row][col+1][1],\
                        self.rotatedPoints[row][col+1][2],\
                        data.centerBoxX, 0, data.centerBoxZ)
                    canvas.create_line((perspX1,data.height-perspZ1),\
                        (perspX3,data.height-perspZ3), fill=color)
                except:
                    pass

################################################################################
## PARAMETRIC3D2P
################################################################################

class Parametric3D2P(object):
    def __init__(self, function):
        self.display = copy.copy(function)
        f = copy.copy(function)
        breakIndex = f.index("\n")
        self.fX = f[:breakIndex]
        f = f[breakIndex+1:]
        breakIndex = f.index("\n")
        self.fY = f[:breakIndex]
        f = f[breakIndex+1:]
        breakIndex = f.index("\n")
        self.fZ = f[:breakIndex]
        f = f[breakIndex+1:]
        breakIndex = f.index("\n")
        tData = f[:breakIndex]
        f = f[breakIndex+1:]
        
        if "\n" in f:
            breakIndex = f.index("\n")
            uData = f[:breakIndex]
            f = f[breakIndex+1:]
            colorList = fuseNumbers(f)
            self.graphRGB = [0,0,0]
            self.graphRGB[0] = colorList[1]
            self.graphRGB[1] = colorList[3]
            self.graphRGB[2] = colorList[5]
        else:
            uData = f
            self.graphRGB = [0,0,0]
        
        breakIndex = tData.index(",")
        self.t1Min = evaluateExpression(subPiE(fuseNumbers(tData[:breakIndex])))
        tData = tData[breakIndex+1:]
        breakIndex = tData.index(",")
        self.t1Max = evaluateExpression(subPiE(fuseNumbers(tData[:breakIndex])))
        tData = tData[breakIndex+1:]
        self.t1Step = evaluateExpression(subPiE(fuseNumbers(tData)))
        
        breakIndex = uData.index(",")
        self.t2Min = evaluateExpression(subPiE(fuseNumbers(uData[:breakIndex])))
        uData = uData[breakIndex+1:]
        breakIndex = uData.index(",")

        self.t2Max = evaluateExpression(subPiE(fuseNumbers(uData[:breakIndex])))
        uData = uData[breakIndex+1:]
        self.t2Step = evaluateExpression(subPiE(fuseNumbers(uData)))
        
        self.rotatedPoints = None
        self.t1Values = None
        self.t2Values = None
        
    
    def f(self, t1Value, t2Value):
        # x = (4+math.cos(t1Value))*math.cos(t2Value)
        # y = (4+math.cos(t1Value))*math.sin(t2Value)
        # z = math.sin(t1Value)
        funct = fuseNumbers(self.fX[2:])
        for i in range(len(funct)):
            if funct[i]=="π":
                funct[i] = math.pi
            elif funct[i]=="e":
                funct[i] = math.e
            elif funct[i]=="t":
                funct[i] = t1Value
            elif funct[i]=="u":
                funct[i] = t2Value
        x = evaluateExpression(funct)
        if x==None:
            assert(False)
        
        funct = fuseNumbers(self.fY[2:])
        for i in range(len(funct)):
            if funct[i]=="π":
                funct[i] = math.pi
            elif funct[i]=="e":
                funct[i] = math.e
            elif funct[i]=="t":
                funct[i] = t1Value
            elif funct[i]=="u":
                funct[i] = t2Value
        y = evaluateExpression(funct)
        if y==None:
            assert(False)
        
        funct = fuseNumbers(self.fZ[2:])
        for i in range(len(funct)):
            if funct[i]=="π":
                funct[i] = math.pi
            elif funct[i]=="e":
                funct[i] = math.e
            elif funct[i]=="t":
                funct[i] = t1Value
            elif funct[i]=="u":
                funct[i] = t2Value
        z = evaluateExpression(funct)
        if z==None:
            assert(False)
        return (x, y, z)
    
    def setPoints(self, data):
        self.t1Values = getList(self.t1Min, self.t1Max, self.t1Step)
        self.t2Values = getList(self.t2Min, self.t2Max, self.t2Step)            
        self.rotatedPoints = [[[0,0,0] for i in range(len(self.t2Values))] for i in\
            range(len(self.t1Values))]
        for row in range(len(self.t1Values)):
            for col in range(len(self.t2Values)):
                # getting cartesian coordinates
                t1Value = self.t1Values[row]
                t2Value = self.t2Values[col]
                try:
                    x, y, z = self.f(t1Value, t2Value)
                except:
                    self.rotatedPoints[row][col][0] = None
                    continue
                if not (data.axisMin[0] <= x <= data.axisMax[0])\
                    or not (data.axisMin[1] <= y <= data.axisMax[1])\
                    or not (data.axisMin[2] <= z <= data.axisMax[2]):
                    self.rotatedPoints[row][col][0] = None
                else:
                    self.rotatedPoints[row][col][0],\
                        self.rotatedPoints[row][col][1],\
                        self.rotatedPoints[row][col][2] =\
                        x, y, z
                    pixelX, pixelY, pixelZ = cartesianToPixel(data, x, y, z)
                    rotated = rotate(data, pixelX, pixelY, pixelZ,\
                        data.centerBoxX, 0, data.centerBoxZ)
                    self.rotatedPoints[row][col][0],\
                        self.rotatedPoints[row][col][1],\
                        self.rotatedPoints[row][col][2] = rotated[0],\
                        rotated[1], rotated[2]
    
    def drawPoints(self, data, canvas):
        self.setPoints(data)
        for row in range(len(self.t1Values)):
            for col in range(len(self.t2Values)):
                try:
                    x, z = perspective(data, self.rotatedPoints[row][col][0],\
                        self.rotatedPoints[row][col][1],\
                        self.rotatedPoints[row][col][2],\
                        data.centerBoxX, 0, data.centerBoxZ)
                    r = getDotSize(data, self.rotatedPoints[row][col][1])
                    color = getPointColor(data, self.rotatedPoints[row][col][1],\
                        self.graphRGB)
                    if data.showPoints:
                        canvas.create_oval((x-r,data.height-z-r),\
                            (x+r,data.height-z+r), width=0, fill=color)
                except:
                    pass
    
    def drawWires(self, data, canvas):
        for row in range(len(self.t1Values)):
            for col in range(len(self.t2Values)):
                try:
                    perspX1, perspZ1 =\
                        perspective(data, self.rotatedPoints[row][col][0],\
                        self.rotatedPoints[row][col][1],\
                        self.rotatedPoints[row][col][2],\
                        data.centerBoxX, 0, data.centerBoxZ)
                    color = getPointColor(data, self.rotatedPoints[row][col][1],\
                        self.graphRGB)
                except:
                    continue
                try:
                    perspX2, perspZ2 =\
                        perspective(data, self.rotatedPoints[row+1][col][0],\
                        self.rotatedPoints[row+1][col][1],\
                        self.rotatedPoints[row+1][col][2],\
                        data.centerBoxX, 0, data.centerBoxZ)
                    canvas.create_line((perspX1,data.height-perspZ1),\
                        (perspX2,data.height-perspZ2), fill=color)
                except:
                    pass
                try:
                    perspX3, perspZ3 =\
                        perspective(data, self.rotatedPoints[row][col+1][0],\
                        self.rotatedPoints[row][col+1][1],\
                        self.rotatedPoints[row][col+1][2],\
                        data.centerBoxX, 0, data.centerBoxZ)
                    canvas.create_line((perspX1,data.height-perspZ1),\
                        (perspX3,data.height-perspZ3), fill=color)
                except:
                    pass

################################################################################
## PARAMETRIC3D1P
################################################################################

class Parametric3D1P(object):
    def __init__(self, function):
        self.display = copy.copy(function)
        f = copy.copy(function)
        breakIndex = f.index("\n")
        self.fX = f[:breakIndex]
        f = f[breakIndex+1:]
        breakIndex = f.index("\n")
        self.fY = f[:breakIndex]
        f = f[breakIndex+1:]
        breakIndex = f.index("\n")
        self.fZ = f[:breakIndex]
        f = f[breakIndex+1:]
        
        if "\n" in f:
            breakIndex = f.index("\n")
            tData = f[:breakIndex]
            f = f[breakIndex+1:]
            colorList = fuseNumbers(f)
            self.graphRGB = [0,0,0]
            self.graphRGB[0] = colorList[1]
            self.graphRGB[1] = colorList[3]
            self.graphRGB[2] = colorList[5]
        else:
            tData = f
            self.graphRGB = [0,0,0]
        
        breakIndex = tData.index(",")
        self.tMin = evaluateExpression(subPiE(fuseNumbers(tData[:breakIndex])))
        tData = tData[breakIndex+1:]
        breakIndex = tData.index(",")
        self.tMax = evaluateExpression(subPiE(fuseNumbers(tData[:breakIndex])))
        tData = tData[breakIndex+1:]
        self.tStep = evaluateExpression(subPiE(fuseNumbers(tData)))
        
        self.rotatedPoints = None
        self.tValues = None
    
    def f(self, tValue):
        funct = fuseNumbers(self.fX[2:])
        for i in range(len(funct)):
            if funct[i]=="π":
                funct[i] = math.pi
            elif funct[i]=="e":
                funct[i] = math.e
            elif funct[i]=="t":
                funct[i] = tValue
        x = evaluateExpression(funct)
        if x==None:
            assert(False)
        
        funct = fuseNumbers(self.fY[2:])
        for i in range(len(funct)):
            if funct[i]=="π":
                funct[i] = math.pi
            elif funct[i]=="e":
                funct[i] = math.e
            elif funct[i]=="t":
                funct[i] = tValue
        y = evaluateExpression(funct)
        if y==None:
            assert(False)
        
        funct = fuseNumbers(self.fZ[2:])
        for i in range(len(funct)):
            if funct[i]=="π":
                funct[i] = math.pi
            elif funct[i]=="e":
                funct[i] = math.e
            elif funct[i]=="t":
                funct[i] = tValue
        z = evaluateExpression(funct)
        if z==None:
            assert(False)
        return (x, y, z)
    
    def setPoints(self, data):
        self.tValues = getList(self.tMin, self.tMax, self.tStep)            
        self.rotatedPoints = [[0,0,0] for i in range(len(self.tValues))] 
        for tIndex in range(len(self.tValues)):
            # getting cartesian coordinates
            tValue = self.tValues[tIndex]
            try:
                x, y, z = self.f(tValue)
            except:
                self.rotatedPoints[tIndex][0] = None
                continue
            if not (data.axisMin[0] <= x <= data.axisMax[0])\
                or not (data.axisMin[1] <= y <= data.axisMax[1])\
                or not (data.axisMin[2] <= z <= data.axisMax[2]):
                self.rotatedPoints[tIndex][0] = None
            else:
                self.rotatedPoints[tIndex][0],\
                    self.rotatedPoints[tIndex][1],\
                    self.rotatedPoints[tIndex][2] =\
                    x, y, z
                pixelX, pixelY, pixelZ = cartesianToPixel(data, x, y, z)
                rotated = rotate(data, pixelX, pixelY, pixelZ,\
                    data.centerBoxX, 0, data.centerBoxZ)
                self.rotatedPoints[tIndex][0],\
                    self.rotatedPoints[tIndex][1],\
                    self.rotatedPoints[tIndex][2] = rotated[0],\
                    rotated[1], rotated[2]
    
    def drawPoints(self, data, canvas):
        self.setPoints(data)
        for tIndex in range(len(self.tValues)):
            try:
                x, z = perspective(data, self.rotatedPoints[tIndex][0],\
                    self.rotatedPoints[tIndex][1],\
                    self.rotatedPoints[tIndex][2],\
                    data.centerBoxX, 0, data.centerBoxZ)
                r = getDotSize(data, self.rotatedPoints[tIndex][1])
                color = getPointColor(data, self.rotatedPoints[tIndex][1],\
                    self.graphRGB)
                if data.showPoints:
                    canvas.create_oval((x-r,data.height-z-r),\
                        (x+r,data.height-z+r), width=0, fill=color)
            except:
                pass
    
    def drawWires(self, data, canvas):
        for tIndex in range(len(self.tValues)):
            try:
                perspX1, perspZ1 =\
                    perspective(data, self.rotatedPoints[tIndex][0],\
                    self.rotatedPoints[tIndex][1],\
                    self.rotatedPoints[tIndex][2],\
                    data.centerBoxX, 0, data.centerBoxZ)
                color = getPointColor(data, self.rotatedPoints[tIndex][1],\
                    self.graphRGB)
            except:
                continue
            try:
                perspX2, perspZ2 =\
                    perspective(data, self.rotatedPoints[tIndex+1][0],\
                    self.rotatedPoints[tIndex+1][1],\
                    self.rotatedPoints[tIndex+1][2],\
                    data.centerBoxX, 0, data.centerBoxZ)
                canvas.create_line((perspX1,data.height-perspZ1),\
                    (perspX2,data.height-perspZ2), fill=color)
            except:
                pass

################################################################################
## HELPER FUNCTIONS
################################################################################

# inclusive on both ends
def getList(min, max, step):
    result = []
    currentNum = min
    while currentNum<max:
        result.append(currentNum)
        currentNum += step
    result.append(max)
    return result

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

# turns cartesian coordinates to pixel coordinates
def cartesianToPixel(data, cartX, cartY, cartZ):
    pixelX = (cartX-data.axisMin[0])/(data.axisMax[0]-data.axisMin[0])*(data.width*data.boxSize)\
        + (data.centerBoxX-data.width*(0.5*data.boxSize))
    pixelY = (cartY-data.axisMin[1])/(data.axisMax[1]-data.axisMin[1])*(data.width*data.boxSize)\
        - data.width*(0.5*data.boxSize)
    pixelZ = (cartZ-data.axisMin[2])/(data.axisMax[2]-data.axisMin[2])*(data.height*data.boxSize)\
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
    rotatedX, rotatedY, rotatedZ = rotate(data, pixelX, pixelY, pixelZ, data.centerBoxX, 0, data.centerBoxZ)
    perspX, perspZ = perspective(data, rotatedX, rotatedY, rotatedZ, data.centerBoxX, 0, data.centerBoxZ)
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
    return fadeColor(data.backgroundRGB[0], data.backgroundRGB[1], data.backgroundRGB[2],\
        printRGB[0], printRGB[1], printRGB[2], fade)

# fuses single digit and decimal point strings into ints and floats
# replaces π, φ, e strings with corresponding floats
def fuseNumbers(expression):
    onNumberRun = False
    startIndex = None
    endIndex = None
    for i in range(len(expression)-1, -1, -1):
        if not onNumberRun:
            if expression[i] in "1234567890.":
                if i==0:
                    expression[0] = int(expression[0])
                else:
                    endIndex = i
                    onNumberRun = True
        else: # onNumberRun==True
            if (expression[i] not in "1234567890.") or (i==0):
                if expression[i] not in "123456790.":
                    startIndex = i+1
                else:
                    startIndex = 0
                newEntry = "".join(expression[startIndex:endIndex+1])
                if "." in newEntry:
                    newEntry = float(newEntry)
                else:
                    newEntry = int(newEntry)
                expression = expression[:startIndex] +\
                    [newEntry] +\
                    expression[endIndex+1:]
                onNumberRun, startIndex, endIndex = False, None, None
    return expression

def subPiE(list):
    l = copy.copy(list)
    for i in range(len(l)):
        if l[i]=="π":
            l[i] = math.pi
        elif l[i]=="e":
            l[i] = math.e
    return l
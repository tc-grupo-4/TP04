from scipy import signal
import control as cl
import numpy as np
import matplotlib.pyplot as plt
import random
from Approximation import *

#def convertValueListToPointList(valueList,type):
#    for index, valuePair in enumerate(valueList):
#        for value in valueList:
#            if type == "zero": point=Zero(value, index)



class Point(object):
    Etapa=None
    def __init__(self, value, color):
        self.color=color
        self.value=value
        self.im=np.imag(value)
        self.re=np.real(value)
        self.mod=np.sqrt((self.im)**2+(self.re)**2)
        if self.re != 0:
            self.pha = np.arctan(self.im/self.re)
        elif self.im > 0:
            self.pha = 3.142/2
        else:
            self.pha = -3.142/2
        if self.re < 0:
            self.pha = 3.1415 - self.pha
    

class PointPair(list):
    def __init__(self, points,type,color=None):
        if isinstance(points[0],Point):
            self.extend(points)
        else:
            if color is None: color="r"
            if type == "zero":
                self.extend([Zero(points[0],color),Zero(points[1],color)])
            elif type == "pole":
                self.extend([Pole(points[0],color),Pole(points[1],color)])
            else: raise ValueError("Invalid type value: "+str(type))
        self.color=self[0].color
        self.type=type

    def assignToStage(self, stage):
        for point in self:
            if point.Etapa is not None: point.Etapa.removePoints(self)
            point.Etapa=stage
            self.Etapa=stage
        stage.addPoints(self)
    
    def isZero(self): 
        if self.type=="zero": return True
        else: return False
    def isPole(self): 
        if self.type=="pole": return True
        else: return False

class Zero(Point):
    def isZero(self): 
        return True
    def isPole(self): 
        return False

class Pole(Point):
    def isPole(self): 
        return True
    def isZero(self): 
        return False

class Etapa:
    zeroList=[]
    poleList=[]
    
    def __init__(self, figure=None,figurecanvas=None):
        if figure is not None: self.setFigure(figure)
        if figurecanvas is not None: self.setFigureCanvas(figurecanvas)
        self.ax=None

    def addPoints(self, pointPair):
        if pointPair.isPole(): self.poleList.append(pointPair)
        elif pointPair.isZero(): self.zeroList.append(pointPair)
        else : return
        for point in pointPair: point.Etapa=self
        pointPair.Etapa=self

    def removePoints(self, pointPair):
        if pointPair.isPole(): self.poleList.remove(pointPair)
        elif pointPair.isZero(): self.zeroList.remove(pointPair)
        else : return
        for point in pointPair: point.Etapa=None
        pointPair.Etapa=None

    def getTransferFunction(self):
        return self.num, self.den
 
    def createTransferFunction(self):
        tempZero=[]
        tempPole=[]

        for zeroPair in self.zeroList:
            for zero in zeroPair:
                tempZero.append(zero.value)
        for polePair in self.poleList:
            for pole in polePair:
                tempPole.append(pole.value)

        self.num, self.den, k = signal.zpk2tf(tempZero,tempPole,self.k)
    
    def setFigure(self, figure):
        self.figure=figure

    def setFigureCanvas(self, figurecanvas):
        self.figurecanvas=figurecanvas

    def plotStage(self):
        if self.figure is not None:
            if self.ax is not None: figure.delaxes(self.ax) 
            
            self.ax = self.figure.add_subplot(111, projection='polar')
            polarPlot(self.zeroList, self.poleList, self.ax)
            self.figurecanvas.show()
            
        else: print("Error: Set figure first")
   
def polarPlot(zeros, poles, ax):
    for zeroPair in zeros:
        for zero in zeroPair: ax.plot(zero.pha,zero.mod,'o',color=zero.color)
                
    for polePair in poles:    
        for pole in polePair: ax.plot(pole.pha,pole.mod,'x',color=pole.color)
   


# num = [0.8912509381337455,0.0,6832402540.638172,0.0,7.24572875462745e+18]
# den = [1.0,337194.6633703208,92412209932.89781,8400336197283562.0,1.2883166302894993e+21]

# z,p,k = getPolesAndZerosFromTF(num,den)
# plotPolesAndZeros(z,p)

# hola = Etapa(z[0],p[1],k)
# num,den = hola.getTransferFunction()
# z,p,k = getPolesAndZerosFromTF(num,den)
# plotPolesAndZeros(z,p)

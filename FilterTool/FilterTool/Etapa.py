from scipy import signal
import control as cl
import numpy as np
import matplotlib.pyplot as plt
import random
from Approximation import *




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
    def assignToStage(self, stage):
        if self.Etapa is not None: self.Etapa.removePoints(self)
        self.Etapa=stage
        stage.addPoints(self)


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
    
    def __init__(self, figure=None):
        if figure is not None: self.setFigure(figure)
        

    def addPoints(self, point):
        if point.isPole(): self.poleList.append(pointPair)
        elif point.isZero(): self.zeroList.append(pointPair)
        else : return
        for point in pointPair: point.Etapa=self

    def removePoints(self, point):
        if point.isPole(): self.poleList.remove(pointPair)
        elif point.isZero(): self.zeroList.remove(pointPair)
        else : return
        for point in pointPair: point.Etapa=None

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

    def plotStage(zeros, poles, figure):
        if self.figure is not None:
            if self.ax is not None: figure.delaxes(self.ax) 
            
            self.ax = figure.add_subplot(111, projection='polar')
            polarPlot(self.zeros, self.poles, self.ax)
            figure.show()
            
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

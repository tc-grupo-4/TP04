from scipy import signal
import control as cl
import numpy as np
import matplotlib.pyplot as plt
import random

def plotPolesAndZeros(zeros, poles):
    colors = ['r','g','b','c','m','y','k']
    zeros2plot = []
    ax = plt.subplot(111, projection='polar')
    for i in zeros:
        tempColor = colors[random.randint(0,6)]
        for u in i:
            mod = (np.real(u)**2 + np.imag(u)**2)**0.5
            if np.real(u) != 0:
                pha = np.arctan(np.imag(u)/np.real(u))
            elif np.imag(u) > 0:
                pha = 3.142/2
            else:
                pha = -3.142/2
            if np.real(u) < 0:
                pha = 3.1415 - pha
            temp = [pha,mod,tempColor]
            zeros2plot.append(temp)
        
    for i in zeros2plot:
        ax.plot(i[0],i[1],'o',color=i[2])
    
    poles2plot = []
    for i in poles:
        tempColor = colors[random.randint(0,6)]
        for u in i:
            mod = (np.real(u)**2 + np.imag(u)**2)**0.5
            if np.real(u) != 0:
                pha = np.arctan(np.imag(u)/np.real(u))
            elif np.imag(u) > 0:
                pha = 3.142/2
            else:
                pha = -3.142/2
            if np.real(u) < 0:
                pha = 3.1415 - pha
            temp = [pha,mod,tempColor]
            poles2plot.append(temp)   
    for i in poles2plot:
        ax.plot(i[0],i[1],'x',color=i[2])
    
    plt.show()
    return

def getPolesAndZerosFromTF(num,den):
    ##Recibe un nominador y denominador de una transferencia y devuelve:
    ##  -Zeros: Una lista de listas de zeros agrupados de a par con parte real igual
    ##      Pej: Si los zeros son   Z1 = 1+1j
    ##                              Z2 = 1-1j
    ##                              Z3 = 3
    ##              -> Zeros = [ [1+1j , 1-1j], [3] ]
    ##  -Poles: una lista de listas de polos agrupados de la misma manera
    ##  -K: Ganancia total de la transferencia
    z,p,k = signal.tf2zpk(num,den)
    zeros = []
    poles = []
    used = []
    for i in range(0,len(z)):
        if i not in used:
            grouped = False
            used.append(i)
            for u in range(0,len(z)):
                if u != i:
                    if np.real(z[i]) == np.real(z[u]) and np.real(z[i]) != 0 and u not in used:
                        temp = [z[i],z[u]]
                        used.append(u)
                        zeros.append(temp)
                        grouped = True
                    elif np.imag(z[i])**2 == np.imag(z[u])**2 and np.imag(z[i]) != 0 and u not in used:
                        temp = [z[i],z[u]]
                        used.append(u)
                        zeros.append(temp)
                        grouped = True
            if grouped == False:
                temp = [z[i]]
                zeros.append(temp)
    used = []
    for i in range(0,len(p)):
        if i not in used:
            grouped = False
            used.append(i)
            for u in range(0,len(p)):
                if u != i:
                    if np.real(p[i]) == np.real(p[u]) and u not in used:
                        used.append(u)
                        temp = [p[i],p[u]]
                        poles.append(temp)
                        grouped = True
                    if np.imag(p[i])**2 == np.imag(p[u])**2 and u not in used:
                        used.append(u)
                        temp = [p[i],p[u]]
                        poles.append(temp)
                        grouped = True
            if grouped == False:
                temp = [p[i]]
                poles.append(temp)
    return zeros,poles,k

class Etapa:
    def __init__(self,zeros,poles,k):
        self.z = zeros
        self.p = poles
        self.k = k
        self.createTransferFunction()

    def getTransferFunction(self):
        return self.num, self.den
 
    def plotEtapa(self):
        plotPolesAndZeros(self.num, self.den)
        return

    def createTransferFunction(self):
        self.num, self.den = signal.zpk2tf(self.z,self.p,self.k)
        return

# num = [0.8912509381337455,0.0,6832402540.638172,0.0,7.24572875462745e+18]
# den = [1.0,337194.6633703208,92412209932.89781,8400336197283562.0,1.2883166302894993e+21]

# z,p,k = getPolesAndZerosFromTF(num,den)
# plotPolesAndZeros(z,p)

# hola = Etapa(z[0],p[1],k)
# num,den = hola.getTransferFunction()
# z,p,k = getPolesAndZerosFromTF(num,den)
# plotPolesAndZeros(z,p)


'''
Implementa solo celdas de los tipos:
	LP1 = Pasabajos de 1er Orden
	SKL = Pasabajos Sallen-Key
	SKH = PasaAltos Sallen-Key
	HP1 = PasaAltos de 1er Orden
	BPR = Pasabanda Rauch
	NR = Rechazabanda Rauch
	DT = Doble T

	Para inicializarlo se lo construye con 2 valores:
		1°: Polinomios del numerador y denominador de la funcion transferencia
			Ej:		H(s)= (a s**2 + b s + c) / (d s**2 + e s + f)
					Se pasa una lista de la siguiente forma
					tf = [ [a,b,c] , [d,e,f] ]
		2°: Una variable booleana para denotar si se desean redondear los valores obtenidos de
			los componentes a la norma E12, o si no se lo desea para tener el valor exacto

	Se usa la función getCell que devuelve una lista con 2 elementos:
		1°: Tipo de filtro (usa la nomeclatura de arriba, lo da como string)
		2°: Un diccionario con los valores de cada componente del filtro dependiendo de cada filtro.
			Las claves de los diccionarios son los nombres de los componentes como estan en el palombo
			(pej. si una resistencia se llama Ra, la clave va a ser 'Ra').

'''
#TODO:
#		-Pasabanda Rauch
#		-Notch Rauch
#		-Doble T

class Celda:
	def __init__(self, transferFunction, round = False):	## transferFunction es una lista con 2 elementos, 
		self.tf = transferFunction							## donde cada elemento es un array de coeficientes de orden 2.
		self.roun = round
		self.filterType = None
		return

	def getCell(self):
		self.calcFilterType()
		values = self.calcValues()
		Cell = [self.filterType , values]
		return Cell
	
	def calcFilterType(self):
		nom = self.tf[0]
		den = self.tf[1]
		if nom[0] == 0 and nom[1] == 0 and nom[2] != 0:
			if den[0] == 0 and den[1] != 0 and den[2] != 0:
				self.filterType = 'LP1'
			elif den[0] != 0 and den[1] != 0 and den[2] != 0:
				self.filterType = 'SKL'
		elif nom[0] == 0 and nom[1] != 0 and nom[2] == 0:
			if den[0] == 0 and den[1] != 0 and den[2] != 0:
				self.filterType = 'HP1'
			elif den[0] != 0 and den[1] != 0 and den[2] != 0:
				self.filterType = 'BPR'
		elif nom[0] != 0 and nom[1] == 0 and nom[2] == 0:
			if den[0] == 0 and den[1] != 0 and den[2] != 0:
				self.filterType = 'ERROR'
			elif den[0] != 0 and den[1] != 0 and den[2] != 0:
				self.filterType = 'SKH'
		elif nom[0] != 0 and nom[1] == 0 and nom[2] != 0:
			if den[0] == 0 and den[1] != 0 and den[2] != 0:
				self.filterType = 'ERROR'
			elif den[0] != 0 and den[1] != 0 and den[2] != 0:
				self.filterType = 'DT'
		return

	def calcValues(self):
		temp = None
		if self.filterType == 'LP1':
			temp = self.calcFirstOrderLowPass()
		elif self.filterType == 'SKL':
			temp = self.calcLowSallenKey()
		elif self.filterType == 'SKH':
			temp = calcHighSallenKey()
		elif self.filterType == 'HP1':
			temp = calcFirstOrderHighPass()
		elif self.filterType == 'BPR':
			temp = calcBandRauch()
		elif self.filterType == 'NR':
			temp = calcNotchRauch()
		elif self.filterType == 'DT':
			temp = calcDoubleT()
		return temp

	def calcFirstOrderLowPass(self):
		nom = self.tf[0]
		den = self.tf[1]
		R = None
		Ra = None
		Rb = None
		C = None
		k = nom[2]/den[2]
		a = den[1]/den[2]
		C = 10 * 10**-9		##Fijo constantes
		Rb = 10 * 10**3
		R = a * (1/C)
		Ra = (k-1)*Rb
		if self.roun == True:
			R = roundValueE12(R)
			Ra = roundValueE12(Ra)
			Rb = roundValueE12(Rb)
			C = roundValueE12(C)
		temp = {'R': R, 'Ra': Ra, 'Rb': Rb, 'C': C}
		return temp

	def calcLowSallenKey(self):
		nom = self.tf[0]
		den = self.tf[1]
		R1 = None
		R2 = None
		Ra = None
		Rb = None
		C1 = None
		C2 = None
		k = nom[2]/den[2]
		a = den[0]/den[2]
		b = den[1]/den[2]

		C1 = 10 * 10**-9
		C2 = C1
		Wo = 1 /(a**(1/2))
		R = 1 /(Wo * C1)
		Rb = 10 * 10**3
		Ra = (k-1)*Rb
		if self.roun == True:
			R = roundValueE12(R)
			C1 = roundValueE12(C1)
			C2 = roundValueE12(C2)
			Ra = roundValueE12(Ra)
			Rb =roundValueE12(Rb)

		temp = {'R1':R , 'R2':R , 'C1':C1, 'C2': C2, 'Ra':Ra, 'Rb': Rb }
		return temp

	def calcHighSallenKey(self):
		nom = self.tf[0]
		den = self.tf[1]

		a = den[0]/den[2]
		B = nom[0]/den[2]
		k = B/a
		b = den[1]/den[2]
		Wo = 1/(a**(1/2))

		Rb = 10 * 10**3
		Ra = (k-1) * Rb

		C = 10 * 10**-9
		R = 1/(Wo*C)
		if self.roun == True:
			R =roundValueE12(R)
			C = roundValueE12(C)
			Ra = roundValueE12(Ra)
			Rb = roundValueE12(Rb)

		temp = {'R1':R , 'R2':R , 'C1':C, 'C2': C, 'Ra':Ra, 'Rb': Rb }
		return temp

	def calcFirstOrderHighPass(self):
		nom = self.tf[0]
		den = self.tf[1]
		
		a = den[1]/den[2]
		B = nom[1]/den[2]
		k = B/a
		Wo = 1/a
		
		Rb = 10* 10 **3
		Ra = (k-1)*Rb

		C = 10 * 10**-9
		R = 1/(Wo*C)
		if self.roun == True:
			C=roundValueE12(C)
			R = roundValueE12(R)
			Ra = roundValueE12(Ra)
			Rb = roundValueE12(Rb)

		temp = {'C':C, 'Ra': Ra , 'Rb':Rb, 'R':R}
		return temp

	def calcBandRauch(self):
		return 'FALTA HACER'

	def calcNotchRauch(self):
		return 'FALTA HACER'

	def calcDoubleT(self):
		return 'FALTA HACER'

	def roundValueE12(self,val):
		order = 0
		temp = None
		while val > 10:
			val = val/10
			order = order + 1
		while val < 1:
			val = val*10
			order = order - 1
		
		temp = chooseBetween(val,1,1.2)
		temp = temp + chooseBetween(val,1.2,1.5)
		temp = temp + chooseBetween(val,1.5,1.8)
		temp = temp + chooseBetween(val,1.8,2.2)
		temp = temp + chooseBetween(val,2.2,2.7)
		temp = temp + chooseBetween(val,2.7,3.3)
		temp = temp + chooseBetween(val,3.3,3.9)
		temp = temp + chooseBetween(val,3.9,4.7)
		temp = temp + chooseBetween(val,4.7,5.6)
		temp = temp + chooseBetween(val,5.6,6.8)
		temp = temp + chooseBetween(val,6.8,8.2)
		temp = temp + chooseBetween(val,8.2,10)
		return (temp * (10**order))

	def chooseBetween(self, val, num1,num2):
		if val >= num1 and val < num2:
			if (val-num1) < (num2 -val):
				return num1
			else
				return num2
		return 0
from PyQt5 import QtGui, QtWidgets, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import FilterToolDesign
import sys
import numpy as np


class FilterTool(QtWidgets.QMainWindow, FilterToolDesign.Ui_MainWindow):
    def __init__(self, parent=None):
        super(FilterTool, self).__init__(parent)
        self.setupUi(self)



        # TODO: Borrar esto. Es para probar
        self.fig1 = Figure()
        self.ax1f1 = self.fig1.add_subplot(111)
        self.ax1f1.plot(np.random.rand(5))
        self.addmpl(self.fig1)

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.plotsLayout.addWidget(self.canvas)
        self.canvas.draw()
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    filter_tool = FilterTool()
    filter_tool.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()
from PyQt5 import QtGui, QtWidgets, QtCore
import FilterToolDesign
import sys


class FilterTool(QtWidgets.QMainWindow, FilterToolDesign.Ui_MainWindow):
    def __init__(self, parent=None):
        super(FilterTool, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    filter_tool = FilterTool()
    filter_tool.show()
    app.exec_()


if __name__ == "__main__":
    main()
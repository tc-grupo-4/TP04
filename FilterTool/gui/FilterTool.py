# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FilterTool.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(868, 611)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.plotsLayout = QtWidgets.QVBoxLayout()
        self.plotsLayout.setObjectName("plotsLayout")
        self.MplWidget = MplWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MplWidget.sizePolicy().hasHeightForWidth())
        self.MplWidget.setSizePolicy(sizePolicy)
        self.MplWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.MplWidget.setBaseSize(QtCore.QSize(100, 140))
        self.MplWidget.setObjectName("MplWidget")
        self.plotsLayout.addWidget(self.MplWidget)
        self.gridLayout_12.addLayout(self.plotsLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 868, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.minMaxRadioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.minMaxRadioButton.setObjectName("minMaxRadioButton")
        self.horizontalLayout_17.addWidget(self.minMaxRadioButton)
        self.minOrderSpinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.minOrderSpinBox.setObjectName("minOrderSpinBox")
        self.horizontalLayout_17.addWidget(self.minOrderSpinBox)
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_17.addWidget(self.label_14)
        self.maxOrderSpinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.maxOrderSpinBox.setObjectName("maxOrderSpinBox")
        self.horizontalLayout_17.addWidget(self.maxOrderSpinBox)
        self.gridLayout_8.addLayout(self.horizontalLayout_17, 0, 0, 1, 1)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.maxQRadioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.maxQRadioButton.setObjectName("maxQRadioButton")
        self.horizontalLayout_15.addWidget(self.maxQRadioButton)
        self.maxQdoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox_3)
        self.maxQdoubleSpinBox.setObjectName("maxQdoubleSpinBox")
        self.horizontalLayout_15.addWidget(self.maxQdoubleSpinBox)
        self.gridLayout_8.addLayout(self.horizontalLayout_15, 1, 0, 1, 1)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.customOrderRadioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.customOrderRadioButton.setObjectName("customOrderRadioButton")
        self.horizontalLayout_18.addWidget(self.customOrderRadioButton)
        self.customOrderSpinBox = QtWidgets.QSpinBox(self.groupBox_3)
        self.customOrderSpinBox.setObjectName("customOrderSpinBox")
        self.horizontalLayout_18.addWidget(self.customOrderSpinBox)
        self.gridLayout_8.addLayout(self.horizontalLayout_18, 2, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_13 = QtWidgets.QLabel(self.groupBox_2)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_14.addWidget(self.label_13)
        self.filterTypeComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.filterTypeComboBox.setObjectName("filterTypeComboBox")
        self.filterTypeComboBox.addItem("")
        self.filterTypeComboBox.addItem("")
        self.filterTypeComboBox.addItem("")
        self.filterTypeComboBox.addItem("")
        self.filterTypeComboBox.addItem("")
        self.horizontalLayout_14.addWidget(self.filterTypeComboBox)
        self.gridLayout.addLayout(self.horizontalLayout_14, 0, 0, 1, 1)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_16.addWidget(self.label_15)
        self.approximationComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.approximationComboBox.setObjectName("approximationComboBox")
        self.approximationComboBox.addItem("")
        self.approximationComboBox.addItem("")
        self.approximationComboBox.addItem("")
        self.approximationComboBox.addItem("")
        self.approximationComboBox.addItem("")
        self.approximationComboBox.addItem("")
        self.approximationComboBox.addItem("")
        self.horizontalLayout_16.addWidget(self.approximationComboBox)
        self.gridLayout.addLayout(self.horizontalLayout_16, 1, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.stopBand1DoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.stopBand1DoubleSpinBox.setObjectName("stopBand1DoubleSpinBox")
        self.horizontalLayout_6.addWidget(self.stopBand1DoubleSpinBox)
        self.gridLayout_11.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.stopBand2DoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.stopBand2DoubleSpinBox.setObjectName("stopBand2DoubleSpinBox")
        self.horizontalLayout_5.addWidget(self.stopBand2DoubleSpinBox)
        self.gridLayout_11.addLayout(self.horizontalLayout_5, 0, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.passBand1DoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.passBand1DoubleSpinBox.setObjectName("passBand1DoubleSpinBox")
        self.horizontalLayout_3.addWidget(self.passBand1DoubleSpinBox)
        self.gridLayout_11.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.passBand2DoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.passBand2DoubleSpinBox.setObjectName("passBand2DoubleSpinBox")
        self.horizontalLayout_7.addWidget(self.passBand2DoubleSpinBox)
        self.gridLayout_11.addLayout(self.horizontalLayout_7, 1, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.minAttnDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.minAttnDoubleSpinBox.setObjectName("minAttnDoubleSpinBox")
        self.horizontalLayout_2.addWidget(self.minAttnDoubleSpinBox)
        self.gridLayout_11.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.maxAttnDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.maxAttnDoubleSpinBox.setObjectName("maxAttnDoubleSpinBox")
        self.horizontalLayout_4.addWidget(self.maxAttnDoubleSpinBox)
        self.gridLayout_11.addLayout(self.horizontalLayout_4, 2, 1, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_11, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_4 = QtWidgets.QGroupBox(self.dockWidgetContents)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.attenuationCurvesCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.attenuationCurvesCheckBox.setObjectName("attenuationCurvesCheckBox")
        self.gridLayout_9.addWidget(self.attenuationCurvesCheckBox, 0, 0, 1, 1)
        self.stepResponseCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.stepResponseCheckBox.setObjectName("stepResponseCheckBox")
        self.gridLayout_9.addWidget(self.stepResponseCheckBox, 0, 1, 1, 1)
        self.phaseCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.phaseCheckBox.setObjectName("phaseCheckBox")
        self.gridLayout_9.addWidget(self.phaseCheckBox, 1, 0, 1, 1)
        self.sPlaneCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.sPlaneCheckBox.setObjectName("sPlaneCheckBox")
        self.gridLayout_9.addWidget(self.sPlaneCheckBox, 1, 1, 1, 1)
        self.groupDelayCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.groupDelayCheckBox.setObjectName("groupDelayCheckBox")
        self.gridLayout_9.addWidget(self.groupDelayCheckBox, 2, 0, 1, 1)
        self.freqResponseCheckBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.freqResponseCheckBox.setObjectName("freqResponseCheckBox")
        self.gridLayout_9.addWidget(self.freqResponseCheckBox, 2, 1, 1, 1)
        self.gridLayout_10.addLayout(self.gridLayout_9, 0, 0, 1, 1)
        self.computePushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.computePushButton.setObjectName("computePushButton")
        self.gridLayout_10.addWidget(self.computePushButton, 1, 0, 1, 1)
        self.saveResultsPushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.saveResultsPushButton.setObjectName("saveResultsPushButton")
        self.gridLayout_10.addWidget(self.saveResultsPushButton, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_4)
        self.gridLayout_5.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.dockWidget.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.dockWidget.setWindowTitle(_translate("MainWindow", "Filter Parameters"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Approximation Settings"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Parameters"))
        self.minMaxRadioButton.setText(_translate("MainWindow", "Min Order"))
        self.label_14.setText(_translate("MainWindow", "Max Order"))
        self.maxQRadioButton.setText(_translate("MainWindow", "Max Q Allowed"))
        self.customOrderRadioButton.setText(_translate("MainWindow", "Custom Order"))
        self.label_13.setText(_translate("MainWindow", "Type"))
        self.filterTypeComboBox.setItemText(0, _translate("MainWindow", "Low-pass"))
        self.filterTypeComboBox.setItemText(1, _translate("MainWindow", "High-pass"))
        self.filterTypeComboBox.setItemText(2, _translate("MainWindow", "Band-pass"))
        self.filterTypeComboBox.setItemText(3, _translate("MainWindow", "Band-reject"))
        self.filterTypeComboBox.setItemText(4, _translate("MainWindow", "All-pass"))
        self.label_15.setText(_translate("MainWindow", "Approximation"))
        self.approximationComboBox.setItemText(0, _translate("MainWindow", "Butterworth"))
        self.approximationComboBox.setItemText(1, _translate("MainWindow", "Bessel"))
        self.approximationComboBox.setItemText(2, _translate("MainWindow", "Chebyshev Type I"))
        self.approximationComboBox.setItemText(3, _translate("MainWindow", "Chebyshev Type II"))
        self.approximationComboBox.setItemText(4, _translate("MainWindow", "Legendre"))
        self.approximationComboBox.setItemText(5, _translate("MainWindow", "Gauss"))
        self.approximationComboBox.setItemText(6, _translate("MainWindow", "Cauer elliptic"))
        self.groupBox.setTitle(_translate("MainWindow", "Footprint"))
        self.label_5.setText(_translate("MainWindow", "Stop Band 1"))
        self.label_4.setText(_translate("MainWindow", "Stop Band 2"))
        self.label_2.setText(_translate("MainWindow", "Pass Band 1"))
        self.label_6.setText(_translate("MainWindow", "Pass Band 2"))
        self.label.setText(_translate("MainWindow", "Min Attenuated"))
        self.label_3.setText(_translate("MainWindow", "Max Attenuated"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Plots"))
        self.attenuationCurvesCheckBox.setText(_translate("MainWindow", "Attenuation Curves"))
        self.stepResponseCheckBox.setText(_translate("MainWindow", "Step Response"))
        self.phaseCheckBox.setText(_translate("MainWindow", "Phase"))
        self.sPlaneCheckBox.setText(_translate("MainWindow", "S Plane Diagram"))
        self.groupDelayCheckBox.setText(_translate("MainWindow", "Group Delay"))
        self.freqResponseCheckBox.setText(_translate("MainWindow", "Frequency Response"))
        self.computePushButton.setText(_translate("MainWindow", "Compute"))
        self.saveResultsPushButton.setText(_translate("MainWindow", "Save Results"))
from mplwidget import MplWidget

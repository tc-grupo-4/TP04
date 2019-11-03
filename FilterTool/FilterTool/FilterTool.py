from PyQt5 import QtGui, QtWidgets, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import FilterToolDesign
import sys
import numpy as np
from Template import Template
from Approximation import Approximation
import matplotlib.pyplot as mpl
from distutils.spawn import find_executable
import math
from Etapa import *

def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'INFO'
    elif mode == QtCore.QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtCore.QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    file=open("log.txt","a+")
    file.write('qt_message_handler: line: %d, func: %s(), file: %s' % (
          context.line, context.function, context.file))
    file.write('  %s: %s\n' % (mode, message))
    file.close()
    
     


## Class inherited from Ui_MainWindow to customize GUI design and behaviour
class FilterTool(QtWidgets.QMainWindow, FilterToolDesign.Ui_MainWindow):
    def __init__(self, parent=None):
        super(FilterTool, self).__init__(parent)
        self.setupUi(self)
        
        # configure to use latex interpreter
        
        if find_executable('latex'):
            mpl.rc('font',**{'family':'serif','serif':['Palatino']})
            mpl.rc('text', usetex=True)
            
        # array containing approximation types
        self.approx_types = ['butterworth', 'bessel', 'cheby_1', 'cheby_2', 'legendre', 'gauss', 'cauer']

        self.currentApproxComboBox.currentIndexChanged.connect(self.on_set_current_approx_clicked)
        self.setStagesPushButton.clicked.connect(self.updateStages)
        # connect 'preview aproximation' button to handler
        self.previewApproxButton.clicked.connect(self.on_preview_clicked)
        # connect clear approximation button to handler
        self.clearApproxButton.clicked.connect(self.on_clear_previews_clicked)
        # connect approximation type combo box to handler
        self.approximationComboBox.currentIndexChanged.connect(self.validate_approximation)
        # connect 'Compute' button to handler.
        self.computePushButton.clicked.connect(self.on_compute_clicked)
        # connect 'Set Template' button to handler
        self.setTemplateButton.clicked.connect(self.on_set_template_clicked)
        # connect filter type combo box selection changed to handler
        self.filterTypeComboBox.currentIndexChanged.connect(self.on_filter_type_changed)
        # connect spinboxes valueChanged to handlers
        self.minAttnDoubleSpinBox.valueChanged.connect(self.validate_template)
        self.maxAttnDoubleSpinBox.valueChanged.connect(self.validate_template)
        self.passBand1DoubleSpinBox.valueChanged.connect(self.validate_template)
        self.passBand2DoubleSpinBox.valueChanged.connect(self.validate_template)
        self.stopBand1DoubleSpinBox.valueChanged.connect(self.validate_template)
        self.stopBand2DoubleSpinBox.valueChanged.connect(self.validate_template)
        # connect approximation input config parameters widgets to handler
        self.approximationComboBox.currentIndexChanged.connect(self.validate_approximation)
        self.minMaxRadioButton.clicked.connect(self.validate_approximation)
        self.minOrderSpinBox.valueChanged.connect(self.validate_approximation)
        self.maxOrderSpinBox.valueChanged.connect(self.validate_approximation)
        self.maxQRadioButton.clicked.connect(self.validate_approximation)
        self.maxQdoubleSpinBox.valueChanged.connect(self.validate_approximation)
        self.customOrderRadioButton.clicked.connect(self.validate_approximation)
        self.customOrderSpinBox.valueChanged.connect(self.validate_approximation)
        # connect plot settings to handlers
        self.attenuationCurvesCheckBox.clicked.connect(self.validate_approximation)
        self.phaseCheckBox.clicked.connect(self.validate_approximation)
        self.groupDelayCheckBox.clicked.connect(self.validate_approximation)
        self.stepResponseCheckBox.clicked.connect(self.validate_approximation)
        self.sPlaneCheckBox.clicked.connect(self.validate_approximation)
        self.freqResponseCheckBox.clicked.connect(self.validate_approximation)
        # hide stopband2 & passband2 widgets
        self.hide_pass_stop_2()
        # validate template parameters
        self.validate_template()
        # set template_submited to False
        ## @var template_submited
        #  Bool variable indicatign whether the template has been submited
        self.template_submited = False
        # validate approximation settings
        self.validate_approximation()
        ## @var validation_computed
        #  Bool variable indicating whether the approximation has been computed
        self.validation_computed = False
        # Disable save pushbutton
        self.saveResultsPushButton.setEnabled(False)
        # setup figures and canvases
        self.set_mpl()
        # array containing every preview ploted
        self.plotted_previews = []
        # initialize plot options
        self.any_plots_checked()
        
        # indica si alguna vez se ploteo esto
        self.att_plotted = False
        self.phase_plotted = False
        self.step_plotted = False
        self.s_plane_plotted = False
        self.freq_response_plotted = False
        self.group_delay_plotted = False
        
        self.preview_already_plotted = False
        self.currentApproximation=None
        self.approximations=[]
        self.zerosGroupBoxes=[]
        self.polesGroupBoxes=[]
        self.stages=[]
        self.mainStageFigure=None
        self.currentApproxComboBox.addItem("None")
        self.currentApproxComboBox.setCurrentText("None")
       
        


        
    ## Helper to hide unused GUI widgets.
    #  Hides unused frequency input fields when 'Low-pass' or 'High-pass'
    #  @details filter type is selected.
    #  @param self The object pointer
    def hide_pass_stop_2(self):
        self.stopBand2_label.hide()
        self.stopBand2DoubleSpinBox.hide()
        self.passBand2_label.hide()
        self.passBand2DoubleSpinBox.hide()


    ## Helper to show hided GUI widgets
    #  @details Shows hided frequency input fields when needed.
    #  @param self The object pointer
    def show_pass_stop_2(self):
        self.stopBand2_label.show()
        self.stopBand2DoubleSpinBox.show()
        self.passBand2_label.show()
        self.passBand2DoubleSpinBox.show()


    ## Helper to instantiate figures and canvas
    #  @details Instantiates every figure and canvas to be used by de program
    #  @param self The object pointer
    def set_mpl(self):
        self.template_fig = Figure()
        self.template_canvas = FigureCanvas(self.template_fig)
        self.att_fig = Figure()
        self.att_canvas = FigureCanvas(self.att_fig)
        self.phase_fig = Figure()
        self.phase_canvas = FigureCanvas(self.phase_fig)
        self.group_fig = Figure()
        self.group_canvas = FigureCanvas(self.group_fig)
        self.step_fig = Figure()
        self.step_canvas = FigureCanvas(self.step_fig)
        self.s_plane_fig = Figure()
        self.s_plane_canvas = FigureCanvas(self.s_plane_fig)
        self.freq_fig = Figure()
        self.freq_canvas = FigureCanvas(self.freq_fig)


    ## Handles a filter type combo box index change.
    #  @details Execuetes whwnever the selected index in filter type combo box changes.
    #  @param self The object pointer
    def on_filter_type_changed(self):
        selectedText = self.filterTypeComboBox.currentText()
        if selectedText == 'Low-pass':
            self.hide_pass_stop_2()
        if selectedText == 'High-pass':
            self.hide_pass_stop_2()
        if selectedText == 'Band-pass':
            self.show_pass_stop_2()
        if selectedText == 'Band-reject':
            self.show_pass_stop_2()
        return



    ## Handler that validets a new template parameter setting.
    #  @details Whenever a template parameter is changed, the new configuration is
    #  validated to determine if the user can submit it.
    #  @param self The object pointer
    def validate_template(self):
        selected_filter = self.filterTypeComboBox.currentText()
        template = Template(selected_filter,
                            omega_p1 = self.passBand1DoubleSpinBox.value(),
                            omega_s1 = self.stopBand1DoubleSpinBox.value(),
                            omega_p2 = self.passBand2DoubleSpinBox.value(),
                            omega_s2 = self.stopBand2DoubleSpinBox.value(),
                            att_p = self.maxAttnDoubleSpinBox.value(),
                            att_s = self.minAttnDoubleSpinBox.value(),
                            final = False)

        valid = template.is_valid()
        self.setTemplateButton.setEnabled(valid)

    ## Helper to clear all figures
    #  @details Deletes every canvas contained in the plotslayout
    #  @param self The object pointer
    def clear_plot_layout(self):
        for i in reversed(range(self.plotsLayout.count())):
            self.plotsLayout.itemAt(i).widget().figure.clf()
            self.plotsLayout.itemAt(i).widget().draw()
            self.plotsLayout.itemAt(i).widget().setParent(None)
        

    ## Set template handler
    #  @details Executes when a new template is submited (prevoisly validated)
    #  and plots it to the specified axes.
    #  @param self The object pointer
    def on_set_template_clicked(self):
        # Create the specified template
        ## @var selected_filter
        #  String value. Indicates the filter type selected for the template
        self.selected_filter = self.filterTypeComboBox.currentText()
        ## @var template
        #  Template insatance with the specified parameters.
        self.template = Template(self.selected_filter,
                                omega_p1 = self.passBand1DoubleSpinBox.value(),
                                omega_s1 = self.stopBand1DoubleSpinBox.value(),
                                omega_p2 = self.passBand2DoubleSpinBox.value(),
                                omega_s2 = self.stopBand2DoubleSpinBox.value(),
                                att_p = self.maxAttnDoubleSpinBox.value(),
                                att_s = self.minAttnDoubleSpinBox.value(),
                                final = True)
        # remove all plots widgets. in plotLayout
        self.clear_plot_layout()
        # plot template in specified axes
        self.template_axes = self.template_fig.add_subplot(211)
        self.template_axes_norm = self.template_fig.add_subplot(212)
        self.template.plot_template_in_axes(self.template_axes, self.template_axes_norm)
        # add canvas0 to plotLayout
        self.plotsLayout.addWidget(self.template_canvas)
        # show canvas0
        self.template_canvas.show()
        # redraw canvas0
        self.template_canvas.draw()
        # set template submited to True
        self.template_submited = True
        self.validate_approximation()
        pass

    ## Validates the approximation settings
    #  @details Veryfies if the approximation setings are valid and whether a template is 
    #  submitted.
    #  @param self The object pointer
    #  @return A boolean value. True if approximation is ready to compute. False otherwise
    def validate_approximation(self):
        valid = False

        approx_index = self.approximationComboBox.currentIndex()
        self.approx_type = self.approx_types[approx_index]

        if approx_index == 1 or approx_index == 4 or approx_index == 5: #Bessel, Legendre y Gauss
            self.minMaxRadioButton.setEnabled(False)
        else:
            self.minMaxRadioButton.setEnabled(True)

        if self.customOrderRadioButton.isChecked():
            self.restriction = 'custom_order'
            valid = self.customOrderSpinBox.value() > 0
        elif self.maxQRadioButton.isChecked():
            self.restriction = 'max_q'
            valid = self.maxQdoubleSpinBox.value() > 0
        elif self.minMaxRadioButton.isChecked():
            self.restriction = 'min_max_order'
            valid = self.minOrderSpinBox.value() < self.maxOrderSpinBox.value()
            valid = valid and self.minOrderSpinBox.value() > 0
            valid = valid and self.maxOrderSpinBox.value() > 0
        else:
            valid = False
        can_compute = valid and self.any_plots_checked()
        self.computePushButton.setEnabled(can_compute and self.template_submited)
        self.previewApproxButton.setEnabled(valid and self.template_submited)
      
    ## Checks if any plot option selected
    #  @details Veryfies if any of the plots option checkboxes is checked
    #  @param self The object pointer
    #  @return A boolean value. True if any checkbox checked. False otherwise
    def any_plots_checked(self):
        ret = False
        ## @var plot_attenuation
        #  Boolean variable that indicates whether the attenuation curve ust be plotted
        self.plot_attenuation = self.attenuationCurvesCheckBox.isChecked()
        ## @var plot_phase
        #  Boolean variable that indicates whether the phase response must be plotted
        self.plot_phase = self.phaseCheckBox.isChecked()
        ## @var plot_group_delay
        #  Boolean variable that indicates whether the group delay must be plotted
        self.plot_group_delay = self.groupDelayCheckBox.isChecked()
        ## @var plot_step_response
        #  Boolean variable that indicates whether the step response must be plotted
        self.plot_step_response = self.stepResponseCheckBox.isChecked()
        ## @var plot_s_plane
        #  Boolean variable that indicates whether the S plane must be plotted
        self.plot_s_plane = self.sPlaneCheckBox.isChecked()
        ## @var plot_freq_resp
        #  Boolean varialbe that indicates whether the frequency response must be plotted
        self.plot_freq_resp = self.freqResponseCheckBox.isChecked()

        ret = self.plot_attenuation or self.plot_phase or self.plot_group_delay or self.plot_step_response or self.plot_s_plane or self.plot_freq_resp
        return ret


    def on_preview_clicked(self):
        index = self.approximationComboBox.currentIndex()
        approximation = Approximation(self, self.template,
                                         restriction = self.restriction,
                                         min_order = self.minOrderSpinBox.value(),
                                         max_order = self.maxOrderSpinBox.value(),
                                         max_q = self.maxQdoubleSpinBox.value(),
                                         custom_order = self.customOrderSpinBox.value(),
                                         approx_type=self.approx_type)
        
        left, right = self.template_axes.get_xlim()
        left_N, right_N = self.template_axes_norm.get_xlim()
        limits = {'left':left, 'right':right, 'left_N':left_N, 'right_N':right_N}
        preview_lines = approximation.plot_preview_to_axes(self.template_axes, self.template_axes_norm, limits)
        self.currentApproxComboBox.addItem(approximation.legend)
        #self.currentApproxComboBox.setItemText(0, QtCore.QCoreApplication.translate("MainWindow", approximation.legend))
        
        self.approximations.append(approximation)
        self.currentApproxComboBox.setCurrentText(approximation.legend)
        
        for line in preview_lines:
            if line != None:
                self.plotted_previews.append(line)
        # show canvas0
        self.template_canvas.show()
        # redraw canvas0
        self.template_canvas.draw()
        self.preview_already_plotted = True
        #self.initStages() 


    def on_clear_previews_clicked(self):
        if self.preview_already_plotted:
            for line in self.plotted_previews:
                line.pop(0).remove()
            self.template_canvas.draw()
            self.plotted_previews = []
            self.template_axes.get_legend().remove()
            self.template_axes_norm.get_legend().remove()
            self.template_canvas.draw()
            self.preview_already_plotted = False
        # redraw template to sclae properly
        # remove all plots widgets. in plotLayout
        self.clear_plot_layout()
        # plot template in specified axes
        self.template_axes = self.template_fig.add_subplot(211)
        self.template_axes_norm = self.template_fig.add_subplot(212)
        self.template.plot_template_in_axes(self.template_axes, self.template_axes_norm)
        # add canvas0 to plotLayout
        self.plotsLayout.addWidget(self.template_canvas)
        # show canvas0
        self.template_canvas.show()
        # redraw canvas0
        self.template_canvas.draw()
        # set template submited to True
        self.template_submited = True
        self.approximations.clear()
        self.currentApproxComboBox.Items.clear()
        self.currentApproximation=None
        self.currentApproxComboBox.setCurrentText("None")
        self.validate_approximation()
        

    def on_compute_clicked(self):
        # eliminar los plots de plotsLayout
        compute_options = [self.plot_attenuation, self.plot_phase, self.plot_group_delay, self.plot_step_response, self.plot_s_plane, self.plot_freq_resp]
        count = 0
        
        for opt in compute_options:
            if opt:
                count = count + 1
        self.plots_axes = []
        if self.plot_attenuation:
            # if previously plotted, clear
            if self.att_plotted:
                self.att_axes.clear()
            # create axes in figure
            self.att_axes = self.att_fig.add_subplot(111)
            left, right = self.approximation.plot_attenuation_to_axes(self.att_axes)

            t_left, t_right = self.template_axes.get_xlim()
            if t_left > left:
                left = t_left

            if t_right < right:
                right = t_right

            self.att_axes.set_xlim(left, right)
            self.att_axes.set_ylim(auto=True)
            self.att_axes.grid(True, which='minor',axis='both')
            self.att_axes.yaxis.grid()
            self.att_plotted = True
            self.att_canvas.draw()
            self.att_canvas.show()
        if self.plot_phase:
            # if previously plotted, clear
            if self.phase_plotted:
                self.phase_axes.clear()
            # create axes in figure
            self.phase_axes = self.phase_fig.add_subplot(111)
            left, right = self.template_axes.get_xlim()
            limits = {'left':left, 'right':right}
            p_left, p_right = self.approximation.plot_phase_to_axes(self.phase_axes, limits)

            if p_left > left:
                left = p_left

            if p_right < right:
                right = p_right
            self.phase_axes.set_xlim(left, right)
            self.phase_axes.set_ylim(auto=True)
            self.phase_axes.legend()
            self.phase_axes.grid(True, which='minor',axis='both')
            self.phase_axes.yaxis.grid()
            self.phase_plotted = True
            self.phase_canvas.draw()
            self.phase_canvas.show()
        if self.plot_group_delay:
            # if previously plotted, clear
            if self.group_delay_plotted:
                self.group_axes.clear()
            # create axes in figure
            self.group_axes = self.group_fig.add_subplot(111)
            left, right = self.template_axes.get_xlim()
            limits = {'left':left, 'right':right}
            p_left, p_right = self.approximation.plot_group_delay_to_axes(self.group_axes, limits)

            self.group_axes.set_ylim(auto=True)
            self.group_axes.legend()
            self.group_axes.grid(True, which='minor',axis='both')
            self.group_axes.xaxis.grid()
            self.group_axes.yaxis.grid()
            self.group_delay_plotted = True
            self.group_canvas.draw()
            self.group_canvas.show()
        if self.plot_step_response:
            # if previously plotted, clear
            if self.step_plotted:
                self.step_axes.clear()
            # create axes in figure
            self.step_axes = self.step_fig.add_subplot(111)
            left, right = self.template_axes.get_xlim()
            limits = {'left':left, 'right':right}
            self.approximation.plot_step_response_to_axes(self.step_axes)

            self.step_axes.set_ylim(auto=True)
            self.step_axes.legend()
            self.step_axes.grid(True, which='minor',axis='both')
            self.step_axes.xaxis.grid()
            self.step_axes.yaxis.grid()
            self.step_plotted = True
            self.step_canvas.draw()
            self.step_canvas.show()
        if self.plot_s_plane:
            # if previously plotted, clear
            if self.s_plane_plotted:
                self.s_plane_axes.clear()
            # create axes in figure
            self.s_plane_axes = self.s_plane_fig.add_subplot(111, projection='polar')
            left, right = self.template_axes.get_xlim()
            limits = {'left':left, 'right':right}
            self.approximation.plot_s_plane_to_axes(self.s_plane_axes)

            self.s_plane_axes.set_ylim(auto=True)
            self.s_plane_axes.legend()
            self.s_plane_plotted = True
            self.s_plane_canvas.draw()
            self.s_plane_canvas.show()
        if self.plot_freq_resp:
            # if previously plotted, clear
            if self.freq_response_plotted:
                self.freq_axes.clear()
            # create axes in figure
            self.freq_axes = self.freq_fig.add_subplot(111)
            left, right = self.template_axes.get_xlim()
            limits = {'left':left, 'right':right}
            p_left, p_right = self.approximation.plot_freq_response_to_axes(self.freq_axes, limits)

            if p_left > left:
                left = p_left

            if p_right < right:
                right = p_right
            self.freq_axes.set_xlim(left, right)
            self.freq_axes.set_ylim(auto=True)
            self.freq_axes.legend()
            self.freq_axes.grid(True, which='minor',axis='both')
            self.freq_axes.yaxis.grid()
            self.freq_response_plotted = True
            self.freq_canvas.draw()
            self.freq_canvas.show()
        return


    def on_set_current_approx_clicked(self):
        
        selectedLegend=self.currentApproxComboBox.currentText()
        if selectedLegend != "None":
            for approximation in self.approximations:
                if approximation.legend==selectedLegend: selectedApproximation=approximation
            self.setCurrentApproximation(selectedApproximation)
        else : self.setCurrentApproximation(None)

    class groupBoxPar(QtWidgets.QGroupBox):
        radioButtons=[]
        par=None
        
        
    class stageRadioButton(QtWidgets.QRadioButton):
        stage=None
        
    def updateStages(self):
        self.currentApproximation.updateStages()
        
    def clearLayout(self, layout):
        if layout.count()!=0:
            for i in reversed(range(layout.count())): 
                tempWidget=layout.itemAt(i).widget()
                if tempWidget is not None and str(tempWidget.accessibleName())!="scroll": tempWidget.setParent(None)
    
    def setCurrentApproximation(self, approximation):
        self.clearLayout(self.horizontalLayout_30)
        self.clearLayout(self.horizontalLayout_29)
        self.clearLayout(self.paresGroupBoxLayout)
        self.currentApproximation=approximation
        if approximation is not None:
            self.setStagesPushButton.show()
            self.horizontalLayout_30.addWidget(approximation.mainStageFigureCanvas)
            approximation.plotToStagesTab()
            for stage in approximation.stages:  
                self.horizontalLayout_29.addWidget(stage.figurecanvas)
                stage.plotStage()
            for pairList in [approximation.poles, approximation.zeros]:
                for pair in pairList:
                    self.paresGroupBoxLayout.addWidget(pair.groupBox)
            #currentItem=[self.currentApproxComboBox.itemText(count) for count in range(self.currentApproxComboBox.count())]  
        else: 
            self.setStagesPushButton.hide()
            #self.currentApproximation=None
            #self.currentApproxComboBox.setCurrentText("None")


            #for item in [self.polesGroupBoxes, self.zerosGroupBoxes]:
            #    if item != []:     
            #        for groupbox in item:
            #            for radioButton in groupbox.radioButtons:
            #                if radioButton.isChecked():
            #                    groupbox.par.assignToStage(radioButton.stage)
            #    else: print("Update stages: no zero or pole detected")
            #for stage in self.stages:
            #    stage.plotStage()
            #    stage.figurecanvas.draw()
            
    
    #def resetTransferFigure(self):
    #    fig = Figure()
    #    figure_canvas = FigureCanvas(fig)
    #    self.horizontalLayout_30.addWidget(figure_canvas)
    #    # show canvas0
    #    figure_canvas.show()
    #    # redraw canvas0
    #    figure_canvas.draw()
    #    return fig, figure_canvas

    #    def getNewStageFigure(self):
    #        fig = Figure()
    #        figure_canvas = FigureCanvas(fig)
    #        return fig, figure_canvas
    #    self.horizontalLayout_29.addWidget(figure_canvas)
    #    # show canvas0
    #    figure_canvas.show()
    #    # redraw canvas0
    #    figure_canvas.draw()
            
def main():
    QtCore.qInstallMessageHandler(qt_message_handler)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    filter_tool = FilterTool()
    filter_tool.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()
from PyQt5 import QtGui, QtWidgets, QtCore
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import FilterToolDesign
import sys
import numpy as np
from Template import Template
import Approximation
import matplotlib.pyplot as mpl

## Class inherited from Ui_MainWindow to customize GUI design and behaviour
class FilterTool(QtWidgets.QMainWindow, FilterToolDesign.Ui_MainWindow):
    def __init__(self, parent=None):
        super(FilterTool, self).__init__(parent)
        self.setupUi(self)

        # configure to use latex interpreter
        mpl.rc('font',**{'family':'serif','serif':['Palatino']})
        mpl.rc('text', usetex=True)

        # array containing approximation types
        self.approx_types = ['butterworth', 'bessel', 'chevy_1', 'chevy_2', 'legendre', 'gauss', 'cauer']

        # connect 'preview aproximation' button to handler
        self.previewApproxButton.clicked.connect(self.on_preview_clicked)
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
        self.fig0 = Figure()
        self.canvas0 = FigureCanvas(self.fig0)
        self.fig1 = Figure()
        self.canvas1 = FigureCanvas(self.fig1)
        self.fig2 = Figure()
        self.canvas2 = FigureCanvas(self.fig2)
        self.fig3 = Figure()
        self.canvas3 = FigureCanvas(self.fig3)
        self.fig4 = Figure()
        self.canvas4 = FigureCanvas(self.fig4)
        self.fig5 = Figure()
        self.canvas5 = FigureCanvas(self.fig5)
        self.fig6 = Figure()
        self.canvas6 = FigureCanvas(self.fig6)

        self.figure_list = [self.fig0, self.fig1, self.fig2, self.fig3, self.fig4, self.fig5, self.fig6]


    ## Handles a filter type combo box index change.
    #  @details Execuetes whwnever the selected index in filter type combo box changes.
    #  @param self The object pointer
    def on_filter_type_changed(self):
        selectedText = self.filterTypeComboBox.currentText()
        if selectedText == 'Low-pass':
            self.hide_pass_stop_2()
        if selectedText == 'High-Pass':
            self.hide_pass_stop_2()
        if selectedText == 'Band-pass':
            self.show_pass_stop_2()
        if selectedText == 'Band-reject':
            self.show_pass_stop_2()


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
        self.ax1f0 = self.fig0.add_subplot(211)
        self.ax2f0 = self.fig0.add_subplot(212)
        self.template.plot_template_in_axes(self.ax1f0, self.ax2f0)
        # add canvas0 to plotLayout
        self.plotsLayout.addWidget(self.canvas0)
        # show canvas0
        self.canvas0.show()
        # redraw canvas0
        self.canvas0.draw()
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
        self.approximation = Approximation.Butterworth(self.template,
                                         restriction = self.restriction,
                                         min_order = self.minOrderSpinBox.value(),
                                         max_order = self.maxOrderSpinBox.value(),
                                         max_q = self.maxQdoubleSpinBox.value(),
                                         custom_order = self.customOrderSpinBox.value())
        self.approximation.compute_approximation()
        self.approximation.plot_preview_to_axes(self.ax1f0, self.ax2f0)
        # show canvas0
        self.canvas0.show()
        # redraw canvas0
        self.canvas0.draw()


    def on_compute_clicked(self):
        pass
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    filter_tool = FilterTool()
    filter_tool.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()
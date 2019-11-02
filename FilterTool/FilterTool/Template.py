from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import colors as mcolors
import math
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


class Template(object):
    def __init__(self, filter_type, **kwargs):
        self.filter_types = {'Low-pass', 'High-pass', 'Band-pass', 'Band-reject'}
        
        if filter_type in self.filter_types:
            ## @var filter_type
            #  String variable indicating the template filter type
            self.filter_type = filter_type
        
        ## @var omega_p1
        #  Lowest passband frequency in Hz
        self.omega_p1 = kwargs['omega_p1']
        ## @var omega_s1
        #  Lowest stopband frquency in Hz
        self.omega_s1 = kwargs['omega_s1']
        ## @var omega_p2
        #  Highest passband frequency in Hz
        self.omega_p2 = kwargs['omega_p2']
        ## @var omega_s2
        #  Highest stopband frequency in Hz
        self.omega_s2 = kwargs['omega_s2']
        ## @var att_p
        #  Max attenuation in passband
        self.att_p = kwargs['att_p']
        ## @var att_s
        #  Min attenuation in stopband
        self.att_s = kwargs['att_s']

        self.final = kwargs['final']

        if self.final:
            self.__normalize()
        return


    ## Validates template data
    #  @details Checks if the configuration of the template is valid
    #  @param self The object pointer
    #  @return Boolean value. True if valid. False otherwise
    def is_valid(self):
        if self.filter_type == 'Low-pass':
            ret = self.__validate_low_pass()
        elif self.filter_type == 'High-pass':
            ret = self.__validate_high_pass()
        elif self.filter_type == 'Band-pass':
            ret = self.__validate_band_pass()
        elif self.filter_type == 'Band-reject':
            ret = self.__validate_band_reject()
        else:
            ret = False
        return ret


    ## Validation for low pass template type
    #  @param self The object pointer
    #  @return Boolean value. True if valid. False otherwise
    def __validate_low_pass(self):
        valid = False
        valid = (self.omega_p1 < self.omega_s1) and (self.att_p < self.att_s)
        return valid


    ## Validation for high pass template type
    #  @param self The object pointer
    #  @return Boolean value. True if valid. False otherwise
    def __validate_high_pass(self):
        valid = False
        valid = (self.omega_s1 < self.omega_p1) and (self.att_p < self.att_s)
        return valid


    ## Validation for band pass template type
    #  @param self The object pointer
    #  @return Boolean value. True if valid. False otherwise
    def __validate_band_reject(self):
        valid = False
        valid = (self.omega_p1 < self.omega_s1) and (self.omega_s1 < self.omega_s2) and (self.omega_s2 < self.omega_p2)
        valid = valid and (self.att_p < self.att_s)
        valid = valid and self.__validate_symmetry(self.omega_p1, self.omega_s1, self.omega_p2, self.omega_s2)
        return valid


    ## Validation for band reject template type
    #  @param self The object pointer
    #  @return Boolean value. True if valid. False otherwise
    def __validate_band_pass(self):
        valid = False
        valid = (self.omega_s1 < self.omega_p1) and (self.omega_p1 < self.omega_p2) and (self.omega_p2 < self.omega_s2)
        valid = valid and (self.att_p < self.att_s)
        valid = valid and self.__validate_symmetry(self.omega_p1, self.omega_s1, self.omega_p2, self.omega_s2)
        return valid


    ## Validates if template is symmetric
    #  @param self The object pointer
    #  @param wp1 Lowest passband frequency
    #  @param ws1 Lowest stopband frequency
    #  @param wp2 Highest psasband frequency
    #  @param ws2 Highest stopband frequency
    #  @return Boolean value. True if symmetric condition fullfilled. False otherwise
    def __validate_symmetry(self, wp1, ws1, wp2, ws2):
        valid = False
        valid = (wp1*wp2 == ws1*ws2)
        return valid


    def __normalize(self):
        self.omega_pN = 1
        if self.filter_type == 'Low-pass':
            self.omega_sN = self.omega_s1/self.omega_p1
        elif self.filter_type == 'High-pass':
            self.omega_sN = self.omega_p1/self.omega_s1
        elif self.filter_type == 'Band-pass':
            delta_ws = self.omega_s2 - self.omega_s1
            delta_wp = self.omega_p2 - self.omega_p1
            self.omega_sN = delta_ws/delta_wp
        elif self.filter_type == 'Band-reject':
            delta_ws = self.omega_s2 - self.omega_s1
            delta_wp = self.omega_p2 - self.omega_p1
            self.omega_sN = delta_wp/delta_ws
        return

            

    ## Plots the template in specified axes.
    #  @details receives an axes object and plots the template in it
    #  @param self The object pointer
    #  @param axes The axes object where the plot is to be drawn
    def plot_template_in_axes(self, axes, axes_N):
        self.__plot_normalized(axes_N)
        if self.filter_type == 'Low-pass':
            self.__plot_low_pass(axes)
        elif self.filter_type == 'High-pass':
            self.__plot_high_pass(axes)
        elif self.filter_type == 'Band-pass':
            self.__plot_band_pass(axes)
        elif self.filter_type == 'Band-reject':
            self.__plot_band_reject(axes)
        else:
            pass
        axes.set_xlabel(r'$\omega [rad/seg] (log)$')
        axes.set_ylabel(r'$|A(\omega)| [dB]$')
        axes.set_title(r'Configured Template')
        axes_N.set_xlabel(r'$\frac{\omega}{\omega_N} (log)$')
        axes_N.set_ylabel(r'$|A(\omega)| [dB]$')
        axes_N.set_title(r'Normalized Template')
        return axes


    def __plot_low_pass(self, axes):


        int_p, dec_p = divmod(math.log10(self.omega_p1),1)
        int_s, dec_s = divmod(math.log10(self.omega_s1),1)

        x_left = int_p - 1
        x_right = int_s + 2

        rect1 = Rectangle((0, self.att_p), self.omega_p1, 1e3*self.att_s)
        rect2 = Rectangle((self.omega_s1, 0), 1e3*self.omega_s1, self.att_s)
        rectangles = []
        rectangles.append(rect1)
        rectangles.append(rect2)
        patch_collection = PatchCollection(rectangles, facecolor='tab:gray', alpha=0.5, edgecolor='k', hatch='/')
        axes.add_collection(patch_collection)
        axes.set_xscale('log')
        axes.set_ylim([0, 2*self.att_s])
        axes.set_xlim([math.pow(10,x_left), math.pow(10,x_right)])
       

    def __plot_high_pass(self, axes):


        int_p, dec_p = divmod(math.log10(self.omega_p1),1)
        int_s, dec_s = divmod(math.log10(self.omega_s1),1)

        x_left = int_p - 1
        x_right = int_s + 2

        rect1 = Rectangle((0, 0), self.omega_s1, self.att_s)
        rect2 = Rectangle((self.omega_p1, self.att_p), 1e3*self.omega_s1, 1e3*self.att_s)
        rectangles = []
        rectangles.append(rect1)
        rectangles.append(rect2)
        patch_collection = PatchCollection(rectangles, facecolor='tab:gray', alpha=0.5, edgecolor='k', hatch='/')
        axes.add_collection(patch_collection)
        axes.set_xscale('log')
        axes.set_ylim([0, 2*self.att_s])
        axes.set_xlim([math.pow(10,x_left), math.pow(10,x_right)])


    def __plot_band_pass(self, axes):


        int_p, dec_p = divmod(math.log10(self.omega_s1),1)
        int_s, dec_s = divmod(math.log10(self.omega_s2),1)

        x_left = int_p - 1
        x_right = int_s + 2

        rect1 = Rectangle((0, 0), self.omega_s1, self.att_s)
        rect2 = Rectangle((self.omega_p1, self.att_p), self.omega_p2 - self.omega_p1, 1e3*self.att_s)
        rect3 = Rectangle((self.omega_s2, 0), 1e6*self.omega_p2, self.att_s)
        rectangles = []
        rectangles.append(rect1)
        rectangles.append(rect2)
        rectangles.append(rect3)
        patch_collection = PatchCollection(rectangles, facecolor='tab:gray', alpha=0.5, edgecolor='k', hatch='/')
        axes.add_collection(patch_collection)
        axes.set_xscale('log')
        axes.set_ylim([0, 2*self.att_s])
        axes.set_xlim([math.pow(10,x_left), math.pow(10,x_right)])

        
    def __plot_band_reject(self, axes):


        int_p, dec_p = divmod(math.log10(self.omega_p1),1)
        int_s, dec_s = divmod(math.log10(self.omega_p2),1)

        x_left = int_p - 1
        x_right = int_s + 2

        rect1 = Rectangle((0, self.att_p), self.omega_p1, 1e3*self.att_s)
        rect2 = Rectangle((self.omega_s1, 0), self.omega_s2 - self.omega_s1, self.att_s)
        rect3 = Rectangle((self.omega_p2, self.att_p), 1e6*self.omega_p2, 1e3*self.att_s)
        rectangles = []
        rectangles.append(rect1)
        rectangles.append(rect2)
        rectangles.append(rect3)
        patch_collection = PatchCollection(rectangles, facecolor='tab:gray', alpha=0.5, edgecolor='k', hatch='/')
        axes.add_collection(patch_collection)
        axes.set_xscale('log')
        axes.set_ylim([0, 2*self.att_s])
        axes.set_xlim([math.pow(10,x_left), math.pow(10,x_right)])


    def __plot_normalized(self, axes):


        int_p, dec_p = divmod(math.log10(self.omega_pN),1)
        int_s, dec_s = divmod(math.log10(self.omega_sN),1)

        x_left = int_p - 1
        x_right = int_s + 2

        rect1 = Rectangle((0, self.att_p), self.omega_pN, 1e3*self.att_s)
        rect2 = Rectangle((self.omega_sN, 0), 1e6*self.omega_sN, self.att_s)
        rectangles = []
        rectangles.append(rect1)
        rectangles.append(rect2)
        patch_collection = PatchCollection(rectangles, facecolor='tab:gray', alpha=0.5, edgecolor='k', hatch='/')
        axes.add_collection(patch_collection)
        axes.set_xscale('log')
        axes.set_ylim([0, 2*self.att_s])
        axes.set_xlim([math.pow(10,x_left), math.pow(10,x_right)])
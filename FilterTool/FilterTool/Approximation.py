from Template import Template
from scipy import signal
import math
import numpy as np

class Approximation(object):
    """description of class"""
    def __init__(self, template,**kwargs):

        self.template = template
        self.restriction = kwargs['restriction']
        self.min_order = kwargs['min_order']
        self.max_order = kwargs['max_order']
        self.max_q = kwargs['max_q']
        self.custom_order = kwargs['custom_order']


class Butterworth(Approximation):
    def __init__(self, template, **kwargs):
        super().__init__(template, **kwargs)

        self.approx_type = 'butterworth'
        self.__compute_parameters()

    def __compute_parameters(self):
        if self.restriction == 'custom_order':
            self.__parameters_cusotm_order()
        elif self.restriction == 'max_q':
            self.__parameters_max_q()

        if self.template.filter_type == 'Low-pass' or self.template.filter_type == 'High-pass':
            self.wp = self.template.omega_p1
            self.ws = self.template.omega_s1
        elif self.template.filter_type == 'Band-pass' or self.template.filter_type == 'Band-reject':
            self.wp = [self.template.omega_p1, self.template.omega_p2]
            self.ws = [self.template.omega_s1, self.template.omega_s2]

        if self.template.filter_type == 'Low-pass':
            self.filter_t = 'lowpass'
        elif self.template.filter_type == 'High-pass':
            self.filter_t = 'highpass'
        elif self.template.filter_type == 'Band-pass':
            self.filter_t = 'bandpass'
        elif self.template.filter_type == 'Band-reject':
            self.filter_t = 'bandstop'
            
    def __parameters_cusotm_order(self):
        self.order = self.custom_order
        self.epsilon = math.sqrt(math.pow(10,self.template.att_s/10)-1)/math.pow(self.template.omega_sN, self.custom_order)

    def __parameters_max_q(self):
        aux = (2/math.pi)*math.acos(1/(2*self.max_q))
        n_max = 1/(1-aux)
        i, d = divmod(n_max,1)
        self.order_max_q = i

    def __parameters_min_max_order(self):
        self.epsilon_n_max = math.sqrt(math.pow(10,self.template.att_s/10)-1)/math.pow(self.template.omega_sN, self.max_order)
        self.epsilon_n_min = math.sqrt(math.pow(10,self.template.att_s/10)-1)/math.pow(self.template.omega_sN, self.min_order)

    def compute_approximation(self):
        self.__compute_approximation_norm()
        self.__compute_approximation_denorm()


    def __compute_approximation_denorm(self):
        # compute the approximation for the denormalized template
        N, wn = signal.buttord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.order
        elif self.restriction == 'max_q':
            if N < self.order_max_q:
                self.N = N
            elif N > self.order_max_q:
                self.N = self.order_max_q
        elif self.restriction == 'min_max_order':
            if N < self.min_order:
                self.N = self.min_order
            elif N > self.max_order:
                self.N = self.max_order
            else:
                self.N = N

        self.num, self.den = signal.butter(self.N, wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.butter(self.N, wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.butter(self.N, wn, self.filter_t, analog=True, output='sos')

    def __compute_approximation_norm(self):
        # compute the approximation for the normalized template
        N, wn = signal.buttord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.order
        elif self.restriction == 'max_q':
            if N < self.order_max_q:
                self.N = N
            elif N > self.order_max_q:
                self.N = self.order_max_q
        elif self.restriction == 'min_max_order':
            if N <= self.min_order:
                self.N = self.min_order
            elif N >= self.max_order:
                self.N = self.max_order
            else:
                self.N = N

        self.num_norm, self.den_norm = signal.butter(self.N, wn, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.butter(self.N, wn, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.butter(self.N, wn, 'lowpass', analog=True, output='sos')

    def plot_preview_to_axes(self,axes, axes_N):
        w, h = signal.freqs(self.den, self.num, 10000)
        axes.semilogx(w, 20 * np.log10(abs(h)))

        w_n, h_n = signal.freqs(self.den_norm, self.num_norm, 10000)
        axes_N.semilogx(w_n, 20 * np.log10(abs(h_n)))
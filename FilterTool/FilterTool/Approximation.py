from Template import Template
from scipy import signal
import math
import numpy as np


# TODO: sacar solo debug
import matplotlib.pyplot as mpl

class Approximation(object):
    """description of class"""
    def __init__(self, template,**kwargs):

        self.template = template
        self.restriction = kwargs['restriction']
        self.min_order = kwargs['min_order']
        self.max_order = kwargs['max_order']
        self.max_q = kwargs['max_q']
        self.custom_order = kwargs['custom_order']
        self.approx_type = kwargs['approx_type']

        if self.approx_type == 'butterworth':
            self.approx_type_pretty = 'Butterworth'
        elif self.approx_type == 'bessel':
            self.approx_type_pretty = 'Bessel'
        elif self.approx_type == 'cheby_1':
            self.approx_type_pretty = 'Chebyshev I'
        elif self.approx_type == 'cheby_2':
            self.approx_type_pretty = 'Chebyshev II'
        elif self.approx_type == 'legendre':
            self.approx_type_pretty = 'Legendre'
        elif self.approx_type == 'gauss':
            self.approx_type_pretty = 'Gauss'
        elif self.approx_type == 'cauer':
            self.approx_type_pretty = 'Cauer'

        self.__compute_parameters()

    def __compute_parameters(self):
        if self.restriction == 'max_q':
            self.__parameters_max_q()

        if self.template.filter_type == 'Low-pass':
            self.wp = self.template.omega_p1
            self.ws = self.template.omega_s1
            self.filter_t = 'lowpass'
        elif self.template.filter_type == 'High-pass':
            self.wp = self.template.omega_p1
            self.ws = self.template.omega_s1
            self.filter_t = 'highpass'
        elif self.template.filter_type == 'Band-pass':
            self.filter_t = 'bandpass'
            self.wp = [self.template.omega_p1, self.template.omega_p2]
            self.ws = [self.template.omega_s1, self.template.omega_s2]
        elif self.template.filter_type == 'Band-reject':
            self.filter_t = 'bandstop'
            self.wp = [self.template.omega_p1, self.template.omega_p2]
            self.ws = [self.template.omega_s1, self.template.omega_s2]


    def __parameters_max_q(self):
        if self.approx_type == 'butterworth':
            aux = (2/math.pi)*math.acos(1/(2*self.max_q))
            n_max = 1/(1-aux)
            i, d = divmod(n_max,1)
            self.order_max_q = i
        elif self.approx_type == 'bessel':
            pass
        elif self.approx_type == 'cheby_1':
            pass
        elif self.approx_type == 'cheby_2':
            pass
        elif self.approx_type == 'lgendre':
            pass
        elif self.approx_type == 'gauss':
            pass
        elif self.approx_type == 'cauer':
            pass


    def __compute_epsilon(self):
        self.order = self.N
        if self.approx_type == 'butterworth':
            self.epsilon = math.sqrt(math.pow(10,self.template.att_s/10)-1)/math.pow(self.template.omega_sN, self.order)
        elif self.approx_type == 'bessel':
            pass
        elif self.approx_type == 'cheby_1':
            self.epsilon = math.sqrt(math.pow(10,self.template.att_s/10)-1)/math.cosh(self.order * math.acosh(self.template.omega_sN))
        elif self.approx_type == 'cheby_2':
            self.epsilon = 1/(math.cosh(math.acosh(1/self.template.omega_pN) * self.order) * math.sqrt(math.pow(10, self.template.att_p/10) - 1))
            pass
        elif self.approx_type == 'legendre':
            pass
        elif self.approx_type == 'gauss':
            pass
        elif self.approx_type == 'cauer':
            pass


    def compute_approximation(self):
        if self.approx_type == 'butterworth':
            self.__compute_approximation_denorm_butter()
            self.__compute_approximation_norm_butter()
        elif self.approx_type == 'bessel':
            self.__compute_approximation_denorm_bessel()
            self.__compute_approximation_norm_bessel()
        elif self.approx_type == 'cheby_1':
            self.__compute_approximation_denorm_cheby_1()
            self.__compute_approximation_norm_cheby_1()
        elif self.approx_type == 'cheby_2':
            self.__compute_approximation_denorm_cheby_2()
            self.__compute_approximation_norm_cheby_2()
        elif self.approx_type == 'bessel':
            pass
        elif self.approx_type == 'gaiss':
            pass
        elif self.approx_type == 'cauer':
            self.__compute_approximation_denorm_cauer()
            self.__compute_approximation_norm_cauer()
            pass

    def __compute_approximation_denorm_butter(self):
        # compute the approximation for the denormalized template
        N, wn = signal.buttord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.custom_order
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


    def __compute_approximation_norm_butter(self):
        # compute the approximation for the normalized template
        N, wn = signal.buttord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.custom_order
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


    def __compute_approximation_denorm_bessel(self):
        wn = self.wp
        if self.restriction == 'custom_order':
            self.N = self.custom_order
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

        self.num, self.den = signal.bessel(self.N, wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.bessel(self.N, wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.bessel(self.N, wn, self.filter_t, analog=True, output='sos')


    def __compute_approximation_norm_bessel(self):
        wn = self.template.omega_pN
        if self.restriction == 'custom_order':
            self.N = self.custom_order
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

        self.num_norm, self.den_norm = signal.bessel(self.N, wn, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.bessel(self.N, wn, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.bessel(self.N, wn, 'lowpass', analog=True, output='sos')


    def __compute_approximation_denorm_cheby_1(self):
        # compute the approximation for the denormalized template
        N, wn = signal.cheb1ord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.custom_order
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

        self.__compute_epsilon()

        self.num, self.den = signal.cheby1(self.N, self.template.att_p, wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.cheby1(self.N, self.template.att_p, wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.cheby1(self.N, self.template.att_p, wn, self.filter_t, analog=True, output='sos')


    def __compute_approximation_norm_cheby_1(self):
        # compute the approximation for the normalized template
        N, wn = signal.cheb1ord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.custom_order
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
        
        self.__compute_epsilon()

        self.num_norm, self.den_norm = signal.cheby1(self.N, self.template.att_p, wn, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.cheby1(self.N, self.template.att_p, wn, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.cheby1(self.N, self.template.att_p, wn, 'lowpass', analog=True, output='sos')


    def __compute_approximation_denorm_cheby_2(self):
        # compute the approximation for the denormalized template
        N, wn = signal.cheb2ord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.custom_order
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


        self.num, self.den = signal.cheby2(self.N, self.template.att_s, wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.cheby2(self.N, self.template.att_s, wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.cheby2(self.N, self.template.att_s, wn, self.filter_t, analog=True, output='sos')


    def __compute_approximation_norm_cheby_2(self):
        # compute the approximation for the normalized template
        N, wn = signal.cheb2ord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.custom_order
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

        self.num_norm, self.den_norm = signal.cheby2(self.N, self.template.att_s, wn, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.cheby2(self.N, self.template.att_s, wn, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.cheby2(self.N, self.template.att_s, wn, 'lowpass', analog=True, output='sos')


    def __compute_approximation_denorm_cauer(self):
        # compute the approximation for the denormalized template
        N, wn = signal.ellipord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.custom_order
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

        self.num, self.den = signal.ellip(self.N, self.template.att_p, self.template.att_s, wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.ellip(self.N, self.template.att_p, self.template.att_s, wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.ellip(self.N, self.template.att_p, self.template.att_s, wn, self.filter_t, analog=True, output='sos')


    def __compute_approximation_norm_cauer(self):
        # compute the approximation for the normalized template
        N, wn = signal.ellipord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if self.restriction == 'custom_order':
            self.N = self.custom_order
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

        self.num_norm, self.den_norm = signal.ellip(self.N, self.template.att_p, self.template.att_s, wn, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.ellip(self.N, self.template.att_p, self.template.att_s, wn, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.ellip(self.N, self.template.att_p, self.template.att_s, wn, 'lowpass', analog=True, output='sos')

    def plot_preview_to_axes(self, axes, axes_N, limits):
        n_str = str(self.N)
        legend = self.approx_type_pretty + ' - Order: ' + n_str
        left = limits['left']
        right = limits['right']
        left_N = limits['left_N']
        right_N = limits['right_N']
        
        w, h = signal.freqs(self.den, self.num,worN = np.logspace(math.log10(left), math.log10(right), 1000))
        line = axes.semilogx(w, 20 * np.log10(abs(h)), label=legend)
        max_value = np.max(20 * np.log10(abs(h)))
        axes.legend(loc='best')
        bottom, top = axes.get_ylim()
        if max_value > top:
            axes.set_ylim((bottom, max_value))
        w_n, h_n = signal.freqs(self.den_norm, self.num_norm, np.logspace(math.log10(left_N), math.log10(right_N), 1000))
        line_N = axes_N.semilogx(w_n, 20 * np.log10(abs(h_n)), label=legend)
        axes_N.legend(loc='best')
        max_value = np.max(20 * np.log10(abs(h_n)))
        axes.legend(loc='best')
        bottom, top = axes_N.get_ylim()
        if max_value > top:
            axes_N.set_ylim((bottom, max_value))

        return [line,line_N]

    def plot_attenuation_to_axes(self, axes):
        legend = 'Attenuation'
        n_points = 10000
        w, h = signal.freqs(self.den, self.num, n_points)
        line = axes.semilogx(w, 20 * np.log10(abs(h)), label=legend)
        axes.set_xlabel(r'$\omega [rad/seg]$')
        axes.set_ylabel(r'$|A(\omega)| [dB]$')
        axes.legend(loc='best')
        first_w = w.item(0)
        last_w = w.item(n_points-1)

        return first_w, last_w

    def plot_phase_to_axes(self, axes,limits):
        legend = 'Phase'
        n_points = 1000
        sys = signal.TransferFunction(self.num, self.den)
        left = limits['left']
        right = limits['right']
        w_in = np.logspace(np.log10(left), np.log10(right), num=n_points)
        w, mag, phase = signal.bode(sys, w_in)
        line = axes.semilogx(w, phase, label=legend)
        axes.set_xlabel(r'$\omega [rad/seg]$')
        axes.set_ylabel(r'Phase')
        first_w = w.item(0)
        last_w = w[-1]

        return first_w, last_w

    def plot_group_delay_to_axes(self, axes, limits):
        legend = 'Group Delay'
        n_points = 1000
        w, gd = signal.group_delay((self.num, self.den))
        axes.plot(w, gd, label=legend)
        axes.set_xlabel(r'Frequency [rad/sample]')
        axes.set_ylabel(r'Group Delay [samples]')
        first_w = w.item(0)
        last_w = w[-1]

        return first_w, last_w

    def plot_step_response_to_axes(self, axes):
        legend = 'Step Response'
        n_points = 1000
        t, y = signal.step((self.num, self.den),N=n_points)
        axes.plot(t, y, label=legend)
        axes.set_xlabel(r'Time(seg)')
        axes.set_ylabel(r'V[Volts]')

    def plot_s_plane_to_axes(self, axes):
        legend_poles = 'Poles'
        marker_poles = 'x'
        legend_zeros = 'Zeros'
        marker_zeros = 'o'


        r_poles = []
        theta_poles = []
        r_zeros = []
        theta_zeros = []

        for complex in self.poles:
            r = np.real(complex)
            i = np.imag(complex)
            rho = np.sqrt(r**2 + i**2)
            theta = np.arctan2(i,r)
            r_poles.append(rho)
            theta_poles.append(theta)


        for complex in self.zeros:
            r = np.real(complex)
            i = np.imag(complex)
            rho = np.sqrt(r**2 + i**2)
            theta = np.arctan2(i,r)
            r_zeros.append(rho)
            theta_zeros.append(theta)

        if theta_poles:
            axes.scatter(theta_poles, r_poles, label=legend_poles, marker=marker_poles)
        if theta_zeros:
            axes.scatter(theta_zeros, r_zeros, label=legend_zeros, marker=marker_zeros)

    def plot_freq_response_to_axes(self, axes, limits):
        legend = 'Frequency Response[dB]'
        n_points = 1000
        sys = signal.TransferFunction(self.num, self.den)
        left = limits['left']
        right = limits['right']
        w_in = np.logspace(np.log10(left), np.log10(right), num=n_points)
        w, mag, phase = signal.bode(sys, w_in)
        line = axes.semilogx(w, mag, label=legend)
        axes.set_xlabel(r'$\omega [rad/seg]$')
        axes.set_ylabel(r'Mag')
        first_w = w.item(0)
        last_w = w[-1]

        return first_w, last_w


from Template import Template
from scipy import signal
import math
import numpy as np
import cmath
# TODO: sacar solo debug
import matplotlib.pyplot as mpl
from Etapa import *

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
        self.den=[]
        self.num=[]
        self.den_norm=[]
        self.num_norm=[]
        

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

        if self.restriction == 'max_q':
            self.__parameters_max_q()
        elif self.restriction == 'custom_order':
            self.order = self.__parameters_custom_order()
        elif self.restriction == 'min_max_order':
            self.order = self.__parameters_min_max_order()


    def __parameters_custom_order(self):
        order = self.custom_order
        if self.approx_type == 'butterworth':
            N, self.wn = signal.buttord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
            N_norm, self.wn_N = signal.buttord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)
        elif self.approx_type == 'bessel':
            pass
        elif self.approx_type == 'cheby_1':
            N, self.wn = signal.cheb1ord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
            N_norm, self.wn_N = signal.cheb2ord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)
        elif self.approx_type == 'cheby_2':
            N, self.wn = signal.cheb2ord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
            N_norm, self.wn_N = signal.cheb1ord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)
        elif self.approx_type == 'lgendre':
            pass
        elif self.approx_type == 'gauss':
            pass
        elif self.approx_type == 'cauer':
            N, self.wn = signal.ellipord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
            N_norm, self.wn_N = signal.ellipord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        return order


    def __order_min_max_butter(self):
        N, self.wn = signal.buttord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
        N_norm, self.wn_N = signal.buttord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if N < self.min_order:
            order = self.min_order
        elif N > self.max_order:
            order = self.max_order
        else:
            order = N

        return order


    def __order_min_max_cheby_1(self):
        N, self.wn = signal.cheb1ord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
        N_norm, self.wn_N = signal.cheb2ord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if N < self.min_order:
            order = self.min_order
        elif N > self.max_order:
            order = self.max_order
        else:
            order = N

        return order


    def __order_min_max_cheby_2(self):
        N, self.wn = signal.cheb2ord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
        N_norm, self.wn_N = signal.cheb1ord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if N < self.min_order:
            order = self.min_order
        elif N > self.max_order:
            order = self.max_order
        else:
            order = N

        return order


    def __order_min_max_cauer(self):
        N, self.wn = signal.ellipord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
        N_norm, self.wn_N = signal.ellipord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if N < self.min_order:
            order = self.min_order
        elif N > self.max_order:
            order = self.max_order
        else:
            order = N

        return order


    def __parameters_max_q(self):
        if self.approx_type == 'butterworth':
            order_q = self.__order_max_q_butter()
            N, self.wn = signal.buttord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
            N_norm, self.wn_N = signal.buttord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)
        elif self.approx_type == 'bessel':
            order_q = self.__order_max_q_bessel()
            N = order_q
        elif self.approx_type == 'cheby_1':
            order_q = self.__order_max_q_cheby_1()
            N, self.wn = signal.cheb1ord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
            N_norm, self.wn_N = signal.cheb2ord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)
        elif self.approx_type == 'cheby_2':
            order_q = self.__order_max_q_cheby_2()
            N, self.wn = signal.cheb2ord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
            N_norm, self.wn_N = signal.cheb1ord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)
        elif self.approx_type == 'lgendre':
            pass
        elif self.approx_type == 'gauss':
            pass
        elif self.approx_type == 'cauer':
            order_q = self.__order_max_q_cauer()
            N, self.wn = signal.ellipord(self.wp, self.ws, self.template.att_p, self.template.att_s, analog=True)
            N_norm, self.wn_N = signal.ellipord(self.template.omega_pN, self.template.omega_sN, self.template.att_p, self.template.att_s, analog=True)

        if order_q > N:
            self.order = N
        elif order_q <= N:
            self.order = order_q


    def __parameters_min_max_order(self):
        if self.approx_type == 'butterworth':
            order = self.__order_min_max_butter()
            pass
        elif self.approx_type == 'cheby_1':
            order = self.__order_min_max_cheby_1()
            pass
        elif self.approx_type == 'cheby_2':
            order = self.__order_min_max_cheby_2()
            pass
        elif self.approx_type == 'cauer':
            order = self.__order_min_max_cauer()
            pass
        return order
        

    def __order_max_q_butter(self):
        found = False
        order = 0
        wn = self.wp
        q = []
        while not found:
            order = order + 1
            zeros, poles, gain = signal.butter(order, wn, self.filter_t, analog=True, output='zpk')
            for p in poles:
                r, phi = cmath.polar(p)
                q.append(r/(2*abs(r*math.cos(phi))))
            max_q = max(q)
            if (q and max_q >= self.max_q ) or order > 15:
                found = True
        return order


    def __order_max_q_bessel(self):
        found = False
        order = 0
        wn = self.wp
        q = []
        while not found:
            order = order + 1
            zeros, poles, gain = signal.bessel(order, wn, self.filter_t, analog=True, output='zpk')
            for p in poles:
                r, phi = cmath.polar(p)
                q.append(r/(2*abs(r*math.cos(phi))))
            max_q = max(q)
            if (q and max_q >= self.max_q ) or order > 15:
                found = True
        return order


    def __order_max_q_cheby_1(self):
        found = False
        order = 0
        wn = self.wp
        q = []
        while not found:
            order = order + 1
            zeros, poles, gain = signal.cheby1(order, self.template.att_p, wn, self.filter_t, analog=True, output='zpk')
            for p in poles:
                r, phi = cmath.polar(p)
                q.append(r/(2*abs(r*math.cos(phi))))
            max_q = max(q)
            if (q and max_q >= self.max_q ) or order > 15:
                found = True
        return order


    def __order_max_q_cheby_2(self):
        found = False
        order = 0
        wn = self.wp
        q = []
        while not found:
            order = order + 1
            zeros, poles, gain = signal.cheby2(order, self.template.att_s, wn, self.filter_t, analog=True, output='zpk')
            for p in poles:
                r, phi = cmath.polar(p)
                q.append(r/(2*abs(r*math.cos(phi))))
            max_q = max(q)
            if (q and max_q >= self.max_q ) or order > 15:
                found = True
        return order


    def __order_max_q_cauer(self):
        found = False
        order = 0
        wn = self.wp
        q = []
        while not found:
            order = order + 1
            zeros, poles, gain = signal.ellip(order, self.template.att_p, self.template.att_s, wn, self.filter_t, analog=True, output='zpk')
            for p in poles:
                r, phi = cmath.polar(p)
                q.append(r/(2*abs(r*math.cos(phi))))
            max_q = max(q)
            if (q and max_q >= self.max_q ) or order > 15:
                found = True
        return order


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
        self.num, self.den = signal.butter(self.order, self.wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.butter(self.order, self.wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.butter(self.order, self.wn, self.filter_t, analog=True, output='sos')


    def __compute_approximation_norm_butter(self):
        self.num_norm, self.den_norm = signal.butter(self.order, 1, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.butter(self.order, self.wn_N, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.butter(self.order, self.wn_N, 'lowpass', analog=True, output='sos')


    def __compute_approximation_denorm_bessel(self):
        self.num, self.den = signal.bessel(self.order, self.wp, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.bessel(self.order, self.wp, self.filter_t, analog=True, output='zpk')
        self.sos = signal.bessel(self.order, self.wp, self.filter_t, analog=True, output='sos')


    def __compute_approximation_norm_bessel(self):
        self.num_norm, self.den_norm = signal.bessel(self.order, self.template.omega_pN, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.bessel(self.order, self.template.omega_pN, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.bessel(self.order, self.template.omega_pN, 'lowpass', analog=True, output='sos')


    def __compute_approximation_denorm_cheby_1(self):
        self.num, self.den = signal.cheby1(self.order, self.template.att_p, self.wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.cheby1(self.order, self.template.att_p, self.wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.cheby1(self.order, self.template.att_p, self.wn, self.filter_t, analog=True, output='sos')


    def __compute_approximation_norm_cheby_1(self):        
        self.num_norm, self.den_norm = signal.cheby1(self.order, self.template.att_p, 1, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.cheby1(self.order, self.template.att_p, self.wn_N, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.cheby1(self.order, self.template.att_p, self.wn_N, 'lowpass', analog=True, output='sos')


    def __compute_approximation_denorm_cheby_2(self):
        self.num, self.den = signal.cheby2(self.order, self.template.att_s, self.wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.cheby2(self.order, self.template.att_s, self.wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.cheby2(self.order, self.template.att_s, self.wn, self.filter_t, analog=True, output='sos')


    def __compute_approximation_norm_cheby_2(self):
        self.num_norm, self.den_norm = signal.cheby2(self.order, self.template.att_s, 1, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.cheby2(self.order, self.template.att_s, self.wn, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.cheby2(self.order, self.template.att_s, self.wn, 'lowpass', analog=True, output='sos')


    def __compute_approximation_denorm_cauer(self):
        self.num, self.den = signal.ellip(self.order, self.template.att_p, self.template.att_s, self.wn, self.filter_t, analog=True, output='ba')
        self.zeros, self.poles, self.gain = signal.ellip(self.order, self.template.att_p, self.template.att_s, self.wn, self.filter_t, analog=True, output='zpk')
        self.sos = signal.ellip(self.order, self.template.att_p, self.template.att_s, self.wn, self.filter_t, analog=True, output='sos')



    def __compute_approximation_norm_cauer(self):
        self.num_norm, self.den_norm = signal.ellip(self.order, self.template.att_p, self.template.att_s, 1, 'lowpass', analog=True, output='ba')
        self.zeros_norm, self.poles_norm, self.gain_norm = signal.ellip(self.order, self.template.att_p, self.template.att_s, self.wn, 'lowpass', analog=True, output='zpk')
        self.sos_norm = signal.ellip(self.order, self.template.att_p, self.template.att_s, self.wn, 'lowpass', analog=True, output='sos')


    def compute_factorization(self):
        self.sos = signal.zpk2sos(selg.zeros, self.poles, self.gain)


    def plot_preview_to_axes(self, axes, axes_N, limits):
        n_str = str(self.order)
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

    def getZPKList(self):
        ##Recibe un nominador y denominador de una transferencia y devuelve:
        ##  -Zeros: Una lista de listas de zeros agrupados de a par con parte real igual
        ##      Pej: Si los zeros son   Z1 = 1+1j
        ##                              Z2 = 1-1j
        ##                              Z3 = 3
        ##              -> Zeros = [ [1+1j , 1-1j], [3] ]
        ##  -Poles: una lista de listas de polos agrupados de la misma manera
        ##  -K: Ganancia total de la transferenci
        z,p,k = signal.tf2zpk(self.num,self.den)
        zeros = []
        poles = []
        used = []
        colors = ['r','g','b','c','m','y','k']
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
        
        for index, pair in enumerate(zeros):
            for zero in pair:
                zero=Zero(zero,colors[index])
        for index, pair in enumerate(poles):
            for pole in pair:
                pole=Pole(pole,colors[index])
        return zeros,poles,k
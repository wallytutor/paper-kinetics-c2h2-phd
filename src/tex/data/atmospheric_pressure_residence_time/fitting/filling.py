#!/home/dalmazsi1/python3.4/bin/python

""" Compute exit concentration from RTD and global kinetics.
    Author : Walter Dal'Maz Silva
    Date   : 15th December 2015
"""

import pylab
import numpy as np
import matplotlib.pyplot as plt

Qin = 500.0/6.0e+07 #m3/s
Vr  = 1.0e-03       #m3

time = np.arange(0.0, 2000.0, 0.1)

for t in time:
    yt_yo = (1.0-np.exp(-(Qin/Vr)*t))
    if (np.fabs(yt_yo-1.0) < 1.0e-05):
        print(' Steady after %.3e' %t)
        break
        
##def integrate(tmax, dt, Yi, Wi, pars):
##
##    time = np.array(0.0e+00, tmax, dt)
##
##    def Wbar(*Yi, *Wi):
##        return 1.0/np.sum([y/w for w, y in zip(Yi, Wi)])
##            
##    def rho(P, T, *Yi, *Wi):
##        RGASC = 8.31442
##        return P*Wbar(Yi, Wi)/(RGASC*T)
##
##    def johnson_SB(t, *pars):
##        np.seterr(all='ignore')        
##        f_delta, f_lambda, f_xi, f_gamma = pars
##        z       = (t-f_xi)/f_lambda
##        arg_log   = np.fabs(z/(1.0-z))
##        pre_exp = f_delta/(f_lambda*np.sqrt(2.0*np.pi)*z*(1.0-z))
##        arg_exp = -0.5*(f_gamma+f_delta*np.log(arg_log))**2.0
##        func    = pre_exp*np.exp(arg_exp)
##        return func
##
##    def dYdt(t, m, mdot, Yin, Yk, rho, Wk, *pars):
##        return (1.0/m)*(mdot*(Yin-Yk*johnson_SB(t, pars))-k*(rho*Yk/Wk)**2.0
##
##    save = open('concentration_t.dat', 'w')
##    for t in time:
##        Yi[0] += dYdt*dt
##        save.write(str('%.3f %.6e\n' %(t, Yk)))
##
##
##Yi = [0.02, 0.98]
##Wi = [0.026, 0.028]
##
##integrate(3000.0, 1.0, pars)

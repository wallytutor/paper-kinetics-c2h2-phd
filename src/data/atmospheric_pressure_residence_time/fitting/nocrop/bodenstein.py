#!/home/dalmazsi1/python3.4/bin/python

""" Estimate Bodenstein number from RTD.
    Fit Johnson distribution peak to data.
    Levenberg-Marquardt algorithm
    Author : Walter Dal'Maz Silva
    Date   : 72th Nakar 9820#F
"""

import warnings
import pylab
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ----------------------------------------------------------------------------
# File info
# ----------------------------------------------------------------------------

def fit_johnson(srcf, *pars, plot=True):

    guess=(1.361543e+00, 9.912823e+02, 5.400621e+00, 2.582672e+00)
    
    data = np.genfromtxt(srcf, delimiter='	')
    colt, colf, to = pars
    
    t  = data[1:, colt]
    f  = data[1:, colf]

    ti = t[to]
    t  = t[to:]
    f  = f[to:]
    t -= ti

    def johnson_SB(t, *pars):
        np.seterr(all='ignore')        
        f_delta, f_lambda, f_xi, f_gamma = pars
        z       = (t-f_xi)/f_lambda
        arg_log   = np.fabs(z/(1.0-z))
        pre_exp = f_delta/(f_lambda*np.sqrt(2.0*np.pi)*z*(1.0-z))
        arg_exp = -0.5*(f_gamma+f_delta*np.log(arg_log))**2.0
        func    = pre_exp*np.exp(arg_exp)
        return func

    # Optimize function
    try:
        popt, pcov = curve_fit(johnson_SB, t, f, guess, maxfev = 1000000)
        res = johnson_SB(t, *popt)
    except RuntimeError:
        print("Error - fit_johnson curve_fit failed")
    
    fit = str(" p0=[%.16e, %.16e,\n     %.16e, %.16e]"\
              %(popt[0], popt[1], popt[2], popt[3]))
              
    if plot:
        print(fit)
        plt.title(srcf)
        plt.xlabel('t')
        plt.ylabel('f')
        plt.xlim(np.min(t), np.max(t))
        plt.ylim(np.min(f), 1.05*np.max(f))
        plt.plot(t, f)
        plt.plot(t, res, 'r-')
        plt.legend(['data', 'fit1'])
        plt.show()

    return t, res, fit

# ----------------------------------------------------------------------------
# File info
# ----------------------------------------------------------------------------

def fit_bodenstein(src, crop, cols, plot=True, guess=10.0,\
                   title='', d_L=0.05/0.10):
    report = open('report.dat', 'a')
    colt, colE = cols

    def bodenstein(theta, Bo):
        np.seterr(all='ignore')
        pre_exp = np.sqrt(Bo/(4*theta*np.pi))
        arg_exp = Bo*(1.0-theta)**2.0/(4.0*theta)
        func    = pre_exp/(np.exp(arg_exp))
        return func
            
    # Find a Johnson fit for the peak
    t, E, fit = fit_johnson(src, colt, colE, crop, plot=True)

    # Compute reduced time
    theta   = t/np.trapz(t*E, t)
    E_theta = t*E

    theta   = theta[1:]
    E_theta = E_theta[1:]

    # Optimize function
    try:
        popt, pcov = curve_fit(bodenstein, theta, E_theta, guess)
        res = bodenstein(theta, popt)
    except RuntimeError:
        print("Error - fit_johnson curve_fit failed")

    # Save data
    report.write(src)
    report.write('\n Fitting graphic in  %s.png' %title)
    report.write('\n Bodenstein number   %.3f' %popt[0])
    report.write('\n Peclet_ax number    %.3f' %(popt[0]*d_L))
    report.write('\n Integral =          %.2f' %(np.trapz(res, theta)))
    report.write('\n Johnson parameters: \n\t'+fit)
    report.write('\n\n\n')

    if plot:
        plt.xlabel('theta')
        plt.ylabel('E(theta)')
        plt.plot(theta, E_theta)
        plt.plot(theta, res, 'r-')
        plt.legend(['data', 'fit'])
        pylab.savefig(title+'.png', dpi=400)
        plt.close()
    report.close()
    
# ----------------------------------------------------------------------------
# File info
# ----------------------------------------------------------------------------

temps = ['T1023K_', 'T1173K_']
flows = ['D0500CCN2', 'D1000CCN2']
loads = ['./../../unloaded/', './../../loaded/']

files = [(loads[0]+temps[0]+flows[0], 1, (0,1), 'u'+temps[0]+flows[0]),\
         (loads[0]+temps[1]+flows[0], 1, (0,1), 'u'+temps[1]+flows[0]),\
         (loads[0]+temps[1]+flows[1], 1,  (0,1), 'u'+temps[1]+flows[1]),\
         (loads[1]+temps[0]+flows[0], 1, (0,1), 'l'+temps[0]+flows[0]),\
         (loads[1]+temps[1]+flows[0], 1, (0,1), 'l'+temps[1]+flows[0]),\
         (loads[1]+temps[1]+flows[1], 1, (0,1), 'l'+temps[1]+flows[1])]

# ----------------------------------------------------------------------------
# Treat data
# ----------------------------------------------------------------------------

for f in files:
    src, crop, cols, title = f
    print(' Starting problem analysis...', src)
    fit_bodenstein(src+'.dat', crop, cols, title=title, plot=True)

# ----------------------------------------------------------------------------
# End of file
# ----------------------------------------------------------------------------

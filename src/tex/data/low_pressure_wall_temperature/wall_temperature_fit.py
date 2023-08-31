# -*- coding: utf-8 -*-
"""
wall_temperature_fit.py
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def curve(x, Treg, *args):
    Treg *= 0.98
    a1, a2, m1, m2 = args
    st_trm = 1.0 - np.exp(-(x / a1) ** m1)
    nd_trm = 1.0 - np.exp(-(x / a2) ** m2)
    st_trm *= (Treg - 300.0)
    nd_trm *= (Treg - 400.0)
    return 300.0 + st_trm - nd_trm

if __name__ == '__main__':
    data = pd.read_csv('data.csv')

    arrX = data['x']
    X = np.linspace(min(arrX), max(arrX), 100)
    T = [h for h in data.columns.values if h != 'x']
    G = 0.1, 0.6, 2.0, 2.0

    plt.clf()
    for Tmp in T:
        arrT = data[Tmp]

        def wrap(x, *g):
            return curve(x, float(Tmp), *g)

        popt, pcov = curve_fit(wrap, arrX, arrT, G, maxfev=8000)
        plt.plot(arrX, arrT)
        plt.plot(X, wrap(X, *popt))
        print(Tmp, popt)

    plt.show()
    # plt.savefig('fit-plateau.png')

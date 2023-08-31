# -*- coding: utf-8 -*-
"""
wall_temperature_plot.py
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from wall_temperature_fit import curve


print(plt.style.available)

data = pd.read_csv('data.csv')
X = data['x']
T = {'773': [0.04132785, 0.36577369, 1.92089871, 12.45807035],
     '1073': [0.02505570, 0.40273247, 0.81240579, 16.32508022],
     '1273': [0.02682819, 0.39723982, 0.90958936, 11.93402048]}

plt.clf()
plt.style.use('seaborn-paper')
plt.figure(figsize=(5, 4))
mpl.rcParams['font.size'] = 14
mpl.rcParams['axes.labelsize'] = 14
mpl.rcParams['xtick.labelsize'] = 12
mpl.rcParams['ytick.labelsize'] = 12
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['axes.linewidth'] = 2.0
mpl.rcParams['axes.edgecolor'] = 'k'
plt.grid(color='k', linestyle=':')
font = FontProperties()
font.set_size('x-small')

Xcalc = np.linspace(0, 0.4, 100)
for k, v in T.items():
    Tcalc = curve(Xcalc, float(k), *T[k])
    Tmeas = data[k]
    plt.plot(100*Xcalc, Tcalc, label='_nolegend_')
    plt.scatter(100*X, Tmeas, label='${{{}}}\,\mathrm{{K}} $'.format(k))

plt.legend(loc='lower center', bbox_to_anchor=(0.5, 0.01), ncol=3,
           frameon=True, fancybox=False, shadow=False, prop=font)
plt.xlabel('Position along reactor axis ($\mathrm{cm}$)')
plt.ylabel('Wall temperature ($\mathrm{K}$)')
plt.xlim(0, 40)
plt.ylim(300, 1300)
plt.yticks(np.arange(300, 1301, 200))
plt.subplots_adjust(bottom=0.13, top=0.98, right=0.97, left=0.16)
plt.savefig('wall_temperature_plot', dpi=300)

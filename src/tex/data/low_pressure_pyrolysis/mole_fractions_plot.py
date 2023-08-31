#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
residence_time_plot.py
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

files = ['exp_0030mbar.csv', 'exp_0050mbar.csv', 'exp_0100mbar.csv']

plt.clf()
plt.style.use('seaborn')
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

ax = plt.subplot(1, 1, 1)
qr = r'\mathrm{hPa}'

data = pd.read_csv(files[0])
x, y = data['T'], 100 * data['C2H2-m']
ax.plot(x, y, 'o-', label='$30\,{}$'.format(qr))

data = pd.read_csv(files[1])
x, y = data['T'], 100 * data['C2H2-m']
ax.plot(x, y, 'o-', label='$50\,{}$'.format(qr))

data = pd.read_csv(files[2])
x, y = data['T'], 100 * data['C2H2-m']
ax.plot(x, y, 'o-', label='$100\,{}$'.format(qr))

plt.legend(frameon=True, fancybox=False, shadow=False, prop=font)
plt.xlabel('Control temperature ($\mathrm{K}$)')
plt.ylabel('Mole fraction $\\times{}100$')
plt.xlim(750, 1300)
plt.ylim(19, 37)
plt.xticks(np.arange(773, 1274, 100))
plt.yticks(np.arange(20, 37, 4))
plt.subplots_adjust(bottom=0.13, top=0.98, right=0.97, left=0.16)
plt.savefig('fractions_low_pressure', dpi=300)

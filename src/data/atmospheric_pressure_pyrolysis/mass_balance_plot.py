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

files = ['mass_balance_c_0500sccm.csv', 'mass_balance_h_0500sccm.csv']

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

data = pd.read_csv(files[0])
x, y = data['T'], 100 * data['CT']
ax.plot(x, y, 'o-', label='Total $\mathrm{C}$ atoms')

data = pd.read_csv(files[1])
x, y = data['T'], 100 * data['HT']
ax.plot(x, y, 'o-', label='Total $\mathrm{H}$ atoms')

plt.legend(frameon=True, fancybox=False, shadow=False, prop=font)
plt.xlabel('Control temperature ($\mathrm{K}$)')
plt.ylabel('Retrieved mole balance - $\Psi{}(\%)$')
plt.xlim(850, 1250)
plt.ylim(15, 105)
plt.xticks(np.arange(873, 1224, 50))
plt.yticks(np.arange(20, 101, 10))
plt.subplots_adjust(bottom=0.13, top=0.98, right=0.97, left=0.16)
plt.savefig('balance_atmospheric_pressure', dpi=300)

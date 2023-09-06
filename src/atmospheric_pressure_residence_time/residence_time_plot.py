#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
residence_time_plot.py
"""

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

files = ['unloaded/T1173K_D0500CCN2.csv',
         'unloaded/T1173K_D1000CCN2.csv']

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

label = '{:.0f}'
unit = '\,\mathrm{cm^{3}\,min^{-1}}'

for fname in files:
    data = pd.read_csv(fname)
    x = data['t(s)']
    y = 100 * data['E(s)']
    flow = float(fname[-12:-8])
    lab = label.format(flow)
    plt.plot(x, y, label='${}$'.format(lab + unit))

ylabel = ('Probability density'
          ' ($\\times{}10^{-2}\mathrm{s^{-1}}$)')
plt.legend(frameon=True, fancybox=False, shadow=False, prop=font)
plt.xlabel('Residence time $\\tau_{eff}$ ($\mathrm{s}$)')
plt.ylabel(ylabel)
plt.xlim(0, 700)
plt.ylim(0, 1)
plt.subplots_adjust(bottom=0.13, top=0.98, right=0.97, left=0.16)
plt.savefig('residence_time_plot', dpi=300)

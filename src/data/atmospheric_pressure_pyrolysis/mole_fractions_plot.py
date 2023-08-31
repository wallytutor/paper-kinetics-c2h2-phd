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
from matplotlib.patches import Rectangle

files = ['mole_fraction_0500sccm.csv', 'mole_fraction_1000sccm.csv']

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
im1l, im2l = [], []
for fname in files:
    data = pd.read_csv(fname)
    x, y1, y2 = data['T'], 100 * data['C2H2'], 100 * data['H2']
    im1l.append(ax.plot(x, y1, 'o-')[0])
    im2l.append(ax.plot(x, y2, 'o-')[0])

extra = Rectangle((0, 0), 1, 1, fc="w", fill=False,
                  edgecolor='none', linewidth=0)

legend_handle = [extra,  extra, extra,
                 extra, im1l[0], im1l[1],
                 extra, im2l[0], im2l[1]]

qr = r'$\mathrm{cm^3\,min^{-1}}$'
label_col_1 = ['', r'500 {}'.format(qr), r'1000 {}'.format(qr)]
label_s1 = [r'$\mathrm{C_2H_2}$']
label_s2 = [r'$\mathrm{H_2}$']
label_empty = ['']

legend_labels = np.concatenate([label_col_1,
                                label_s1, label_empty * 2,
                                label_s2, label_empty * 2])

ax.legend(legend_handle, legend_labels,
          frameon=True, fancybox=False,
          shadow=False, prop=font, borderpad=1,
          handlelength=2,
          ncol=3, handletextpad=-1.8)

plt.xlabel('Control temperature ($\mathrm{K}$)')
plt.ylabel('Mole fraction $\\times{}100$')
plt.xlim(850, 1250)
plt.ylim(-0.1, 2.2)
plt.xticks(np.arange(873, 1224, 50))
plt.yticks(np.arange(0.0, 2.11, 0.3))
plt.subplots_adjust(bottom=0.13, top=0.98, right=0.97, left=0.16)
plt.savefig('fractions_atmospheric_pressure_main', dpi=300)

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
im1l, im2l = [], []
for fname in files:
    data = pd.read_csv(fname)
    x, y1, y2 = data['T'], 1000 * data['CH4'], 1000 * data['C2H4']
    im1l.append(ax.plot(x, y1, 'o-')[0])
    im2l.append(ax.plot(x, y2, 'o-')[0])

extra = Rectangle((0, 0), 1, 1, fc="w", fill=False,
                  edgecolor='none', linewidth=0)

legend_handle = [extra,  extra, extra,
                 extra, im1l[0], im1l[1],
                 extra, im2l[0], im2l[1]]

qr = r'$\mathrm{cm^3\,min^{-1}}$'
label_col_1 = ['', r'500 {}'.format(qr), r'1000 {}'.format(qr)]
label_s1 = [r'$\mathrm{CH_4}$']
label_s2 = [r'$\mathrm{C_2H_4}$']
label_empty = ['']

legend_labels = np.concatenate([label_col_1,
                                label_s1, label_empty * 2,
                                label_s2, label_empty * 2])

ax.legend(legend_handle, legend_labels,
          frameon=True, fancybox=False,
          shadow=False, prop=font, borderpad=1,
          handlelength=2,
          ncol=3, handletextpad=-1.8)

plt.xlabel('Control temperature ($\mathrm{K}$)')
plt.ylabel('Mole fraction $\\times{}1000$')
plt.xlim(850, 1250)
plt.ylim(-0.05, 1.05)
plt.xticks(np.arange(873, 1224, 50))
plt.yticks(np.arange(0.0, 1.1, 0.2))
plt.subplots_adjust(bottom=0.13, top=0.98, right=0.97, left=0.16)
plt.savefig('fractions_atmospheric_pressure_other', dpi=300)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-source.py

@author: dalmazsi1
"""

import pandas as pd
from XCantera.plug import PlugFlowReactorWrap

# ****************************************************************************
# Global configuration file
# ****************************************************************************

config = """
[ GENERAL ]

walltemp = 300 + {}
hommechn = hydrocarbon-norinaga-2009-gas.cti
gasphase = gas
energyeq = on
transmod = None
filesave = {}
transrad = {}
conducti = 1000000 * T

[ GEOMETRY ]

radius = 0.014
length = 0.450
slices = 0.0005

[ OPERATION ]

P = {}
Q = {}

[ INLET ]

N2       = {}
H2       = {}
C2H2     = 0.3528
CH3COCH3 = 0.0065
CH4      = 0.0007

[ SOLVER ]

relerr = 1.0e-15
abserr = 1.0e-20
saveat = 0.005
"""

# ****************************************************************************
# Global configuration file
# ****************************************************************************

data = pd.read_csv('conditions-source.csv')

for idx, row in data.iterrows():
    if idx < 10:
        continue

    P = row['P']
    Q = row['Q']
    R = row['R']
    W = row['W']
    N2 = row['N2']
    H2 = row['H2']
    save = row['save']

    conf = config.format(W, save, R, P, Q, N2, H2)
    pfr = PlugFlowReactorWrap(conf, zipall=False, each=10)
    pfr.plot(['C2H2'])

# ****************************************************************************
# EOF
# ****************************************************************************

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run-simple.py

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
hommechn = hydrocarbon-dalmazsi-2017-trans-gas.cti
gasphase = gas
energyeq = on
transmod = Multi
filesave = {}
transrad = {}

[ GEOMETRY ]

radius = 0.014
length = 0.450
slices = 0.001

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

relerr = 1.0e-12
abserr = 1.0e-20
saveat = 0.005
"""

# ****************************************************************************
# Global configuration file
# ****************************************************************************

data = pd.read_csv('conditions-simple.csv')

for idx, row in data.iterrows():
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

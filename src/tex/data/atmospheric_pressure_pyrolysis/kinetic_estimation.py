#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:40:25 2018

@author: dalmazsi1
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import ode


r = 0.025
L = 0.10
V = np.pi * r**2 * L
R = 8.314472
P = 101325
T = 298

data = pd.read_csv("kinetic_estimation.csv")
data = data.loc[data["Q"] < 1000]
#data.loc[data["Q"] == 1000, ("T")] *= 0.98
data["R"] = data["T"] / T
data["Q"] = data["Q"] * data["R"] / 60e+06
data["tau"] = V / data["Q"]


def conc(X, T):
    return P * X / (R * T)


def arr(A, E, T):
    return A * np.exp(-E / (R * T))


def equation(M, A, E):
    X, T, Q = M
    Ci = conc(X, T)
    C0 = conc(0.0207, T)
    kf = arr(A, E, T)
    return Q * (C0 - Ci) - 2 * kf * Ci**2


def kinetic(t, X, T, A, E, Q):
    Ci = conc(X, T)
    C0 = conc(0.0207, T)
    kf = arr(A, E, T)
    return (R * T / P) * (Q * (C0 - Ci) - 2 * kf * Ci**2) / V


M = data[["X", "T", "Q"]].as_matrix().T
y = np.zeros(len(data.index))

p0 = [136364.38142581, 179183.21953297]
popt, pcov = curve_fit(equation, M, y, p0=p0)
print("Arrhenius parameters ", popt)
A, E = popt


data = pd.read_csv("kinetic_estimation.csv")
#data.loc[data["Q"] == 1000, ("T")] *= 0.98
data["R"] = data["T"] / T
data["Q"] = data["Q"] * data["R"] / 60e+06
data["tau"] = V / data["Q"]

sol = []
for i,row in data.iterrows():
    T = row["T"]
    t = row["tau"]
    Q = row["Q"]
    solver = ode(kinetic)
    solver.set_integrator("vode", method="bdf")
    solver.set_initial_value(0.0, t=0.0)
    solver.set_f_params(T, A, E, Q)
    solver.integrate(10 * t)
    sol.append(*solver.y)
    
data["Y"] = sol
data["C"] = data["X"] / data["Y"]
print(data)


plt.scatter(data["X"], data["Y"])
plt.plot(data["X"], data["X"], "k")
plt.show()
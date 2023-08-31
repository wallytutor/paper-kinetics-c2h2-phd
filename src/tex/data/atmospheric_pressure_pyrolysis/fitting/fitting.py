#!/usr/bin/python
# by Walter Dal'Maz Silva

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

fname = ["../mole_fraction_0500sccm.csv",
         "../mole_fraction_1000sccm.csv"]

RGAS = 8.314472
x0 = 0.0207
L = 0.100
R = 0.025
V = L * np.pi * R ** 2

data0 = pd.read_csv(fname[0])
data1 = pd.read_csv(fname[1])
data0["t"] = V / (500 / 6.0e+07)
data1["t"] = V / (1000 / 6.0e+07)
data0["t"] *= 298.0 / data0["T"]
data1["t"] *= 298.0 / data1["T"]

data = data0.append(data1)
data = data.loc[:,("T", "t", "C2H2")]


def C(x, T):
    return 101325.0 * x / (RGAS * T)


def k(T, Ai, Ei):
    return Ai * np.exp(-Ei / (RGAS * T))


def model(X, *args):
    Ai, Ei, n = args
    term0 = C(x0, X[:, 0]) ** (1.0 - n)
    term1 = k(X[:, 0], Ai, Ei) * (n - 1.0) * X[:, 1]
    return (term0 + term1) ** (1.0 / (1.0 - n))


data["C2H2"] = C(data["C2H2"], data["T"])
X = data.as_matrix(columns=["T", "t"])
Y = data.as_matrix(columns=["C2H2"])
Y = Y.reshape((len(data.index),))

p0 = (1.0e+09, 1.0e+05, 1.5)
bounds = ([0, 1.0e+04, 1], [+np.inf, +np.inf, 4.0])
popt, pcov = curve_fit(model, X, Y, p0, bounds=bounds)
print(popt)

data["C2H2-calc"] = model(X, *popt)
data["k(T)"] = k(data["T"], popt[0], popt[1])
print(data)

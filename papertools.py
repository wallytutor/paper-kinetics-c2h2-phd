# -*- coding: utf-8 -*-
from scipy.optimize import curve_fit
import statistics
import warnings
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# There are some known small discontinuities in mechanism thermodynamics
# data. Here we suppress warnings regarding this long known issue.
ct.suppress_thermo_warnings()


def temperature_profile(x, T_sp, a1, a2, m1, m2):
    """ Wall temperature profile function. """
    st_trm = (T_sp - 301.0) * (1.0 - np.exp(-(x / a1) ** m1))
    nd_trm = (T_sp - 400.0) * (1.0 - np.exp(-(x / a2) ** m2))
    return 301.0 + st_trm - nd_trm


def fit_wall_temperature(Twall, scale):
    """ Fit wall temperature parameters for case construction. """
    params = []

    plt.close("all")
    plt.style.use("seaborn-white")
    plt.figure(figsize=(12, 6))

    X = np.linspace(Twall["x"].min(), Twall["x"].max(), 100)

    for k, T_sp in enumerate(Twall.columns[1:]):
        arrX = Twall["x"].to_numpy()
        arrT = Twall[T_sp].to_numpy()

        def wrap(x, a1, a2, m1, m2):
            T_pv = float(T_sp) * scale[k]
            return temperature_profile(x, T_pv, a1, a2, m1, m2)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            guess = 0.1, 0.6, 2.0, 2.0
            popt, pcov = curve_fit(wrap, arrX, arrT, guess, maxfev=10_000)
        
        params.append([float(T_sp), scale[k], *popt])
        plt.scatter(arrX, arrT, label=f"{T_sp} K")
        plt.plot(X, wrap(X, *popt), "k:", label="_none_")
        
    plt.grid(linestyle=":")
    plt.xlabel("Position [m]")
    plt.ylabel("Temperature [K]")
    plt.legend(loc=2)
    plt.tight_layout()
    plt.savefig("figures/wall_temperature_fit", dpi=300)
    plt.close("all")

    params_df = pd.DataFrame(params)
    params_df.columns = ["T", "scale", "a1", "a2", "m1", "m2"]
    return params_df


def report_dimensionless(mechanism, T, P, X, L, U):
    """ Compute dimensionless numbers for chemical reactors.

    Parameters
    ----------
    gas : cantera.Solution
        Reactor gas phase.
    L : float
        Characteristic length [m].
    U : float
        Characteristic speed [m/s].
    """
    gas = ct.Solution(mechanism)
    gas.TPX = T, P, X

    alpha_D = statistics.mean(gas.mix_diff_coeffs)
    nu = gas.viscosity / gas.density

    print(f"{gas.report()}\n"
          f"Viscosity... {gas.viscosity:.6e} Pa.s\n"
          f"Re   ....... {reynolds_number(U, L, nu):6e}\n"
          f"Pr_D ....... {prandtl_number(nu, alpha_D):6e}\n"
          f"Pe_D ....... {peclet_number(U, L, alpha_D):6e}\n\n")


def reynolds_number(U, L, nu):
    """ Reynolds number.

    Parameters
    ----------
    U : float or array(flow)
        Fluid velocity [m/s].
    L : float
        Problem characteristic length [m].
    nu : float
        Fluid kinematic velocity [m**2/s].
    """
    return U * L / nu


def prandtl_number(nu, kappa):
    """ Prandtl number.

    Parameters
    ----------
    nu : float
        Fluid kinematic velocity [m**2/s].
    kappa : float.
        Relevant transport coefficient (heat or species) [m**2/s].
    """
    return nu / kappa


def peclet_number(U, L, kappa):
    """ Peclet number.

    Parameters
    ----------
    U : float or array(flow)
        Fluid velocity [m/s].
    L : float
        Problem characteristic length [m].
    kappa : float.
        Relevant transport coefficient (heat or species) [m**2/s].
    """
    return U * L / kappa


def compare_cantera_chemfoam(mechanism, casename, T, P, X, tend=1.0):
    """ Compute solution for comparison with OpenFOAM. """
    gas = ct.Solution(mechanism)
    gas.TPX = T, P, X

    reactor = ct.IdealGasConstPressureReactor(energy="on")
    reactor.insert(gas)

    net = ct.ReactorNet([reactor])
    net.advance(tend)
    
    _results_report_cantera(reactor, gas)
    _results_report_chemfoam(casename)


def _results_report_cantera(reactor, gas):
    """ Report generation for `compare_cantera_chemfoam`. """
    Y = gas.mass_fraction_dict()

    print("Cantera:\n", ", ".join([
        f"T = {reactor.thermo.T:.1f}",
        f"p = {reactor.thermo.P:.0f}",
        f"C2H2 = {Y['C2H2']:.6f}",
        f"CH4 = {Y['CH4']:.6f}"
    ]))


def _results_report_chemfoam(casename):
    """ Report generation for `compare_cantera_chemfoam`. """
    print("\nOpenFOAM:\n")
    with open(f"{casename}/log.chemFoam") as fp:
        row = fp.readlines()[-6].split(",")[1:]
        row = ",".join(row)[:-1]

    with open(f"{casename}/1.000000/CH4") as fp:
        row += ", CH4 =" + fp.readlines()[20:21][0][23:-2]

    print(row)

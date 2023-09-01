# -*- coding: utf-8 -*-
import statistics
import cantera as ct

# There are some known small discontinuities in mechanism thermodynamics
# data. Here we suppress warnings regarding this long known issue.
ct.suppress_thermo_warnings()


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
# -*- coding: utf-8 -*-
from textwrap import dedent
from scipy.optimize import curve_fit
import statistics
import warnings
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyvista as pv

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
    
    print(f"\nCalculations using {mechanism.name}")
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


def plot_mesh(mesh_file, cpos=None, mtm=None, notebook=True):
    """ Display the mesh with axes and camera/zoom configuration.
    
    Parameters
    ----------
    mesh_file : path-like
        Path to mesh file to be parsed for display.
    cpos : list(tuple(floats))
        Camera position passed to `Plotter.show`.
    mtm : np.ndarray [4x4]
        Transformation matrix (for scaling/rotation) passed to
        `Plotter.camera.model_transform_matrix`.
    notebook : bool
        Set to `True` for rendering in a notebook.
    """
    grid = pv.read(mesh_file)
    p = pv.Plotter(notebook=notebook)
    p.set_background(color="k")
    p.add_mesh(grid.copy(), show_edges=True, color="w")
    p.add_axes()
    
    if mtm is not None:
        p.camera.model_transform_matrix = mtm
        
    p.show(cpos=cpos)

    
def get_gmsh2_patches_names(mesh_file):
    """ Get patches names from GMSH v2 file (.msh) for OpenFOAM.
    
    File header is expected to have a structure similar to::

        ```
        $MeshFormat
        2.2 0 8
        $EndMeshFormat
        $PhysicalNames
        6
        2 2 "front"
        2 3 "back"
        2 4 "wall"
        2 5 "inlet"
        2 6 "outlet"
        3 1 "inner"
        $EndPhysicalNames
        ```
        
    Parameters
    ----------
    mesh_file : path-like
        Path to mesh file to be parsed for retrieving data.

    Returns
    -------
    list[str]
        List of patches names as provided in file header.
        
    Raises
    ------
    Exception
        Something is malformed/unexpected in header so that the
        number of patches does not match the expected length.
    ValueError
        Version of GMSH file is not compatible with OpenFOAM.
    """
    names = []
    start = False
    fspec = None
        
    with open(mesh_file) as fp:
        for line in fp.readlines():
            if line.startswith("$MeshFormat"):
                continue

            if line.startswith("$EndMeshFormat"):
                continue

            if line.startswith("$PhysicalNames"):
                start = True
                continue

            if line.startswith("$EndPhysicalNames"):
                break

            if start:
                names.append(line.split()[-1].replace('"', ""))
            else:
                fspec = line[:-1]

        if (gotlen := len(names) - 1) != (expected := int(names[0])):
            raise Exception(f"Bad number of patches: {gotlen} != {expected}")

        if not fspec.startswith("2"):
            raise ValueError(f"OpenFOAM expects GMSH 2 format, got {fspec}")
            
        # TODO check if volumes are always last, so that they can be popped
        # automatically. Also test with a multi-region mesh.
        return names[1:]

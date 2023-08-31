import os
import statistics
import numpy as np
import matplotlib.pyplot as plt
import cantera as ct

plt.style.use('ggplot')
ct.add_directory(os.path.abspath('data'))


class DimLess(object):
    """ DimLess

        Compute dimensionless numbers for chemical reactors.

        Parameters
        ==========
        gas : cantera.Solution
            Reactor gas phase.
        L : float
            Characteristic length [m].
        U : float
            Characteristic speed [m/s].
    """
    def __init__(self, gas, L, U):
        alpha_D = statistics.mean(gas.mix_diff_coeffs)
        nu = gas.viscosity / gas.density
        
        #for s, d in zip(gas.species_names, gas.mix_diff_coeffs):
        #    print(s, d)

        self._Re = self.Re(U, L, nu)

        self.Pr_D = self.Pr(nu, alpha_D)
        self.Pe_D = self.Pe(U, L, alpha_D)
        self.No_D = [self.Pr_D, self.Pe_D]

        self.props = (gas.density, gas.viscosity, L, U)
        self.No = [self._Re] + self.No_D

    @staticmethod
    def Re(U, L, nu):
        """ Re

            Returns Reynolds number.

            Parameters
            ==========
            U : float or array(flow)
                Fluid velocity [m/s].
            L : float
                Problem characteristic length [m].
            nu : float
                Fluid kinematic velocity [m**2/s].
        """
        return U * L / nu

    @staticmethod
    def Pr(nu, kappa):
        """ Pr

            Returns Prandtl number.

            Parameters
            ==========
            nu : float
                Fluid kinematic velocity [m**2/s].
            kappa : float.
                Relevant transport coefficient (heat or species) [m**2/s].
        """
        return nu / kappa

    @staticmethod
    def Pe(U, L, kappa):
        """ Pe

            Returns Peclet number.

            Parameters
            ==========
            U : float or array(flow)
                Fluid velocity [m/s].
            L : float
                Problem characteristic length [m].
            kappa : float.
                Relevant transport coefficient (heat or species) [m**2/s].
        """
        return U * L / kappa

    def __str__(self):
        """ Print formatter. """
        gaspro = (">> Gas density....... {:.6e} kg/m\u00B3\n"
                  ">> Gas viscosity..... {:.6e} Pa.s\n"
                  ">> Strip velocity.... {:.6e} m/s\n"
                  ">> Strip length...... {:.6e} m\n\n").format(*self.props)
        output = (">> Re   = {:6e}\n"
                  ">> Pr_D = {:6e}\n"
                  ">> Pe_D = {:6e}\n\n").format(*self.No)
        return gaspro + output

    def report(self):
        """ Print formatted object data. """
        print(self)

# ----------------------------------------------------------------------------
# Define conditions
# ----------------------------------------------------------------------------

T = 1173.0                       # Temperature [K]
P = 5000.0                       # Pressure [Pa]
X = {'N2': 0.64, 'C2H2': 0.36}   # Composition [mole fraction]
U = 1.0                          # Velocity [m/s]
L = 1.0                          # Length [m]

gas = ct.Solution('CT-hydrocarbon-dalmazsi-2017-mech.xml', 'gas',
        transport_model='Multi')
gas.TPX = T, P, X
print(gas.report())

dim = DimLess(gas, L, U)
dim.report()

# ----------------------------------------------------------------------------
# EOF
# ----------------------------------------------------------------------------

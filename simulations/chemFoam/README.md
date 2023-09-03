# Perfect-stirred reactor simulations

In this  directory we compare results obtained for a perfect-stirred reactor (PSR) using Cantera and chemFoam (the zero-dimensional kinetics solver of OpenFOAM). This is done with the original mechanism by Norinaga (2009) comprised of 243 species and the one obtained in my thesis through extensive DRG skeletal combinations. Mechanisms are stored in another [repository](https://github.com/wallytutor/archive-databases/tree/main) and have been cloned relative to the root of the current one.

## Usage guide for `chemFoam`

Setup of [`chemFoam`](https://www.openfoam.com/documentation/guides/latest/doc/guide-applications-solvers-combustion-chemFoam.html) is simple, we only need the following structure:

### `system/`

- `controlDict`: there we set the system to integrate over one physical second and store only the final state.

- `fvSchemes`: the only definition in regards the time-derivative: explicit solver `Euler` is expected here.

- `fvSolution`: only the integrated species content `Yi` is required.

### `constants/`

- `chemistryProperties`: provides ODE problem parameters. The most important feature here is the use of `seulex` integrator, this being reported to provide the best treatment of stiff systems from chemical kinetics.

- `initialConditions`: we provide the values for automatic generation of `0/` directory. It is a particularity of `chemFoam` that it generates that directory by processing this dictionary. Here we define the reactor to be held at constant pressure and state that composition is provided in mole fractions.

- `thermophysicalProperties`: a `chemistryReader` is provided to be able to interpret mechanism files in the required format. It is recommended to perform conversion for Chemkin II format and check files for any errors, giving preference to OpenFOAM own format here. The use of `<constant>` means the files are to be stored in the `constant/` case directory.

More about `chemFoam` is provided in a dedicated [wiki](https://openfoamwiki.net/index.php/ChemFoam).

## Verification of reference case

For verification of the following reports, first one must execute (under Linux) the [runall.sh](runall.sh) script for generation of `chemFoam` results, then use the [report.py](report.py) script found in this directory for post-processing. The report below provides and order of magnitude of some dimensionless numbers.

```bash
  gas:

       temperature   1173.2 K
          pressure   5000 Pa
           density   0.014098 kg/m^3
  mean mol. weight   27.503 kg/kmol
   phase of matter   gas

                          1 kg             1 kmol     
                     ---------------   ---------------
          enthalpy        4.2021e+06        1.1557e+08  J
   internal energy        3.8474e+06        1.0582e+08  J
           entropy             10261        2.8221e+05  J/K
    Gibbs function       -7.8355e+06        -2.155e+08  J
 heat capacity c_p            1741.7             47901  J/K
 heat capacity c_v            1439.4             39587  J/K

                      mass frac. Y      mole frac. X     chem. pot. / RT
                     ---------------   ---------------   ---------------
              C2H2           0.33401            0.3528           -9.0479
               CH4        0.00041999           0.00072           -43.879
          CH3COCH3          0.013684           0.00648           -73.972
                N2           0.65189              0.64           -28.735
     [  +37 minor]                 0                 0  

Viscosity... 3.965682e-05 Pa.s
Re   ....... 3.555050e+02
Pr_D ....... 8.671141e-01
Pe_D ....... 3.082634e+02
```

## Comparison of Cantera and chemFoam

Predicted final compositions and temperature are in good agreement between both solvers. There are many factors that might be the origin of the deviations we observe here, which could be related to internals of models, ODE integrator, ... but that is above the scope of the present paper.

- DRG mechanism

```bash
Cantera:
 T = 1298.8, p = 5000, C2H2 = 0.242606, CH4 = 0.001410

OpenFOAM:

 T = 1299.9, p = 5000, C2H2 = 0.24196, CH4 = 0.00141113
```

- Detailed mechanism

```bash
Cantera:
 T = 1299.7, p = 5000, C2H2 = 0.240127, CH4 = 0.001216

OpenFOAM:

 T = 1301.02, p = 5000, C2H2 = 0.239335, CH4 = 0.00121622
```

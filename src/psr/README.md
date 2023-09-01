---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.6
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Comparison of Cantera and chemFoam

In this notebook we compare results obtained for a perfect-stirred reactor (PSR) using Cantera and chemFoam (the zero-dimensional kinetics solver of OpenFOAM). This is done with the original mechanism by Norinaga (2009) comprised of 243 species and the one obtained in my thesis through extensive DRG skeletal combinations. There are some known small discontinuities in mechanism thermodynbamics data. Here we suppress warnings regarding this long known issue.

```python
from pathlib import Path
import cantera as ct
import pandas as pd

ct.suppress_thermo_warnings()
```

Mechanisms are stored in another [repository](https://github.com/wallytutor/archive-databases/tree/main) and have been cloned relative to the root of the current one. Below we assembly the paths to retrieve Cantera files.

```python
databases = Path("../../../archive-databases/kinetics/")

norinaga2009 = "Norinaga_2009/CT-hydrocarbon-norinaga-2009-mech.yaml"
dalmazsi2017 = "Dalmazsi_2017_sk41/CT-hydrocarbon-dalmazsi-2017-mech.yaml"

norinaga2009 = databases / norinaga2009
dalmazsi2017 = databases / dalmazsi2017
```

Next we compute the reference initial conditions in required units. Since acetylene is stored in liquid acetone, pollution of the gas is expected are discussed by Noringa (2009). Chemical composition is provided in mole fractions, a more convenient quantity when dealing with low pressure gas phases.

```python
# Temperature [K]
T = 1173.15

# Pressure [Pa]
P = 5000.0

# Relative C2H2 mole fraction.
C = 0.36

# Dictionary of detailed mole fractions.
X = {"N2":       0.64,
     "C2H2":     0.980 * C,
     "CH3COCH3": 0.018 * C,
     "CH4":      0.002 * C}

pd.DataFrame.from_dict([X])
```

Below we run both cases and compare values from the solvers, showing good aggreement between temperature and chemical composition for major species.

```python
def compare_cantera_chemfoam(mechanism, name, tend=1.0):
    """ Compute solution for comparison with OpenFOAM. """
    gas = ct.Solution(mechanism)
    gas.TPX = T, P, X

    reactor = ct.IdealGasConstPressureReactor(energy="on")
    reactor.insert(gas)

    net = ct.ReactorNet([reactor])
    net.advance(tend)
    
    Y = gas.mass_fraction_dict()
    
    print("Cantera:\n", ", ".join([
        f"T = {reactor.thermo.T:.1f}",
        f"p = {reactor.thermo.P:.0f}",
        f"C2H2 = {Y['C2H2']:.6f}",
        f"CH4 = {Y['CH4']:.6f}"
    ]))

    print("\nOpenFOAM:\n")
    with open(f"{name}/log.chemFoam") as fp:
        row = fp.readlines()[-6].split(",")[1:]
        row = ",".join(row)[:-1]

    with open(f"{name}/1.000000/CH4") as fp:
        row += ", CH4 =" + fp.readlines()[20:21][0][23:-2]

    print(row)
```

```python
compare_cantera_chemfoam(dalmazsi2017, "dalmazsi-2017")
```

```python
compare_cantera_chemfoam(norinaga2009, "norinaga-2009")
```

## Afterword: `chemFoam` tutorial

### `system/`

- System dictionaries for `chemFoam` are quite simple. A traditional `controlDict` is expected and there we set the system to integrate over one physical second and store only the final state.

- The only definition in `fvSchemes` regards the time-derivative: explicit solver `Euler` is expected here.

- In the case of `fvSolution` only the integrated species content `Yi` is required.

### `constants/`

- File `chemistryProperties` provides ODE problem parameters. The most important feature here is the use of `seulex` integrator, this being reported to provide the best treatment of stiff systems from chemical kinetics.

- In `initialConditions` we provide the values for automatic generation of `0/` directory. It is a particularity of `chemFoam` that it generates that directory by processing this dictionary. Here we define the reactor to be held at constant pressure and state that composition is provided in mole fractions.

- The case is closed by the `thermophysicalProperties`. A `chemistryReader` is provided to be able to interpret mechanism files in the required format. It is recommended to perform conversion for Chemkin II format and check files for any errors, giving preference to OpenFOAM own format here. The use of `<constant>` means the files are to be stored in the `constant/` case directory.

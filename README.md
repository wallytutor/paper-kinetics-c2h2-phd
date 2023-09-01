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

# Analysis of acetylene pyrolysis

Analysis of acetylene kinetics under conditions relevant to gas carburizing. The study is conducted with a DRG skeletal mechanism and comprise both PFR
1-D simulations and 3-D CFD cases. All cases are validated experimentally and data is made available for verification.

## About

Data explored in this paper is provided in my [PhD thesis](http://docnum.univ-lorraine.fr/public/DDOC_T_2017_0158_DAL_MAZ_SILVA.pdf), mainly in Chapter 5. The kinetics mechanisms used in this study are provided in different formats at:

- [DRG skeletal mechanism tested in this work](https://github.com/wallytutor/archive-databases/tree/main/kinetics/Dalmazsi_2017_sk41)
- [Norinaga's reference detailed mechanism](https://github.com/wallytutor/archive-databases/tree/main/kinetics/Norinaga_2009)

## Summary of calculations

- [x] Verification of mechanisms with PSR models with Cantera and chemFoam (this file)
- [ ] [Simulation of experimental conditions with a non-isothermal PFR](src/pfr/)
- [ ] [Extension to real geometry of reactor with OpenFOAM](src/foam/)

## To-do's

- [ ] Validate new release of PFR model with wall temperature / simulate.
- [ ] Migrate FOAM case preparation from Python to Julia (*majordome*).
- [ ] Run FOAM mesh convergence/simulations and extract results.
- [ ] Add Graf (2007) as a baseline comparison to paper.
- [ ] Export mechanism with pyJac and benchmark in FOAM.
- [ ] Finish paper text and publish.

## Comparison of Cantera and chemFoam

In this notebook we compare results obtained for a perfect-stirred reactor (PSR) using Cantera and chemFoam (the zero-dimensional kinetics solver of OpenFOAM). This is done with the original mechanism by Norinaga (2009) comprised of 243 species and the one obtained in my thesis through extensive DRG skeletal combinations.

```python
%load_ext autoreload
%autoreload 2
```

```python
from pathlib import Path
import cantera as ct
import pandas as pd
from papertools import report_dimensionless
from papertools import compare_cantera_chemfoam
from papertools import fit_wall_temperature
```

Mechanisms are stored in another [repository](https://github.com/wallytutor/archive-databases/tree/main) and have been cloned relative to the root of the current one. Below we assembly the paths to retrieve Cantera files.

```python
databases = Path("../archive-databases/kinetics/")

norinaga2009 = "Norinaga_2009/CT-hydrocarbon-norinaga-2009-mech.yaml"
dalmazsi2017 = "Dalmazsi_2017_sk41/CT-hydrocarbon-dalmazsi-2017-mech.yaml"

norinaga2009 = databases / norinaga2009
dalmazsi2017 = databases / dalmazsi2017
```

Next we compute the reference initial conditions in required units. Since acetylene is stored in liquid acetone, pollution of the gas is expected are discussed by Noringa (2009). Chemical composition is provided in mole fractions, a more convenient quantity when dealing with low pressure gas phases.

```
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

# Velocity [m/s]
U = 1.0

# Length [m]
L = 1.0

report_dimensionless(dalmazsi2017, T, P, X, L, U)
```

## DRG mechanism

```
Cantera:
 T = 1298.8, p = 5000, C2H2 = 0.242606, CH4 = 0.001410

OpenFOAM:

 T = 1299.9, p = 5000, C2H2 = 0.24196, CH4 = 0.00141113
```

```python
compare_cantera_chemfoam(dalmazsi2017, "psr-dalmazsi-2017", T, P, X)
```

## Detailed mechanism

```
Cantera:
 T = 1299.7, p = 5000, C2H2 = 0.240127, CH4 = 0.001216

OpenFOAM:

 T = 1301.02, p = 5000, C2H2 = 0.239335, CH4 = 0.00121622
```

```python
compare_cantera_chemfoam(norinaga2009, "psr-norinaga-2009", T, P, X)
```

<!-- #region -->
## Afterword: `chemFoam` tutorial

Dictionaries for `chemFoam` are quite simple, we only need the following folders/files:


### `system/`

- `controlDict`: there we set the system to integrate over one physical second and store only the final state.

- `fvSchemes`: the only definition in regards the time-derivative: explicit solver `Euler` is expected here.

- `fvSolution`: only the integrated species content `Yi` is required.

### `constants/`

- `chemistryProperties`: provides ODE problem parameters. The most important feature here is the use of `seulex` integrator, this being reported to provide the best treatment of stiff systems from chemical kinetics.

- `initialConditions`: we provide the values for automatic generation of `0/` directory. It is a particularity of `chemFoam` that it generates that directory by processing this dictionary. Here we define the reactor to be held at constant pressure and state that composition is provided in mole fractions.

- `thermophysicalProperties`: a `chemistryReader` is provided to be able to interpret mechanism files in the required format. It is recommended to perform conversion for Chemkin II format and check files for any errors, giving preference to OpenFOAM own format here. The use of `<constant>` means the files are to be stored in the `constant/` case directory.
<!-- #endregion -->

## Reactor geometry and temperature profile

A sketch of the chemical reactor is provided below. Gas inlet is made by the left side in the diameter of 28 mm and flows at about room temperature until reaching the heated chamber at 20 cm. Pressure is measured at outlet and this will be important later for proper setup of boundary conditions.

<center><img src="figures/reactor.png"/></center>

To fit a function of wall temperature profile the following table is used. Notice here that measurements do not cover the full 80 cm of the reactor, but are in fact centered in the hot zone across a length of 52 cm. The first 3 rows we manually added (not actual measurements, so heated chamber starts actually at 12 cm) to provide a physically suitable shape for fitting the curve. Same was done on last row because measurement on chamber exit was highly unreliable because of thermocouple placement and contact with the wall.

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right">
      <th></th>
      <th>x</th>
      <th>773</th>
      <th>873</th>
      <th>973</th>
      <th>1023</th>
      <th>1073</th>
      <th>1123</th>
      <th>1173</th>
      <th>1223</th>
      <th>1273</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.00</td>
      <td>298</td>
      <td>298.0</td>
      <td>298</td>
      <td>298</td>
      <td>298.0</td>
      <td>298</td>
      <td>298.0</td>
      <td>298.0</td>
      <td>298.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.05</td>
      <td>299</td>
      <td>299.0</td>
      <td>299</td>
      <td>299</td>
      <td>299.0</td>
      <td>299</td>
      <td>299.0</td>
      <td>299.0</td>
      <td>299.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.10</td>
      <td>300</td>
      <td>300.0</td>
      <td>300</td>
      <td>300</td>
      <td>300.0</td>
      <td>300</td>
      <td>300.0</td>
      <td>300.0</td>
      <td>300.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.12</td>
      <td>400</td>
      <td>503.0</td>
      <td>653</td>
      <td>689</td>
      <td>726.0</td>
      <td>755</td>
      <td>783.0</td>
      <td>793.0</td>
      <td>803.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.15</td>
      <td>650</td>
      <td>757.0</td>
      <td>873</td>
      <td>896</td>
      <td>919.0</td>
      <td>959</td>
      <td>1000.0</td>
      <td>1048.0</td>
      <td>1095.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.20</td>
      <td>750</td>
      <td>834.0</td>
      <td>918</td>
      <td>965</td>
      <td>1013.0</td>
      <td>1057</td>
      <td>1101.0</td>
      <td>1151.0</td>
      <td>1200.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.25</td>
      <td>762</td>
      <td>850.0</td>
      <td>949</td>
      <td>1001</td>
      <td>1052.0</td>
      <td>1098</td>
      <td>1143.0</td>
      <td>1189.0</td>
      <td>1235.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.30</td>
      <td>763</td>
      <td>869.0</td>
      <td>971</td>
      <td>1018</td>
      <td>1064.0</td>
      <td>1110</td>
      <td>1156.0</td>
      <td>1205.0</td>
      <td>1253.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.35</td>
      <td>763</td>
      <td>859.0</td>
      <td>954</td>
      <td>1001</td>
      <td>1047.5</td>
      <td>1095</td>
      <td>1142.5</td>
      <td>1188.5</td>
      <td>1233.5</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.40</td>
      <td>763</td>
      <td>849.0</td>
      <td>937</td>
      <td>984</td>
      <td>1031.0</td>
      <td>1080</td>
      <td>1129.0</td>
      <td>1172.0</td>
      <td>1214.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.45</td>
      <td>582</td>
      <td>697.5</td>
      <td>780</td>
      <td>837</td>
      <td>894.0</td>
      <td>931</td>
      <td>967.5</td>
      <td>990.5</td>
      <td>1012.5</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0.50</td>
      <td>440</td>
      <td>546.0</td>
      <td>623</td>
      <td>690</td>
      <td>757.0</td>
      <td>782</td>
      <td>806.0</td>
      <td>809.0</td>
      <td>811.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>0.52</td>
      <td>400</td>
      <td>400.0</td>
      <td>400</td>
      <td>400</td>
      <td>400.0</td>
      <td>400</td>
      <td>400.0</td>
      <td>400.0</td>
      <td>400.0</td>
    </tr>
  </tbody>
</table>

```python
Twall = pd.read_csv("data/wall-temperature.csv")
```

As we observe on row 7, temperature in the middle of the reactor heated zone does not reach the set-point value. Below we verify that actually abot 99% of the value is actually reached and this is an important factor for a proper kinetics simulation given the exponential role of activation energies.

```python
T_pv = Twall.iloc[7, 1:].to_numpy()
T_sp = Twall.columns[1:].astype(float).to_numpy()

scale = (T_pv / T_sp)
scale
```

Given the increasing-plateau-decreasing shape of the profile, a composition of sigmoid functions is proposed as a model for the data. The function is evaluated in terms of temperature and has a physical parameter `T_sp` for set-point temperature. Other parameters are fitted to match the profile. Parameters `a1`/`a2` provide the inflexion points and `m1`/`m2` the slopes of uphill/downhill profiles. We make use of `scipy.optimize.curve_fit` to find the unknown parameters and visualize the results.

![Wall temperature](figures/wall_temperature_fit.png)

```python
params = fit_wall_temperature(Twall, scale)
```

## Setup of CFD cases

```python
conditions = pd.DataFrame([
    {"N":  1, "P":  5000, "Q": 222, "T":  773, "X": 0.352},
    {"N":  2, "P":  5000, "Q": 222, "T":  873, "X": 0.364},
    {"N":  3, "P":  5000, "Q": 222, "T":  973, "X": 0.364},
    {"N":  4, "P":  5000, "Q": 222, "T": 1073, "X": 0.346},
    {"N":  5, "P":  5000, "Q": 222, "T": 1123, "X": 0.312},
    {"N":  6, "P":  5000, "Q": 222, "T": 1173, "X": 0.307},
    {"N":  7, "P":  5000, "Q": 222, "T": 1273, "X": 0.298},
    {"N":  8, "P":  3000, "Q": 222, "T": 1173, "X": 0.323},
    {"N":  9, "P":  3000, "Q": 222, "T": 1223, "X": 0.314},
    {"N": 10, "P": 10000, "Q": 222, "T": 1173, "X": 0.249},
    {"N": 11, "P": 10000, "Q": 222, "T": 1223, "X": 0.226},
    {"N": 12, "P": 10000, "Q": 222, "T": 1273, "X": 0.201},
    {"N": 13, "P": 10000, "Q": 378, "T": 1023, "X": 0.343},
    {"N": 14, "P": 10000, "Q": 378, "T": 1123, "X": 0.298},
]).set_index("N")
```

## Summary of CFD results

<table>
    <tr>
        <td style="text-align: center;" width="50px">Case</td>
        <td style="text-align: center;" width="150px">Measured</td>
        <td style="text-align: center;" width="150px">PFR (Norinaga, 2009)</td>
        <td style="text-align: center;" width="150px">CFD (Skeletal model)</td> 
    </tr>
    <tr>
        <td style="text-align: center;">4</td>
        <td style="text-align: center;">0.346</td>
        <td style="text-align: center;">0.340</td>
        <td style="text-align: center;">0.336</td> 
    </tr>
    <tr>
        <td style="text-align: center;">5</td>
        <td style="text-align: center;">0.312</td>
        <td style="text-align: center;">0.321</td>
        <td style="text-align: center;">0.319</td> 
    </tr>
    <tr>
        <td style="text-align: center;">6</td>
        <td style="text-align: center;">0.307</td>
        <td style="text-align: center;">0.302</td>
        <td style="text-align: center;">0.299</td> 
    </tr>
    <tr>
        <td style="text-align: center;">7</td>
        <td style="text-align: center;">0.288</td>
        <td style="text-align: center;">0.287</td>
        <td style="text-align: center;">0.286</td> 
    </tr>
    <tr>
        <td style="text-align: center;">8</td>
        <td style="text-align: center;">0.323</td>
        <td style="text-align: center;">0.327</td>
        <td style="text-align: center;">0.323</td> 
    </tr>
    <tr>
        <td style="text-align: center;">9</td>
        <td style="text-align: center;">0.314</td>
        <td style="text-align: center;">0.320</td>
        <td style="text-align: center;">0.314</td> 
    </tr>
    <tr>
        <td style="text-align: center;">10</td>
        <td style="text-align: center;">0.249</td>
        <td style="text-align: center;">0.230</td>
        <td style="text-align: center;">0.234</td> 
    </tr>
    <tr>
        <td style="text-align: center;">11</td>
        <td style="text-align: center;">0.226</td>
        <td style="text-align: center;">0.219</td>
        <td style="text-align: center;">0.222</td> 
    </tr>
    <tr>
        <td style="text-align: center;">12</td>
        <td style="text-align: center;">0.201</td>
        <td style="text-align: center;">0.208</td>
        <td style="text-align: center;">0.216</td> 
    </tr>
    <tr>
        <td style="text-align: center;">13</td>
        <td style="text-align: center;">0.343</td>
        <td style="text-align: center;">0.342</td>
        <td style="text-align: center;">0.338</td> 
    </tr>
    <tr>
        <td style="text-align: center;">14</td>
        <td style="text-align: center;">0.298</td>
        <td style="text-align: center;">0.292</td>
        <td style="text-align: center;">0.292</td> 
    </tr>
</table>

<center>
    <!-- <h3>Case No. 4</h3>
    <img src="figures/004.png" />
    <h3>Case No. 5</h3>
    <img src="figures/005.png" />
    <h3>Case No. 6</h3>
    <img src="figures/006.png" />
    <h3>Case No. 7</h3>
    <img src="figures/007.png" />
    <h3>Case No. 8</h3>
    <img src="figures/008.png" /> -->
    <h3>Case No. 9</h3>
    <img src="figures/009.png" />
    <!-- <h3>Case No. 10</h3>
    <img src="figures/010.png" />
    <h3>Case No. 11</h3>
    <img src="figures/011.png" />
    <h3>Case No. 12</h3>
    <img src="figures/012.png" />
    <h3>Case No. 13</h3>
    <img src="figures/013.png" />
    <h3>Case No. 14</h3>
    <img src="figures/014.png" /> -->
</center>

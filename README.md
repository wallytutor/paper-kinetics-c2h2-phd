---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.5
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

- [x] [Verification of mechanisms with PSR models with Cantera and chemFoam](simulations/chemFoam)
- [ ] [Simulation of experimental conditions with a non-isothermal PFR](src/pfr/)
- [ ] [Extension to real geometry of reactor with OpenFOAM](src/foam/)

## To-do's

- [ ] Validate new release of PFR model with wall temperature / simulate.
- [ ] Migrate FOAM case preparation from Python to Julia (*majordome*).
- [ ] Run FOAM mesh convergence/simulations and extract results.
- [ ] Add Graf (2007) as a baseline comparison to paper.
- [ ] Export mechanism with pyJac and benchmark in FOAM.
- [ ] Finish paper text and publish.

```python
%load_ext autoreload
%autoreload 2
```

```python
from pathlib import Path
import cantera as ct
import numpy as np
import pandas as pd
import pyvista as pv
from papertools import report_dimensionless
from papertools import compare_cantera_chemfoam
from papertools import fit_wall_temperature
from papertools import generate_wall_bc
from papertools import plot_mesh
```

```python
pv.set_jupyter_backend("static")
# pv.start_xvfb()
```

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


The following table compiles the parameters fitting the selected function.

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right">
      <th></th>
      <th>T</th>
      <th>scale</th>
      <th>a1</th>
      <th>a2</th>
      <th>m1</th>
      <th>m2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>773.0</td>
      <td>0.987063</td>
      <td>0.143839</td>
      <td>0.465366</td>
      <td>8.498838</td>
      <td>15.589542</td>
    </tr>
    <tr>
      <th>1</th>
      <td>873.0</td>
      <td>0.995418</td>
      <td>0.138845</td>
      <td>0.485018</td>
      <td>7.161445</td>
      <td>12.858167</td>
    </tr>
    <tr>
      <th>2</th>
      <td>973.0</td>
      <td>0.997945</td>
      <td>0.130311</td>
      <td>0.490096</td>
      <td>7.219046</td>
      <td>12.825122</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1023.0</td>
      <td>0.995112</td>
      <td>0.131512</td>
      <td>0.495795</td>
      <td>6.623234</td>
      <td>14.073047</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1073.0</td>
      <td>0.991612</td>
      <td>0.132188</td>
      <td>0.500856</td>
      <td>6.254105</td>
      <td>16.953023</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1123.0</td>
      <td>0.988424</td>
      <td>0.131778</td>
      <td>0.501189</td>
      <td>6.313607</td>
      <td>17.562174</td>
    </tr>
    <tr>
      <th>6</th>
      <td>1173.0</td>
      <td>0.985507</td>
      <td>0.131360</td>
      <td>0.501379</td>
      <td>6.396870</td>
      <td>18.019476</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1223.0</td>
      <td>0.985282</td>
      <td>0.131623</td>
      <td>0.498994</td>
      <td>6.550948</td>
      <td>15.856001</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1273.0</td>
      <td>0.984289</td>
      <td>0.131839</td>
      <td>0.496996</td>
      <td>6.695226</td>
      <td>14.754026</td>
    </tr>
  </tbody>
</table>

```python
params = fit_wall_temperature(Twall, scale)
```

We translate the fitted function in C++ and create a `codedFixedValue` boundary condition for enforcing the profile.

Below we illustrate the generation of a coded boundary condition from one of the cases.

```python
generate_wall_bc(params.iloc[4].to_dict())
```

## Setup of CFD cases

Cases below 1073 K may be skipped because there is no decomposition of acetylene for the given residence times.

```python
cpos = ((0.3, 0.005, 1.0),
        (0.3, 0.005, 0.0),
        (0.0, 0.000, 0.0))

mtm = np.diag([1, 20, 1, 1])

plot_mesh("cfd-dalmazsi-2017-base/wedge.msh", cpos=cpos, mtm=mtm)
```

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

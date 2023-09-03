# -*-  coding: utf-8 -*-
from importlib.machinery import SourceFileLoader
from pathlib import Path
import numpy as np
import yaml

# Root of paper-kinetics-c2h2-phd repository.
project_root = Path(__file__).parent.resolve().parents[1]

# Assuming archive-databases has been cloned at the same level.
databases = project_root / "../archive-databases/kinetics/"

# Names and then path to mechanism files.
norinaga2009 = "CT-hydrocarbon-norinaga-2009-mech.yaml"
dalmazsi2017 = "CT-hydrocarbon-dalmazsi-2017-mech.yaml"
norinaga2009 = databases / "Norinaga_2009" / norinaga2009
dalmazsi2017 = databases / "Dalmazsi_2017_sk41" / dalmazsi2017

# Data file with conditions used in project, get reference case.
with open(project_root / "data/conditions.yaml") as fp:
    data = yaml.safe_load(fp)["reference_case"]

# Make sure composition is not corrupted.
assert np.isclose(1.0, sum(data["X"].values()))

# Load helper module with all tools from project.
module_path = str(project_root / "papertools.py")
source = SourceFileLoader("papertools", module_path)
papertools = source.load_module()

# Unpack arguments from data.
args = data["T"], data["P"], data["X"], data["L"], data["U"]
T, P, X, L, U = args

# Generate dimensionless numbers and comparison reports.
papertools.report_dimensionless(dalmazsi2017, T, P, X, L, U)
papertools.compare_cantera_chemfoam(dalmazsi2017, "dalmazsi-2017", T, P, X)
papertools.compare_cantera_chemfoam(norinaga2009, "norinaga-2009", T, P, X)

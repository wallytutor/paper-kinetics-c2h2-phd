#!/usr/bin/python3
""" Basic reaction path diagram for acetylene pyrolysis.

Author: Walter Dal'Maz Silva
Date: January 25th 2018
"""

import os
import cantera as ct

T = 1173.16
P = 5000.00
X = {"N2": 0.64, "C2H2": 0.3528, "CH3COCH3": 0.0065, "CH4": 0.0007}
gas = ct.Solution("data/hydrocarbon-dalmazsi-2017-trans-gas.cti")
gas.TPX = T, P, X

for element in ["H", "C"]:
    dot_file = "ReactionPathDiagram_{}.dot".format(element)
    img_file = "ReactionPathDiagram_{}.png".format(element)
    dot_file = os.path.join("results", dot_file)
    img_file = os.path.join("results", img_file)

    diagram = ct.ReactionPathDiagram(gas, element)
    diagram.font = "CMU Serif"
    diagram.show_details = False
    diagram.scale = -1
    diagram.threshold = 0.05
    diagram.dot_options="node[fontsize=20,shape=\"box\"]"
    diagram.write_dot(dot_file)

    dot_cmd = "dot {0} -Tpng -o{1} -Gdpi=300"
    os.system(dot_cmd.format(dot_file, img_file))


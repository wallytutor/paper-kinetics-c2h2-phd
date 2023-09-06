#!/usr/bin/python3
""" Basic reaction path diagram for acetylene pyrolysis.

Reference:
    https://www.tilmanbremer.de/2017/06/
    tutorial-generating-reaction-path-diagrams-with-cantera-and-python/

Author: Walter Dal'Maz Silva
Date: January 25th 2018
"""

import os
import cantera as ct


def dict2str(d):
    return "".join(["-{}={} ".format(k,v) for k,v in d.items()])


T = 1173.16
P = 5000.00
X = {"N2": 0.64, "C2H2": 0.3528, "CH3COCH3": 0.0065, "CH4": 0.0007}
gas = ct.Solution("data/hydrocarbon-dalmazsi-2017-trans-gas.cti")
gas.TPX = T, P, X

rea = ct.IdealGasReactor(gas)
sim = ct.ReactorNet([rea])
sim.advance(1.0)

for element in ["H", "C"]:
    dot_file = "ReactionPathDiagram_{}.dot".format(element)
    mod_file = "ReactionPathDiagram_{}.mod".format(element)
    img_file = "ReactionPathDiagram_{}.png".format(element)
    dot_file = os.path.join("results", dot_file)
    img_file = os.path.join("results", img_file)

    diagram = ct.ReactionPathDiagram(gas, element)
    diagram.font = "CMU Serif"
    diagram.show_details = False
    diagram.scale = -1
    diagram.threshold = 0.1
    diagram.dot_options="node[fontsize=20,shape=\"box\"]"
    diagram.write_dot(dot_file)

    with open(mod_file, "wt") as outfile:
        with open(dot_file, "rt") as infile:
            for row in infile:
                if row.startswith(" label"):
                    row = ""
                row = row.replace(", 0.9\"", ", 0.0\"")
                row = row.replace("style=\"setlinewidth(", "penwidth=")
                row = row.replace(")\", arrowsize", ", arrowsize")

                if row.find("color=\"0.7, ") != -1:
                    start = row.find("color=\"0.7, ")
                    end = row.find(", 0.0\"")

                    saturation = float(row[start + 12:end])
                    if saturation > 1:
                        saturationnew = 0
                    else:
                        saturationnew=round(abs(saturation-1), 2)

                    row = row.replace(", 0.0\"", "\"")
                    row = row.replace("0.7, ", "0.7, 0.0, ")

                    try:
                        row = row.replace(str(saturation), str(saturationnew))
                    except (NameError) as err:
                        print(err)
                        pass

                outfile.write(row)

    d = {#"Earrowhead": "onormal",
         "Esamehead": "true",
         #"Estyle": "dashed",
         "Nstyle": "filled",
         "Nfillcolor": "white",
         "Nshape": "box",
         "Gdpi": 300,
         "Gbgcolor": "#FBFBEF",
         "Grotate": 90,
         "Gnodesep": 0.1}

    dot_cmd = "dot {0} -Tpng -o{1} " + dict2str(d)
    os.system(dot_cmd.format(mod_file, img_file))


#!/usr/bin/env bash

. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

/usr/bin/gmsh wedge.geo -3 -format msh2 > log.gmsh

runApplication gmshToFoam wedge.msh

runApplication checkMesh

# pip install PyFoam
# pyFoamChangeBoundaryType.py . front wedge
# pyFoamChangeBoundaryType.py . back  wedge
#!/usr/bin/env bash

. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

gmsh wedge.geo -3 -format msh2 > log.gmsh

runApplication gmshToFoam wedge.msh

runApplication checkMesh

# pyFoamChangeBoundaryType.py . front wedge
# pyFoamChangeBoundaryType.py . back  wedge
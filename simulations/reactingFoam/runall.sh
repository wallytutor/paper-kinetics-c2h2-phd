#!/usr/bin/env bash

# Before running this script, activate OpenFOAM if not already done!
# openfoam2212

# Get current script directory.
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Source OpenFOAM helpers.
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

function reactingFoamCaseRun()
{
    casename=${1}
    casedir=${HERE}/${casename}

    # Copy mesh to case directory.
    cp -avr ${HERE}/case/constant/polyMesh  ${casedir}/constant/

    # Copy mechanism and thermodynamics data to case.
    # Here we are only using dalmazsi-2017 mechanism.
    cp ${HERE}/../../data/dalmazsi-2017/* ${casedir}/constant/

    # Enter case and run application.
    # This is for sequential runs only.
    cd ${casedir} && runApplication `getApplication` &

    # cd ${casedir}
    # runApplication decomposePar
    # runParallel `getApplication` &
}

# List cases to run here.
reactingFoamCaseRun 004-new

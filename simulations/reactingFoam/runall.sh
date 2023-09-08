#!/usr/bin/env bash

# Get current script directory.
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Source OpenFOAM helpers.
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

function reactingFoamCaseRun()
{
    casename=${1}
    casedir=${HERE}/${casename}

    # Copy common files to new case.
    cp -avr ${HERE}/case/constant/  ${casedir}/constant/
    cp -avr ${HERE}/case/system/  ${casedir}/system/

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
# reactingFoamCaseRun 004
# reactingFoamCaseRun 005
# reactingFoamCaseRun 006
# reactingFoamCaseRun 007
# reactingFoamCaseRun 008-new
# reactingFoamCaseRun 009-new
# reactingFoamCaseRun 010-new
reactingFoamCaseRun 011-new
# reactingFoamCaseRun 012-new
# reactingFoamCaseRun 013-new
# reactingFoamCaseRun 014-new

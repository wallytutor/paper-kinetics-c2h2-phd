#!/usr/bin/env bash

# Before running this script, activate OpenFOAM if not already done!
# openfoam2212

# Get current script directory.
HERE=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Source OpenFOAM helpers.
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

# Helper function to run a case.
function chemFoamCaseRun()
{
    casename=${1}
    casedir=${HERE}/${casename}

    # Clean start.
    [ -d ${casedir} ] && rm -rf ${casedir}

    # Create case directory.
    mkdir ${casedir}

    # Copy standard case setup to case.
    cp -avr ${HERE}/case/* ${casedir}/

    # Copy mechanism and thermodynamics to case.
    cp ${HERE}/../../data/${casename}/* ${casedir}/constant/

    # Enter case and run application.
    cd ${casedir} && runApplication `getApplication`
}

chemFoamCaseRun norinaga-2009 && cd ${HERE}
chemFoamCaseRun dalmazsi-2017 && cd ${HERE}

#!/bin/bash

# . ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

# function runpsrcase()
# {
#     rm -rf chemFoam.out log.chemFoam '0.000000/' '1.000000/'
#     runApplication `getApplication`
# }

# function runcfdcase()
# {
#     casepath=${1}

#     cp -avr cfd-dalmazsi-2017-base/constant/polyMesh  ${casepath}/constant/
#     cp cfd-dalmazsi-2017-base/constant/reactions ${casepath}/constant/
#     cp cfd-dalmazsi-2017-base/constant/thermo    ${casepath}/constant/

#     cd ${casepath}
#     runApplication decomposePar
#     runParallel $(getApplication) &

# }

# # cd psr-dalmazsi-2017 && runpsrcase && cd ..
# # cd psr-norinaga-2009 && runpsrcase && cd ..

# runcfdcase 'cfd-dalmazsi-2017-004'
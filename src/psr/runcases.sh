#!/bin/bash

. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions

function runcase()
{
    rm -rf chemFoam.out log.chemFoam '0.000000/' '1.000000/'
    runApplication `getApplication`
}

cd dalmazsi-2017 && runcase && cd ..
cd norinaga-2009 && runcase && cd ..

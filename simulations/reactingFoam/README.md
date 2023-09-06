# Wedge reactor simulation

## About cases

Directory [reference](reference/) keeps old versions of the cases with a worse fitting of wall temperature. These are kept for reference only and are not used in the paper. All cases that are actually cited are found under this same parent directory.

## Running the cases

1. Activate the right version of OpenFOAM with `openfoam2212`.
1. Enter [case](case/) and generate mesh with `generatemesh.sh`.
1. Edit [boundaries](case/constant/polyMesh/boundary) so that both `front` and `back` are of type `wedge`.
1. Check and then run script [runall.sh](runall.sh) for running cases sequentially.

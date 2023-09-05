# Wedge reactor simulation

## Running the cases

1. Enter [case](case/) and generate mesh with `generatemesh.sh`.
1. Edit [boundaries](case/constant/polyMesh/boundary) so that both `front` and `back` are of type `wedge`.
1. Check and then run script [runall.sh](runall.sh) for running cases.

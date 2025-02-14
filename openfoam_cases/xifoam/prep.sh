#!/bin/sh
# cd ${0%/*} || exit 1    # Run from this directory

# # Source tutorial run functions
# . $WM_PROJECT_DIR/bin/tools/RunFunctions
# cp -r 0.orig 0

# application=dfLowMachFoam

# runApplication blockMesh
# # runApplication setFields
# runApplication decomposePar
# runApplication mpirun -np 4 --allow-run-as-root $application -parallel
#!/bin/sh
cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions


cp -r 0.orig/ 0/
runApplication blockMesh
runApplication topoSet
runApplication etf_field_init_xi
# runApplication setFields
# runApplication etf_field_init
runApplication decomposePar
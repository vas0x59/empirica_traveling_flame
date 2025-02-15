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

H=$1
W=$2
T=$3

HC=$(echo "$H / 0.0007" | bc)
WC=$(echo "$W / 0.0007" | bc)

cp -r 0.orig/ 0/

foamDictionary -entry H -set $H system/geomC
foamDictionary -entry W -set $W system/geomC
foamDictionary -entry HC -set $HC system/geomC
foamDictionary -entry WC -set $WC system/geomC
foamDictionary -entry T -set $T system/geomC

sttmp=$(echo "$H + 0.005" | bc -l)

runApplication blockMesh
runApplication topoSet
runApplication etf_field_init_xi $sttmp

# runApplication setFields
# runApplication etf_field_init
runApplication decomposePar
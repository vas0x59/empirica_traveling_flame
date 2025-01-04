# #!/bin/sh
. $WM_PROJECT_DIR/bin/tools/RunFunctions

application=dfLowMachFoam

runApplication mpirun -np 10 --allow-run-as-root $application -parallel

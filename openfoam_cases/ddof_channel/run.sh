# #!/bin/sh
. $WM_PROJECT_DIR/bin/tools/RunFunctions

application=reactingFoam

runApplication mpirun -np 12 --allow-run-as-root $application -parallel


cd ${0%/*} || exit 1    # Run from this directory

# Source tutorial run functions
. $WM_PROJECT_DIR/bin/tools/RunFunctions


cp -r 0.orig/ 0/

python generate_mesh.py -nopopup
gmshToFoam mesh.msh2
python3 ../../utils/modify_mesh_boundary.py ./constant/polyMesh/boundary "border_liquid border border_0"



runApplication etf_field_init
runApplication setFields
# runApplication etf_field_init
runApplication decomposePar
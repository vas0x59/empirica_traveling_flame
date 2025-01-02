#!/bin/sh
./clean.sh

cp -r 0.orig 0

python generate_mesh.py -nopopup

gmshToFoam mesh.msh

python3 ../../utils/modify_mesh_boundary.py ./constant/polyMesh/boundary "liquid start end"

# setFields
setExprFields

setFields

decomposePar
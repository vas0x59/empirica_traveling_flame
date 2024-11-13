#!/bin/sh
# cd "${0%/*}" || exit                                # Run from this directory
. ${WM_PROJECT_DIR:?}/bin/tools/CleanFunctions      # Tutorial clean functions
#------------------------------------------------------------------------------

cleanCase0

cp -r 0.orig 0

blockMesh

setFields

decomposePar

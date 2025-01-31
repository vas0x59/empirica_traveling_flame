#!/bin/sh
./clean.sh

chemkinToFoam constant/mechs/deepflame_ethanol_gri_reduced/ethanol66.ck

cp -r 0.orig 0

blockMesh

setFields

decomposePar

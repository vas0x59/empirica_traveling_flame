#!/bin/sh
./clean.sh

cp -r 0.orig 0

python generate_mesh.py -nopopup

gmshToFoam mesh.msh


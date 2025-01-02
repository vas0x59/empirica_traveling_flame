#!/bin/sh
./clean.sh

cp -r 0.orig 0

blockMesh

setFields

decomposePar

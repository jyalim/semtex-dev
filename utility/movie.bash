#!/usr/bin/env bash
 
jobs=8
sesh=tcf

for j in {0..2}; do 
  for k in {0..9}; do 
    jid=z.${sesh}.3${j}.${k}; 
    kid=zcyl.${sesh}.3${j}.${k}; 
    mpirun -n $jobs dns_mp $sesh
    cp ${sesh}.fld ${sesh}.rst
    addfield -l -s ${sesh} ${sesh}.fld > ${jid}.fld 
    sem2vtk -m ${sesh}.msh -o ${jid}.vtk ${jid}.fld 
    sem2vtk -c -m ${sesh}.msh -o ${kid}.vtk ${jid}.fld 
    rm tmp.*
  done
done

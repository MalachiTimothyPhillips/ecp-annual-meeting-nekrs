#!/bin/bash
baseDir=/gpfs/alpine/scratch/malachi/csc262/siam-pp-22/kershaw/weak-scaling-study

for eps in 0.05; do
  mkdir eps-$eps
  cd eps-$eps
#for preconditioner in semfem asm ras cheby-asm cheby-jac cheby-ras; do
  for preconditioner in cheby-asm cheby-ras semfem cheby-jac "cheby-asm-1" "cheby-asm-3" "cheby-ras-1" "cheby-ras-3" "cheby-jac-boomeramg-1" "cheby-asm-pmg-7531" "cheby-ras-pmg-7531"; do
    for nodes in 1 2 4 8 16 32 64; do
      mkdir $preconditioner-$nodes
      cd $preconditioner-$nodes
      cp $baseDir/eps-$eps/$preconditioner-$nodes/nekRS* .
      cd ../
    done
  done
  cd ../
done

#!/bin/bash
baseDir=/gpfs/alpine/scratch/malachi/csc262/siam-pp-22/kershaw/fixed-size

for eps in 0.05; do
  mkdir eps-$eps
  cd eps-$eps
  for preconditioner in semfem asm ras cheby-asm cheby-jac cheby-ras cheby-asm-1 cheby-asm-3 cheby-ras-1 cheby-ras-3; do
    for order in 2 3 4 5 6 7 8 9 10; do
      mkdir $preconditioner-p-$order
      cd $preconditioner-p-$order
      cp $baseDir/eps-$eps/$preconditioner-p-$order/nekRS* .
      cd ../
    done
  done
  cd ../
done

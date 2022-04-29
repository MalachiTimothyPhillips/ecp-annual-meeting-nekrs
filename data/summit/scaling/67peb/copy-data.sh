#!/bin/bash
baseDir=/gpfs/alpine/scratch/malachi/csc262/siam-pp-22/67peb

# setup dir
for preconditioner in cheby-asm cheby-ras semfem cheby-jac "cheby-asm-1" "cheby-asm-3" "cheby-ras-1" "cheby-ras-3" "cheby-jac-boomeramg-1" "cheby-asm-pmg-7531" "cheby-ras-pmg-7531" auto combo combo-v2 combo-v3; do
  for nnodes in 1 2 3 4; do
    for precision in "fp32"; do
      cd $precision
      mkdir $preconditioner-$nnodes
      cd ../
    done
  done
done

for preconditioner in cheby-asm cheby-ras semfem cheby-jac "cheby-asm-1" "cheby-asm-3" "cheby-ras-1" "cheby-ras-3" "cheby-jac-boomeramg-1" "cheby-asm-pmg-7531" "cheby-ras-pmg-7531" auto combo combo-v2 combo-v3; do
  for nnodes in 1 2 3 4; do
    cp $baseDir/$preconditioner-fp32-$nnodes/nekRS_* fp32/$preconditioner-$nnodes/
  done
done

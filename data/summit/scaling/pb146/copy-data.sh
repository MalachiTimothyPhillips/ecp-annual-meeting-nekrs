#!/bin/bash
baseDir=/gpfs/alpine/scratch/malachi/csc262/siam-pp-22/pb146/runs

# setup dir
for preconditioner in cheby-asm cheby-ras semfem cheby-jac "cheby-asm-1" "cheby-asm-3" "cheby-ras-1" "cheby-ras-3" "cheby-jac-boomeramg-1" "cheby-asm-pmg-7531" "cheby-ras-pmg-7531" auto combo combo-v2 combo-v3; do
#for nnodes in "0.5" "0.75" 1 2 3; do
  for nnodes in 0.5; do
##for precision in "fp64" "fp32" "fp16"; do
    for precision in "fp32"; do
      cd $precision
      mkdir $preconditioner-$nnodes
      cd ../
    done
  done
done

#for preconditioner in cheby-asm cheby-ras semfem cheby-jac "cheby-asm-1" "cheby-asm-3" "cheby-ras-1" "cheby-ras-3" "cheby-jac-boomeramg-1" "cheby-asm-pmg-7531" "cheby-ras-pmg-7531" auto; do
for preconditioner in combo-v2 combo-v3; do
  for nnodes in 0.5; do
#cp $baseDir/$preconditioner-fp16-$nnodes/nekRS_* fp16/$preconditioner-$nnodes/
    cp $baseDir/$preconditioner-fp32-$nnodes/nekRS_* fp32/$preconditioner-$nnodes/
#cp $baseDir/$preconditioner-fp64-$nnodes/nekRS_* fp64/$preconditioner-$nnodes/
  done
done

## copy auto pressure results
#for preconditioner in "auto"; do
#  for nnodes in 1 2 4 8 16; do
#    for precision in "fp32"; do
#      cd $precision
#      mkdir $preconditioner-$nnodes
#      cd ../
#    done
#  done
#done
#
#preconditioner=auto
#for nnodes in 1 2 4 8 16; do
#  cp $baseDir/cheby-asm-fp32-$nnodes/auto_preco_nekRS* fp32/$preconditioner-$nnodes/
#done

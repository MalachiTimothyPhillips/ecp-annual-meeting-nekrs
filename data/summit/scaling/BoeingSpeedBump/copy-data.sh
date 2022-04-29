#!/bin/bash
baseDir=/gpfs/alpine/scratch/malachi/csc262/debugging/ramesh/for_malachi_07.07.2021

# setup dir
for preconditioner in "asm" "ras" "cheby-asm" "cheby-ras" "semfem" "cheby-jac" "cheby-jac-boomeramg-1" "cheby-asm-1" "cheby-ras-1" "cheby-asm-3" "cheby-ras-3" "cheby-asm-pmg-9751" "cheby-ras-pmg-9751" "cheby-asm" "cheby-ras" "semfem" "cheby-jac" auto combo combo-v2 combo-v3 combo-v4; do
  for nnodes in 16 24 36 48 60 72; do
#for precision in "fp64" "fp32" "fp16"; do
    for precision in "fp32"; do
      cd $precision
      mkdir $preconditioner-$nnodes
      cd ../
    done
  done
done

#for preconditioner in "asm" "ras" "cheby-asm" "cheby-ras" "semfem" "cheby-jac" "cheby-jac-boomeramg-1" "cheby-asm-1" "cheby-ras-1" "cheby-asm-3" "cheby-ras-3" "cheby-asm-pmg-9751" "cheby-ras-pmg-9751" "cheby-asm" "cheby-ras" "semfem" "cheby-jac" auto; do
for preconditioner in combo combo-v2 combo-v3 combo-v4; do
  for nnodes in 16 24 36 48 60 72; do
#cp $baseDir/$preconditioner-fp16-$nnodes/nekRS_* fp16/$preconditioner-$nnodes/
    cp $baseDir/$preconditioner-fp32-$nnodes/nekRS_* fp32/$preconditioner-$nnodes/
#cp $baseDir/$preconditioner-fp64-$nnodes/nekRS_* fp64/$preconditioner-$nnodes/
  done
done

# copy auto pressure results
#for preconditioner in "auto"; do
#  for nnodes in 24 36 48 60 72; do
#    for precision in "fp32"; do
#      cd $precision
#      mkdir $preconditioner-$nnodes
#      cd ../
#    done
#  done
#done
#
#preconditioner=auto
#for nnodes in 24 36 48 60 72; do
#  cp $baseDir/cheby-asm-fp32-$nnodes/auto_preco_nekRS* fp32/$preconditioner-$nnodes/
#done


#!/bin/bash

#BSUB -J "trainRF"
#BSUB -We 141 
#BSUB -n 1
#BSUB -M 32
#BSUB -e logs/trainRF.error.%I.%J
#BSUB -o logs/trainRF.out.%I.%J

Rscript trainRF.R trainRF.Rout

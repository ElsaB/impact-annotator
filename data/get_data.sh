#!/bin/bash

# get the raw IMPACT mutation data
printf "\n-> Get the raw IMPACT mutation data\n"
username=$1 # your luna username
scp ${username}@luna:/ifs/work/leukgen/home/eb2/impact_mutations/all_IMPACT_mutations_180508.txt .

# get the cleaned IMPACT mutation data
printf "\n-> Get the cleaned IMPACT mutation data\n"
printf "It might take some time (around 2 minutes)...\n"
Rscript utils/get_cleaned_impact.R

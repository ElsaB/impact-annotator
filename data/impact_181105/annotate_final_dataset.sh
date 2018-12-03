#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

printf "\n${GREEN}-> Annotate the final dataset (~ 2 minutes)...${NC}\n"
Rscript -e 'data_path <- ".";source("utils/compute_final_dataset.R");annotate_final_dataset()'

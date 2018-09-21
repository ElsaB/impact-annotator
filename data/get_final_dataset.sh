#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

printf "\n${GREEN}-> Get the final IMPACT mutation data (~ 10 minutes)...${NC}\n"
Rscript utils/get_final_dataset.R

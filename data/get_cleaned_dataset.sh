#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

printf "\n${GREEN}-> Get the cleaned IMPACT mutation data (~ 2 minutes)...${NC}\n"
Rscript utils/get_cleaned_impact.R

#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color


# get the raw IMPACT mutation data
printf "\n${GREEN}-> Get the raw IMPACT mutation data...${NC}\n"
# if in cluster we just copy the file, otherwise we scp
if (echo "$HOSTNAME" | grep -q "selene") || (echo "$HOSTNAME" | grep -q "luna")
then
	cp /ifs/work/leukgen/home/eb2/impact_mutations/all_IMPACT_mutations_180508.txt .
else
	username=$1 # your luna username
	scp ${username}@luna:/ifs/work/leukgen/home/eb2/impact_mutations/all_IMPACT_mutations_180508.txt .
fi


# get the cleaned IMPACT mutation data
printf "\n${GREEN}-> Get the cleaned IMPACT mutation data...${NC}\n"
printf "It might take some time (around 2 minutes)...\n"
Rscript utils/get_cleaned_impact.R



# get the raw key data
printf "\n${GREEN}-> Get the raw key data...${NC}\n"
# if in cluster we just copy the file, otherwise we scp
if (echo "$HOSTNAME" | grep -q "selene") || (echo "$HOSTNAME" | grep -q "luna")
then
	cp /ifs/work/leukgen/home/eb2/impact_mutations/key.txt .
else
	scp ${username}@luna:/ifs/work/leukgen/home/eb2/impact_mutations/key.txt .
fi
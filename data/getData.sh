#!/bin/bash

# get the raw IMPACT mutation data

username=$1 # your luna username

scp ${username}@luna:/ifs/work/leukgen/home/eb2/impact_mutations/all_IMPACT_mutations_180508.txt .

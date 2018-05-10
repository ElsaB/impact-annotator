#!/bin/bash

# get the raw IMPACT mutation data

username=$1 # your luna username

scp ${username}@luna:/ifs/res/papaemme/users/eb2/impact-annotator/data/all_IMPACT_mutations_180508.txt .

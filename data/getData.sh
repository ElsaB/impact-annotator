#!/bin/bash

# get the raw IMPACT mutation data

username=$1 # your luna username

scp ${username}@luna:/ifs/res/papaemme/users/eb2/impact-annotator/data/data_mutations_extended_180508.txt .

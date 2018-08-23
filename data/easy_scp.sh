#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

username=$1 # your cluster username
input_path=$2
output_path=$3

echo -e "${GREEN}scp ${username}@selene.mskcc.org:/home/${username}/impact-annotator/${input_path} ${output_path}${NC}"
scp ${username}@selene.mskcc.org:/home/${username}/impact-annotator/${input_path} ${output_path}
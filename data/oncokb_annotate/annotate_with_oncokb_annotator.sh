#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color


# prepare the impact dataset for impact-annotator
printf "\n${GREEN}-> Prepare the cleaned IMPACT mutation data 'cleaned_IMPACT_mutations_180508.txt' for oncokb-annotator...${NC}\n"
Rscript prepare_for_annotation.R

# create a 2.7 python virtual env
source `which virtualenvwrapper.sh` # find the path to use virtualenvwrapper functions
printf "\n${GREEN}-> Create a python 2.7 virtual env...${NC}\n"
mkvirtualenv --python=python2.7 oncokb-annotator_env
printf "\n${GREEN}-> Install matplotlib and its dependencies...${NC}\n"
pip install matplotlib

# launch oncokb-annotator
printf "\n${GREEN}-> Launch oncokb-annotator...${NC}\n"
python oncokb-annotator/MafAnnotator.py -i 'ready_to_annotate_cleaned_IMPACT_mutations_180508.txt' -o 'oncokb_annotated_cleaned_IMPACT_mutations_180508.txt' > /dev/null

printf "\n${GREEN}-> Do some cleaning...${NC}\n"
# remove the temporary .txt output from prepare_for_annotation.R
rm 'ready_to_annotate_cleaned_IMPACT_mutations_180508.txt'
# remove the oncokb-annotator virtualenv
deactivate
rmvirtualenv oncokb-annotator_env

#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # no color


printf "\n${GREEN}-> Get the oncokb-annotator repo...${NC}\n"
git clone https://github.com/oncokb/oncokb-annotator.git


printf "\n${GREEN}-> Prepare the final IMPACT mutation data 'final_IMPACT_mutations_180508.txt' for oncokb-annotator...${NC}\n"
Rscript prepare_for_annotation.R
head ready_to_annotate_final_IMPACT_mutations_180508.txt

# create a 2.7 python virtual env with the appropriate dependencies
source `which virtualenvwrapper.sh` # find the path to use virtualenvwrapper functions
printf "\n${GREEN}-> Create a python 2.7 virtual env...${NC}\n"
mkvirtualenv --python=python2.7 oncokb-annotator_env
printf "\n${GREEN}-> Install matplotlib and its dependencies...${NC}\n"
pip install matplotlib


printf "\n${GREEN}-> Launch oncokb-annotator...${NC}\n"
python oncokb-annotator/MafAnnotator.py -i 'ready_to_annotate_final_IMPACT_mutations_180508.txt' -o 'oncokb_annotated_final_IMPACT_mutations_180508.txt' > /dev/null


printf "\n${GREEN}-> Cleaning...${NC}\n"
rm 'ready_to_annotate_final_IMPACT_mutations_180508.txt'
rm -rf oncokb-annotator
# deactivate and remove the oncokb-annotator virtualenv
deactivate
rmvirtualenv oncokb-annotator_env

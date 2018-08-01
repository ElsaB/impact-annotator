#!/bin/bash

# prepare the impact dataset for impact-annotator
printf "\n-> Prepare the cleaned IMPACT mutation data 'cleaned_IMPACT_mutations_180508.txt' for oncokb-annotator...\n"
Rscript prepare_for_annotation.R

# create a 2.7 python virtual env
source `which virtualenvwrapper.sh` # find the path to use virtualenvwrapper functions
printf "\n-> Create a python 2.7 virtual env...\n"
mkvirtualenv --python=python2.7 oncokb-annotator_env > /dev/null
printf "\n-> Install matplotlib and its dependencies...\n"
pip install matplotlib > /dev/null

# launch oncokb-annotator
printf "\n-> Launch oncokb-annotator...\n"
python oncokb-annotator/MafAnnotator.py -i 'ready_to_annotate_cleaned_IMPACT_mutations_180508.txt' -o 'oncokb_annotated_cleaned_IMPACT_mutations_180508.txt' > /dev/null

printf "\n-> Do some cleaning...\n"
# remove the temporary .txt output from prepare_for_annotation.R
rm 'ready_to_annotate_cleaned_IMPACT_mutations_180508.txt'
# remove the oncokb-annotator virtualenv
deactivate
rmvirtualenv oncokb-annotator_env

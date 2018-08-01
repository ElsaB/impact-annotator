#!/bin/bash


printf "\nWARNING: this shell script has to be run in the cluster \n"


# prepare the impact dataset for impact-annotator
printf "\n-> Annotate the cleaned IMPACT mutation data 'cleaned_IMPACT_mutations_180508' with oncokb-annotator\n"
Rscript prepare_for_annotation.R

# create a 2.7 python virtual env
source `which virtualenvwrapper.sh` # find the path to use virtualenvwrapper functions
printf "Create a python 2.7 virtual env\n"
mkvirtualenv --python=python2.7 oncokb-annotator_env
pip install matplotlib

# launch a job oncokb-annotator
#bsub -I -We 59 -R select[internet] 'python oncokb-annotator/MafAnnotator.py -i "ready_to_annotate_cleaned_IMPACT_mutations_180508.txt" -o "oncokb_annotated_cleaned_IMPACT_mutations_180508.txt'

python oncokb-annotator/MafAnnotator.py -i 'ready_to_annotate_cleaned_IMPACT_mutations_180508.txt' -o 'oncokb_annotated_cleaned_IMPACT_mutations_180508.txt'

# remove the temporary .txt output of prepare_for_annotation.R
rm 'ready_to_annotate_cleaned_IMPACT_mutations_180508.txt'
# remove the oncokb-annotator virtualenv
deactivate
rmvirtualenv oncokb-annotator_env

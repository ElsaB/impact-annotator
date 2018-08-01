#!/bin/bash


# annotate data with oncokb-annotator
printf "\n-> Annotated the cleaned IMPACT mutation data 'cleaned_IMPACT_mutations_180508' with oncokb-annotator\n"
printf "WARNING: this shell script has to be run in the cluster \n"
printf "It might take some time (around 6 minutes)...\n"
Rscript prepare_for_annotation.R
mkvirtualenv --python=python2.7 oncokb-annotator
bsub -I -We 59 -R select[internet] 'python oncokb-annotator/MafAnnotator.py -i "ready_to_annotate_cleaned_IMPACT_mutations_180508.txt" -o "oncokb_annotated_cleaned_IMPACT_mutations_180508.txt'
#rm "ready_to_annotate_cleaned_IMPACT_mutations_180508.txt"
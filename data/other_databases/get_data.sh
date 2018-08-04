#!/bin/bash

# get CIViC data
# Data downloaded from https://civicdb.org/releases under "Variant Summaries", 01/07/18 version
printf "\n-> Get the raw CIViC data\n"
curl https://civicdb.org/downloads/01-Jul-2018/01-Jul-2018-VariantSummaries.tsv --output "other_databases/CIViC_01-Jul-2018-VariantSummaries.tsv"

# get CancerGenomeInterpreter data
# Data downloaded from https://www.cancergenomeinterpreter.org/mutations, 01/17/18 version.
printf "\n-> Get the raw CancerGenomeInterpreter data\n"
curl https://www.cancergenomeinterpreter.org/data/catalog_of_validated_oncogenic_mutations_latest.zip?ts=20180216 --output "other_databases/CGI_catalog_of_validated_oncogenic_mutations_latest.zip"
unzip other_databases/CGI_catalog_of_validated_oncogenic_mutations_latest.zip > /dev/null
rm other_databases/CGI_catalog_of_validated_oncogenic_mutations_latest.zip
rm other_databases/README.txt
rm other_databases/cancer_acronyms.txt
mv other_databases/catalog_of_validated_oncogenic_mutations.tsv other_databases/CGI_catalog_of_validated_oncogenic_mutations.tsv
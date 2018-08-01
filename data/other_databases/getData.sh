#!/bin/bash


# get CIViC data
printf "\n-> Get the raw CIViC data\n"
# Data downloaded from https://civicdb.org/releases under "Variant Summaries", 01/07/18 version
curl https://civicdb.org/downloads/01-Jul-2018/01-Jul-2018-VariantSummaries.tsv --output "./CIViC_01-Jul-2018-VariantSummaries.tsv"
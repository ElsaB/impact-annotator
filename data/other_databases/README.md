# Get other databases data

To get the data run in the cluster or on your working computer:
```shell
$ bash get_data.sh
```

The output files are:

* `CIViC_01-Jul-2018-VariantSummaries.tsv`: [CIViC](https://civicdb.org/) dataset (01/07/2018)  
Downoladed from https://civicdb.org/releases under "Variant Summaries/01-jul-2018"

* `CGI_catalog_of_validated_oncogenic_mutations.tsv`: [Cancer Genome Interpreter](https://www.cancergenomeinterpreter.org/home) dataset (01/07/2018)  
Downloaded from https://www.cancergenomeinterpreter.org/mutations

* `allAnnotatedVariants.txt`: [OncoKB](http://oncokb.org) dataset (up-to-date version)  
Downloaded from http://oncokb.org/api/v1/utils/allAnnotatedVariants.txt

* `PMK_IPM_Knowledgebase_Interpretations_Complete_20180807-1922.xlsx`: [Precision Medecine Knowledgebase](https://pmkb.weill.cornell.edu) dataset (up-to-date version)  
Downloaded from https://pmkb.weill.cornell.edu/therapies/download.xlsx

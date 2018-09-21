# Get the data

### Structure

* **`/annotate_with_click_annotvcf`**: this folder is used to annotate the dataset `all_IMPACT_mutations_180508.txt` with click_annotvcf.  

* **`/annotate_with_oncokb`**: this folder is used to annotate the dataset `cleaned_IMPACT_mutations_180508.txt` with oncokb-annotator.

* **`/annotate_with_oncokb_final_dataset`**: this folder is used to annotate the click_annotvcf-annotated impact dataset with oncokb-annotator.

* **`/dominik`**: :construction: *work in progress* :construction:

* **`/other_databases`**: work with other databases than OncoKB.

* **`/utils`**: useful data-related scripts and files.

***

The following explains how to download each dataset used in the study. More informations on the scripts and the outputs are given in the associated folders.  
:warning: Some dataset needs other datasets to be computed, listed after "Input:". Please always check that you have the input datasets listed before trying to run the script to get the output dataset(s).

### Raw datasets and databases
* **Raw data**  
    Input:  
    Outputs:  
    * `all_IMPACT_mutations_180508.txt` (raw dataset, IMPACT mutations data shared by Ahmet on the 180508)
    * `key.txt` (dataset given by Dominik, gives information like cancer type, BAM id, matched normal, ... on some of the `Tumor_Sample_Barcode`)

    Command:
    ```shell
    $ bash get_raw_dataset.sh your_cluster_username
    ```

* **Other databases ([`/other_databases`](https://github.com/ElsaB/impact-annotator/blob/master/data/other_databases) folder)**  
    Input:  
    Outputs:  
    * `/other_databases/CIViC_01-Jul-2018-VariantSummaries.tsv`
    * `/other_databases/CGI_catalog_of_validated_oncogenic_mutations.tsv`
    * `/other_databases/allAnnotatedVariants.txt`
    * `/other_databases/PMK_IPM_Knowledgebase_Interpretations_Complete_20180807-1922.xlsx`

    Command:
    ```shell
    $ cd other_databases
    $ bash get_data.sh
    ```

### Cleaned dataset used in the analysis part
* **Cleaned dataset**:  
    Input: `all_IMPACT_mutations_180508.txt`  
    Output: `cleaned_IMPACT_mutations_180508.txt` (cleaned dataset obtained at the end of [`first_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/first_study/first_analysis.ipynb)).

    Command:
    ```shell
    $ bash get_cleaned_dataset.sh
    ```
    
* **Cleaned dataset annotated with OncoKB ([`/annotate_with_oncokb`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_oncokb) folder)**  
    Input: `cleaned_IMPACT_mutations_180508.txt`  
    Output: `/annotate_with_oncokb/oncokb_annotated_cleaned_IMPACT_mutations_180508.txt`  

    Command: :warning: run on cluster
    ```shell
    $ cd annotate_with_oncokb
    $ bsub -We 20 -R select[internet] -o job_output.txt "bash annotate_with_oncokb_annotator.sh"
    ```

### Final dataset used in the rest of the study
* **Raw dataset annotated with click_annotvcf ([`/annotate_with_click_annotvcf`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_click_annotvcf) folder)**  
    Input: `all_IMPACT_mutations_180508.txt`  
    Outputs:  
    * `/annotate_with_click_annotvcf/all_IMPACT_mutations_180508.vcf`  
    * `/annotate_with_click_annotvcf/click_annotvcf_IMPACT_mutations_180508.txt`
    
    Command: :warning: run on cluster
    ```shell
    $ cd annotate_with_click_annotvcf
    $ bsub -o job_output.txt "bash annotate_with_click_annotvcf.sh"
    ```

* **Curated final dataset**  
    Inputs:  
    * `/annotate_with_click_annotvcf/click_annotvcf_IMPACT_mutations_180508.txt`
    * `/annotate_with_click_annotvcf/all_IMPACT_mutations_180508.vcf`   

    Output: `final_IMPACT_mutations_180508.txt` (final dataset obtained at the end of [`compute_final_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/compute_final_dataset.ipynb)).

    Command:  
    ```shell
    $ bash get_final_dataset.sh
    ```

* **Final dataset annotated with OncoKB ([`/annotate_with_oncokb_final_dataset`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_oncokb_final_dataset) folder)**  
    Input: `final_IMPACT_mutations_180508.txt`  
    Output: `/annotate_with_oncokb_final_dataset/oncokb_annotated_final_IMPACT_mutations_180508.txt`  
    
    Command: :warning: run on cluster
    ```shell
    $ cd annotate_with_oncokb_final_dataset
    $ bsub -We 20 -R select[internet] -o job_output.txt "bash annotate_with_oncokb_annotator.sh"
    ```

* **Curated and annotated final dataset**  
    Input: `/annotate_with_oncokb_final_dataset/oncokb_annotated_final_IMPACT_mutations_180508.txt`  
    Output: `annotated_final_IMPACT_mutations_180508.txt`

    Command:  
    ```shell
    $ bash annotate_final_dataset.sh
    ```


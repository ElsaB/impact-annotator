# Get the raw and cleaned dataset

To get the data run in the cluster or on your working computer:
```shell
$ bash get_data.sh your_cluster_username
```

The output files are:

- `all_IMPACT_mutations_180508.txt`: raw dataset (IMPACT mutations data shared by Ahmet on the 180508).

- `cleaned_IMPACT_mutations_180508.txt`: cleaned dataset (dataset obtained at the end of [`first_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/first_analysis.ipynb)).

***

### Command to `scp` quickly

From your computer you can use the [`easy_scp.sh`](https://github.com/ElsaB/impact-annotator/blob/master/data/easy_scp.sh) script to `scp` quickly a file from the cluster, here are a few examples:
```shell
$ bash easy_scp.sh guilminp data/all_IMPACT_mutations_180508.txt .
$ bash easy_scp.sh guilminp data/cleaned_IMPACT_mutations_180508.txt .
$ bash easy_scp.sh guilminp data/annotate_with_oncokb/oncokb_annotated_cleaned_IMPACT_mutations_180508.txt ./annotate_with_oncokb
```

### Structure

* **`/annotate_with_click_annotvcf`**: this folder is used to annotate the dataset `all_IMPACT_mutations_180508.txt` with click_annotvcf.  
:construction: *work in progress* :construction:  

* **`/annotate_with_oncokb`**: this folder is used to annotate the dataset `cleaned_IMPACT_mutations_180508.txt` with oncokb-annotator.

* **`/dominik`**: :construction: *work in progress* :construction:

* **`/other_databases`**: work with other databases than OncoKB.

* **`/utils`**: useful data-related scripts and files.
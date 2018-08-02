:construction: *work in progress* :construction:

# Get the raw and cleaned dataset

To get the data run **in the cluster**:
```shell
$ bash get_data.sh your_cluster_username
```

The output files are:

- `all_IMPACT_mutations_180508.txt`: raw dataset (IMPACT mutations data shared by Ahmet on the 180508).

- `cleaned_IMPACT_mutations_180508.txt`: cleaned dataset (dataset obtained at the end of [`first_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/first_analysis.ipynb)).

***

#### oncokb
This folder is used to annotate the dataset `cleaned_IMPACT_mutations_180508.txt` with oncokb-annotator.

#### other_databases
Download other databases used in the notebook ...

#### utils
Useful scripts and files.
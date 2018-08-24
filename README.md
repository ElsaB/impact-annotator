:construction: *work in progress* :construction:

# impact-annotator

**Build an automatic annotator of driver mutations from IMPACT data.**

***

### Working with this repository
You can clone this repository using:
```shell
$ git clone https://github.com/ElsaB/impact-annotator.git
```

The repository was written and tested under `R 3.5.1` and `R 3.2.3`. To work with this repository please:

* Make sure to have the following R packages installed:
	* `tidyverse`
	* `gridExtra`
	* `utf8`
	* `readxl`
```R
# execute in an R console
install.packages("tidyverse", repos = "http://cran.us.r-project.org")
install.packages("gridExtra", repos = "http://cran.us.r-project.org")
install.packages("utf8",      repos = "http://cran.us.r-project.org")
install.packages("readxl",    repos = "http://cran.us.r-project.org")
```

* Make sure to download the data in the `/data` and `/data/other_databases` folders, the instructions are detailed there.
```shell
$ cd data
$ bash get_data.sh your_cluster_username
```
```shell
$ cd data/other_databases
$ bash get_data.sh
```

* If you want to annotate the data with OncoKB, please run oncokb-annotator in the `data/annotate_with_oncokb` folder, the instructions are detailed there.
```shell
$ cd data/annotate_with_oncokb
$ bsub -I -We 20 -R select[internet] "bash annotate_with_oncokb_annotator.sh"
```

### Structure of the repository

* **`/analysis`**: folder to design and run analysis, contains several sub-folders: `/description`, `/prediction`, `/validation`

* **`/data`**: raw data and main processed data, processed data should be reprducible from raw data.  
:warning: This folder should not be versionned.

* **`/doc`**: useful documentation, bibliography, slides for talks...

* **`/results`**: folder where the main results are summarized in a markdown (entries in the form YYMMDD).

* **`/src`**: main scripts that are used across analysis (predictors, cross-validation scripts, evaluation scripts, tools...)


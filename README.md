:construction: *work in progress* :construction:

# impact-annotator

**Build an automatic annotator of driver mutations from IMPACT data.**

***

### Working with this repository
You can clone this repository using:
```bash
$ git clone https://github.com/ElsaB/impact-annotator.git
```

The repository was written and tested under `R 3.5.1` and `R 3.2.3`. To work with this repository please:

* Make sure to download the data in the `data` and `data/other_databases` folders, the instructions are detailed there.
```bash
$ bash data/get_data.sh your_cluster_username
$ bash data/other_databases/get_data.sh
```
* Make sure to have the following R packages installed:
	* `tidyverse`
	* `gridExtra`
```R
# to execute in an R console
install.packages("tidyverse", repos="http://cran.us.r-project.org")
install.packages("gridExtra", repos="http://cran.us.r-project.org")
```


### Structure of the repository

##### data
Raw data and main processed data.  
This should not be versionned.  
Processed data should be reproducible from raw data.

##### doc
Useful documentation, biblio, slides for talks...

##### src
Main scripts that are used across analysis eg: predictors, cross-validation scripts, evaluation scripts.

##### analysis
Folder where you design and run analysis.

This should be split into several sub-folders:
* description
* prediction
* validation

I suggest that within those sub-folders we create entry folder in the form YYMMDD.


##### results

Folder where we summarize the main results in a mardown (notebook.md).

The markdown should have entries in the form YYMMDD that can point to other markdowns from the analysis part.

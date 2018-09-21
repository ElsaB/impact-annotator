:construction: *work in progress* :construction:

# impact-annotator

**Build an automatic annotator of driver mutations from IMPACT data.**

***

### Working with this repository
You can clone this repository using:
```shell
$ git clone https://github.com/ElsaB/impact-annotator.git
```

The repository was written and tested under `R 3.5.1` and `R 3.2.3`, working with Jupyter Notebook. To work with this repository please:

* Make sure to have the following R packages installed:
	* `tidyverse`
	* `gridExtra`
	* `utf8`
	* `hexbin`

    ```R
    # execute in an R console
    install.packages("tidyverse", repos = "http://cran.us.r-project.org")
    install.packages("gridExtra", repos = "http://cran.us.r-project.org")
    install.packages("utf8",      repos = "http://cran.us.r-project.org")
    install.packages("readxl",    repos = "http://cran.us.r-project.org")
    install.packages("hexbin",    repos = "http://cran.us.r-project.org")
    ```
* Go to the [`\data`](https://github.com/ElsaB/impact-annotator/tree/master/data) folder and follow the `README.md` to download all the necessary data.

### Details on the notebooks
All notebooks will begin with the following lines, which load a set of custom function designed by us, and setup the R environment by loading the appropriate libraries:
```R
source("../../../src/utils/custom_tools.R")
setup_environment("../../../src/utils")
```

### Structure of the repository

* **`/analysis`**: folder to design and run analysis, contains several sub-folders: `/description`, `/prediction`, `/validation`

* **`/data`**: raw data and main processed data, processed data should be reprducible from raw data  
    :warning: This folder should not be versionned.

* **`/doc`**: useful documentation, bibliography, slides for talks

* **`/results`**: folder where the main results are summarized in a markdown (entries in the form YYMMDD)

* **`/src`**: main scripts that are used across analysis (predictors, cross-validation scripts, evaluation scripts, tools...)

* **`/temp`**: drafts and temporary files

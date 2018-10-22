:construction: *work in progress* :construction:

# impact-annotator

**Build an automatic annotator of driver mutations from IMPACT data.**

***


## Working with this repository
You can clone this repository using:
```shell
$ git clone https://github.com/ElsaB/impact-annotator.git
```

#### Step 1: Setup your R environment
The first part of the repository was written and tested under `R 3.5.1` and `R 3.2.3`, working with Jupyter Lab. To work with this repository please make sure to have the following R packages installed:

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

#### Step 2: Setup your Python environment
The second part of the repository was written and tested under `Python 3.6`, working with Jupyter Lab. To work with this repository please:

**Step 2.1: Setup the python virtualenv on the cluster**

To create the virtualenv used by the jobs, please run the following commands:
```bash
# create the virtualenv
$ mkvirtualenv --python=python3.6 impact-annotator_env
# install useful libraries
$ pip install ipython nb_conda_kernels numpy matplotlib seaborn scikit-learn pandas imblearn
```
Some useful command lines:
```bash
# activate the virtualenv
$ workon impact-annotator_env
# deactivate the virtualenv
$ deactivate
# remove the virtualenv
$ rmvirtualenv impact-annotator_env
```
Please add the following in your `.bashrc` or `.bashprofile` to use virtualenv function from the notebook later:
```bash
source `which virtualenvwrapper.sh`
```

**Step 2.2: Setup the python conda-env on your local computer**

To create the conda-env, please run the following commands (reply `y` to the prompt `Proceed ([y]/n)?`):
```bash
# create the conda-env and load the appropriate libraries
$ conda create --name impact-annotator_env python=3.6 ipython nb_conda_kernels numpy matplotlib seaborn scikit-learn pandas imblearn
```
Some useful command lines:
```bash
# activate the conda-env
$ source activate impact-annotator_env
# deactivate the conda-env
$ source deactivate
# remove the conda-env
$ conda env remove --name impact-annotator_env

```

:warning: Please always activate the conda-env before running any Python notebook, to make sure you have all the necessary dependecies and the good libraries version:
```bash
$ source activate impact-annotator_env; jupyter notebook
# or
$ source activate impact-annotator_env; jupyter lab
```

The module `setup_environment.ipy` automatically check that you're running the notebook under the `impact-annotator_env` conda-env, you can check it yourself by running in the notebook:
```ipython
# prints the current conda-env used
!echo $CONDA_DEFAULT_ENV
# list all the conda-env on your computer, the one you're working on is indicated by a star
!conda env list
```

#### Step 3: Download the data
Go to the [`\data`](https://github.com/ElsaB/impact-annotator/tree/master/data) folder and follow the `README.md` to download all the necessary data.

#### Checklist
- [ ] Downloaded the R packages `tidyverse`, `gridExtra`, `utf8` and `hexbin`
- [ ] Created a cluster virtualenv `impact-annotator_env`
- [ ] Added ```source `which virtualenvwrapper.sh``` in `.bashrc` or `.bashprofile`
- [ ] Created a local conda-env `impact-annotator_env`
- [ ] Have remembered to always activate the conda env `impact-annotator_env` before running a jupyter notebook/jupyter lab instance (`$ source activate impact-annotator_env`)




## Details on the notebooks
All R notebooks will begin with the following lines, which load a set of custom function designed by us, and setup the R environment by loading the appropriate libraries:
```R
source("../../../src/utils/custom_tools.R")
setup_environment("../../../src/utils")
```

All Python notebooks will begin with the following lines, which load a set of custom function designed by us, and load appropriate libraries, it also makes sure that you're working on the `impact-annotator_env` that you should have created earlier:
```python
%run ../setup_environment.ipy
# if you want to send jobs on the cluster from the notebook on your local computer:
%run ../Selene_Job.ipy 
```



## Structure of the repository

* **`/analysis`**: folder to design and run analysis, contains several sub-folders: `/description`, `/prediction`, `/validation`

* **`/data`**: raw data and main processed data, processed data should be reprducible from raw data  
    :warning: This folder should not be versionned.

* **`/doc`**: useful documentation, bibliography, slides for talks

* **`/results`**: folder where the main results are summarized in a markdown (entries in the form YYMMDD)

* **`/src`**: main scripts that are used across analysis (predictors, cross-validation scripts, evaluation scripts, tools...)

* **`/temp`**: drafts and temporary files

:construction: *work in progress* :construction:

# impact-annotator

**Develop a knowledge-based approach using MSK-IMPACT data to build an automatic variant classifier.**

***

## Repository structure

- **`analysis/`**: folder to design and run analysis, contains several sub-folders:
    - `description/`: this part is written in R and contains the description/annotation/formating process of the dataset
    - `prediction/`: this part is written in Python and contains the classifier building process

- **`data/`**: raw data and main processed data, processed data should be reprducible from raw data  
  > :warning: This folder should not be versionned.

- **`doc/`**: useful documentation, bibliography, slides for talks

- **`temp/`**: drafts, temporary files and old scripts

- **`utils/`**: main scripts used across analysis (predictors, cross-validation scripts, evaluation scripts, tools...)




## Work with this repository
You can clone this repository using:
```shell
$ git clone https://github.com/ElsaB/impact-annotator.git
```

### Step 1: Setup your R environment
The first part of the repository was written and tested under `R 3.5.1` and `R 3.2.3`, working with JupyterLab.

To work with this repository please make sure to have the following R packages installed:

- `tidyverse`
- `gridExtra`
- `utf8`
- `readxl`
- `hexbin`

```R
# run in an R console
install.packages('tidyverse', repos = 'http://cran.us.r-project.org')
install.packages('gridExtra', repos = 'http://cran.us.r-project.org')
install.packages('utf8',      repos = 'http://cran.us.r-project.org')
install.packages('readxl',    repos = 'http://cran.us.r-project.org')
install.packages('hexbin',    repos = 'http://cran.us.r-project.org')
```

### Step 2: Setup your Python environment
The second part of the repository was written and tested under `Python 3.6`, working with JupyterLab. You can see the requirements under [`conda-env_requirements.yml`](https://github.com/ElsaB/impact-annotator/blob/master/conda-env_requirements.txt). The main Python packages used are:

- `numpy`
- `matplotlib`
- `seaborn`
- `pandas`
- `scikit-learn`
- `imbalanced-learn`
- `ipython`
- `nb_conda_kernels`

To work with this repository please:

#### Step 2.1: Setup a python virtualenv on the cluster

To create the virtualenv used by the jobs, please run the following commands on your selene cluster session:
```bash
# create the virtualenv
$ mkvirtualenv --python=python3.6 impact-annotator_env
# install useful libraries
$ pip install numpy matplotlib seaborn pandas scikit-learn imbalanced-learn ipython nb_conda_kernels
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

Please add the following line in your `.bashrc` or `.bash_profile` to use virtualenv functions directly from the notebook later:
```bash
# add in your .bashrc or .bash_profile
source `which virtualenvwrapper.sh`
```

#### Step 2.2: Setup a python conda-env on your local computer

To create the conda-env, please run the following command:
```bash
# create the conda-env and load the appropriate libraries
$ conda env create --name impact-annotator_env --file conda-env_requirements.yml
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

> :warning: Please always activate the `impact-annotator_env` conda-env before running any Python notebook, to make sure you have all the necessary dependecies and the good libraries version:
> ```bash
> # if you use jupyter notebook
> $ source activate impact-annotator_env; jupyter notebook
> 
> # if you use jupyter lab
> $ source activate impact-annotator_env; jupyter lab
> ```

In any Python Jupyter notebook, importing the file `utils/python/setup_environment.ipy` automatically check that you're running the notebook under the `impact-annotator_env` conda-env, you can check it yourself by running in the notebook:
```ipython
# prints the current conda-env used
!echo $CONDA_DEFAULT_ENV

# list all the conda-env on your computer, the one you're working on is indicated by a star
!conda env list
```

### Step 3: Download the data
Go to the [`data/`](https://github.com/ElsaB/impact-annotator/tree/master/data) folder and follow the `README.md` to download all the necessary data.

### Step 3: Checklist
- [ ] Download R packages `tidyverse`, `gridExtra`, `utf8`, `readxl`, `hexbin`
- [ ] Create cluster virtualenv `impact-annotator_env`
- [ ] Add <code>source \`which virtualenvwrapper.sh\`</code> in `.bashrc` or `.bash_profile`
- [ ] Create local conda-env `impact-annotator_env`
- [ ] Remember to always activate the conda-env `impact-annotator_env` before running a Jupyter Notebook/JupyterLab instance (`$ source activate impact-annotator_env`)




## Details on the notebooks
All R notebooks will begin with the following lines, which load a set of custom function designed by us, and setup the R environment by loading the appropriate libraries:
```R
source("../../../utils/R/custom_tools.R")
setup_environment("../../../utils/R")
```

All Python notebooks will begin with the following lines, which load a set of custom function designed by us, and load appropriate libraries, it also makes sure that you're working on the `impact-annotator_env` that you should have created earlier:
```ipython
%run ../../../utils/Python/setup_environment.ipy

# if you want to send jobs on the cluster from the notebook on your local computer, please also run:
%run ../../../utils/Python/Selene_Job.ipy 
```

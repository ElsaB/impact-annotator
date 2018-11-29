# todo list

### General
- [ ] read paper in details and understand differences/similarities
- [ ] remove unmatched cases

### GitHub
- [x] create `conda-env_requirements.yml` and remove prefix
- [x] reorganize `src/` folder to `utils/R` and `utils/Python`
- [ ] simplify `.gitignore`
- [x] mv `ml_tools.py` to `temp/old/`
- [ ] use > in .md
- [x] check main `README.md`
- [ ] check main `README.md` repository structure
- [ ] sort `temp/` folder
- [ ] check `data/` folder
- [ ] check `analysis/` folder
- [ ] check all R notebooks
- [ ] check all Python notebooks
- [ ] change main description of projet (get all rights - ask Elsa)
- [ ] merge other todo list


### Sampling
- [ ] undersampling inconsistent sorted/shuffle
- [ ] Optimise undersampling/oversampling (imblearn technics)
- [ ] Unify patients and key for cross-validation? (http://scikit-learn.org/stable/modules/cross_validation.html#group-cv) -> Gfold repeated cross-validation


### Other
- [ ] Errors only appearing in detailed CV
- [ ] Rewrite `cluster_job_tutorial.ipynb`
- [ ] Rename metrics to experience
- [ ] Metric representative of patient


### Ideas
- [ ] Deep learning
- [ ] Web interface
- [ ] More artefacts
- [ ] Call again the IMPACT `.bam` files with a uniform caller to perform analysis


### temp
- `conda create -c conda-forge --name impact-annotator_env python=3.6 ipython nb_conda_kernels numpy matplotlib seaborn scikit-learn pandas imbalanced-learn`
- **`results/`**: folder where the main results are summarized in a markdown (entries in the form YYMMDD)
- `conda env export > conda-env_requirements.txt`
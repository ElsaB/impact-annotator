# todo list

### General
- [x] read paper in details and understand differences/similarities
- [x] remove unmatched cases

### GitHub
- [x] create `conda-env_requirements.yml` and remove prefix
- [x] reorganize `src/` folder to `utils/R` and `utils/Python`
- [x] mv `ml_tools.py` to `temp/old/`
- [x] check main `README.md`
- [x] merge other todo list
- [x] simplify `.gitignore`

### Final clean
- [ ] create new and clean git repository
- [ ] sort `temp/` folder
- [ ] check `data/` folder
- [ ] check `analysis/` folder
- [ ] check main `README.md` repository structure
- [ ] check all R notebooks
- [ ] check all Python notebooks
- [ ] change main description of projet (get all rights - ask Elsa)
- [ ] explain impact_181105
- [ ] clean `sorted_sampling_issue.ipynb`
- [ ] Comment Python notebooks
- [ ] Specifi `ssh-add` is necessary for anyone to use selene_job.ipy

### Sampling and cross-validation
- [ ] undersampling inconsistent sorted/shuffle
- [ ] Optimise undersampling/oversampling (imblearn technics)
- [ ] Unify patients and key for cross-validation? (http://scikit-learn.org/stable/modules/cross_validation.html#group-cv) -> Gfold repeated cross-validation

### Other
- [x] Bug with `Uniform` prediction
- [x] change summary color handling
- [ ] Errors only appearing in detailed CV
- [ ] Rewrite `cluster_job_tutorial.ipynb` and add a section on how to use `Metrics` and `Summary`
- [ ] Metric representative of patient

### Ideas
- [ ] Deep learning
- [ ] Web interface
- [ ] More artefacts
- [ ] Data augmentation
- [ ] Polynomial regression: extending linear models with basis functions
        from sklearn.preprocessing import PolynomialFeatures
        poly = PolynomialFeatures(degree=2)
        X_poly = poly.fit_transform(X)
        print(X_poly.shape)
- [ ] Feature selection: https://github.com/amueller/scipy-2017-sklearn/blob/master/notebooks/19.Feature_Selection.ipynb
- [ ] More features ? (number of callers, caller flags...)
- [ ] COSMIC Peak arount mutation (Noushin idea)
- [ ] OncoKB likely oncogenic, predicted oncogenic: go back on this classification later on
- [ ] Call again the IMPACT `.bam` files with a uniform caller to perform analysis

### temp
- `conda create -c conda-forge --name impact-annotator_env python=3.6 ipython nb_conda_kernels numpy matplotlib seaborn scikit-learn pandas imbalanced-learn`
- `conda env export > conda-env_requirements.txt`
- Warning, dummy variables are also scaled!

Other:
Benchmarking articles
- https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0484-1
- https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5610688/

Databases
- ClinVar [CIViC, CGI, PMK]
- Drug Gene Knwoledge Database [CIViC]
- Database of Curated Mutations [CIViC]
- ClinGen [CIViC]
- PharmKGB [CIViC]
- Bccancer.bc.ca [Elli]
- Drug gene interaction database [pct]
- Precision cancer medecine [pct]
- Tumor Portal [OncoKB]
- Targeted Cancer Portal [OncoKB]
https://github.com/seandavi/awesome-cancer-variant-databases/blob/master/README.md

- Features:
    - SIFT, Polyphen, CADD score used in a lot of algorithm
    - GAVIN, DANN
    - HGMD database? HGMD count ?
    - CHASM feature supplementary materials
    - CanDra feature supplementary materials
    - Cscape feature supplementary material
    - Expecto


['maroon', 'firebrick', 'crimson', 'tomato', 'coral', 'lightcoral']

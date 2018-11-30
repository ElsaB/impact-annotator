# todo list

### General
- [ ] read paper in details and understand differences/similarities
- [ ] remove unmatched cases

### GitHub
- [x] create `conda-env_requirements.yml` and remove prefix
- [x] reorganize `src/` folder to `utils/R` and `utils/Python`
- [x] mv `ml_tools.py` to `temp/old/`
- [x] check main `README.md`
- [ ] simplify `.gitignore`
- [ ] check main `README.md` repository structure
- [ ] sort `temp/` folder
- [ ] check `data/` folder
- [ ] check `analysis/` folder
- [ ] check all R notebooks
- [ ] check all Python notebooks
- [ ] change main description of projet (get all rights - ask Elsa)
- [ ] merge other todo list

error click_annotvcf


### Sampling
- [ ] undersampling inconsistent sorted/shuffle
- [ ] Optimise undersampling/oversampling (imblearn technics)


### Cross-validation
- [ ] Unify patients and key for cross-validation? (http://scikit-learn.org/stable/modules/cross_validation.html#group-cv) -> Gfold repeated cross-validation


### Other
- [x] Bug with `Uniform` prediction
- [ ] Comment notebooks
- [ ] Errors only appearing in detailed CV
- [ ] Rewrite `cluster_job_tutorial.ipynb` and add a section on how to use `Metrics` and `Summary`
- [ ] Rename metrics to experience
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
- **`results/`**: folder where the main results are summarized in a markdown (entries in the form YYMMDD)
- `conda env export > conda-env_requirements.txt`

Warning, dummy variables are also scaled!

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


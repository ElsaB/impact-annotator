:construction: *work in progress* :construction:

# Machine learning variant annotation projects

**TODO:**

* CHASM feature supplementary materials
* CanDra feature supplementary materials
* Cscape feature supplementary materials
* Publications that have used CHASM (http://wiki.chasmsoftware.org/index.php/Publications)
* https://genomebiology.biomedcentral.com/articles/10.1186/s13059-014-0484-1
* ENCODE dataset
* HGMD, PolyPhen2, SIFT, CADD, DANN, FATHMM-MKL, FunSeq2, MutationAssesor, CanPredict
* http://www.cravat.us/CRAVAT/help.jsp?chapter=analysis_tools&article=vest
* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5610688/

**Table of contents**

* [CHASM](#chasm)
* [CanDrA](#candra)
* [CScape](#cscape)


## CHASM
**Website:** http://wiki.chasmsoftware.org/index.php/CHASM_Overview  
**Paper:** [link](https://www.ncbi.nlm.nih.gov/pubmed/19654296?ordinalpos=2&itool=EntrezSystem2.PEntrez.Pubmed.Pubmed_ResultsPanel.Pubmed_DefaultReportPanel.Pubmed_RVDocSum) Carter H, Chen S, Isik L, Tyekucheva S, Velculescu VE, Kinzler KW, Vogelstein B, Karchin R.(2009)Cancer-specific high-throughput annotation of somatic mutations: computational prediction of driver missense mutations.Cancer Research. 69(16):6660-7  
**Date:** August 2009  

* Somatic and missense mutations only
* Discriminate between known driver missense mutations and randomly generated missense mutations
* Algorithm:
	* Random Forest (500 trees and default parameters mtry = 7)
	* Compared with SVM
	* Area under ROC curve > 0.91, area under precision-recall curve > 0.79
* Features:
	* Trained on 49 predictive features (cf. supplementary material) selected among 80 features
	* Feature selection done with a protocol based on mutual information (generalized version of correlation)
	* Features with missing values estimated with k-nearest neighbors algorithm
	* Prior to training all features standardized with the Z-score method.
* Dataset:
	* 2488 missense driver mutations from COSMIC database and recent research (1244 for feature selection and 1244 for classifier training)
	* Synthetic passenger generated according to background base substitution frequencies obvserved for the specific tumor type. Bsampling from eight multinomial distributions that depend on di-nucleotide context and tumor type (4500 for feature selection and 4500 for classifier training)
* Comparison with PolyPhen, SIFT, CanPredict and KinaseSVM
* Last updated on the website on 2014.
* Propose a whole set of software and precomputed data to run CHASM on your own mutations dataset.
* Now included in CRAVAT online.



## CanDrA
**Website:** http://bioinformatics.mdanderson.org/main/CanDrA  
**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3813554/) Mao Y, Chen H, Liang H, Meric-Bernstam F, Mills GB, Chen K. CanDrA: Cancer-Specific Driver Missense Mutation Annotation with Optimized Features. Adamovic T, ed. PLoS ONE. 2013;8(10):e77945. doi:10.1371/journal.pone.0077945.  
**Date:** October 2013  

* Missense mutations only
* Work only on glioblastoma mutliforme (GBM) and ovarian carcinoma (OVC)
* Algorithm:
	* Weighted SVM
	* 3 categories: driver, no-call and passenger
* Features:
	* 95 structural and evolutionary features computed by over 10 functional prediction algorithms such as CHASM, SIFT and MutationAssessor (cf. supplementary material)
	* 4 types of features: evolutionary conservation (a), phyciochemical properties of the protein (b), protein domains (c) and sequence context (d)
	* MutationAssessor and SIFT (a), SNPs3D (a,b), CanPredict (a,c), MutationTaster and SNAP (a,b,c), CHASM and Polyphen2 (a,b,c,d)
	* Importance of disease-specific factors (cancer type, ...)
	* From 4 data portals: CHASM's SNVBOX, ENSEMBL Variant Effect Predictor, Mutation Assessor and ANNOVAR.
	* Features with missing values estimated with k-nearest neighbors algorithm
	* See article for details on feature selection [Feature Selection and Evaluation page 3]
	* For GBM: 21 final features, AUCs of 0.911 and 0.941
	* For OVC: 22 final features, AUCs of 0.953
* Dataset:
	* COSMIC, TCGA, Cancer Cell Line Encyclopedia (CCLE)
	* Driver mutation: mutation observed in at least two different samples, from either TCGA or COSMIC
	* Excluded reccurent mutations that coincided with other putative functional mutations (indels, nonsense mutations, nonstop mutations, splice site mutations, translation start site mutations) in the same gene of the same sample
	* 67 mutations for GBM and 61 for OVC (92.5% and 80.3% considered as drivers in previous study) only from COSMIC and TCGA
	* Passenger mutations from hyper-mutated samples (COSMIC, TCGA and CCLE): 490 mutations for GBM and 462 for OVC
	* Construction of a cancer-type specific expanded set of drivers and passengers following an empirical rule (observed in at least 3 tumor samples or ...): 1529 GBM and 1768 OVC putative drivers, 1259 GBM and 8075 OVC passenger mutations.
* Comparison to CHASM: not clear if efficient way of producing synthetic passenger mutations, new predictive features not considered in CHASM, random forest perhaps not optimal (small training set size and high-dimensionality of the data), new recent data
* CanDrA Plus: 15 cancer types and extra model working for all cancer
* Last update: 2013


## CScape
**Website:** http://cscape.biocompute.org.uk  
**Paper:** [link](https://www.nature.com/articles/s41598-017-11746-4) Rogers MF, Shihab H, Gaunt TR, Campbell C (2017). CScape: a tool for predicting oncogenic single-point mutations in the cancer genome. Nature Scientific Reports  
**Date:** September 2017   

* Predicts the oncogenic status (disease-driver or neutral)
* Somatic and point mutations only
* In the coding and non-coding regions of the cancer genome
* Online software
* Algorithm:
	* Leave-one-chromosome cross-validation, randomly selected balanced sets of 1,000 positive and 1,000 negative mutations
	* Two distinc classifiers: CS-coding for coding regions and CS-noncoding for noncoding regions
	* Multiple Kernel Learning
	* Balanced accuracy of 72.3% in coding regions and 62.9% in non-coding regions. Can achieve up to 91% balanced accuracy in coding regions and 70% in non-coding regions on independent dataset
* Features:
	* More than 30 features groups (cf. supplementary material: 30 distinct ENCODE datasets)
	* New feature for the non-cdoing predictor
	* Greedy sequential learning to indentify an optimal combination og feature groups
* Dataset:
	* Positive 46,420 (pathogenic) dataset: COSMIC database (version 75, November 2015) with reccurence at least 5 for coding regions and 3 for non-coding regions (work done on finding the best threshold to increase accuracy while limiting bias)
	* Negative dataset: 131,714 SNVs from the 1,000 Genomes Project (could contain true positive because unannotated) located not too far from the positive dataset mutations
* Comparison with PolyPhen2, SIFT, FATHMM-MKL, MutationAssesor, CADD and DANN
* Test on multiples databases (ICGC, TCGA, ClinVar, ...)












:construction: *work in progress* :construction:

# Variant annotation databases

See the notebook [`analysis/description/180731_pierre/comparison_between_variant_annotation_databases.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/comparison_between_variant_annotation_databases.ipynb) for direct comparison between these databases and OncoKB.

**TODO:**

* Read CIViC paper page 1 par on the right.
* OncoKB
* Read CancerGenomeInterpreter paper page 1 par on the right. 2 first lines 2nd page
* CHASM, CanDrA, CADD, MA. FATHMM cf. supplementary figure 2 of CancerGenomeInterpreter paper
* http://cadd.gs.washington.edu/home
* http://fathmm.biocompute.org.uk/about.html
* http://wiki.chasmsoftware.org/index.php/CHASM_Overview
* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3813554/
* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5860356/
* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3558800/
* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3673218/
* https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4083756/
* https://github.com/seandavi/awesome-cancer-variant-databases
* Individual algorithms + meta-predictors (Condel and CanDrA)
 

**Table of contents**

* [CIViC](#civic)
* [Cancer Genome Interpreter](#cancer-genome-interpreter)
* [Precision Medicine Knowledgebase](#precision-medicine-knowledgebase)
* [Other](#other)
	* ..
	* ..



## CIViC
**Website:** https://civicdb.org/  
**Paper:** [link](https://www.nature.com/articles/ng.3774) Griffith M\*,†, Spies NC\*, Krysiak K\*, McMichael JF, Coffman AC, Danos AM, Ainscough BJ, Ramirez CA, Rieke DT, Kujan L, Barnell EK, Wagner AH, Skidmore ZL, Wollam A, Liu CJ, Jones MR, Bilski RL, Lesurf R, Feng YY, Shah NM, Bonakdar M, Trani L, Matlock M, Ramu A, Campbell KM, Spies GC, Graubert AP, Gangavarapu K, Eldred JM, Larson DE, Walker JR, Good BM, Wu C, Su AI, Dienstmann R, Margolin AA, Tamborero D, Lopez-Bigas N, Jones SJ, Bose R, Spencer DH Wartman LD, Wilson RK, Mardis ER, Griffith OL†. 2016. CIViC is a community knowledgebase for expert crowdsourcing the clinical interpretation of variants in cancer. Nat Genet. 49, 170–174 (2017); doi: http://dx.doi.org/10.1038/ng.3774. \*These authors contributed equally to this work. †Corresponding author.  
**Date:** August 2009  

Pierre - *"It's a crowdsourcing OncoKB."*

* **What is it?** CIViC is a community expert-crowdsourced knowledgebase for clinical interpretation of variants in cancer. It describes the therapeutic, prognostic, diagnosic and predisposing relevance of inherited and somatic variants of all types.
* **Where does the data comes from?** National team of experts collaborating remotely within a centralized curation interface. Agreement between at least two independant contributors (and at least one must be an expert editor) before acceptance of new evidence or revisions of existing content. Validated curators can add a variant description if there is evidence link to cancer with some clinical relevance.
* **Size of the database?** 1,678 curated interpretations of clinical relevance for 713 variants affecting 283 genes (in January 2017, from the article).
* **Other informations**  
    * Scoring system of the variants.
    * Present itself as more open and transparent that the concurrency.
    * All variant types supported as well as all variants origine (somatic mutation, germline mutation and germline polymorphism).



## Cancer Genome Interpreter
**Website:** https://www.cancergenomeinterpreter.org/home  
**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5875005/) Cancer Genome Interpreter Annotates The Biological And Clinical Relevance Of Tumor Alterations  
**Date:** August 2009  

Pierre - *"It's OncoKB with an heuristic rule based-on variant annotater addon"*

* **What is it?** Cancer Genome Interpreter is a platform that systematizes the interpretation of cancer genomes, the main hallmark of which is streamlining and automatization of the whole process. It identifies all known and likely tumorigenic genomic alterations and annotate all variants that constitutes biomarkers.
* **Where does the data comes from?** Employs existing or newly developed resources and computational methods. Alterations that are clinically or experimentally validated to drive tumor phenotypes –previously culled from public sources– are identified by the CGI, whereas the effect of the remaining alterations of uncertain significance are predicted using in silico approaches, such as OncodriveMUT (for mutations). Validated oncogenic mutations catalog: DoCM, ClinVar and OncoKB + results of several published experimental assays.
* **Size of the database?** 837 genes in 193 different cancer types, 5314 validated mutations (March 2018, from the article).
* **Other informations**  
    * Automatically recognizes the format, remaps the variants as needed and standardized the annotation for downstream compatibility. 
    * All analysis are cancer-specific and thus the tumor type of the samples to analyze is required.
* **OncodriveMUT**  
    * The CGI asseses the tumorigenic potential of the variants of unknown significance with OncodriveMUT "a newly developed rule-based approach that combines the values of these features". Used by the CGI to analyze the mutations in cancer genes that are not found in the Catalog of Validated Oncogenic Mutations.
    * Relevant features used to classify the mutations:
        * Oncogene vs TSG
        * Consequence type (synonymous, missense, inframe indel or truncating)
        * Position within the transcript
        * If it alls in a mutation hotspot or cluster
        * Predicted functional impact
        * Frequency within the human population
        * If it occurs in a domain of the protein that is depleted of germline variants  
    * Using a set of heuristic rules. Compared the performance obtained with a machine-learning approach: random forest with 1,000 estimators trained in a ten fold cross-validation with 70% of the features in order to predict the remaining 30%. Both the machine-learning and the heuristic approach exhibited similar performace, therefore decided to use the heuristic rules.
    * Analyzed cohorts of tumors (6,92 samples across 28 cancer types) and samples from healthy donors (60,706 unrelated individuals).
    * Performance in the task of classifying driver and passenger mutations assessed using the Catalog of Validated Oncogenic Mutations ($n = 5314$) and a collected set of neutral PAMS affecting cancer gene ($n = 1676$): 86% accuracy.



## Precision Medicine Knowledgebase
**Website:** https://pmkb.weill.cornell.edu  
**Article:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5391733/) Huang L, Fernandes H, Zia H, et al. The cancer precision medicine knowledge base for structured clinical-grade mutations and interpretations. Journal of the American Medical Informatics Association : JAMIA. 2017;24(3):513-519. doi:10.1093/jamia/ocw148.  
**Date:** October 2016    

*Pierre - "Bla"*

* **What is it?** My Cancer Genome is a precision cancer medicine knowledge resource for physicians, patients, caregivers and researchers. It gives information on what mutations make cancers grow and related therapeutic implications, including available clinical trials.
* **Where does the data comes from?** A database (DIRECT) has been established, it contains information about the potential clinical significance of specific tumor mutations. To compile the information in DIRECT, the PCMI team used a retrospective PubMed medical subject heading (MeSH) search to identify patient-level, mutation-specific, drug response data from different studies in NSCLC. The initial goal of the DIRECT database was to catalogue clinically relevant somatic mutations in lung cancer. The project began by cataloguing data from patients with EGFR mutations but will be expanding to incorporate data on all known mutations with potential clinical significance in various types of cancer.  Not sure if DIRECT is the only database used, the website says "Currently, DIRECT catalogues drug response data from patients with non-small cell lung cancer (NSCLC) whose tumors harbor mutations in EGFR", but maybe the website is not up-to-date. Indeed, we can find other cancer type variants on the website.
* **Size of the database?** Unknown.
* **Other informations**  
    * Focused on "patient focus content".


## Other

### candl
**Website:** http://candl.osu.edu  
The current version number is 1.1 - Mar2015. The most recent update to data was on 5:15pm, July 31st, 2015.


### pct
**Website:** https://pct.mdanderson.org/home  
Modified on Fri, 12 Sep 2014 16:46:06 GMT  
Data not public.


### MyCancerGenome
**Website:** https://www.mycancergenome.org  
**Article:** DIRECT paper at https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4121886/, published in Clin Cancer Res. in April 2013. DIRECT stands for 'DNA-mutation Inventory to Refine and Enhance Cancer Treatment', it contains information about the potential clinical significance of specific tumor mutations (it is the database on which MyCancerGenome is running?).  
**Author:** Vanderbilt-Ingram Cancer Center  
**Data:** not public

*Pierre - "It's an old OncoKB."*

* **What is it?** My Cancer Genome is a precision cancer medicine knowledge resource for physicians, patients, caregivers and researchers. It gives information on what mutations make cancers grow and related therapeutic implications, including available clinical trials.
* **Where does the data comes from?** A database (DIRECT) has been established, it contains information about the potential clinical significance of specific tumor mutations. To compile the information in DIRECT, the PCMI team used a retrospective PubMed medical subject heading (MeSH) search to identify patient-level, mutation-specific, drug response data from different studies in NSCLC. The initial goal of the DIRECT database was to catalogue clinically relevant somatic mutations in lung cancer. The project began by cataloguing data from patients with EGFR mutations but will be expanding to incorporate data on all known mutations with potential clinical significance in various types of cancer.  Not sure if DIRECT is the only database used, the website says "Currently, DIRECT catalogues drug response data from patients with non-small cell lung cancer (NSCLC) whose tumors harbor mutations in EGFR", but maybe the website is not up-to-date. Indeed, we can find other cancer type variants on the website.
* **Size of the database?** Unknown.
* **Other informations**
    * Focused on "patient focus content".

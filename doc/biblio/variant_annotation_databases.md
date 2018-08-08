:construction: *work in progress* :construction:

# Variant annotation databases

<!---
**TODO:**

* To study:
    * OncoKB [all]
    * ClinVar [CIViC, CGI, PMK]
    * Gene Drug Knwoledge Database [CIViC]
    * Database of Curated Mutations [CIViC]
    * ClinGen [CIViC]
    * PharmKGB [CIViC]
    * Cancer Driver Log [CIViC]
    * DoCM [CGI]
    * Bccancer.bc.ca [Elli]
    * Drug gene interaction database [pct]
    * Precision cancer medecine [pct]
* Supplementary table 1 [CIViC]
* Additional file 1: Table S1 [CGI]
* https://github.com/seandavi/awesome-cancer-variant-databases/blob/master/README.md
--->


**Summary and table of contents**

| Database name                                                         | Variants | Genes | Date     | Public             | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | -------------------------------------------- |
| [CIViC](#civic)                                                       | 1936     | 358   | 08/08/18 | :white_check_mark: | https://civicdb.org/home                     |
| [Cancer Genome Interpreter](#cancer-genome-interpreter)               | 5601     | 765   | 08/08/18 | :white_check_mark: | https://www.cancergenomeinterpreter.org/home |
| [Precision Medicine Knowledgebase](#precision-medicine-knowledgebase) | 2168     | 606   | 08/08/18 | :white_check_mark: | https://pmkb.weill.cornell.edu               |
| [MyCancerGenome](#mycancergenome)                                     | ?        | ?     | -        | :x:                | https://www.mycancergenome.org               |
| [JAX-Clinical Knowledgebase](#jax-clinical-knowledgebase)             | ?        | 82    | 08/08/18 | :x:                | https://ckb.jax.org                          |
| [Personalized Cancer Therapy](#personalized-cancer-therapy)           | ?        | ?     | -        | :x:                | https://pct.mdanderson.org                   |
| [CanDL](#candl)                                                       |          |       |          |                    | https://candl.osu.edu                        |

See the notebook [`analysis/description/180731_pierre/comparison_between_variant_annotation_databases.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/comparison_between_variant_annotation_databases.ipynb) for direct comparison between some of these databases (when the data was available and usable) and OncoKB.



## CIViC
| Database name                                                         | Variants | Genes | Date     | Public             | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | -------------------------------------------- |
| [CIViC](#civic)                                                       | 1936     | 358   | 08/08/18 | :white_check_mark: | https://civicdb.org/home                     |

**Paper:** [link](https://www.nature.com/articles/ng.3774) Griffith M\*,†, Spies NC\*, Krysiak K\*, McMichael JF, Coffman AC, Danos AM, Ainscough BJ, Ramirez CA, Rieke DT, Kujan L, Barnell EK, Wagner AH, Skidmore ZL, Wollam A, Liu CJ, Jones MR, Bilski RL, Lesurf R, Feng YY, Shah NM, Bonakdar M, Trani L, Matlock M, Ramu A, Campbell KM, Spies GC, Graubert AP, Gangavarapu K, Eldred JM, Larson DE, Walker JR, Good BM, Wu C, Su AI, Dienstmann R, Margolin AA, Tamborero D, Lopez-Bigas N, Jones SJ, Bose R, Spencer DH Wartman LD, Wilson RK, Mardis ER, Griffith OL†. 2016. CIViC is a community knowledgebase for expert crowdsourcing the clinical interpretation of variants in cancer. Nat Genet. 49, 170–174 (2017); doi: http://dx.doi.org/10.1038/ng.3774. \*These authors contributed equally to this work. †Corresponding author.  
**Publication date:** January 2017  

Pierre - *"It's a crowdsourcing OncoKB."*

* **What is it?** CIViC is a community expert-crowdsourced knowledgebase for clinical interpretation of variants in cancer. It describes the therapeutic, prognostic, diagnosic and predisposing relevance of inherited and somatic variants of all types.
* **Where does the data comes from?** National team of experts collaborating remotely within a centralized curation interface. Agreement between at least two independant contributors (and at least one must be an expert editor) before acceptance of new evidence or revisions of existing content. Validated curators can add a variant description if there is evidence link to cancer with some clinical relevance.
* **Size of the database?**
    * In January 2017, from the article: 1,678 curated interpretations of clinical relevance for 713 variants affecting 283 genes
    * 08/08/18, from the website: 1936 variants for 358 genes
* **Other informations**  
    * Scoring system of the variants.
    * Present itself as more open and transparent that the concurrency.
    * All variant types supported as well as all variants origine (somatic mutation, germline mutation and germline polymorphism).



## Cancer Genome Interpreter
| Database name                                                         | Variants | Genes | Date     | Public             | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | -------------------------------------------- |
| [Cancer Genome Interpreter](#cancer-genome-interpreter)               | 5601     | 765   | 08/08/18 | :white_check_mark: | https://www.cancergenomeinterpreter.org/home |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5875005/) Tamborero D, Rubio-Perez C, Deu-Pons J, et al. Cancer Genome Interpreter annotates the biological and clinical relevance of tumor alterations. Genome Medicine. 2018;10:25. doi:10.1186/s13073-018-0531-8.  
**Publication date:** March 2018  

Pierre - *"It's OncoKB + an heuristic rule to sort the unknown variants"*

* **What is it?** Cancer Genome Interpreter is a platform that systematizes the interpretation of cancer genomes, the main hallmark of which is streamlining and automatization of the whole process. It identifies all known and likely tumorigenic genomic alterations and annotate all variants that constitutes biomarkers.
* **Where does the data comes from?** Employs existing or newly developed resources and computational methods. Alterations that are clinically or experimentally validated to drive tumor phenotypes –previously culled from public sources– are identified by the CGI, whereas the effect of the remaining alterations of uncertain significance are predicted using in silico approaches, such as OncodriveMUT (for mutations). Validated oncogenic mutations catalog: DoCM, ClinVar and OncoKB + results of several published experimental assays.
* **Size of the database?**
    * March 2018, from the article: 5314 validated mutations
    * * 08/08/18, from the website: 765 genes in 246 different cancer types, 5601 validated mutations
* **Other informations**  
    * Automatically recognizes the format, remaps the variants as needed and standardized the annotation for downstream compatibility. 
    * All analysis are cancer-specific and thus the tumor type of the samples to analyze is required.
* **OncodriveMUT**  
    * The CGI asseses the tumorigenic potential of the variants of unknown significance with OncodriveMUT "a newly developed rule-based approach that combines the values of these features". Used by the CGI to analyze the mutations in cancer genes that are not found in the Catalog of Validated Oncogenic Mutations.
    * Relevant features used to classify the mutations:
        * Oncogene vs TSG
        * Consequence type (synonymous, missense, inframe indel or truncating)
        * Position within the transcript
        * If it falls in a mutation hotspot or cluster
        * Predicted functional impact
        * Frequency within the human population
        * If it occurs in a domain of the protein that is depleted of germline variants  
    * Using a set of heuristic rules. Compared the performance obtained with a machine-learning approach: random forest with 1,000 estimators trained in a ten fold cross-validation with 70% of the features in order to predict the remaining 30%. Both the machine-learning and the heuristic approach exhibited similar performace, therefore decided to use the heuristic rules.
    * Analyzed cohorts of tumors (6,792 samples across 28 cancer types) and samples from healthy donors (60,706 unrelated individuals).
    * Performance in the task of classifying driver and passenger mutations assessed using the Catalog of Validated Oncogenic Mutations ($n = 5314$) and a collected set of neutral PAMS affecting cancer gene ($n = 1676$): 86% accuracy.



## Precision Medicine Knowledgebase
| Database name                                                         | Variants | Genes | Date     | Public             | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | -------------------------------------------- |
| [Precision Medicine Knowledgebase](#precision-medicine-knowledgebase) | 2168     | 606   | 08/08/18 | :white_check_mark: | https://pmkb.weill.cornell.edu               |

**Article:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5391733/) Huang L, Fernandes H, Zia H, et al. The cancer precision medicine knowledge base for structured clinical-grade mutations and interpretations. Journal of the American Medical Informatics Association : JAMIA. 2017;24(3):513-519. doi:10.1093/jamia/ocw148.  
**Publication date:** October 2016    

*Pierre - "It's a more controlled CIViC."*

* **What is it?** Interactive online application for collaborative editing, maintenance, and sharing of structured clinical-grade cancer mutations interpretations.
* **Where does the data comes from?** All interpretations written or approved by board-certificate molecular pathologists (PMKB's employees). All interpretations must be supported by at least 1 litterature citation
* **Size of the database?**
    * October 2016, from the article: 457 variants descriptions with 281 clinical-grade interpretations
    * 08/08/18, from the website: 2168 variants for 606 genes
* **Other informations**  
    * Support of all major variant types: small localized mutations (SNV, indels, ...), copy number alterations and gene fusions
    * Distinct user roles including high-level approvers



## MyCancerGenome
| Database name                                                         | Variants | Genes | Date     | Public             | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | -------------------------------------------- |
| [MyCancerGenome](#mycancergenome)                                     | ?        | ?     | -        | :x:                | https://www.mycancergenome.org               |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4121886/) Yeh P, Chen H, Andrews J, Naser R, Pao W, Horn L. DNA-Mutation Inventory to Refine and Enhance Cancer Treatment (DIRECT): A Catalog of Clinically Relevant Cancer Mutations to Enable Genome-Directed Anticancer Therapy. Clinical cancer research : an official journal of the American Association for Cancer Research. 2013;19(7):1894-1901.  doi:10.1158/1078-0432.CCR-12-1894.  
**Publication date:** January 2013  

*Pierre - "It's an old OncoKB."*

* **What is it?** My Cancer Genome is a precision cancer medicine knowledge resource for physicians, patients, caregivers and researchers. It gives information on what mutations make cancers grow and related therapeutic implications, including available clinical trials.
* **Where does the data comes from?** A database (DIRECT: 'DNA-mutation Inventory to Refine and Enhance Cancer Treatment') has been established, it contains information about the potential clinical significance of specific tumor mutations. To compile the information in DIRECT, the PCMI team used a retrospective PubMed medical subject heading (MeSH) search to identify patient-level, mutation-specific, drug response data from different studies in NSCLC. The initial goal of the DIRECT database was to catalogue clinically relevant somatic mutations in lung cancer. The project began by cataloguing data from patients with EGFR mutations but will be expanding to incorporate data on all known mutations with potential clinical significance in various types of cancer.  Not sure if DIRECT is the only database used, the website says "Currently, DIRECT catalogues drug response data from patients with non-small cell lung cancer (NSCLC) whose tumors harbor mutations in EGFR", but maybe the website is not up-to-date. Indeed, we can find other cancer type variants on the website.
* **Size of the database?** Unknown.
* **Other informations**
    * Focused on "patient focus content".



## JAX-Clinical Knowledgebase
| Database name                                                         | Variants | Genes | Date     | Public             | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | -------------------------------------------- |
| [JAX-Clinical Knowledgebase](#jax-clinical-knowledgebase)             | ?        | 82    | 08/08/18 | :x:                | https://ckb.jax.org                          |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pubmed/26772741) Patterson SE, Liu R, Statz CM, Durkin D, Lakshminarayana A, Mockus SM. The clinical trial landscape in oncology and connectivity of somatic mutational profiles to targeted therapies. Human Genomics. 2016;10:4. doi:10.1186/s40246-016-0061-7.  
**Publication date:** January 2016  

*Pierre - "It's an OncoKB with only variants that have a targeted therapy available."*

* **What is it?** Identification and annotation of clinically relevant cancer variants.  
* **Where does the data comes from?** FDA-approved therapy or targeted therapy in clinical trials. Data dynamically curated by experts. In-house databse (the JAX Clinical Knowledgebase JAX-CKB): semi-automated/manually curated database of gene/variant annotations, therapy knowledge, diagnostic/prognostic information, and clinical trials related to oncology.  
* **Size of the database?** January 2016, from the article: 358 genes, 1108 targeted therapies.
* **Other informations**
    * Filtering to ensure the high-quality somatic variations: low coverage, vaf, silent mutations, likely germline, outside of coding regions
    * All types of mutations



## Personalized Cancer Therapy
| Database name                                                         | Variants | Genes | Date     | Public             | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | -------------------------------------------- |
| [Personalized Cancer Therapy](#personalized-cancer-therapy)           | ?        | ?     | -        | :x:                | https://pct.mdanderson.org                   |

**Paper:** [link](http://cancerres.aacrjournals.org/content/77/21/e123.full-text.pdf) Katherine C. Kurnit, Ann M. Bailey, Jia Zeng, Amber M. Johnson, Md. Abu Shufean, Lauren Brusco, Beate C. Litzenburger, Nora S. Sánchez, Yekaterina B. Khotskaya, Vijaykumar Holla, Amy Simpson, Gordon B. Mills, John Mendelsohn, Elmer Bernstam, Kenna Shaw and Funda Meric-Bernstam “Personalized Cancer Therapy”: A Publicly Available Precision Oncology Resource Cancer Res November 1 2017 (77) (21) e123-e126; DOI: 10.1158/0008-5472.CAN-17-0341  
**Publication date:** November 2017  

*Pierre - "Same as JAX-CKB."*

* **What is it?** Information on the function of common genomic alterations and their therapeutic implications. Clinical significance and actionability of genomic alterations and identification of matched targeted therapies.
* **Where does the data comes from?** High-throughput litterature from the MEDLINE database + manually reviewed litterature by a precision oncology decision support (team including oncologists, geneticists, molecular biologists, computational scientists, ...). They validate and record the functional implication in tumorigenesis of each alteration. Genes registered must 1) be cancer-associated, 2) have evidence that targeting the gene may result in tumor suppression, 3) drugs either FDA-approved or clinically investigated. Then a systematic scientific literrature review is performed. Functional annotation of variants: cBIO, COSMIC, published findings.
* **Size of the database?** Unknown.
* **Other informations**
    * Comparison with OncoKB: clinical trials availables



## CanDL
| Database name                                                         | Variants | Genes | Date     | Public             | Website                                      |
| --------------------------------------------------------------------- | -------- | ----- | :------: | :----------------: | -------------------------------------------- |
| [CanDL](#candl)                                                       |          |       |          |                    | https://candl.osu.edu                        |

**Paper:** [link](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4597274/) Damodaran S, Miya J, Kautto E, et al. Cancer Driver Log (CanDL): Catalog of Potentially Actionable Cancer Mutations. The Journal of Molecular Diagnostics : JMD. 2015;17(5):554-559. doi:10.1016/j.jmoldx.2015.05.002.  
**Publication date:** September 2015  

*Pierre - "Bla"*

* **What is it?** Bla
* **Where does the data comes from?** Bla
* **Size of the database?** Bla
* **Other informations**
    * Bla

# First study [Pierre] 

### List of all the notebooks

* **[`first_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/first_analysis.ipynb)**   
First look at the raw data `all_IMPACT_mutations_180508.txt`. This notebook is centered on the analysis of the data feature per feature, and on the different filters applied on the dataset to clean it. The fifth part only will mix different features to study the relation between them.  

* **[`first_analysis_unsolved_issues.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/first_analysis_unsolved_issues.ipynb)**  
List of all the unsolved questions/issues found in the raw data `all_IMPACT_mutations_180508.txt`, this notebook should be read in the context of `first_analysis.ipynb` which periodically refers to it.  

* **[`annotate_cleaned_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/annotate_cleaned_dataset.ipynb)**  
Enrich the cleaned data `cleaned_IMPACT_mutations_180508.txt` by adding some features:
	* `Kaviar_AF`
	* `cosmic_count`
	* `is_a_hotspot`
	* `is_a_3d_hotspot`
	* `oncogenic`
	* `gene_type`
	* `BAM_id`
	* `cancer_code`
	* `cancer_type`

* **[`coding_mutations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/coding_mutations_analysis.ipynb)**  
Further analysis on the cleaned dataset `cleaned_IMPACT_mutations_180508.txt`, enriched with the annotations from the `add_features()` function obtained at the end of [`annotate_cleaned_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/annotate_cleaned_dataset.ipynb). The `synonymous_SNV` are excluded from this study, which only focus on the coding mutations.

* **[`oncokb_annotations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/oncokb_annotations_analysis.ipynb)**  
This notebook studies the OncoKB annotations added with oncokb-annotator (see [`/data/annotate_with_oncokb`](https://github.com/ElsaB/impact-annotator/tree/master/data/annotate_with_oncokb)) and via the [`annotate_cleaned_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/annotate_cleaned_dataset.ipynb) notebook. The `synonymous_SNV` will be removed from the study.  

* **[`comparison_between_variant_annotation_databases.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/comparison_between_variant_annotation_databases.ipynb)** :construction: *work in progress* :construction:  
This notebook is directly linked to [`doc/biblio/variant_annotation_databases.md`](https://github.com/ElsaB/impact-annotator/blob/master/doc/biblio/variant_annotation_databases.md) which compares and describes different variant annotation databases. The aim of this notebook is to compare the annotations of some of the databases studied in the markdown with OncoKB annotations.  

* **[`click_annotvcf_annotations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/click_annotvcf_annotations_analysis.ipynb)** :construction: *work in progress* :construction:    
This notebook studies the annotations added with click_annotvcf, see [`/data/annotate_with_click_annotvcf`](https://github.com/ElsaB/impact-annotator/tree/master/data/annotate_with_click_annotvcf).  


### Details on the notebooks
All notebooks will begin with the following lines, which load a set of custom function designed by us, and setup the R environment by loading the appropriate libraries:
```R
source("../../../src/utils/custom_tools.R")
setup_environment("../../../src/utils")
```
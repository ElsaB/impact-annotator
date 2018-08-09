# Pierre's analysis 

### List of all the notebooks present in this folder:

* **[`first_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/first_analysis.ipynb)**   
First look at the raw data `all_IMPACT_mutations_180508.txt`. This notebook is centered on the analysis of the data feature per feature, and on the different filters applied on the dataset to clean it. The fifth part only will mix different features to study the relation between them.  

* **[`first_analysis_unsolved_issues.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/first_analysis_unsolved_issues.ipynb)**  
List of all the unsolved questions/issues found in the raw data `all_IMPACT_mutations_180508.txt`, this notebook should be read in the context of `first_analysis.ipynb` which periodically refers to it.  
:construction: *work in progress* :construction:

* **[`annotate_cleaned_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/annotate_cleaned_dataset.ipynb)**  
Enrich the cleaned data `cleaned_IMPACT_mutations_180508.txt` by adding some features:
	* `Kaviar_AF`
	* `cosmic_count`
	* `is_a_hotspot`
	* `is_a_3d_hotspot`
	* `oncogenic`
	* `gene_type`

* **[`coding_mutations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/coding_mutations_analysis.ipynb)**  
Further analysis on the cleaned dataset `cleaned_IMPACT_mutations_180508.txt`, enriched with the annotations from the `add_features()` function obtained at the end of [`annotate_cleaned_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/annotate_cleaned_dataset.ipynb). The `synonymous_SNV` are excluded from this study, which only focus on the coding mutations.

* **[`synonymous_mutations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/synonymous_mutations_analysis.ipynb)**  
This study will focus only on the `synonymous_SNV` mutations, trying first to filter the non-somatic synonymous mutations and then to study the reccurent synonymous mutations. This notebook follows the methodology of the [`coding_mutations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/coding_mutations_analysis.ipynb) notebook.  
:construction: *work in progress* :construction:

* **[`oncokb_annotations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/oncokb_annotations_analysis.ipynb)**  
This notebook studies the OncoKB annotations added with oncokb-annotator and via the [`annotate_cleaned_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/annotate_cleaned_dataset.ipynb) notebook.  
:construction: *work in progress* :construction:

* **[`comparison_between_variant_annotation_databases.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/comparison_between_variant_annotation_databases.ipynb)**  
:construction: *work in progress* :construction:


### Details on the notebooks:
All notebooks will begin with the following lines, which load a set of custom function designed by us, and setup the R environment by loading the appropriate libraries:
```R
source("../../../src/utils/custom_tools.R")
setup_environment("../../../src/utils")
```
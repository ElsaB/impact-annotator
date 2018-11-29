# Main results

This markdown gathers the main results from the analysis notebooks.

### Clean the data and various analysis 
:calendar: *13/07/18 - 13/08/18*

**Data cleaning**  
Creation of the `get_cleaned_impact()` function which:

* removes some useless features (unique value features and redundant features)
* filter the rows (keep only the selected mutations consequence, filter the rows according to some read features, correct the `Hugo_Symbol` `Consequence` and `HGVSp_Short` features, ...)
* create some useful feature: `mut_key` (ex: `17_7577515_T_G`), `sample_mut_key` (ex: `P-0000012-T02-IM3_17_7577515_T_G`), `frequency_in_normals` (ex: `0.158`)

**Main interesting values**

* 248,293 mutations (synonymous included, they represent ≈ 20.1% of the dataset)
* 22,990 tumor samples (mean of ≈ 10.8% called mutations per tumor sample)
* 21,252 patients
* 475 genes
* Mean sample coverage: 722

**Adding new features**
Creation of the `add_features()` function which adds the following features to the cleaned dataset: `Kaviar_AF`, `cosmic_count`, `is_a_hotspot`, `is_a_3d_hotspot`, `oncogenic`, `gene_type`, `BAM_id`, `cancer_code`, `cancer_type`.

**General analysis**  
General analysis of the dataset feature per feature, focusing only on the coding mutations or only on the synonymous mutations.

See:

* [`first_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/first_analysis.ipynb)
* [`first_analysis_unsolved_issues.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/first_analysis_unsolved_issues.ipynb)
* [`annotate_cleaned_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/annotate_cleaned_dataset.ipynb)
* [`coding_mutations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/coding_mutations_analysis.ipynb)
* [`synonymous_mutations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/synonymous_mutations_analysis.ipynb)


### Creating the labels
*23/07/18 - 20/08/18*



See:

* [`oncokb_annotations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/oncokb_annotations_analysis.ipynb)
* [`comparison_between_variant_annotation_databases.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/180731_pierre/comparison_between_variant_annotation_databases.ipynb)
* [`variant_annotation_databases.md`](https://github.com/ElsaB/impact-annotator/blob/master/doc/biblio/variant_annotation_databases.md)


### Old
- **180529**

parameters distributions on the coding somatic / non-somatics variants:

	- cd ../analysis/description/180510_elsa
	- make coding

- **180510**

get the raw data with: 

	- cd ../data
	- bash getData.sh your_username_luna
	
first analysis:

	- cd ../analysis/description/180510_elsa
	- make
 
- **180509**

github is up

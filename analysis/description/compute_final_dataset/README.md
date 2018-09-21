# Compute final dataset [Pierre] 

### List of all the notebooks

* **[`click_annotvcf_annotations_analysis.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/compute_final_dataset/click_annotvcf_annotations_analysis.ipynb)**  
This notebook studies the annotations added with click_annotvcf, see [`/data/annotate_with_click_annotvcf`](https://github.com/ElsaB/impact-annotator/tree/master/data/annotate_with_click_annotvcf).  

* **[`get_final_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/compute_final_dataset/get_final_dataset.ipynb)**  
This notebook computes the final dataset used in the next part from the raw impact. It combines a lot of knowledge from the [`/analysis/description/first_study`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/first_study) folder to filter, clean, curate and annotate the raw dataset. The final annotation kept is the one from VEP. All the operations made are stored in the [`compute_final_dataset.R`](https://github.com/ElsaB/impact-annotator/blob/master/data/utils/compute_final_dataset.R) file, and can be applied on the raw dataset by using the `get_final_dataset()` function.

* **[`annotate_final_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/compute_final_dataset/annotate_final_dataset.ipynb)**  
This notebook annotates the final dataset obtained at the end of [`get_final_dataset.ipynb`](https://github.com/ElsaB/impact-annotator/blob/master/analysis/description/compute_final_dataset/get_final_dataset.ipynb), by adding some features. All the operations made are stored in the [`compute_final_dataset.R`](https://github.com/ElsaB/impact-annotator/blob/master/data/utils/compute_final_dataset.R) file, and can be applied on the raw dataset by using the `annotate_final_dataset()` function.
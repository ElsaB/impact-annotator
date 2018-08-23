:construction: *work in progress* :construction:  

# Annotate the mutations with the click_annotvcf pipeline

To annotate the raw dataset `all_IMPACT_mutations_180508.txt` with the [click_annotvcf](https://github.com/leukgen/click_annotvcf/tree/add-normals) pipeline run **in the cluster**:
```shell
!! $ bsub -I -We 20 -R select[internet] "bash annotate_with_oncokb_annotator.sh"
```

The output file `click_annotvcf_IMPACT_mutations_180508.txt` is the annotated version.

The CPU time on the cluster was !! (≈ !! minutes).

***

### Details

We use [click_annotvcf](https://github.com/leukgen/click_annotvcf/tree/add-normals) to annotate the dataset.

The script [`annotate_with_click_annotvcf.sh`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_click_annotvcf/annotate_with_click_annotvcf.sh) does the following:

* Create a `.vcf` file from the raw data by calling [`convert_to_vcf.py`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_click_annotvcf/convert_to_vcf.py)

* Activate the python `staging3.6` environment. This virtualenv will be deactivated at the end of the script.

* Run click_annotvcf.

* Do some cleaning (remove temporary files)
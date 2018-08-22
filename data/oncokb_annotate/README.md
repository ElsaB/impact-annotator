# Annotate the mutations with oncokb-annotator

To annotate the cleaned dataset `cleaned_IMPACT_mutations_180508.txt` with the oncokb annotations from [oncokb-annotator](https://github.com/oncokb/oncokb-annotator) run **in the cluster**:
```shell
$ bsub -I -We 20 -R select[internet] "bash annotate_with_oncokb_annotator.sh"
```

The output file `oncokb_annotated_cleaned_IMPACT_mutations_180508.txt` is the annotated version.

The CPU time on the cluster was 495.6 seconds (≈ 8 minutes).

***

### Details

We use [oncokb-annotator](https://github.com/oncokb/oncokb-annotator) to annotate the dataset.

The script [`annotate_with_oncokb_annotator.sh`](https://github.com/ElsaB/impact-annotator/blob/master/data/oncokb/annotate_with_oncokb_annotator.sh) does the following:

* Clone the repository at https://github.com/oncokb/oncokb-annotator:
```bash
git clone https://github.com/oncokb/oncokb-annotator.git
```

* Call [`prepare_for_annotation.R`](https://github.com/ElsaB/impact-annotator/blob/master/data/oncokb/prepare_for_annotation.R) which does some minor changes on the dataset. Indeed oncokb-annotator needs a `Variant_Classification` feature, which can be computed from the `Consequence` feature as follow:

| Consequence               | Variant_Classification |
| ------------------------- | ---------------------- |
| stopgain_SNV 				| Nonsense_Mutation		 |
| splicing 					| Splice_Site			 |
| nonsynonymous_SNV 		| Missense_Mutation		 |
| nonframeshift_insertion 	| In_Frame_Ins			 |
| nonframeshift_deletion 	| In_Frame_Del			 |
| frameshift_insertion 		| Frame_Shift_Ins		 |
| frameshift_deletion 		| Frame_Shift_Del		 |
| synonymous_SNV 			| Silent				 |	

* Create a python2.7 virtualenv named `oncokb-annotator-env` and install matplotlib (needed by oncokb-annotator). This virtualenv will be removed at the end of the script:
```bash
mkvirtualenv --python=python2.7 oncokb-annotator_env
pip install matplotlib

# ... further

deactivate
rmvirtualenv oncokb-annotator_env
```

* Run oncokb-annotator.

* Do some cleaning (remove temporary file and the oncokb-annotator repository)
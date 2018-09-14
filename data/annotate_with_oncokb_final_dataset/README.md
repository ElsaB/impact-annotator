# Annotate the mutations with oncokb-annotator

:warning: This folder is a slightly modfied version of [`annotate_with_oncokb_annotator`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_oncokb/), but applied on the final dataset rather than on the clean dataset. Please follow the link to read the associated `README.md`.

The modifications made to the original version are listed under:

* The output file is not `oncokb_annotated_cleaned_IMPACT_mutations_180508` but `oncokb_annotated_final_IMPACT_mutations_180508`.
* The script [`prepare_for_annotation.R`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_oncokb_final_dataset/prepare_for_annotation.R) uses the following conversion table:

| Consequence               | Variant_Classification |
| ------------------------- | ---------------------- |
| missense_variant 			| Missense_Mutation		 |
| frameshift_variant 		| ?			             |
| stop_gained 		        | Nonsense_Mutation		 |
| splice_acceptor_variant   | Splice_Site            |
| inframe_deletion 	        | In_Frame_Del			 |
| splice_donor_variant 	    | Splice_Site			 |
| inframe_insertion 		| In_Frame_Ins		     |
| start_lost 		        | Start_Codon_Del		 |
| stop_lost 			    | Nonstop_Mutation		 |	

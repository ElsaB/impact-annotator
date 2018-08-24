:construction: *work in progress* :construction:  

# Annotate the mutations with the click_annotvcf pipeline

To annotate the raw dataset `all_IMPACT_mutations_180508.txt` with the [click_annotvcf](https://github.com/leukgen/click_annotvcf/tree/add-normals) pipeline run **in the cluster**:
```shell
$ bsub -M 64 -o job_output.txt "bash annotate_with_click_annotvcf.sh"
```

The output files are:
* `click_annotvcf_IMPACT_mutations_180508.txt.gz`, the annotated version.
* `all_IMPACT_mutations_180508.vcf`, the `.vcf` file after conversion
* `job_output.txt` the output of the job

It can happen that click_annotvcf crashes at the "Running filter_noncoding..." part, at this point of the script we already have the output file we are looking for though, so it is not a real matter.

You can use the following to unzip `click_annotvcf_IMPACT_mutations_180508.txt.gz`:
```shell
$ gzip -d click_annotvcf_IMPACT_mutations_180508.txt.gz
```

The CPU time on the cluster was 21278s (≈ 6 hours).

***

### Details

We use [click_annotvcf](https://github.com/leukgen/click_annotvcf/tree/add-normals) to annotate the dataset.

The script [`annotate_with_click_annotvcf.sh`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_click_annotvcf/annotate_with_click_annotvcf.sh) does the following:

* Create a `.vcf` file from the raw data by calling [`convert_impact_to_vcf.py`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_click_annotvcf/convert_impact_to_vcf.py)
```bash
INPUT_FILE="../all_IMPACT_mutations_180508.txt"
OUTPUT_VCF="temp/all_IMPACT_mutations_180508.vcf"

python3 convert_impact_to_vcf.py $INPUT_FILE $OUTPUT_VCF

sed -i '1s/^/##fileformat=VCFv4.2\n/' $OUTPUT_VCF
sed -i '2s/^/#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n/' $OUTPUT_VCF
```

* Activate the python `staging3.6` environment. This virtualenv will be deactivated at the end of the script.

* Run `click_annotvcf annotvcf`.
```bash
click_annotvcf annotvcf \
--input_vcf $OUTPUT_VCF.gz \
--outdir temp \
--output_prefix annotvcf \
--assembly GRCH37D5 \
--reference /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta \
--vagrent /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/vagrent/Homo_sapiens_KnC.GRCh37.75.vagrent.cache.gz \
--vep-dir /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/vep/cache/ \
--ensembl-version 91 \
--custom /ifs/work/leukgen/home/leukbot/tests/vep/gnomad_genomes/gnomad.genomes.r2.0.1.sites.noVEP.vcf.gz gnomAD_genome AC_AFR,AC_AMR,AC_ASJ,AC_EAS,AC_FIN,AC_NFE,AC_OTH,AC_Male,AC_Female,AN_AFR,AN_AMR,AN_ASJ,AN_EAS,AN_FIN,AN_NFE,AN_OTH,AN_Male,AN_Female,AF_AFR,AF_AMR,AF_ASJ,AF_EAS,AF_FIN,AF_NFE,AF_OTH,AF_Male,AF_Female,Hom_HomR,Hom_AMR,Hom_ASJ,Hom_EAS,Hom_FIN,Hom_NFE,Hom_OTH,Hom_Male,Hom_Female \
--custom /ifs/work/leukgen/home/leukbot/tests/vep/gnomad_exomes/gnomad.exomes.r2.0.1.sites.noVEP.vcf.gz gnomAD_exome AC_AFR,AC_AMR,AC_ASJ,AC_EAS,AC_FIN,AC_NFE,AC_OTH,AC_Male,AC_Female,AN_AFR,AN_AMR,AN_ASJ,AN_EAS,AN_FIN,AN_NFE,AN_OTH,AN_Male,AN_Female,AF_AFR,AF_AMR,AF_ASJ,AF_EAS,AF_FIN,AF_NFE,AF_OTH,AF_Male,AF_Female,Hom_HomR,Hom_AMR,Hom_ASJ,Hom_EAS,Hom_FIN,Hom_NFE,Hom_OTH,Hom_Male,Hom_Female \
--custom /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81/CosmicMergedVariants.vcf.gz COSMIC GENE,STRAND,CDS,AA,CNT,SNP \
--cosmic /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81
```

* Do some cleaning (remove temporary files).

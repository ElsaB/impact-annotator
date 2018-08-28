# Annotate the mutations with the click_annotvcf pipeline

To annotate the raw dataset `all_IMPACT_mutations_180508.txt` with the [click_annotvcf](https://github.com/leukgen/click_annotvcf/tree/add-normals) pipeline run **in the cluster**:
```shell
$ bsub -M 8 -o job_output.txt "bash annotate_with_click_annotvcf.sh"
```

The output files are:
* `click_annotvcf_IMPACT_mutations_180508.txt`, the annotated version.
* `all_IMPACT_mutations_180508.vcf`, the `.vcf` file after conversion
* `job_output.txt` the output of the job

The CPU time on the cluster was 21278s (≈ 6 hours).

***

### Details

We use [click_annotvcf](https://github.com/leukgen/click_annotvcf/tree/add-normals) to annotate the dataset. The script [`annotate_with_click_annotvcf.sh`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_click_annotvcf/annotate_with_click_annotvcf.sh) does the following:

* Create a `.vcf` file from the raw data by calling [`convert_impact_to_vcf.py`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_click_annotvcf/convert_impact_to_vcf.py)
```bash
INPUT_FILE="../all_IMPACT_mutations_180508.txt"
OUTPUT_VCF="temp/all_IMPACT_mutations_180508.vcf"

python3 convert_impact_to_vcf.py $INPUT_FILE $OUTPUT_VCF

sed -i '1s/^/##fileformat=VCFv4.2\n/' $OUTPUT_VCF
sed -i '2s/^/#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\n/' $OUTPUT_VCF
```
The script [`convert_impact_to_vcf.py`](https://github.com/ElsaB/impact-annotator/blob/master/data/annotate_with_click_annotvcf/convert_impact_to_vcf.py) does the following:
	* Load impact from the given input file and create vcf-like columns
	* Modify INS and DEL mutations to match VCF format (eg : -/A ⟹ T/TA and A/- ⟹ TA/T)
	* Remove duplicated rows
	* Save the `.vcf` impact as the given output file

<sup> * </sup> See in next section why we chose to create the `.vcf` by hand instead of using [vcf2maf](https://github.com/mskcc/vcf2maf).

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
#--cosmic /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81
```
The cosmic annotations were removed from the call to click_annotvcf as it made the file grow from ≈ 500 MB to 44 GB.

* Do some cleaning (remove temporary files).

### Use of vcf2maf
To convert our dataset to `.vcf` we also tried to use [vcf2maf](https://github.com/mskcc/vcf2maf), which contains a maf2vcf function. However, we faced two problems that lead us to do our own script:

* The resulting `.vcf` was heavy to work on as each mutation is unnecessarily linked to its `Tumor_Sample_Barcode`, thus adding more than 20,000 extra columns to the `.vcf` file (due to our ≈20,000 `Tumor_Sample_Barcode` in impact).
* The processing to create the `.vcf` file was way longer.

See the script used to clone the vcf2maf repo and apply `maf2vcf.pl` on impact:

```bash
GREEN='\033[0;32m'
NC='\033[0m' # no color

mkdir temp

INPUT_FILE="../all_IMPACT_mutations_180508.txt"
OUTPUT_VCF="temp/all_IMPACT_mutations_180508.vcf"

printf "\n${GREEN}-> Get the vcf2maf repo...${NC}\n"
export VCF2MAF_URL=`curl -sL https://api.github.com/repos/mskcc/vcf2maf/releases | grep -m1 tarball_url | cut -d\" -f4`
curl -L -o temp/mskcc-vcf2maf.tar.gz $VCF2MAF_URL
tar -zxf temp/mskcc-vcf2maf.tar.gz --directory temp

printf "\n${GREEN}-> Convert .txt to .vcf...${NC}\n"
perl temp/mskcc-vcf2maf-decbf60/maf2vcf.pl --input-maf $INPUT_FILE --output-dir temp --ref-fasta /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta

cp $OUTPUT_VCF .
```


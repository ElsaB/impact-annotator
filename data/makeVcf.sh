#!/bin/bash

#BSUB -J "annotate"
#BSUB -We 141
#BSUB -n 1
#BSUB -M 64
#BSUB -e /home/glodzikd/code/impact-annotator/data/annot.error.%I.%J
#BSUB -o /home/glodzikd/code/impact-annotator/data/annot.out.%I.%J

# make a VCF file
INPUT_FILE="all_IMPACT_mutations_180508.txt"
OUTPUT_VCF="all_IMPACT_mutations_180508.vcf"

echo "##fileformat=VCFv4.2" > $OUTPUT_VCF
echo -e "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT" >> $OUTPUT_VCF
cat "$INPUT_FILE" | grep -v "##" | awk  'BEGIN{OFS="\t";FS="\t"}NR>1{
	print $5,$6,".", $12,$13,".", ".", ".", "."}' >> "$OUTPUT_VCF"

gzip "$OUTPUT_VCF"


#java -jar GenomeAnalysisTK.jar \
#   -T ValidateVariants \
#   -R reference.fasta \
#   -V "$OUTPUT_VCF" \

/ifs/work/leukgen/bin/python/.virtualenvs/users/zhouy1/leuktools/bin/click_annotvcf annotvcf     --input_vcf /home/glodzikd/code/impact-annotator/data/all_IMPACT_mutations_180508.vcf.gz     --outdir /home/glodzikd/code/impact-annotator/data/juanes/     --output_prefix annotvcf     --assembly GRCH37D5     --reference /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta     --vagrent /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/vagrent/Homo_sapiens_KnC.GRCh37.75.vagrent.cache.gz     --custom /ifs/work/leukgen/home/leukbot/tests/vep/gnomad_genomes/gnomad.genomes.r2.0.1.sites.noVEP.vcf.gz gnomAD_genome AC_AFR,AC_AMR,AC_ASJ,AC_EAS,AC_FIN,AC_NFE,AC_OTH,AC_Male,AC_Female,AN_AFR,AN_AMR,AN_ASJ,AN_EAS,AN_FIN,AN_NFE,AN_OTH,AN_Male,AN_Female,AF_AFR,AF_AMR,AF_ASJ,AF_EAS,AF_FIN,AF_NFE,AF_OTH,AF_Male,AF_Female,Hom_HomR,Hom_AMR,Hom_ASJ,Hom_EAS,Hom_FIN,Hom_NFE,Hom_OTH,Hom_Male,Hom_Female     --custom /ifs/work/leukgen/home/leukbot/tests/vep/gnomad_exomes/gnomad.exomes.r2.0.1.sites.noVEP.vcf.gz gnomAD_exome AC_AFR,AC_AMR,AC_ASJ,AC_EAS,AC_FIN,AC_NFE,AC_OTH,AC_Male,AC_Female,AN_AFR,AN_AMR,AN_ASJ,AN_EAS,AN_FIN,AN_NFE,AN_OTH,AN_Male,AN_Female,AF_AFR,AF_AMR,AF_ASJ,AF_EAS,AF_FIN,AF_NFE,AF_OTH,AF_Male,AF_Female,Hom_HomR,Hom_AMR,Hom_ASJ,Hom_EAS,Hom_FIN,Hom_NFE,Hom_OTH,Hom_Male,Hom_Female     --custom /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81/CosmicMergedVariants.vcf.gz COSMIC GENE,STRAND,CDS,AA,CNT,SNP     --cosmic /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/81     --bedfile /ifs/work/leukgen/ref/bedfiles/IMPACT-468.bed

# convert to Annovar format

INPUT_FILE="all_IMPACT_mutations_180508.txt"
OUTPUT_FILE="all_IMPACT_mutations_180508.simple"
cat "$INPUT_FILE" | grep -v "##" | awk  'BEGIN{OFS="\t";FS="\t"}NR>1{
	print $5,$6,$6+length($12)-1,$12,$13;}' > "$OUTPUT_FILE"
	
	
~/software/annovar/annotate_variation.pl -downdb -webfrom annovar -buildver hg19 dbnsfp30a humandb/	
~/software/annovar/annotate_variation.pl -downdb -webfrom annovar -buildver hg19 1000g2015aug humandb/	
~/software/annovar/annotate_variation.pl -downdb -webfrom annovar -buildver hg19 kaviar_20150923 humandb/	
~/software/annovar/annotate_variation.pl -downdb -webfrom annovar -buildver hg19 cosmic70 humandb/	
~/software/annovar/annotate_variation.pl -downdb -webfrom annovar -buildver hg19 icgc21 humandb/	

table_annovar.pl ex1.avinput humandb/ -protocol dbnsfp30a -operation f -build hg19 -nastring .

db=~/software/annovar/humandb

~/software/annovar/table_annovar.pl \
"$OUTPUT_FILE" \
"$db" \
-buildver hg19 \
-nastring . \
-protocol dbnsfp30a,1000g2015aug_all,kaviar_20150923,cosmic70 \
-operation f,f,f,f \
-remove	    
  

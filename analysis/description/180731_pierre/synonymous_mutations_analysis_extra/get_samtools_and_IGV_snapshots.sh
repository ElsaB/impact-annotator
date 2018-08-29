#!/bin/bash

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m' # no Color

while IFS= read line
do
	printf "\n${GREEN}-> /$line${NC}\n"

	cd $line

	
	printf "${BLUE}Get .sam with samtools...${NC}\n"

	mkdir -p samtools

	while IFS= read line
	do
		IFS=$'\t' read -r -a array <<< "$line"

		INPUT_BAM="${array[0]}"
		chr="${array[1]}"
		pos="${array[2]}"

		OUTPUT_SAM=samtools/${INPUT_BAM##*/}
		OUTPUT_SAM=${OUTPUT_SAM%.*}.sam
		pos1=$((pos-50))
		pos2=$((pos+50))

		printf "$INPUT_BAM $chr $pos -> $OUTPUT_SAM ..."

		samtools view -h $INPUT_BAM $chr:$pos1-$pos2 -o $OUTPUT_SAM

		printf " done\n"

	done < "list_BAM.tsv"

	mkdir -p snaps

	printf "${BLUE}Get IGV snapshots with toil_snapigv...${NC}\n"

	toil_snapigv \
		jobstore \
		--writeLogs snaps/logs_toil \
		--logFile snaps/head_job.toil \
		--setEnv TOIL_LSF_JOBNAME='IGVBATCH' \
		--outdir snaps \
		--list list_BAM.tsv \
		--window 50 \
		--genome /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/igv/gr37offline.genome \
		--igv_jar /ifs/work/leukgen/opt/igv/batch_runner_patch/igv.jar \
		--igv_hw

	cd ..

done < "mut_key_dir_name.tsv"







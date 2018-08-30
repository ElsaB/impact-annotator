#!/bin/bash

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # no Color


# for each line in "mut_key_dir_name.tsv" (each mutation key folder)
while IFS= read line
do
	printf "\n${GREEN}-> /$line${NC}\n"

	# go to the folder
	cd $line

	printf "${BLUE}Get .sam with samtools...${NC}\n"

	# create the .sam in /samtools by iterating through "list_BAM.tsv" to get the BAM id path, chromosome and position, and calling each time samtools
	mkdir -p samtools

	while IFS= read line
	do
		IFS=$'\t' read -r -a array <<< "$line"

		INPUT_BAM="${array[0]}"
		chr="${array[1]}"
		pos="${array[2]}"

		INPUT_BAM_FILE_NAME=${INPUT_BAM##*/} # remove the path name

		# if the file doesn't exist in /ifs/dmpshare/share/irb12_245/, we skip the samtools and don't copy it in corrected_list_BAM.tsv, the input of toil_snapigv
		if (grep -q $INPUT_BAM_FILE_NAME ../list_irb12_245.txt)
		then
			echo "$line" >> corrected_list_BAM.tsv
		else
			printf "${RED}${INPUT_BAM_FILE_NAME} removed from corrected_list_BAM.tsv${NC}\n"
			continue
		fi

		OUTPUT_SAM=samtools/${INPUT_BAM_FILE_NAME%.*}.sam 	 # change the file descriptor to .sam
		pos1=$((pos-50))
		pos2=$((pos+50))

		printf "$INPUT_BAM $chr $pos -> $OUTPUT_SAM ..."

		samtools view -h $INPUT_BAM $chr:$pos1-$pos2 -o $OUTPUT_SAM

		printf " done\n"

	done < "list_BAM.tsv"

	# create the IGV snapchots in /snaps, by giving "list_BAM.tsv" to toil_snapigv
	mkdir -p snaps

	printf "${BLUE}Get IGV snapshots with toil_snapigv...${NC}\n"

	toil_snapigv \
		jobstore \
		--writeLogs snaps/logs_toil \
		--logFile snaps/head_job.toil \
		--setEnv TOIL_LSF_JOBNAME='IGVBATCH' \
		--outdir snaps \
		--list corrected_list_BAM.tsv \
		--window 50 \
		--genome /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/igv/gr37offline.genome \
		--igv_jar /ifs/work/leukgen/opt/igv/batch_runner_patch/igv.jar \
		--igv_hw

	cd ..

done < "mut_key_dir_name.tsv"

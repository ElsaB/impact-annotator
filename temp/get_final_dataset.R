data_path <- "../data"



source("../src/utils/custom_tools.R")
setup_environment("../src/utils")


id_colnames  <- c("ID_VARIANT",
                  "CHR",
                  "START",
                  "END",
                  "REF",
                  "ALT")

vag_colnames <- c("VAG_VT",
                  "VAG_GENE",
                  "VAG_cDNA_CHANGE",
                  "VAG_PROTEIN_CHANGE",
                  "VAG_EFFECT")

vep_colnames <- c("VEP_Consequence",
                  "VEP_SYMBOL",
                  "VEP_HGVSc",
                  "VEP_HGVSp",
                  "VEP_Amino_acids", 
                  "VEP_VARIANT_CLASS",
                  "VEP_BIOTYPE")

vep_add_colnames <- c("VEP_IMPACT",
                      "VEP_CLIN_SIG",
                       "VEP_AF", 
                       "VEP_MAX_AF", 
                       "VEP_MAX_AF_POPS", 
                       "VEP_gnomAD_AF",
                       "VEP_SIFT", 
                       "VEP_PolyPhen", 
                       "VEP_COSMIC_CNT")


get_impact_annotated <- function() {
    impact_annotated <- read.table(paste0(data_path, "/annotate_with_click_annotvcf/click_annotvcf_IMPACT_mutations_180508.txt"),
                                   sep = "\t", stringsAsFactors = FALSE, header = TRUE, comment = "#")

    impact_annotated <- impact_annotated[, c(id_colnames, vag_colnames, vep_colnames, vep_add_colnames)]

    impact_vcf <- read.table(paste0(data_path, "/annotate_with_click_annotvcf/all_IMPACT_mutations_180508.vcf"),
                             sep = "\t", stringsAsFactors = FALSE, header = FALSE, comment = "#")
    colnames(impact_vcf) <- c("CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO", "FORMAT")

    impact_vcf$OLD_REF <- sapply(impact_vcf$INFO, function(x) strsplit(strsplit(x, '=')[[1]][2], '/')[[1]][1])
    impact_vcf$OLD_ALT <- sapply(impact_vcf$INFO, function(x) strsplit(strsplit(x, '=')[[1]][2], '/')[[1]][2])
    impact_vcf$OLD_POS <- sapply(impact_vcf$INFO, function(x) strsplit(strsplit(x, '=')[[1]][2], '/')[[1]][3])

    impact_vcf$join_key <- paste(impact_vcf$CHROM, impact_vcf$POS, impact_vcf$REF, impact_vcf$ALT, sep = '_')

    impact_vcf <- unique(impact_vcf)
    impact_annotated <- unique(impact_annotated)


    impact_annotated <- left_join(impact_annotated,
                                  impact_vcf[, c("join_key", "OLD_REF", "OLD_ALT", "OLD_POS")],
                                  by = c("ID_VARIANT" = "join_key"))

    return (impact_annotated)
}


add_click_annotvcf_annotations <- function(impact, impact_annotated) {
    impact_annotated$join_key <- paste(impact_annotated$CHR,
                                       impact_annotated$OLD_POS,
                                       impact_annotated$OLD_REF,
                                       impact_annotated$OLD_ALT,
                                       sep = '_')

    impact$mut_key <- paste(impact$Chromosome,
                        impact$Start_Position,
                        impact$Reference_Allele,
                        impact$Tumor_Seq_Allele2,
                        sep = '_')

    impact_annotated <- unique(impact_annotated)

    colnames_to_keep <- c(vag_colnames, vep_colnames, vep_add_colnames)

    impact[, colnames_to_keep] <- left_join(impact, impact_annotated,
                                            by = c("mut_key" = "join_key"))[, c(vag_colnames,
                                                                                vep_colnames,
                                                                                vep_add_colnames)]

    return (impact)
}


filter_impact <- function(impact) {
    # [-7 features] remove the unique-value features
    impact[, c("Entrez_Gene_Id",
               "Center",
               "NCBI_Build",
               "Strand",
               "dbSNP_RS",
               "Matched_Norm_Sample_Barcode",
               "variant_status")] <- list(NULL)
    # [-3 features] remove the redundant features
    impact[, c("Match_Norm_Seq_Allele1", "Match_Norm_Seq_Allele2", "Tumor_Seq_Allele1")] <- list(NULL)


    # [~ every rows] select only the most deleterious VEP consequence
    impact$VEP_Consequence <- sapply(impact$VEP_Consequence, function(x) strsplit(x, '&')[[1]][1])
    # [-375,418 rows] remove the non-interesting VEP_Consequence mutations
    impact <- impact[impact$VEP_Consequence %in% c("missense_variant",
                                                   "frameshift_variant",
                                                   "stop_gained",
                                                   "splice_acceptor_variant",
                                                   "inframe_deletion",
                                                   "splice_donor_variant",
                                                   "inframe_insertion",
                                                   "start_lost",
                                                   "stop_lost"),]


    # [-5,496 rows] remove rows having `confidence_class = UNKNOWN` or `confidence_class = OK_NOT_SO`
    impact <- impact[! impact$confidence_class %in% c("UNKNOWN", "OK_NOT_SO"),]


    # [-9,156 rows] remove the contaminated rows minor_contamination > 0.01
    impact <- impact[impact$minor_contamination <= 0.01,]
    # [-1 feature] remove the minor_contamination feature
    impact["minor_contamination"] <- NULL


    # [-311 rows] remove rows having n_depth < 20
    impact <- impact[impact$n_depth >= 20,]


    # [-44 rows] remove the rows having t_alt_plus_count + t_alt_neg_count != t_alt_count
    impact <- impact[impact$t_alt_plus_count + impact$t_alt_neg_count == impact$t_alt_count,]


    # [+1 feature] create a sample mutation key feature to idenfity unique rows
    impact$sample_mut_key <- paste(impact$Tumor_Sample_Barcode, impact$mut_key, sep = '_')
    # [+1 feature] create a patient key feature to idenfity unique patient
    impact$patient_key <- substr(impact$Tumor_Sample_Barcode, 1, 9)


    # [~5696 rows] modify wrong/synonymous Hugo_Symbol
    old_Hugo_Symbol = c('MLL3', 'PAK7', 'RFWD2', 'MYCL1', 'MLL2', 'MLL', 'FAM46C', 'MRE11A', 'PARK2', 'FAM175A',
                        'TCEB1', 'WHSC1', 'WHSC1L1', 'FAM58A', 'SETD8', 'MLL4')
    new_Hugo_Symbol = c('KMT2C', 'PAK5', 'COP1', 'MYCL', 'KMT2D', 'KMT2A', 'TENT5C', 'MRE11', 'PRKN', 'ABRAXAS1',
                        'ELOC', 'NSD2', 'NSD3', 'CCNQ', 'KMT5A', 'KMT2B')
    has_old_symbol <- which(impact$Hugo_Symbol %in% old_Hugo_Symbol)
    impact$Hugo_Symbol[has_old_symbol] <- new_Hugo_Symbol[match(impact$Hugo_Symbol[has_old_symbol], old_Hugo_Symbol)]

    # [~1270 rows] Hugo_Symbol = CDKN2Ap16INK4A -> CDKN2A
    impact$Hugo_Symbol[impact$Hugo_Symbol == "CDKN2Ap16INK4A"] <- "CDKN2A"

    # [-713 rows] Hugo_Symbol = CDKN2Ap14ARF and CDKN2A in the tumor sample
    dd <- impact %>% group_by(Tumor_Sample_Barcode) %>%
                     summarise(has_both_reading_frame = sum(Hugo_Symbol == "CDKN2Ap14ARF") > 0 &
                                                          sum(Hugo_Symbol == "CDKN2A") > 0) %>%
                     filter(has_both_reading_frame)
    impact <- impact[! (impact$Hugo_Symbol == "CDKN2Ap14ARF" &
                        impact$Tumor_Sample_Barcode %in% dd$Tumor_Sample_Barcode),]


    # [-48 rows] duplicated mutation for the same sample_mut_key
    impact_redundant_to_delete <- impact %>% group_by(sample_mut_key) %>%
                                             filter(n() >= 2) %>%
                                             filter(t_depth == min(t_depth)) %>%
                                             filter(t_vaf == min(t_vaf))
    impact <- impact[! (impact$sample_mut_key %in% impact_redundant_to_delete$sample_mut_key &
                        impact$t_depth %in% impact_redundant_to_delete$t_depth &
                        impact$t_vaf %in% impact_redundant_to_delete$t_vaf),]

    return (impact)
}


print("Get raw impact...")
impact <- read.table(paste0(data_path, "/all_IMPACT_mutations_180508.txt"),
                     sep = "\t", stringsAsFactors = FALSE, header = TRUE)

print("Get impact_annotated (impact annotated with click_annotvcf)...")
impact_annotated <- get_impact_annotated()

print("Join impact and impact_annotated...")
impact <- add_click_annotvcf_annotations(impact, impact_annotated)

print("Filter impact...")
impact <- filter_impact(impact)
print(nrow(impact))



#write.table(impact_cleaned, "./cleaned_IMPACT_mutations_180508.txt", sep = "\t", row.names = FALSE)





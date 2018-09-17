impact <- read.table("../final_IMPACT_mutations_180508.txt",
					 sep = "\t", stringsAsFactors = FALSE, header = TRUE)


impact <- impact[,c("mut_key", "VEP_SYMBOL", "VEP_Consequence", "VEP_HGVSp")]

colnames(impact) <- c("mut_key", "Hugo_Symbol", "VEP_Consequence", "HGVSp_Short")


selected_mutation_types = c("missense_variant",
                            "frameshift_variant",
                            "stop_gained",
                            "splice_acceptor_variant",
                            "inframe_deletion",
                            "splice_donor_variant",
                            "inframe_insertion",
                            "start_lost",
                            "stop_lost")

get_variant_classification <- function(Consequence) {
    Variant_Classification = c("Missense_Mutation", 
                               "In_Frame_Ins", # ?
                               "Nonsense_Mutation",
                               "Splice_Site",
                               "In_Frame_Del",
                               "Splice_Site",
                               "In_Frame_Ins",
                               "Start_Codon_Del",
                               "Nonstop_Mutation")
    
    return (Variant_Classification[match(Consequence, selected_mutation_types)])
}

impact$Variant_Classification <- sapply(impact$VEP_Consequence, get_variant_classification)

impact <- unique(impact)

write.table(impact, "./ready_to_annotate_final_IMPACT_mutations_180508.txt", sep = "\t", row.names = FALSE)

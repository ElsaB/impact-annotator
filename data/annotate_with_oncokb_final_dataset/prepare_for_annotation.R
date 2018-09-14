impact <- read.table("../final_IMPACT_mutations_180508.txt",
					 sep = "\t", stringsAsFactors = FALSE, header = TRUE)

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
                               "?",
                               "Nonsense_Mutation",
                               "Splice_Site",
                               "In_Frame_Del",
                               "Splice_Site",
                               "In_Frame_Ins",
                               "Start_Codon_Del",
                               "Nonstop_Mutation")
    
    return (Variant_Classification[match(Consequence, selected_mutation_types)])
}

impact$Variant_Classification <- sapply(impact$Consequence, get_variant_classification)

write.table(impact, "./ready_to_annotate_final_IMPACT_mutations_180508.txt", sep = "\t", row.names = FALSE)
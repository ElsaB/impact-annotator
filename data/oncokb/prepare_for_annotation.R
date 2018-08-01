impact <- read.table("../cleaned_IMPACT_mutations_180508.txt",
					 sep = "\t", stringsAsFactors = FALSE, header = TRUE, nrows = 10000)

selected_mutation_types = c("stopgain_SNV",
                             "splicing",
                             "nonsynonymous_SNV",
                             "nonframeshift_insertion",
                             "nonframeshift_deletion",
                             "frameshift_insertion",
                             "frameshift_deletion",
                             "synonymous_SNV")

get_variant_classification <- function(Consequence) {
    Variant_Classification = c("Nonsense_Mutation", 
                               "Splice_Site",
                               "Missense_Mutation",
                               "In_Frame_Ins",
                               "In_Frame_Del",
                               "Frame_Shift_Ins",
                               "Frame_Shift_Del",
                               "Silent")
    
    return (Variant_Classification[match(Consequence, selected_mutation_types)])
}

impact$Variant_Classification <- sapply(impact$Consequence, get_variant_classification)

write.table(impact[1:10000,], "./ready_to_annotate_cleaned_IMPACT_mutations_180508.txt", sep = "\t", row.names = FALSE)
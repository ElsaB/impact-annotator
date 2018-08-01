print("beginning importation")

impact <- read.table("../cleaned_IMPACT_mutations_180508.txt",
					 sep = "\t", stringsAsFactors = FALSE, header = TRUE, nrows = 3000)

print("end importation")

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

print("add classification")
impact$Variant_Classification <- sapply(impact$Consequence, get_variant_classification)

print("write modification")
write.table(impact[1:2000,], "./ready_to_annotate_cleaned_IMPACT_mutations_180508.txt", sep = "\t", row.names = FALSE)
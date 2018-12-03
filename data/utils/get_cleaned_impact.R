source("../../utils/R/custom_tools.R")
setup_environment("../../utils/R/")

impact_cleaned <- get_cleaned_impact(".")

write.table(impact_cleaned, "./cleaned_IMPACT_mutations_180508.txt", sep = "\t", row.names = FALSE)
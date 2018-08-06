source("../src/utils/custom_tools.R")
setup_environment("../src/utils")

impact_cleaned <- get_cleaned_impact(".")

write.table(impact_cleaned, "./cleaned_IMPACT_mutations_180508.txt", sep = "\t", row.names = FALSE)
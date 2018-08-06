# Gather the tools in one file
###################################################################################

# setup the environnment by loading the appropriate libraries and scripts
setup_environment <- function(utils_folder_name) {
  source(paste0(utils_folder_name, "/custom_tools_ggplot.R")) # ggplot tools
  source(paste0(utils_folder_name, "/custom_tools_data.R"))   # tools to handle the data

  suppressPackageStartupMessages(library("tidyverse"))
  suppressPackageStartupMessages(library("gridExtra")) # used to plot ggplots side-by-side

  theme_set(theme_minimal())

  options(repr.plot.res = 300) # set a high-definition resolution (DPI)
}
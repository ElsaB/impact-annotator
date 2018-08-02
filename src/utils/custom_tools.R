# To call before using the methods in this file, setup the environnment by loading the appropriate libraries
setup_environment <- function() {
  suppressPackageStartupMessages(library("tidyverse"))
  suppressPackageStartupMessages(library("cowplot")) # used to plot ggplots side-by-side
  theme_set(theme_minimal())

  options(repr.plot.res = 300) # set a high-definition resolution (DPI)
}




# PLOTS
###################################################################################

# Set the size of the plot in the notebook
notebook_plot_size <- function(width = 6, height = 3) {
  options(repr.plot.width = width, repr.plot.height = height)
}


# Plot two plots side-by-side
plot_side_by_side <- function(plot1, plot2, width = 10, height = 2) {
  notebook_plot_size(width, height)

  plot_grid(plot1, plot2, ncol = 2, nrow = 1)
}


# Plot three plots side-by-side
plot_side_by_side_3 <- function(plot1, plot2, plot3, width = 10, height = 3) {
  notebook_plot_size(width, height)

  plot_grid(plot1, plot2, plot3, ncol = 3, nrow = 1)
}


# Sort a categorical feature over the count of the categories it contains (e.g. sort the associated histogram)
sort_histogram <- function(data, feature_name, reverse = FALSE) {

  if (!reverse) {
    data[, feature_name] <- factor(data[, feature_name], levels = names(rev(sort(table(data[, feature_name])))))
  }
  else {
    data[, feature_name] <- factor(data[, feature_name], levels = names(sort(table(data[, feature_name]))))
  }

  return (data)
}


# Plot two histograns side-by-side to study the contingency table between two features
plot_contingency_table_as_histograms <- function(data, feature_x_name, feature_y_name, width = 10, height = 3) {

  data <- sort_histogram(data, feature_x_name)
  data <- sort_histogram(data, feature_y_name, reverse = TRUE)

  plot1 <- ggplot(data) + geom_bar(aes_string(x = feature_x_name, fill = feature_y_name), show.legend = FALSE) +
                          theme(axis.text.x = element_text(angle = 45, hjust = 1))
  plot2 <- ggplot(data) + geom_bar(aes_string(x = feature_x_name, fill = feature_y_name), position = "fill") +
                          theme(axis.text.x = element_text(angle = 45, hjust = 1)) + labs(y = "frequency")

  plot_side_by_side(plot1, plot2, width, height)               
}


# Plots three histograms side-by-side showing the distribution of the features confidence_class,
# Variant_Type and Consequence for the given dataset. Also prints the number of unique genes mutated
# the given dataset
get_possible_correlations <- function(data) {
    print(paste("Number of different genes: ", toString(length(unique(data$Hugo_Symbol)))))
        
    data <- sort_histogram(data, "confidence_class")
    plot1 <- ggplot(data) + geom_bar(aes(confidence_class)) + theme(axis.text.x = element_text(angle = 45, hjust = 1))
    
    data <- sort_histogram(data, "Variant_Type")
    plot2 <- ggplot(data) + geom_bar(aes(Variant_Type))
    
    data <- sort_histogram(data, "Consequence")
    plot3 <- ggplot(data) + geom_bar(aes(Consequence)) + theme(axis.text.x = element_text(angle = 45, hjust = 1))

    plot_side_by_side_3(plot1, plot2, plot3, 10, 3)
}




plot_histogram_top <- function(data, feature_name, number) {

  data_top <- as.data.frame(rev(sort(table(data[,feature_name])))[1:number])
  colnames(data_top) <- c("feature", "count")
  return (ggplot(data_top) + geom_col(aes(feature, count)) + xlab(feature_name))
}




# DATA
###################################################################################


selected_mutation_types <- c("stopgain_SNV",
                             "splicing",
                             "nonsynonymous_SNV",
                             "nonframeshift_insertion",
                             "nonframeshift_deletion",
                             "frameshift_insertion",
                             "frameshift_deletion",
                             "synonymous_SNV")


is_frameshift <- function(Tumor_Seq_Allele2, Reference_Allele) {
    # we nee to add gsub('-', '', ...) because we have '-' instead of '' when there is no base pair to show
    return ((nchar(gsub('-', '', Tumor_Seq_Allele2)) - nchar(gsub('-', '', Reference_Allele))) %% 3 != 0)
}


# Returns a cleaned IMPACT dataset (see notebook first_analysis.ipynb)
# ~ stands for "modify"
get_cleaned_impact <- function(data_folder_name) {

  # [+35 features, +588,547 rows] get the original dataset
  impact <- read.table(paste0(data_folder_name, "/all_IMPACT_mutations_180508.txt"), sep = "\t", stringsAsFactors = FALSE, header = TRUE)


  # [-7 features] remove the unique-value features
  impact[, c("Entrez_Gene_Id",
             "Center",
             "NCBI_Build",
             "Strand",
             "dbSNP_RS",
             "Matched_Norm_Sample_Barcode",
             "variant_status")] <- NULL


  # [-3 features] remove the redundant features
  impact[, c("Match_Norm_Seq_Allele1", "Match_Norm_Seq_Allele2", "Tumor_Seq_Allele1")] <- NULL


  # [-322,796 rows] remove the non-interesting mutations
  impact <- impact[impact$Consequence %in% c("stopgain_SNV",
                                             "splicing",
                                             "nonsynonymous_SNV",
                                             "nonframeshift_insertion",
                                             "nonframeshift_deletion",
                                             "frameshift_insertion",
                                             "frameshift_deletion",
                                             "synonymous_SNV"),]


  # [-12,975 rows] remove the contaminated rows
  impact <- impact[impact$minor_contamination <= 0.01,]
  # [-1 feature] remove the minor_contamination feature
  impact["minor_contamination"] <- NULL


  # [-373 rows] remove the rows having n_depth < 20
  impact <- impact[impact$n_depth >= 20,]


  # [-46 rows] remove the rows having impact$t_alt_plus_count + impact$t_alt_neg_count != impact$t_alt_count
  impact <- impact[impact$t_alt_plus_count + impact$t_alt_neg_count == impact$t_alt_count,]


  # [+1 feature] create a mutation key feature to idenfity unique mutations
  impact$mut_key <- paste(impact$Chromosome,
                        impact$Start_Position,
                        impact$Reference_Allele,
                        impact$Tumor_Seq_Allele2,
                        sep = '_')
  # [+1 feature] create a sample mutation key feature to idenfity unique rows
  impact$sample_mut_key <- paste(impact$Tumor_Sample_Barcode, impact$mut_key, sep = '_')


  # [~7501 rows] replace the wrong Hugo symbols with the good ones
  old_Hugo_Symbol = c('MLL3', 'PAK7', 'RFWD2', 'MYCL1', 'MLL2', 'MLL', 'FAM46C', 'MRE11A', 'PARK2', 'FAM175A',
                      'TCEB1', 'WHSC1', 'WHSC1L1', 'FAM58A', 'SETD8', 'MLL4')
  new_Hugo_Symbol = c('KMT2C', 'PAK5', 'COP1', 'MYCL', 'KMT2D', 'KMT2A', 'TENT5C', 'MRE11', 'PRKN', 'ABRAXAS1',
                      'ELOC', 'NSD2', 'NSD3', 'CCNQ', 'KMT5A', 'KMT2B')
  old_symbols <- which(impact$Hugo_Symbol %in% old_Hugo_Symbol)
  impact$Hugo_Symbol[old_symbols] <- new_Hugo_Symbol[match(impact$Hugo_Symbol[old_symbols], old_Hugo_Symbol)]
  # [~1334 rows] replace "CDKN2Ap16INK4A" by "CDKN2A"
  impact$Hugo_Symbol[impact$Hugo_Symbol == "CDKN2Ap16INK4A"] <- "CDKN2A"
  # [-808 rows] delete the "CDKN2Ap14ARF" already read in the classic read frame (in "CDKN2Ap16INK4A")
  impact <- impact %>% filter(! (Hugo_Symbol == "CDKN2Ap14ARF" & mut_key %in% impact$mut_key[impact$Hugo_Symbol == "CDKN2A"]))


  # [-2979 rows] remove the hypermutated patient
  impact <- impact[impact$Tumor_Sample_Barcode != "P-0025368-T01-IM6",]


  # [-57 rows] remove the duplicated mutations
  impact_redundant <- impact %>% group_by(sample_mut_key) %>% filter(n() >= 2)
  impact_redundant_to_delete <- impact_redundant %>% group_by(sample_mut_key) %>% filter(t_depth == min(t_depth))
  impact_redundant_to_delete <- impact_redundant_to_delete %>% group_by(sample_mut_key) %>% filter(t_vaf == min(t_vaf))
  impact <- impact %>% filter(! (sample_mut_key %in% impact_redundant_to_delete$sample_mut_key &
                                 t_depth %in% impact_redundant_to_delete$t_depth &
                                 t_vaf %in% impact_redundant_to_delete$t_vaf))


  # [~ every rows] replace the occurence_in_normals feature by frequency_in_normals
  impact$occurence_in_normals[impact$occurence_in_normals == '0'] <- "0;0"
  impact$frequency_in_normals <- sapply(impact$occurence_in_normals,
                                        function(s) as.double(strsplit(s, split = ';')[[1]][2]))
  impact$occurence_in_normals <- NULL


  # [~24 rows] set all the `synonymous_SNV` as "UNKNOWN" for consistancy (24 were classified as "UNLIKELY")
  impact$confidence_class[impact$Consequence == "synonymous_SNV"] <- "UNKNOWN"


  # [-4 rows] remove the mutations impossible to reclassify according to their Variant_Type and HGVSp_Short
  impact <- impact[! impact$sample_mut_key %in% c("P-0002209-T02-IM5_19_13051633_G_A",
                                                  "P-0002955-T01-IM3_11_108143466_A_T",
                                                  "P-0005565-T01-IM5_17_2225414_ATCACCTCAATAGCATCGCTAGGTGTTTCATACCTGTGAG_CTCACAGGTATGAAACACCTAGCGATGCTATTGAGGTGAG",
                                                  "P-0019100-T01-IM6_5_112175190_ATA_ACA"),]
  # [~6 rows] reclassify the mutations to `nonsynonymous_SNV` based on Variant_Type
  impact$Consequence[impact$sample_mut_key %in% c("P-0004486-T01-IM5_1_120468201_A_T",
                                                  "P-0003132-T01-IM5_15_41988433_G_A",
                                                  "P-0009326-T01-IM5_17_74732956_G_A",
                                                  "P-0010818-T01-IM5_17_74732956_G_A",
                                                  "P-0012684-T01-IM5_17_7578254_CT_AA",
                                                  "P-0010818-T02-IM6_17_74732956_G_A")] <- "nonsynonymous_SNV"
  # [~311 rows] reclassify the mutations to frameshift/nonframeshift insertion/deletion based on Variant_Type
  consequence_to_reclassify <- c("nonsynonymous_SNV", "frameshift_insertion", "frameshift_deletion",
                                 "nonframeshift_insertion", "nonframeshift_deletion")
  impact$Consequence[impact$Consequence %in% consequence_to_reclassify &   is_frameshift(impact$Tumor_Seq_Allele2, impact$Reference_Allele) &
                     impact$Variant_Type == "INS"] <- "frameshift_insertion"
  impact$Consequence[impact$Consequence %in% consequence_to_reclassify &   is_frameshift(impact$Tumor_Seq_Allele2, impact$Reference_Allele) &
                     impact$Variant_Type == "DEL"] <- "frameshift_deletion"
  impact$Consequence[impact$Consequence %in% consequence_to_reclassify & ! is_frameshift(impact$Tumor_Seq_Allele2, impact$Reference_Allele) &
                     impact$Variant_Type == "INS"] <- "nonframeshift_insertion"
  impact$Consequence[impact$Consequence %in% consequence_to_reclassify & ! is_frameshift(impact$Tumor_Seq_Allele2, impact$Reference_Allele) &
                     impact$Variant_Type == "DEL"] <- "nonframeshift_deletion"


  # [-148 rows] remove the mutations impossible to reclassify according to their Variant_Type and HGVSp_Short
  impact <- impact[! impact$sample_mut_key %in% read.table(paste0(data_folder_name, "/utils/sample_mut_keys_to_remove.txt" ), sep = "\t")[[1]],]
  # [~1004 rows] reclassify the mutations `Consequence` based on HGVSp_Short
  Consequence_to_reclassify <- read.table(paste0(data_folder_name, "/utils/sample_mut_keys_replace_Consequence.txt"), sep = "\t")
  impact$HGVSp_Short[impact$sample_mut_key %in% Consequence_to_reclassify[[1]]] <- Consequence_to_reclassify[[2]]
  # [~32 rows] correct the HGVSp_Short typos
  HGVSp_Short_typos <- read.table(paste0(data_folder_name, "/utils/sample_mut_keys_replace_HGVSp_Short.txt"), sep = "\t")
  impact$HGVSp_Short[impact$sample_mut_key %in% HGVSp_Short_typos[[1]]] <- HGVSp_Short_typos[[2]]
  

  #[~ 12 rows] temporary
  # Correct weird <- impact_oncokb %>% group_by(mut_key) %>% filter(length(unique(is.a.hotspot)) > 1 | length(unique(is.a.3d.hotspot)) > 1 | length(unique(oncogenic)) > 1) not empty
  # See OTHER/weird_oncokb
  impact$HGVSp_Short[impact$mut_key %in% c("13_48937070_GAACATGAATGTAATATAGATGAG_-")] <- ""
  impact$HGVSp_Short[impact$mut_key %in% c("9_139400334_C_T")] <- "p.X1339_splice"
  impact$HGVSp_Short[impact$mut_key %in% c("9_139412203_C_T")] <- "p.X481_splice"
  impact$HGVSp_Short[impact$mut_key %in% c("X_20148726_C_T" )] <- "p.X113_splice"
  impact$HGVSp_Short[impact$mut_key %in% c("X_20148727_T_A" )] <- "p.X113_splice"
  

  return (impact)
}


get_cosmic_count <- function(cosmic_string) {
    cosmic_string <- strsplit(cosmic_string, "OCCURENCE=")[[1]][2]
    cosmic_string <- strsplit(cosmic_string, ',')[[1]]
    cosmic_string <- sapply(cosmic_string, function(element) as.integer(strsplit(element, '\\(')[[1]][1]))
                
    return (sum(cosmic_string))
}



add_features <- function(data_folder_name, impact, annotations = FALSE, oncokb = FALSE, gene_type = FALSE) {
    
    if (annotations) {
      # 1. Get the raw data
      impact_annotated <- read.table(paste0(data_folder_name, "/dominik/all_IMPACT_mutations_180508.simple.hg19_multianno.txt"),
                                     sep = "\t", stringsAsFactors = FALSE, header = TRUE)


      # 2. Create keys to join the two dataframes and extract the features
      impact_annotated$join_key <- paste(impact_annotated$Chr,
                                         impact_annotated$Start,
                                         impact_annotated$Ref,
                                         impact_annotated$Alt,
                                         sep = '_')
      impact_annotated <- unique(impact_annotated[, c("join_key", "Kaviar_AF", "cosmic70")])
      impact[, c("Kaviar_AF", "cosmic70")] <- left_join(impact, impact_annotated,
                                                        by = c("mut_key" = "join_key"))[, c("Kaviar_AF", "cosmic70")]


      # 3. Process the raw features
      ## Kaviar_AF
      impact$Kaviar_AF[(impact$Kaviar_AF == '.')] <- list('0')
      impact$Kaviar_AF <- sapply(impact$Kaviar_AF, function(s) as.double(s))

      ## cosmic_count
      impact$cosmic70[(impact$cosmic70 == '.')] <- list('OCCURENCE=0')
      impact$cosmic_count <- sapply(impact$cosmic70, get_cosmic_count)
      impact$cosmic70 <- NULL
    }
    
                                   
    if(oncokb) {
      # 1. Get the raw data
      impact_oncokb <- read.table(paste0(data_folder_name, "/oncokb/oncokb_annotated_cleaned_IMPACT_mutations_180508.txt"),
                                  sep = "\t", stringsAsFactors = FALSE, header = TRUE)


      # 2. Create keys to join the two dataframes and extract the features
      impact_oncokb <- unique(impact_oncokb[, c("mut_key", "is.a.hotspot", "is.a.3d.hotspot", "oncogenic")])
      impact[, c("is_a_hotspot", "is_a_3d_hotspot", "oncogenic")] <- left_join(impact, impact_oncokb,
                                                                               by = c("mut_key" = "mut_key"))[, c("is.a.hotspot",
                                                                                                                  "is.a.3d.hotspot",
                                                                                                                  "oncogenic")]


      # 3. Process the raw features
      ## is_a_hostpot
      impact$is_a_hotspot[impact$is_a_hotspot == "Y"  ] <- "yes"
      impact$is_a_hotspot[impact$is_a_hotspot != "yes"] <- "unknown"

      ## is_a_3d_hostpot
      impact$is_a_3d_hotspot[impact$is_a_3d_hotspot == "Y"  ] <- "yes"
      impact$is_a_3d_hotspot[impact$is_a_3d_hotspot != "yes"] <- "unknown"

      ## oncogenic
      impact$oncogenic[impact$oncogenic == ""] <- "Unknown"
    }


    if(gene_type) {
      # 1. Get the raw data
      cancer_genes_list <- read.table(paste0(data_folder_name, "/oncokb/CancerGenesList.txt"),
                                      sep = "\t", stringsAsFactors = FALSE, header = TRUE, comment.char = '')


      # 2. Create keys to join the two dataframes and extract the features
      impact[, c("OncoKB.Oncogene", "OncoKB.TSG")] <- left_join(impact, cancer_genes_list,
                                                                by = c("Hugo_Symbol" = "Hugo.Symbol"))[,c("OncoKB.Oncogene", "OncoKB.TSG")]


      # 3. Process the raw features
      ## gene_type
      impact$gene_type <- "unknown"
      impact$gene_type[impact$OncoKB.Oncogene == "Yes"] <- "oncogene"
      impact$gene_type[impact$OncoKB.TSG == "Yes"]      <- "tsg"
      impact$gene_type[impact$OncoKB.Oncogene == "Yes" & impact$OncoKB.TSG == "Yes"] <- "oncogene_and_tsg"

      impact$OncoKB.Oncogene <- NULL
      impact$OncoKB.TSG      <- NULL
    }
                               
    return (impact)
}


#gene ontology mapper

library(tidyverse)
setwd("C:\Users\username\OneDrive - Imperial College London\Documents\0Oxford_main\fergus paper\code_main\output")
#laptop
#setwd("/Users/fergus/Library/CloudStorage/OneDrive-UniversityofCambridge/Documents/Geneomics/Geneomics/MA_GWAMA/Brain SNPs")

# Get a list of all CSV files in the folder
csv_files <- list.files(pattern = "\\.csv$", full.names = TRUE)

# Read all CSV files and combine them into a single dataframe
brain_snps <- map_df(csv_files, read_csv) 
brain_snps = brain_snps %>%
  dplyr::select(RS) %>%
  unique()


#Filter for SNPs associated with brain tissue expression
instrument_dep_dat_brain = instrument_dep_dat %>%
  filter(SNP %in% brain_snps$RS)
instrument_ls_dat_brain = instrument_ls_dat %>%
  filter(SNP %in% brain_snps$RS)
instrument_neu_dat_brain = instrument_neu_dat %>%
  filter(SNP %in% brain_snps$RS)
instrument_pa_dat_brain = instrument_pa_dat %>%
  filter(SNP %in% brain_snps$RS)
instrument_wb_dat_brain = instrument_wb_dat %>%
  filter(SNP %in% brain_snps$RS)
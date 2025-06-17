# gene ontology mapper

library(tidyverse)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("Please provide a working directory path")
}
setwd(args[1])

# Get a list of all CSV files in the folder
csv_files <- list.files(pattern = "\\.csv$", full.names = TRUE)

# Read all CSV files and combine them into a single dataframe
brain_snps <- map_df(csv_files, read_csv)
brain_snps <- brain_snps %>%
  dplyr::select(RS) %>%
  unique()

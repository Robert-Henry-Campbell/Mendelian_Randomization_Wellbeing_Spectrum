# gene ontology mapper

library(tidyverse)
library(clusterProfiler)
library(org.Hs.eg.db)
library(biomaRt)
library(GOSemSim)
library(topGO)

args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0) {
  stop("Please provide a working directory path")
}
setwd(args[1])

rm(list = ls())

gene_data <- read.csv("data/processed/VEP_output/Clustered_SNPS_for_gene_ontology_annotation_with_VEP.csv")

gene_data_ENSG_only <- gene_data[gene_data$Gene_ID != "", ]

genes <- as.list(gene_data_ENSG_only$Gene_ID)

ensembl <- useMart("ensembl", dataset = "hsapiens_gene_ensembl")

go_annotations <- getBM(attributes = c('ensembl_gene_id', 'hgnc_symbol', 'go_id', 'name_1006', 'namespace_1003'),
                        filters = 'ensembl_gene_id',
                        values = gene_data_ENSG_only$Gene_ID,
                        mart = ensembl)

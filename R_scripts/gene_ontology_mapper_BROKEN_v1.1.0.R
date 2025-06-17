# gene ontology mapper

# warning: this approach is unreliable; manual annotation might be required.

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

rm(list = ls())  # nolint

# placeholder for further analysis steps

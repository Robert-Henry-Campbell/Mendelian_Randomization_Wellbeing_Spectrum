#gene ontology mapper

#warning: this shit never, ever works so give up now and do it manually. https://www.geneontology.org/

#notes 8.1.24
#you ar egoing to do annotation on all the SNPs in each cluster for each wellbeing phenotype (you've alreayd got mapped genes)
#you're waiting for fergus to give you the SNP info for each cluster

#notes 8.15.24
#you've got the SNP cluster info, you've added the genes. 
#


library(tidyverse)
library(clusterProfiler)
library(org.Hs.eg.db)  # Change to the appropriate organism database
library(biomaRt)
library(GOSemSim)
library(topGO)

setwd("C:\\Users\\RobertC\\OneDrive - Imperial College London\\Documents\\0Oxford_main\\fergus paper")

rm(list=ls()) # nolint

#load my gene data(old)
#gene_data <- read.csv("code_main\\VEP_output\\Clustered_SNPS_for_gene_ontology_annotation_with_VEP.csv")
#gene_data <- gene_data[gene_data$Gene_ID != "", ]
#genes <- as.list(gene_data$Gene_ID)

#load my gene data as of 10.25.24
snp_data <- read.csv("r_code_main/r_data/SNPS_no23.csv")

#connecting to ensemble
ensembl <- useMart("ensembl", dataset = "hsapiens_gene_ensembl")

#connecting to a different ensemble IDK
snpMart <- useEnsembl(biomart = "ENSEMBL_MART_SNP", dataset = "hsapiens_snp")

#convert RSID to ENSG
gene_data <- getBM(
  attributes = c("refsnp_id", "ensembl_gene_stable_id"),
  filters = "snp_filter",
  values = snp_data,
  mart = snpMart
)

#drop the empty ENSG rows
gene_data <- gene_data[gene_data$ensembl_gene_stable_id != "", ]


go_annotations <- getBM(attributes = c('ensembl_gene_id', 
                        'hgnc_symbol', 
                        'go_id', 
                        'name_1006', 
                        'namespace_1003'),
                        filters = 'ensembl_gene_id',
                        values = gene_data$ensembl_gene_stable_id,
                        mart = ensembl)

#you're writing off the ENSG codes to CSV and then you're using the online tool
write.csv(gene_data, file = "r_code_main/r_data/gene_data.csv", row.names = FALSE)


# Filter for Biological Process GO terms
biological_process_annotations <- go_annotations[go_annotations$namespace_1003 == "biological_process", ]

# Create a topGOdata object for biological processes
gene_list <- factor(as.integer(gene_data$Gene_ID %in% biological_process_annotations$ensembl_gene_id))
names(gene_list) <- gene_data$Gene_ID

# Ensure there are no unintended values
table(gene_list)  # This should only show counts for "0" and "1"


GOdata <- new("topGOdata",
              ontology = "BP",
              allGenes = gene_list,
              annot = annFUN.gene2GO,
              gene2GO = split(go_annotations$go_id, go_annotations$ensembl_gene_id))

# Get results
#result <- runTest(GOdata, algorithm = "classic", statistic = "fisher")
result <- runTest(GOdata, algorithm = "weight01", statistic = "ks")

pvalues <- score(result)
sum(pvalues == 1)         # Count the number of p-values that are exactly 1
sum(pvalues < 1)          # Count how many p-values are less than 1
length(pvalues) 



allRes <- GenTable(GOdata, topNodes = 150)

# Display results
print(allRes)



##old version below only half works

mart <- useMart("ensembl", dataset = "hsapiens_gene_ensembl")


data <- read.csv("Clustered_SNPS_for_gene_ontology_annotation.csv")
snp_list <- as.data.frame(data$SNP)

gene_data <- getBM(attributes = c('snp', 'ensembl_gene_id', 'external_gene_name'), filters = 'snp', values = snp_list, mart = mart)


# Merge the gene information back to your original data frame
df_with_genes <- merge(data, gene_data, by.x = "SNP", by.y = "snp", all.x = TRUE)

na_genes <- sum(is.na(df_with_genes$ensembl_gene_id))
if (na_genes > 0) {
  print(paste(na_genes, "SNPs did not match any genes"))
}



#random example genes
genes <- c("ENSG00000149292", "ENSG00000109919", "ENSG00000236333", 
           "ENSG00000213672", "ENSG00000173540", "ENSG00000178252", 
           "ENSG00000055955") #this is all random examples

# Convert Ensembl gene IDs to Entrez gene IDs
mart <- useMart("ensembl", dataset = "hsapiens_gene_ensembl")
entrez_ids <- getBM(filters = "ensembl_gene_id", 
                    attributes = c("ensembl_gene_id", "entrezgene_id"),
                    values = genes, 
                    mart = mart)
genes_entrez <- na.omit(entrez_ids$entrezgene_id)


# Perform GO enrichment analysis
enrich_result <- enrichGO(gene = genes_entrez,
                          OrgDb = org.Hs.eg.db,
                          keyType = "ENTREZID",
                          ont = "BP",  # "BP" for Biological Process
                          pAdjustMethod = "BH",
                          pvalueCutoff = 0.01,
                          qvalueCutoff = 0.05)

# View results
print(enrich_result)

# Visualize enrichment results with dotplot
dotplot(enrich_result)

# Alternatively, visualize with barplot
barplot(enrich_result, showCategory=10)  # Adjust the number of categories as needed

#goal: import SNPs and get their associated genes + missense + nonsense status

import pandas as pd
from pathlib import Path

from gwas.vep_utils import (
    get_vep_data,
    parse_vep_results,
    filter_coding_variants,
)

# Base directory relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent



df = pd.read_csv(BASE_DIR / "Clustered_SNPS_for_gene_ontology_annotation.csv")

#extract the SNPS to a list
snp_list = df['SNP'].tolist()



# Get VEP data
vep_results = get_vep_data(snp_list)


#filter the coding variants, this is a check for missense_variant or nonsense_variant
coding_variants_df = filter_coding_variants(vep_results)
#coding_variants_df.to_csv(BASE_DIR / "VEP_output" / "Clustered_SNPS_for_gene_ontology_annotation_with_coding_variants.csv", index=False)

# Parse the results
vep_df = parse_vep_results(vep_results)

# Display the results
print(vep_df)

#join vep_df with df on SNP
df = pd.merge(df, vep_df, on='SNP', how='left')

#write to csv
df.to_csv(BASE_DIR / "VEP_output" / "Clustered_SNPS_for_gene_ontology_annotation_with_VEP.csv", index=False)

pass

import pandas as pd
import os
from pathlib import Path

from gwas.eqtl_checker import fetch_snp_info


# accepts rsid, returns b38 variant id in GTEX format




# Set base directory relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent
GTEX_directory_path = BASE_DIR / 'GTEX_BRAIN_ONLY'
GWAS_directory_path = BASE_DIR / 'GWAS_hits'
OUTPUT_DIR = BASE_DIR / 'output'

# List all files in the specified directory
GTEX_file_names = [f.name for f in GTEX_directory_path.iterdir() if f.is_file()]
GWAS_file_names = [f.name for f in GWAS_directory_path.iterdir() if f.is_file()]

#eQTL merge for each file in the directory 


#GTEX_file_path = 'GTEX_BRAIN_ONLY/Brain_Amygdala.signifpairs.tsv'  # Replace with the path to your file
#GWAS_file_path = 'GWAS_hits/Indep. Signals AVG LS.csv'

for GWAS_file_path in GWAS_file_names:
    for GTEX_file_path in GTEX_file_names:

        # Read the files
        GTEX_df = pd.read_csv(GTEX_directory_path / GTEX_file_path, sep='\t')  # Use tab as delimiter
        GWAS_df = pd.read_csv(GWAS_directory_path / GWAS_file_path, sep=',')  # Use , as delimiter


        # Display the first few rows of the DataFrame to verify it's loaded correctly

        #Now: we create a new column in the GWAS dataframe that contains the SNP ID in the format of the GTEX dataframe
        GWAS_df['variant_id'] = GWAS_df['RS'].apply(lambda rs: fetch_snp_info(rs, GWAS_df))

        
        #GWAS_df['variant_id_1'] = 'chr'+GWAS_df['CHR'].astype(str) +'_' + GWAS_df['BP'].astype(str) + '_' + GWAS_df['A1'] + '_' + GWAS_df['A2'] + '_b38'
        #it's unclear which allele is the reference and which is the alternate. So we're trying both ways
        #GWAS_df['variant_id_2'] = 'chr'+GWAS_df['CHR'].astype(str) +'_' + GWAS_df['BP'].astype(str) + '_' + GWAS_df['A2'] + '_' + GWAS_df['A1'] + '_b38'

        #merge to find overlap
        #GWAS_eQTLs_1_df = pd.merge(GWAS_df, GTEX_df, left_on='variant_id_1', right_on='variant_id', how='inner')
        #GWAS_eQTLs_2_df = pd.merge(GWAS_df, GTEX_df, left_on='variant_id_2', right_on='variant_id', how='inner')

        #new merge
        GWAS_eQTLs_df = pd.merge(GWAS_df, GTEX_df, left_on='variant_id', right_on='variant_id', how='inner')

        print(GTEX_file_path + "|" + "eQTLs_df size: " + str(GWAS_eQTLs_df.shape[0]))

        #save as a csv
        out_file = OUTPUT_DIR / f"{GWAS_file_path} {GTEX_file_path}eQTLs_.csv"
        GWAS_eQTLs_df.to_csv(out_file, index=False)
print('bobo')
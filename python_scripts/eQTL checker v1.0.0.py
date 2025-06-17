import pandas as pd
import os
import requests


# accepts rsid, returns b38 variant id in GTEX format




def fetch_snp_info(rs_id):
    # NCBI dbSNP API base URL
    url = f'https://clinicaltables.nlm.nih.gov/api/snps/v3/search?terms={rs_id}'
    # Send the request to the dbSNP API
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()

        # Extracting the specific data
        # Assuming the data is always in the third list and it's the first sub-list
        chromosome = data[3][0][1]
        position = str(int(data[3][0][2])+1) # Convert to integer and add 1
        allele_change = data[3][0][3]
        if len(allele_change) != 3:
            mutations = allele_change.split(',')
            #strip the whitespace from mutations
            mutations = [mutation.strip() for mutation in mutations]
            index = GWAS_df.index[GWAS_df['RS'] == rs_id].tolist()
            if len(index) != 1:
                input('trouble with the index wow wow wow')
            proposed_allele_change = str(GWAS_df['A2'].loc[index[0]] + '/' + GWAS_df['A1'].loc[index[0]])
            #check if proposed allele change is in the list of mutations
            if proposed_allele_change in mutations:
                allele_change = proposed_allele_change
            else:
                input('error: allele change not in list of mutations')
            
        variant_id = f'chr{chromosome}_{position}_{allele_change[0]}_{allele_change[2]}_b38'
        print(variant_id)    
        return variant_id


os.chdir("C:\\Users\\username\\OneDrive - Imperial College London\\Documents\\0Oxford_main\\fergus paper\\code_main")

GTEX_directory_path = 'GTEX_BRAIN_ONLY/'
GWAS_directory_path = 'GWAS_hits/'

# List all files in the specified directory
GTEX_file_names = [f for f in os.listdir(GTEX_directory_path ) if os.path.isfile(os.path.join(GTEX_directory_path , f))]
GWAS_file_names = [f for f in os.listdir(GWAS_directory_path) if os.path.isfile(os.path.join(GWAS_directory_path, f))]

#eQTL merge for each file in the directory 


#GTEX_file_path = 'GTEX_BRAIN_ONLY/Brain_Amygdala.signifpairs.tsv'  # Replace with the path to your file
#GWAS_file_path = 'GWAS_hits/Indep. Signals AVG LS.csv'

for GWAS_file_path in GWAS_file_names:
    for GTEX_file_path in GTEX_file_names:

        # Read the files
        GTEX_df = pd.read_csv(GTEX_directory_path+GTEX_file_path, sep='\t')  # Use tab as delimiter
        GWAS_df = pd.read_csv(GWAS_directory_path+GWAS_file_path, sep=',')  # Use , as delimiter


        # Display the first few rows of the DataFrame to verify it's loaded correctly

        #Now: we create a new column in the GWAS dataframe that contains the SNP ID in the format of the GTEX dataframe
        GWAS_df['variant_id'] = GWAS_df['RS'].apply(fetch_snp_info)

        
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
        GWAS_eQTLs_df.to_csv("output/"+ GWAS_file_path + ' ' + GTEX_file_path + 'eQTLs_.csv', index=False)
print('bobo')
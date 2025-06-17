#goal: import SNPs and get their associated genes + missense + nonsense status

import requests
import pandas as pd
import os


os.chdir("C:\\Users\\username\\OneDrive - Imperial College London\\Documents\\0Oxford_main\\fergus paper")


def get_vep_data(snp_list):
    url = "https://rest.ensembl.org/vep/human/id"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    
    # Prepare input data
    data = {
        "ids": snp_list
    }

    # Send POST request to the VEP API
    response = requests.post(url, headers=headers, json=data)
    
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data: {response.status_code}, {response.text}")
    
    # Parse the JSON response
    vep_results = response.json()
    return vep_results

def parse_vep_results(vep_results):
    parsed_data = []

    for result in vep_results:
        snp_id = result['id']
        most_severe_consequence = result.get('most_severe_consequence', 'N/A')
        gene_id = None
        gene_name = None
        
        # Find the gene associated with the most severe consequence
        for transcript_consequence in result.get('transcript_consequences', []):
            if most_severe_consequence in transcript_consequence.get('consequence_terms', []):
                gene_id = transcript_consequence.get('gene_id', '')
                gene_name = transcript_consequence.get('gene_symbol', '')
                break  # Stop once the relevant gene information is found

        parsed_data.append({
            'SNP': snp_id,
            'Gene_ID': gene_id,
            'Gene_Name': gene_name,
            'Most_Severe_Consequence': most_severe_consequence
        })

    return pd.DataFrame(parsed_data)


def filter_coding_variants(vep_results):
    coding_variants = []
    for result in vep_results:
        snp_id = result['id']
        for transcript_consequence in result.get('transcript_consequences', []):
            consequence_terms = transcript_consequence.get('consequence_terms', [])
            # Check for missense_variant or nonsense_variant
            if "missense_variant" in consequence_terms or "nonsense_variant" in consequence_terms:
                coding_variants.append({
                    'SNP': snp_id,
                    'Gene_ID': transcript_consequence.get('gene_id', ''),
                    'Gene_Name': transcript_consequence.get('gene_symbol', ''),
                    'Consequence': ', '.join(consequence_terms)
                })
    return pd.DataFrame(coding_variants)

df = pd.read_csv("Clustered_SNPS_for_gene_ontology_annotation.csv")

#extract the SNPS to a list
snp_list = df['SNP'].tolist()



# Get VEP data
vep_results = get_vep_data(snp_list)


#filter the coding variants, this is a check for missense_variant or nonsense_variant
coding_variants_df = filter_coding_variants(vep_results)
#coding_variants_df.to_csv("code_main//VEP_output//Clustered_SNPS_for_gene_ontology_annotation_with_coding_variants.csv", index=False)

# Parse the results
vep_df = parse_vep_results(vep_results)

# Display the results
print(vep_df)

#join vep_df with df on SNP
df = pd.merge(df, vep_df, on='SNP', how='left')

#write to csv
df.to_csv("code_main//VEP_output//Clustered_SNPS_for_gene_ontology_annotation_with_VEP.csv", index=False)

pass

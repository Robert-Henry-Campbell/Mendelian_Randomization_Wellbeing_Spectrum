import requests
import json

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
            input('Error: allele change is not of length 3. Press Enter to continue...')
        variant_id = f'chr{chromosome}_{position}_{allele_change[0]}_{allele_change[-1]}_b38'
        print(variant_id)    
        return variant_id


# Example usage
rs_id = 'rs3781627'  # Replace 'rs555' with your actual rsID
fetch_snp_info(rs_id)
print('chunky bacon')
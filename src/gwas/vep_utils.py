import requests
import pandas as pd


def get_vep_data(snp_list):
    """Query the Ensembl VEP API for a list of SNP IDs."""
    url = "https://rest.ensembl.org/vep/human/id"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"ids": snp_list}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data: {response.status_code}, {response.text}")
    return response.json()


def parse_vep_results(vep_results):
    """Parse VEP API results into a tidy DataFrame."""
    parsed_data = []
    for result in vep_results:
        snp_id = result["id"]
        most_severe = result.get("most_severe_consequence", "N/A")
        gene_id = None
        gene_name = None
        for tc in result.get("transcript_consequences", []):
            if most_severe in tc.get("consequence_terms", []):
                gene_id = tc.get("gene_id", "")
                gene_name = tc.get("gene_symbol", "")
                break
        parsed_data.append({
            "SNP": snp_id,
            "Gene_ID": gene_id,
            "Gene_Name": gene_name,
            "Most_Severe_Consequence": most_severe,
        })
    return pd.DataFrame(parsed_data)


def filter_coding_variants(vep_results):
    """Return coding variants (missense or nonsense) from VEP results."""
    coding_variants = []
    for result in vep_results:
        snp_id = result["id"]
        for tc in result.get("transcript_consequences", []):
            terms = tc.get("consequence_terms", [])
            if "missense_variant" in terms or "nonsense_variant" in terms:
                coding_variants.append({
                    "SNP": snp_id,
                    "Gene_ID": tc.get("gene_id", ""),
                    "Gene_Name": tc.get("gene_symbol", ""),
                    "Consequence": ", ".join(terms),
                })
    return pd.DataFrame(coding_variants)
